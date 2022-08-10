import json
import mysql.connector
import config
from multiprocessing import Process
import time
import logging
from logging.handlers import RotatingFileHandler
import gateway
import acquisition
from test import prd





def main():
    """main"""
    # create logger
    logger = logging.getLogger('myems-fz')
    # specifies the lowest-severity log message a logger will handle,
    # where debug is the lowest built-in severity level and critical is the highest built-in severity.
    # For example, if the severity level is INFO, the logger will handle only INFO, WARNING, ERROR, and CRITICAL
    # messages and will ignore DEBUG messages.
    logger.setLevel(logging.INFO)
    # create file handler which logs messages
    fh = RotatingFileHandler('myems-fz.log', maxBytes=1024*1024, backupCount=1)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(fh)
    # send logging output to sys.stderr
    logger.addHandler(logging.StreamHandler())

    ####################################################################################################################
    # Create Gateway Process
    ####################################################################################################################
    Process(target=gateway.process, args=(logger,)).start()


    # Get Data Sources
    while True:
        # TODO: This service has to RESTART to reload latest data sources and this should be fixed
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
            # sleep several minutes and continue the outer loop to reload points
            time.sleep(6)
            continue

        # Get data sources by gateway and protocol
        try:
            query = (" SELECT ds.id, ds.name, ds.connection "
                     " FROM tbl_data_sources ds, tbl_gateways g "
                     " WHERE  ds.gateway_id = g.id AND g.id = 1 "
                     " ORDER BY ds.id ")
  
            cursor_system_db.execute(query)
            rows_data_source = cursor_system_db.fetchall()
        except Exception as e:
            logger.error("Error in main process " + str(e))
            time.sleep(6)
            continue
        finally:
            if cursor_system_db:
                cursor_system_db.close()
            if cnx_system_db:
                cnx_system_db.close()
        if rows_data_source is None or len(rows_data_source) == 0:
            logger.error("Data Source Not Found, Wait for minutes to retry.")
            # wait for a while and retry
            time.sleep(6)
            continue
        else:
            # Stop to connect these data sources
            break

    for row_data_source in rows_data_source:
        print("Data Source: ID=%s, Name=%s, Connection=%s " %
              (row_data_source[0], row_data_source[1], row_data_source[2]))

        if row_data_source[2] is None or len(row_data_source[2]) == 0:
            logger.error("Data Source Connection Not Found.")
            continue

        try:

            
            server = json.loads(row_data_source[2])
            print(server);
        except Exception as e:
            logger.error("Data Source Connection JSON error " + str(e))
            continue

        if 'host' not in server.keys() \
                or 'port' not in server.keys() \
                or server['host'] is None \
                or server['port'] is None \
                or len(server['host']) == 0 \
                or not isinstance(server['port'], int) \
                or server['port'] < 1:
            
            logger.error("Data Source Connection Invalid.")
            continue

        # fork worker process for each data source
        # todo: how to restart the process if the process terminated unexpectedly

        print("row_data_source=%s,  server['host']=%s, server['port']=%s " %
              (row_data_source[0], server['host'], server['port']))
        Process(target=acquisition.process, args=(logger, row_data_source[0], server['host'], server['port'])).start()
        #acquisition.process(logger, row_data_source[0], server['host'], server['port'])



if __name__ == "__main__":
    main()
