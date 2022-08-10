# -*- coding: utf_8 -*-
import sys
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu_over_tcp as modbus_tcp


logger = modbus_tk.utils.create_logger("console")
if __name__ == "__main__":
	try:
		#master = modbus_tcp.TcpMaster(host="192.168.60.30", port=6565)
		master = modbus_tcp.TcpMaster(host='192.168.40.146',port=502,timeout_in_sec=5)



		logger.info(master.execute(slave=1, function_code=3, starting_address=0, quantity_of_x=10))
        
	except modbus_tk.modbus.ModbusError:
		logger.info("----------------")
		logger.error("%s- Code=%d" % (modbus_tk.modbus.ModbusError, modbus_tk.modbus.ModbusError.get_exception_code()))
		logger.info("================")