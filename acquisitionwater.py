import json
import mysql.connector
import time
import math
from datetime import datetime
import telnetlib
from modbus_tk import modbus_tcp
import requests
from sympy import true
import config
from decimal import Decimal
from test import prd,prm


########################################################################################################################
# Acquisition Procedures
# Step 1: telnet the host
# Step 2: Get point list
# Step 3: Read point values from Modbus slaves
# Step 4: Bulk insert point values and update latest values in historical database
########################################################################################################################


def acquisitionwater(logger, data_source_id, host, port):
    
    print(logger)
    logger.info('======== Acquisition start=======')
    while True:
        # begin of the outermost while loop

        ################################################################################################################
        # Step 1: telnet the host
        ################################################################################################################
        # try:
        #     telnetlib.Telnet(host, port, 10)
        #     print("Succeeded to telnet %s:%s in acquisition process ", host, port)
        # except Exception as e:
        #     logger.error("Failed to telnet %s:%s in acquisition process: %s  ", host, port, str(e))
        #     # go to begin of the outermost while loop
        #     time.sleep(300)
        #     continue

        ################################################################################################################
        # Step 2: Get point list
        ################################################################################################################
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
            # go to begin of the outermost while loop
            time.sleep(60)
            continue

        try:
            query = (" SELECT id, name, object_type, is_trend, ratio, address "
                     " FROM tbl_points "
                     " WHERE data_source_id = %s AND is_virtual = 0 "
                     " ORDER BY id ")
            cursor_system_db.execute(query, (data_source_id, ))
            rows_point = cursor_system_db.fetchall()
        except Exception as e:
            logger.error("Error in step 2.2 of acquisition process: " + str(e))
            if cursor_system_db:
                cursor_system_db.close()
            if cnx_system_db:
                cnx_system_db.close()
            # go to begin of the outermost while loop
            time.sleep(60)
            continue
        if rows_point is None or len(rows_point) == 0:
            # there is no points for this data source
            logger.error("Point Not Found in Data Source (ID = %s), acquisition process terminated ", data_source_id)
            if cursor_system_db:
                cursor_system_db.close()
            if cnx_system_db:
                cnx_system_db.close()
            # go to begin of the outermost while loop
            time.sleep(60)
            continue

        # There are points for this data source
        point_list = list()

        for row_point in rows_point:
            point_list.append({"id": row_point[0],
                               "name": row_point[1],
                               "object_type": row_point[2],
                               "is_trend": row_point[3],
                               "ratio": row_point[4],
                               "address": row_point[5]})

        ## 得到数据点集合 point_list[]
        #prd(point_list)
        ##
        
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
            # go to begin of the outermost while loop
            time.sleep(60)
            continue

        # inner while loop to read all point values periodically
        while True:
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
                    continue

                if 'url' not in address.keys() \
                    or 'add' not in address.keys() :
                    logger.error('Data Source(ID=%s), Point(ID=%s) Invalid address data.',
                                 data_source_id, point['id'])
                    # invalid point is found
                    # go to begin of foreach point loop to process next point
                    continue

                result = dict()
                try:
                    if address["url"][0] != '/':
                        address["url"] = '/'+address["url"]
                    url = f'{host}:{port}{address["url"]}?{address["add"]}'

                    output = ""
                    res = requests.get(url,timeout=3)
                    
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
                        # timeout error
                        # break the foreach point loop
                        break
                    else:
                        # exception occurred when read register value,
                        # go to begin of foreach point loop to process next point
                        continue

                if result is None or not isinstance(result, dict) or len(result) == 0:
                    logger.error("Error in step 3.3 of acquisition process: \n"
                                 " invalid result: None "
                                 " for point_id: " + str(point['id']))
                    # invalid result
                    # go to begin of foreach point loop to process next point
                    continue

                if not isinstance(result['meta'], dict) or \
                    not isinstance(result['data'], dict) :
                    
                    logger.error(f"point_id:<{point['id']}> 返回 {result['meta']} ")
                    # invalid result
                    # go to begin of foreach point loop to process next point
                    continue

                if result['meta']['success'] != true or\
                    len(result['data']['data']) == 0 :    
                    logger.error(" Error in step 3.5 of acquisition process:\n"
                                 " http query not success  "
                                 " for point_id: " + str(point['id']))
                else:
                    value = result['data']['data']
                    logger.info(f"point:{point['id']} value: {value}")

                energy_value_list.append({'point_id': point['id'],
                                            'is_trend': point['is_trend'],
                                            'value': Decimal(value) * point['ratio']})
            # end of foreach point loop

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

            ############################################################################################################
            # Step 4: Bulk insert point values and update latest values in historical database
            ############################################################################################################
            # check the connection to the Historical Database
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

        # end of the inner while loop

    # end of the outermost while loop
