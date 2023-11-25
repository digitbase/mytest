
import calendar
import inspect
import re
import json
import os
import falcon
import re
import falcon
import simplejson as json
import mysql.connector

from datetime import datetime, timedelta, timezone
from decimal import Decimal

loc = locals()


def get_variable_name(variable):
    for k, v in loc.items():
        if loc[k] == variable:
            return k


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except:
        return False
    return True


def pdict(a):
    y = json.dumps(a, sort_keys=True, indent=4, separators=(',', ': '))
    print(y)


st = ['~', '#', '@', '#', '$', '%', '^', '&', '*', '_', '-', '+', '\\']

#直接打印
def prm(a, p=0):
    print(type(a), end='')
    print(' =>> ', (a),end="\n")


#打印结束
def prd(a, p=0):
    prm(a, p)
    print('======= prd end =========')
    os._exit(0)

#写入文件
def prf(a, type='w'):
    fileName = 'res.html'
    if type == 'w':
        with open(fileName, 'w') as file:
            file.write(str(a))
    else:
        with open(fileName, 'a') as file:
            file.write(str(a))


def htmlp(resp, param):
    resp.text = json.dumps(param)


def pres(res):
    resObj = json.loads(res)
    if (type(resObj)) == dict:
        for i in resObj:
            if (i != 'excel_bytes_base64') and \
                    (i != 'parameters'):
                print(f'{i} : {resObj[i]} \n')
    else:
        print(resObj)

