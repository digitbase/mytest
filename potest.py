from decimal import Decimal
import json
import os
import requests
import logging
from logging.handlers import RotatingFileHandler
import mysql.connector
import config
from datetime import *
import time
from test import prd, prm

def getWater(logger, data_source_id, url, token) :


    cnx_system_db = None
    cursor_system_db = None
    try:
        cnx_system_db = mysql.connector.connect(**config.myems_system_db)
        cursor_system_db = cnx_system_db.cursor()
    except Exception as e:
        logger.error("Error in step 2.1 of acquisition process " + str(e))
        if cursor_system_db:
            cursor_system_db.close()
        if cnx_system_db:
            cnx_system_db.close()

    try:
        query = (" SELECT id, name, object_type, is_trend, ratio, address "
                    " FROM tbl_points "
                    " WHERE data_source_id = %s AND is_virtual = 0 "
                    " ORDER BY id "
                    " limit 0,30 "     ## 测试3个表
                    )
        cursor_system_db.execute(query, (data_source_id, ))
        rows_point = cursor_system_db.fetchall()
    except Exception as e:
        logger.error("Error in step 2.2 of acquisition process: " + str(e))
        if cursor_system_db:
            cursor_system_db.close()
        if cnx_system_db:
            cnx_system_db.close()

    if rows_point is None or len(rows_point) == 0:
        # there is no points for this data source
        logger.error("Point Not Found in Data Source (ID = %s), acquisition process terminated ", data_source_id)
        if cursor_system_db:
            cursor_system_db.close()
        if cnx_system_db:
            cnx_system_db.close()


    # There are points for this data source
    point_list = list()

    for row_point in rows_point:
        point_list.append({"id": row_point[0],
                            "name": row_point[1],
                            "object_type": row_point[2],
                            "is_trend": row_point[3],
                            "ratio": row_point[4],
                            "address": row_point[5]})
    
    ################################################################################################################
    # Step 3: Read point values from Modbus slaves
    ################################################################################################################
    # connect to historical database
    cnx_historical_db = None
    cursor_historical_db = None
    try:
        cnx_historical_db = mysql.connector.connect(**config.myems_historical_db)
        cursor_historical_db = cnx_historical_db.cursor()
    except Exception as e:
        logger.error("Error in step 3.1 of acquisition process " + str(e))
        if cursor_historical_db:
            cursor_historical_db.close()
        if cnx_historical_db:
            cnx_historical_db.close()

        if cursor_system_db:
            cursor_system_db.close()
        if cnx_system_db:
            cnx_system_db.close()

    ind = 0
    while ind == 0:
        
        # begin of the inner while loop
        is_modbus_tcp_timed_out = False
        energy_value_list = list()

        # TODO: update point list in another thread
        # foreach point loop
        for point in point_list:
            # begin of foreach point loop
            try:

                address = json.loads(point['address'])
            except Exception as e:
                logger.error("Error in step 3.2 of acquisition process: Invalid point address in JSON " + str(e))
                time.sleep(600)
                continue

            if 'address' not in address.keys() :
                logger.error('Data Source(ID=%s), Point(ID=%s) Invalid address data.',
                                data_source_id, point['id'])
                time.sleep(600)
                continue

            result = dict()
            try:

                header = {"Content-Type": "application/json"}
                aurl = f'{url}?token={token}'


                t = datetime.now()
                nowstr = t.strftime('%Y-%m-%d')

                id = '"'+address["address"]+'"'
                post_dict = '{"meterAddr": '+id+' , "beginDate":"'+nowstr+'", "endDate":"'+nowstr+'", "pageIndex":1, "pageSize":1}'
               
                prm(post_dict)

                res = requests.post(aurl,headers=header,data=post_dict,timeout=5)
                time.sleep(2)
                prm(res.status_code)
                result = res.json()


                if res.status_code != 200:
                        #print('=== request error ====')
                        error_msg = "model request error, status_code: {}, msg: {}".format(res.status_code, res.json())
                        logger.error(error_msg)
                else:
                    print('=== request success ====')
                    result = json.loads(res.text)
            except Exception as e:
                logger.error(str(e) + url)
                if 'timed out' in str(e):
                    is_modbus_tcp_timed_out = True
                    break
                else:
                    continue

            if result is None or not isinstance(result, dict) or len(result) == 0:
                logger.error("Error in step 3.3 of acquisition process: \n"
                                " invalid result: None "
                                " for point_id: " + str(point['id']))
                continue

            if result['code'] != 200 or\
                len(result['data']['data']) == 0 :    
                logger.error(" Error in step 3.5 of acquisition process:\n"
                             " http query not success  "
                             " for point_id: " + str(point['id']))
            else:
                value = result['data']['data'][0]['meternumber']
                energy_value_list.append({'point_id': point['id'],
                                        'is_trend': point['is_trend'],
                                        'value': Decimal(value) * point['ratio']})


        if is_modbus_tcp_timed_out:
            # Modbus TCP connection timeout

            # close the connection to database
            if cursor_historical_db:
                cursor_historical_db.close()
            if cnx_historical_db:
                cnx_historical_db.close()
            if cursor_system_db:
                cursor_system_db.close()
            if cnx_system_db:
                cnx_system_db.close()

            # break the inner while loop
            # go to begin of the outermost while loop
            time.sleep(60)
            break




        if not cnx_historical_db.is_connected():
            try:
                cnx_historical_db = mysql.connector.connect(**config.myems_historical_db)
                cursor_historical_db = cnx_historical_db.cursor()
            except Exception as e:
                logger.error("Error in step 4.1 of acquisition process: " + str(e))
                if cursor_historical_db:
                    cursor_historical_db.close()
                if cnx_historical_db:
                    cnx_historical_db.close()
                # go to begin of the inner while loop
                time.sleep(60)
                continue

        # check the connection to the System Database
        if not cnx_system_db.is_connected():
            try:
                cnx_system_db = mysql.connector.connect(**config.myems_system_db)
                cursor_system_db = cnx_system_db.cursor()
            except Exception as e:
                logger.error("Error in step 4.2 of acquisition process: " + str(e))
                if cursor_system_db:
                    cursor_system_db.close()
                if cnx_system_db:
                    cnx_system_db.close()
                # go to begin of the inner while loop
                time.sleep(60)
                continue

        current_datetime_utc = datetime.utcnow()

        if len(energy_value_list) > 0:
            add_values = (" INSERT INTO tbl_energy_value (point_id, utc_date_time, actual_value) "
                          " VALUES  ")
            trend_value_count = 0
            #prm(energy_value_list)
            for point_value in energy_value_list:
                if point_value['is_trend']:
                    add_values += " (" + str(point_value['point_id']) + ","
                    add_values += "'" + current_datetime_utc.isoformat() + "',"
                    add_values += str(point_value['value']) + "), "
                    trend_value_count += 1

            if trend_value_count > 0:
                try:
                    # trim ", " at the end of string and then execute
                    cursor_historical_db.execute(add_values[:-2])
                    cnx_historical_db.commit()
                except Exception as e:
                    logger.error("Error in step 4.4.1 of acquisition process: " + str(e))
                    # ignore this exception

            # update tbl_energy_value_latest
            delete_values = " DELETE FROM tbl_energy_value_latest WHERE point_id IN ( "
            latest_values = (" INSERT INTO tbl_energy_value_latest (point_id, utc_date_time, actual_value) "
                             " VALUES  ")

            latest_value_count = 0
            for point_value in energy_value_list:
                delete_values += str(point_value['point_id']) + ","
                latest_values += " (" + str(point_value['point_id']) + ","
                latest_values += "'" + current_datetime_utc.isoformat() + "',"
                latest_values += str(point_value['value']) + "), "
                latest_value_count += 1

            if latest_value_count > 0:
                try:
                    # replace "," at the end of string with ")"
                    cursor_historical_db.execute(delete_values[:-1] + ")")
                    cnx_historical_db.commit()

                except Exception as e:
                    logger.error("Error in step 4.4.2 of acquisition process " + str(e))
                    # ignore this exception

                try:
                    # trim ", " at the end of string and then execute
                    cursor_historical_db.execute(latest_values[:-2])
                    cnx_historical_db.commit()

                except Exception as e:
                    logger.error("Error in step 4.4.3 of acquisition process " + str(e))
                    # ignore this exception

        # update data source last seen datetime
        update_row = (" UPDATE tbl_data_sources "
                      " SET last_seen_datetime_utc = '" + current_datetime_utc.isoformat() + "' "
                      " WHERE id = %s ")
        try:
            cursor_system_db.execute(update_row, (data_source_id, ))
            cnx_system_db.commit()
        except Exception as e:
            logger.error("Error in step 4.6 of acquisition process " + str(e))
            if cursor_system_db:
                cursor_system_db.close()
            if cnx_system_db:
                cnx_system_db.close()
            # go to begin of the inner while loop
            time.sleep(60)
            continue

        # sleep interval in seconds and continue the inner while loop
        
        logger.info(f"loop sleep {config.interval_in_seconds} sec. Insert <{len(energy_value_list)}> meter.")
        time.sleep(config.interval_in_seconds)