def subMonth(req, type=0):
    
    
    if type == 0 :
        
        space_id = req.params.get('spaceid')
        period_type = "monthly"
        year = req.params.get('year')
        month = req.params.get('month')
    else :
        space_id = req['spaceid']
        period_type = "monthly"
        year = req['year']
        month = req['month']



    if year is None or year.isdigit() != True or int(year) < 2000 or int(year) > 3000:
        raise falcon.HTTPError(falcon.HTTP_400,
                                title='API.BAD_REQUEST',
                                description='API.INVALID_YEAR')
        
    if  month.isdigit() != True or int(year) >2099 or int(year) <= 0:
                raise falcon.HTTPError(falcon.HTTP_400,
                                        title='API.BAD_REQUEST',
                                        description='API.INVALID_YEAR')

    if month is None :
        raise falcon.HTTPError(falcon.HTTP_400,
                                title='API.BAD_REQUEST',
                                description='API.INVALID_MONTH')
        
    if month.isdigit() != True or int(month) <= 0 or int(month) > 12:
                raise falcon.HTTPError(falcon.HTTP_400,
                                        title='API.BAD_REQUEST',
                                        description='API.INVALID_MONTH')
                
                
    weekDay,monthCountDay = calendar.monthrange(int(year),int(month))
            
    reporting_start_datetime_local = f"{year}-{month}-01T00:00:00"
    reporting_end_datetime_local = f"{year}-{month}-{monthCountDay}T23:59:59"
    
    base = datetime.strptime(reporting_start_datetime_local,
                                            '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc) - timedelta(1)
    base_year = base.year
    base_month = base.month
    base_day = base.day
    base_start_datetime_local = f"{base_year}-{base_month}-01T00:00:00"
    base_end_datetime_local = f"{base_year}-{base_month}-{base_day}T23:59:59"

    

    ################################################################################################################
    # Step 1: valid parameters
    ################################################################################################################
    if space_id is None :
        raise falcon.HTTPError(falcon.HTTP_400,
                                title='API.BAD_REQUEST',
                                description='API.INVALID_SPACE_ID')

    if space_id is not None:
        space_id = str.strip(space_id)
        if not space_id.isdigit() or int(space_id) <= 0:
            raise falcon.HTTPError(falcon.HTTP_400,
                                    title='API.BAD_REQUEST',
                                    description='API.INVALID_SPACE_ID')


    if period_type is None:
        raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST', description='API.INVALID_PERIOD_TYPE')
    else:
        period_type = str.strip(period_type)
        if period_type not in ['hourly', 'daily', 'weekly', 'monthly', 'yearly']:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST', description='API.INVALID_PERIOD_TYPE')

    timezone_offset = int(config.utc_offset[1:3]) * 60 + int(config.utc_offset[4:6])
    if config.utc_offset[0] == '-':
        timezone_offset = -timezone_offset

    base_start_datetime_utc = None
    if base_start_datetime_local is not None and len(str.strip(base_start_datetime_local)) > 0:
        base_start_datetime_local = str.strip(base_start_datetime_local)
        try:
            base_start_datetime_utc = datetime.strptime(base_start_datetime_local,
                                                        '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc) - \
                timedelta(minutes=timezone_offset)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                    description="API.INVALID_BASE_PERIOD_START_DATETIME")

    base_end_datetime_utc = None
    if base_end_datetime_local is not None and len(str.strip(base_end_datetime_local)) > 0:
        base_end_datetime_local = str.strip(base_end_datetime_local)
        try:
            base_end_datetime_utc = datetime.strptime(base_end_datetime_local,
                                                        '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc) - \
                timedelta(minutes=timezone_offset)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                    description="API.INVALID_BASE_PERIOD_END_DATETIME")

    if base_start_datetime_utc is not None and base_end_datetime_utc is not None and \
            base_start_datetime_utc >= base_end_datetime_utc:
        raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                description='API.INVALID_BASE_PERIOD_END_DATETIME')

    if reporting_start_datetime_local is None:
        raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                description="API.INVALID_REPORTING_PERIOD_START_DATETIME")
    else:
        reporting_start_datetime_local = str.strip(reporting_start_datetime_local)
        try:
            reporting_start_datetime_utc = datetime.strptime(reporting_start_datetime_local,
                                                                '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc) - \
                timedelta(minutes=timezone_offset)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                    description="API.INVALID_REPORTING_PERIOD_START_DATETIME")

    if reporting_end_datetime_local is None:
        raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                description="API.INVALID_REPORTING_PERIOD_END_DATETIME")
    else:
        reporting_end_datetime_local = str.strip(reporting_end_datetime_local)
        try:
            reporting_end_datetime_utc = datetime.strptime(reporting_end_datetime_local,
                                                            '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc) - \
                timedelta(minutes=timezone_offset)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                    description="API.INVALID_REPORTING_PERIOD_END_DATETIME")

    if reporting_start_datetime_utc >= reporting_end_datetime_utc:
        raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                description='API.INVALID_REPORTING_PERIOD_END_DATETIME')

    # if turn quick mode on, do not return parameters data and excel file
    is_quick_mode = False


    ################################################################################################################
    # Step 2: query the space
    ################################################################################################################
    cnx_system = mysql.connector.connect(**config.myems_system_db)
    cursor_system = cnx_system.cursor()

    cnx_energy = mysql.connector.connect(**config.myems_energy_db)
    cursor_energy = cnx_energy.cursor()

    cnx_historical = mysql.connector.connect(**config.myems_historical_db)
    cursor_historical = cnx_historical.cursor()

    if space_id is not None:
        cursor_system.execute(" SELECT id, name, area, cost_center_id "
                                " FROM tbl_spaces "
                                " WHERE id = %s ", (space_id,))
        row_space = cursor_system.fetchone()


    if row_space is None:
        if cursor_system:
            cursor_system.close()
        if cnx_system:
            cnx_system.close()

        if cursor_energy:
            cursor_energy.close()
        if cnx_energy:
            cnx_energy.close()

        if cursor_historical:
            cursor_historical.close()
        if cnx_historical:
            cnx_historical.close()
        raise falcon.HTTPError(falcon.HTTP_404, title='API.NOT_FOUND', description='API.SPACE_NOT_FOUND')

    space = dict()
    space['id'] = row_space[0]
    space['name'] = row_space[1]
    space['area'] = row_space[2]
    space['cost_center_id'] = row_space[3]

    ################################################################################################################
    # Step 3: query energy categories
    ################################################################################################################
    energy_category_set = set()
    # query energy categories in base period
    cursor_energy.execute(" SELECT DISTINCT(energy_category_id) "
                            " FROM tbl_space_input_category_hourly "
                            " WHERE space_id = %s "
                            "     AND start_datetime_utc >= %s "
                            "     AND start_datetime_utc < %s ",
                            (space['id'], base_start_datetime_utc, base_end_datetime_utc))
    rows_energy_categories = cursor_energy.fetchall()
    if rows_energy_categories is not None or len(rows_energy_categories) > 0:
        for row_energy_category in rows_energy_categories:
            energy_category_set.add(row_energy_category[0])

    # query energy categories in reporting period
    cursor_energy.execute(" SELECT DISTINCT(energy_category_id) "
                            " FROM tbl_space_input_category_hourly "
                            " WHERE space_id = %s "
                            "     AND start_datetime_utc >= %s "
                            "     AND start_datetime_utc < %s ",
                            (space['id'], reporting_start_datetime_utc, reporting_end_datetime_utc))
    rows_energy_categories = cursor_energy.fetchall()
    if rows_energy_categories is not None or len(rows_energy_categories) > 0:
        for row_energy_category in rows_energy_categories:
            energy_category_set.add(row_energy_category[0])

    # query all energy categories in base period and reporting period
    cursor_system.execute(" SELECT id, name, unit_of_measure, kgce, kgco2e "
                            " FROM tbl_energy_categories "
                            " ORDER BY id ", )
    rows_energy_categories = cursor_system.fetchall()
    if rows_energy_categories is None or len(rows_energy_categories) == 0:
        if cursor_system:
            cursor_system.close()
        if cnx_system:
            cnx_system.close()

        if cursor_energy:
            cursor_energy.close()
        if cnx_energy:
            cnx_energy.close()

        if cursor_historical:
            cursor_historical.close()
        if cnx_historical:
            cnx_historical.close()
        raise falcon.HTTPError(falcon.HTTP_404,
                                title='API.NOT_FOUND',
                                description='API.ENERGY_CATEGORY_NOT_FOUND')
    energy_category_dict = dict()
    for row_energy_category in rows_energy_categories:
        if row_energy_category[0] in energy_category_set:
            energy_category_dict[row_energy_category[0]] = {"name": row_energy_category[1],
                                                            "unit_of_measure": row_energy_category[2],
                                                            "kgce": row_energy_category[3],
                                                            "kgco2e": row_energy_category[4]}

    ################################################################################################################
    # Step 4: query associated sensors
    ################################################################################################################
    point_list = list()
    cursor_system.execute(" SELECT po.id, po.name, po.units, po.object_type  "
                            " FROM tbl_spaces sp, tbl_sensors se, tbl_spaces_sensors spse, "
                            "      tbl_points po, tbl_sensors_points sepo "
                            " WHERE sp.id = %s AND sp.id = spse.space_id AND spse.sensor_id = se.id "
                            "       AND se.id = sepo.sensor_id AND sepo.point_id = po.id "
                            " ORDER BY po.id ", (space['id'], ))
    rows_points = cursor_system.fetchall()
    if rows_points is not None and len(rows_points) > 0:
        for row in rows_points:
            point_list.append({"id": row[0], "name": row[1], "units": row[2], "object_type": row[3]})

    ################################################################################################################
    # Step 5: query associated points
    ################################################################################################################
    cursor_system.execute(" SELECT po.id, po.name, po.units, po.object_type  "
                            " FROM tbl_spaces sp, tbl_spaces_points sppo, tbl_points po "
                            " WHERE sp.id = %s AND sp.id = sppo.space_id AND sppo.point_id = po.id "
                            " ORDER BY po.id ", (space['id'], ))
    rows_points = cursor_system.fetchall()
    if rows_points is not None and len(rows_points) > 0:
        for row in rows_points:
            point_list.append({"id": row[0], "name": row[1], "units": row[2], "object_type": row[3]})

    base = dict()
    if energy_category_set is not None and len(energy_category_set) > 0:
        for energy_category_id in energy_category_set:
            kgce = energy_category_dict[energy_category_id]['kgce']
            kgco2e = energy_category_dict[energy_category_id]['kgco2e']

            base[energy_category_id] = dict()
            base[energy_category_id]['timestamps'] = list()
            base[energy_category_id]['values'] = list()
            base[energy_category_id]['subtotal'] = Decimal(0.0)
            base[energy_category_id]['subtotal_in_kgce'] = Decimal(0.0)
            base[energy_category_id]['subtotal_in_kgco2e'] = Decimal(0.0)

            cursor_energy.execute(" SELECT start_datetime_utc, actual_value "
                                    " FROM tbl_space_input_category_hourly "
                                    " WHERE space_id = %s "
                                    "     AND energy_category_id = %s "
                                    "     AND start_datetime_utc >= %s "
                                    "     AND start_datetime_utc < %s "
                                    " ORDER BY start_datetime_utc ",
                                    (space['id'],
                                    energy_category_id,
                                    base_start_datetime_utc,
                                    base_end_datetime_utc))
            rows_space_hourly = cursor_energy.fetchall()

            rows_space_periodically = utilities.aggregate_hourly_data_by_period(rows_space_hourly,
                                                                                base_start_datetime_utc,
                                                                                base_end_datetime_utc,
                                                                                period_type)
            for row_space_periodically in rows_space_periodically:
                current_datetime_local = row_space_periodically[0].replace(tzinfo=timezone.utc) + \
                                            timedelta(minutes=timezone_offset)
                if period_type == 'hourly':
                    current_datetime = current_datetime_local.strftime('%Y-%m-%dT%H:%M:%S')
                elif period_type == 'daily':
                    current_datetime = current_datetime_local.strftime('%Y-%m-%d')
                elif period_type == 'weekly':
                    current_datetime = current_datetime_local.strftime('%Y-%m-%d')
                elif period_type == 'monthly':
                    current_datetime = current_datetime_local.strftime('%Y-%m')
                elif period_type == 'yearly':
                    current_datetime = current_datetime_local.strftime('%Y')

                actual_value = Decimal(0.0) if row_space_periodically[1] is None else row_space_periodically[1]
                base[energy_category_id]['timestamps'].append(current_datetime)
                base[energy_category_id]['values'].append(actual_value)
                base[energy_category_id]['subtotal'] += actual_value
                base[energy_category_id]['subtotal_in_kgce'] += actual_value * kgce
                base[energy_category_id]['subtotal_in_kgco2e'] += actual_value * kgco2e

    ################################################################################################################
    # Step 8: query reporting period energy input
    ################################################################################################################
    reporting = dict()
    if energy_category_set is not None and len(energy_category_set) > 0:
        for energy_category_id in energy_category_set:
            kgce = energy_category_dict[energy_category_id]['kgce']
            kgco2e = energy_category_dict[energy_category_id]['kgco2e']

            reporting[energy_category_id] = dict()
            reporting[energy_category_id]['timestamps'] = list()
            reporting[energy_category_id]['values'] = list()
            reporting[energy_category_id]['subtotal'] = Decimal(0.0)
            reporting[energy_category_id]['subtotal_in_kgce'] = Decimal(0.0)
            reporting[energy_category_id]['subtotal_in_kgco2e'] = Decimal(0.0)
            reporting[energy_category_id]['toppeak'] = Decimal(0.0)
            reporting[energy_category_id]['onpeak'] = Decimal(0.0)
            reporting[energy_category_id]['midpeak'] = Decimal(0.0)
            reporting[energy_category_id]['offpeak'] = Decimal(0.0)

            cursor_energy.execute(" SELECT start_datetime_utc, actual_value "
                                    " FROM tbl_space_input_category_hourly "
                                    " WHERE space_id = %s "
                                    "     AND energy_category_id = %s "
                                    "     AND start_datetime_utc >= %s "
                                    "     AND start_datetime_utc < %s "
                                    " ORDER BY start_datetime_utc ",
                                    (space['id'],
                                    energy_category_id,
                                    reporting_start_datetime_utc,
                                    reporting_end_datetime_utc))
            rows_space_hourly = cursor_energy.fetchall()

            rows_space_periodically = utilities.aggregate_hourly_data_by_period(rows_space_hourly,
                                                                                reporting_start_datetime_utc,
                                                                                reporting_end_datetime_utc,
                                                                                period_type)
            for row_space_periodically in rows_space_periodically:

                actual_value = Decimal(0.0) if row_space_periodically[1] is None else row_space_periodically[1]
                reporting[energy_category_id]['values'].append(actual_value)
                reporting[energy_category_id]['subtotal'] += actual_value
                reporting[energy_category_id]['subtotal_in_kgco2e'] += actual_value * kgco2e


    if cursor_system:
        cursor_system.close()
    if cnx_system:
        cnx_system.close()

    if cursor_energy:
        cursor_energy.close()
    if cnx_energy:
        cnx_energy.close()

    if cursor_historical:
        cursor_historical.close()
    if cnx_historical:
        cnx_historical.close()

    result = dict()

    result['space'] = dict()
    result['space']['name'] = space['name']
    result['space']['area'] = space['area']

    result['base_period'] = dict()
    result['base_period']['total_in_kgco2e'] = Decimal(0.0)
    if energy_category_set is not None and len(energy_category_set) > 0:
        for energy_category_id in energy_category_set:
            result['base_period']['total_in_kgco2e'] += base[energy_category_id]['subtotal_in_kgco2e']

    result['reporting_period'] = dict()
    result['reporting_period']['total_in_kgco2e'] = Decimal(0.0)

    if energy_category_set is not None and len(energy_category_set) > 0:
        for energy_category_id in energy_category_set:
            result['reporting_period']['total_in_kgco2e'] += reporting[energy_category_id]['subtotal_in_kgco2e']

    result['increment_rate_in_kgco2e'] = \
        (result['reporting_period']['total_in_kgco2e'] - result['base_period']['total_in_kgco2e']) / \
        result['base_period']['total_in_kgco2e'] \
        if result['base_period']['total_in_kgco2e'] > Decimal(0.0) else None
    return (result)




def yearcost(req):
    
    
    space_id = req.params.get('spaceid')
    period_type = "yearly"
    year = req.params.get('year')


    if year is None or year.isdigit() != True or int(year) < 2000 or int(year) > 3000:
        raise falcon.HTTPError(falcon.HTTP_400,
                                title='API.BAD_REQUEST',
                                description='API.INVALID_YEAR')
            
    reporting_start_datetime_local = f"{year}-01-01T00:00:00"
    reporting_end_datetime_local = f"{year}-12-31T23:59:59"
    
    
    

    if space_id is None :
        raise falcon.HTTPError(falcon.HTTP_400,
                                title='API.BAD_REQUEST',
                                description='API.INVALID_SPACE_ID')

    if space_id is not None:
        space_id = str.strip(space_id)
        if not space_id.isdigit() or int(space_id) <= 0:
            raise falcon.HTTPError(falcon.HTTP_400,
                                    title='API.BAD_REQUEST',
                                    description='API.INVALID_SPACE_ID')

    timezone_offset = int(config.utc_offset[1:3]) * 60 + int(config.utc_offset[4:6])
    if config.utc_offset[0] == '-':
        timezone_offset = -timezone_offset


    reporting_start_datetime_local = str.strip(reporting_start_datetime_local)
    try:
        reporting_start_datetime_utc = datetime.strptime(reporting_start_datetime_local,
                                                            '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc) - \
            timedelta(minutes=timezone_offset)
    except ValueError:
        raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                description="API.INVALID_REPORTING_PERIOD_START_DATETIME")

    reporting_end_datetime_local = str.strip(reporting_end_datetime_local)
    try:
        reporting_end_datetime_utc = datetime.strptime(reporting_end_datetime_local,
                                                        '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc) - \
            timedelta(minutes=timezone_offset)
    except ValueError:
        raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                description="API.INVALID_REPORTING_PERIOD_END_DATETIME")

    if reporting_start_datetime_utc >= reporting_end_datetime_utc:
        raise falcon.HTTPError(falcon.HTTP_400, title='API.BAD_REQUEST',
                                description='API.INVALID_REPORTING_PERIOD_END_DATETIME')
    base_end_datetime_utc = None
    base_start_datetime_utc = None
    space_uuid = None

    cnx_system = mysql.connector.connect(**config.myems_system_db)
    cursor_system = cnx_system.cursor()

    cnx_billing = mysql.connector.connect(**config.myems_billing_db)
    cursor_billing = cnx_billing.cursor()

    cnx_historical = mysql.connector.connect(**config.myems_historical_db)
    cursor_historical = cnx_historical.cursor()

    if space_id is not None:
        cursor_system.execute(" SELECT id, name, area, cost_center_id "
                                " FROM tbl_spaces "
                                " WHERE id = %s ", (space_id,))
        row_space = cursor_system.fetchone()
    elif space_uuid is not None:
        cursor_system.execute(" SELECT id, name, area, cost_center_id "
                                " FROM tbl_spaces "
                                " WHERE uuid = %s ", (space_uuid,))
        row_space = cursor_system.fetchone()

    if row_space is None:
        if cursor_system:
            cursor_system.close()
        if cnx_system:
            cnx_system.close()

        if cursor_billing:
            cursor_billing.close()
        if cnx_billing:
            cnx_billing.close()

        if cursor_historical:
            cursor_historical.close()
        if cnx_historical:
            cnx_historical.close()
        raise falcon.HTTPError(falcon.HTTP_404, title='API.NOT_FOUND', description='API.SPACE_NOT_FOUND')

    space = dict()
    space['id'] = row_space[0]
    space['name'] = row_space[1]
    space['area'] = row_space[2]
    space['cost_center_id'] = row_space[3]

    ################################################################################################################
    # Step 3: query energy categories
    ################################################################################################################
    energy_category_set = set()
    # query energy categories in base period
    cursor_billing.execute(" SELECT DISTINCT(energy_category_id) "
                            " FROM tbl_space_input_category_hourly "
                            " WHERE space_id = %s "
                            "     AND start_datetime_utc >= %s "
                            "     AND start_datetime_utc < %s ",
                            (space['id'], base_start_datetime_utc, base_end_datetime_utc))
    rows_energy_categories = cursor_billing.fetchall()
    if rows_energy_categories is not None or len(rows_energy_categories) > 0:
        for row_energy_category in rows_energy_categories:
            energy_category_set.add(row_energy_category[0])

    # query energy categories in reporting period
    cursor_billing.execute(" SELECT DISTINCT(energy_category_id) "
                            " FROM tbl_space_input_category_hourly "
                            " WHERE space_id = %s "
                            "     AND start_datetime_utc >= %s "
                            "     AND start_datetime_utc < %s ",
                            (space['id'], reporting_start_datetime_utc, reporting_end_datetime_utc))
    rows_energy_categories = cursor_billing.fetchall()
    if rows_energy_categories is not None or len(rows_energy_categories) > 0:
        for row_energy_category in rows_energy_categories:
            energy_category_set.add(row_energy_category[0])

    # query all energy categories in base period and reporting period
    cursor_system.execute(" SELECT id, name, unit_of_measure, kgce, kgco2e "
                            " FROM tbl_energy_categories "
                            " ORDER BY id ", )
    rows_energy_categories = cursor_system.fetchall()
    if rows_energy_categories is None or len(rows_energy_categories) == 0:
        if cursor_system:
            cursor_system.close()
        if cnx_system:
            cnx_system.close()

        if cursor_billing:
            cursor_billing.close()
        if cnx_billing:
            cnx_billing.close()

        if cursor_historical:
            cursor_historical.close()
        if cnx_historical:
            cnx_historical.close()
        raise falcon.HTTPError(falcon.HTTP_404,
                                title='API.NOT_FOUND',
                                description='API.ENERGY_CATEGORY_NOT_FOUND')
    energy_category_dict = dict()
    for row_energy_category in rows_energy_categories:
        if row_energy_category[0] in energy_category_set:
            energy_category_dict[row_energy_category[0]] = {"name": row_energy_category[1],
                                                            "unit_of_measure": row_energy_category[2],
                                                            "kgce": row_energy_category[3],
                                                            "kgco2e": row_energy_category[4]}

    ################################################################################################################
    # Step 4: query associated sensors
    ################################################################################################################
    point_list = list()
    cursor_system.execute(" SELECT po.id, po.name, po.units, po.object_type  "
                            " FROM tbl_spaces sp, tbl_sensors se, tbl_spaces_sensors spse, "
                            "      tbl_points po, tbl_sensors_points sepo "
                            " WHERE sp.id = %s AND sp.id = spse.space_id AND spse.sensor_id = se.id "
                            "       AND se.id = sepo.sensor_id AND sepo.point_id = po.id "
                            " ORDER BY po.id ", (space['id'], ))
    rows_points = cursor_system.fetchall()
    if rows_points is not None and len(rows_points) > 0:
        for row in rows_points:
            point_list.append({"id": row[0], "name": row[1], "units": row[2], "object_type": row[3]})

    ################################################################################################################
    # Step 5: query associated points
    ################################################################################################################
    cursor_system.execute(" SELECT po.id, po.name, po.units, po.object_type  "
                            " FROM tbl_spaces sp, tbl_spaces_points sppo, tbl_points po "
                            " WHERE sp.id = %s AND sp.id = sppo.space_id AND sppo.point_id = po.id "
                            " ORDER BY po.id ", (space['id'], ))
    rows_points = cursor_system.fetchall()
    if rows_points is not None and len(rows_points) > 0:
        for row in rows_points:
            point_list.append({"id": row[0], "name": row[1], "units": row[2], "object_type": row[3]})

    ################################################################################################################
    # Step 6: query child spaces
    ################################################################################################################
    child_space_list = list()
    cursor_system.execute(" SELECT id, name  "
                            " FROM tbl_spaces "
                            " WHERE parent_space_id = %s "
                            " ORDER BY id ", (space['id'], ))
    rows_child_spaces = cursor_system.fetchall()
    if rows_child_spaces is not None and len(rows_child_spaces) > 0:
        for row in rows_child_spaces:
            child_space_list.append({"id": row[0], "name": row[1]})

    ################################################################################################################
    # Step 7: query base period energy cost
    ################################################################################################################
    base = dict()
    if energy_category_set is not None and len(energy_category_set) > 0:
        for energy_category_id in energy_category_set:
            base[energy_category_id] = dict()
            # base[energy_category_id]['timestamps'] = list()
            # base[energy_category_id]['values'] = list()
            base[energy_category_id]['subtotal'] = Decimal(0.0)

            cursor_billing.execute(" SELECT start_datetime_utc, actual_value "
                                    " FROM tbl_space_input_category_hourly "
                                    " WHERE space_id = %s "
                                    "     AND energy_category_id = %s "
                                    "     AND start_datetime_utc >= %s "
                                    "     AND start_datetime_utc < %s "
                                    " ORDER BY start_datetime_utc ",
                                    (space['id'],
                                    energy_category_id,
                                    base_start_datetime_utc,
                                    base_end_datetime_utc))
            rows_space_hourly = cursor_billing.fetchall()

            rows_space_periodically = utilities.aggregate_hourly_data_by_period(rows_space_hourly,
                                                                                base_start_datetime_utc,
                                                                                base_end_datetime_utc,
                                                                                period_type)
            for row_space_periodically in rows_space_periodically:
                current_datetime_local = row_space_periodically[0].replace(tzinfo=timezone.utc) + \
                                            timedelta(minutes=timezone_offset)
                if period_type == 'hourly':
                    current_datetime = current_datetime_local.strftime('%Y-%m-%dT%H:%M:%S')
                elif period_type == 'daily':
                    current_datetime = current_datetime_local.strftime('%Y-%m-%d')
                elif period_type == 'weekly':
                    current_datetime = current_datetime_local.strftime('%Y-%m-%d')
                elif period_type == 'monthly':
                    current_datetime = current_datetime_local.strftime('%Y-%m')
                elif period_type == 'yearly':
                    current_datetime = current_datetime_local.strftime('%Y')

                actual_value = Decimal(0.0) if row_space_periodically[1] is None else row_space_periodically[1]
                base[energy_category_id]['timestamps'].append(current_datetime)
                base[energy_category_id]['values'].append(actual_value)
                base[energy_category_id]['subtotal'] += actual_value

    ################################################################################################################
    # Step 8: query reporting period energy cost
    ################################################################################################################
    reporting = dict()
    if energy_category_set is not None and len(energy_category_set) > 0:
        for energy_category_id in energy_category_set:
            reporting[energy_category_id] = dict()
            # reporting[energy_category_id]['timestamps'] = list()
            # reporting[energy_category_id]['values'] = list()
            reporting[energy_category_id]['subtotal'] = Decimal(0.0)
            # reporting[energy_category_id]['toppeak'] = Decimal(0.0)
            # reporting[energy_category_id]['onpeak'] = Decimal(0.0)
            # reporting[energy_category_id]['midpeak'] = Decimal(0.0)
            # reporting[energy_category_id]['offpeak'] = Decimal(0.0)

            cursor_billing.execute(" SELECT start_datetime_utc, actual_value "
                                    " FROM tbl_space_input_category_hourly "
                                    " WHERE space_id = %s "
                                    "     AND energy_category_id = %s "
                                    "     AND start_datetime_utc >= %s "
                                    "     AND start_datetime_utc < %s "
                                    " ORDER BY start_datetime_utc ",
                                    (space['id'],
                                    energy_category_id,
                                    reporting_start_datetime_utc,
                                    reporting_end_datetime_utc))
            rows_space_hourly = cursor_billing.fetchall()

            rows_space_periodically = utilities.aggregate_hourly_data_by_period(rows_space_hourly,
                                                                                reporting_start_datetime_utc,
                                                                                reporting_end_datetime_utc,
                                                                                period_type)
            for row_space_periodically in rows_space_periodically:
                current_datetime_local = row_space_periodically[0].replace(tzinfo=timezone.utc) + \
                                            timedelta(minutes=timezone_offset)
                if period_type == 'hourly':
                    current_datetime = current_datetime_local.strftime('%Y-%m-%dT%H:%M:%S')
                elif period_type == 'daily':
                    current_datetime = current_datetime_local.strftime('%Y-%m-%d')
                elif period_type == 'weekly':
                    current_datetime = current_datetime_local.strftime('%Y-%m-%d')
                elif period_type == 'monthly':
                    current_datetime = current_datetime_local.strftime('%Y-%m')
                elif period_type == 'yearly':
                    current_datetime = current_datetime_local.strftime('%Y')

                actual_value = Decimal(0.0) if row_space_periodically[1] is None else row_space_periodically[1]
                # reporting[energy_category_id]['timestamps'].append(current_datetime)
                # reporting[energy_category_id]['values'].append(actual_value)
                reporting[energy_category_id]['subtotal'] += actual_value

            energy_category_tariff_dict = utilities.get_energy_category_peak_types(space['cost_center_id'],
                                                                                    energy_category_id,
                                                                                    reporting_start_datetime_utc,
                                                                                    reporting_end_datetime_utc)




    if cursor_system:
        cursor_system.close()
    if cnx_system:
        cnx_system.close()

    if cursor_billing:
        cursor_billing.close()
    if cnx_billing:
        cnx_billing.close()

    if cursor_historical:
        cursor_historical.close()
    if cnx_historical:
        cnx_historical.close()

    return reporting