#########################



def getGateWay(gid, logger) :
    cnx_system_db = None
    cursor_system_db = None
    try:
        cnx_system_db = mysql.connector.connect(**config.myems_system_db)
        cursor_system_db = cnx_system_db.cursor()
    except Exception as e:
        logger.error("Error in main process " + str(e))
        if cursor_system_db:
            cursor_system_db.close()
        if cnx_system_db:
            cnx_system_db.close()

    try:
        query = (f" SELECT ds.id, ds.name, ds.connection "
                    " FROM tbl_data_sources ds, tbl_gateways g "
                    " WHERE  ds.gateway_id = g.id AND g.id = %s"
                    " ORDER BY ds.id ")

        cursor_system_db.execute(query, (gid, ))
        rows_data_source = cursor_system_db.fetchall()
    except Exception as e:
        logger.error("Error in main process " + str(e))

    finally:
        if cursor_system_db:
            cursor_system_db.close()
        if cnx_system_db:
            cnx_system_db.close()
    if rows_data_source is None or len(rows_data_source) == 0:
        logger.error("Data Source Not Found, Wait for minutes to retry.")
    return rows_data_source

def main():

    logger = logging.getLogger('myems-water')
    logger.setLevel(logging.INFO)
    fh = RotatingFileHandler('myems-water.log', maxBytes=1024*1024, backupCount=1)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(logging.StreamHandler())
    
    token = ""
    #用水类型ID
    gateWayID = config.getWater['gType']
    post_dict = config.getWater['tpost']
    water_url = config.getWater['wurl']
    url = config.getWater['turl']

 
    #url = 'http://10.3.40.248:8217/api/auth/user/login'
    #post_dict = '{"username": "system","password": "a5c85f32ed50a49d"}'
    header = {"Content-Type": "application/json"}
    res = requests.post(url,data=post_dict,timeout=3).json() 

    #restext= os.system('''curl -H "Content-Type: application/json" -X POST -d '{"username": "system","password": "a5c85f32ed50a49d"}' "http://10.3.40.248:8217/api/auth/user/login"''')
    resObj = requests.post(url,headers=header,data=post_dict,timeout=5).json()
    print(resObj)
   

    
    if (resObj['code'] == 200) :
        #print(resObj['data']['token'])
        logger.info("Get token Success : "+resObj['data']['token'])
        token = resObj['data']['token']
        
        getWater(logger, gateWayID, water_url, token)
    else :
        logger.error("error get token fail ! ")
        





if __name__ == "__main__":
    main()
