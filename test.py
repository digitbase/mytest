import sys
from modbus_tk import modbus_tcp
import telnetlib
import byte_swap


def main():
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = "192.168.40.21"

    port = 502
    try:
        telnetlib.Telnet(host, port, 10)
        print("Succeeded to telnet %s:%s ", host, port)
    except Exception as e:
        print("Failed to telnet %s:%s : %s  ", host, port, str(e))
        return

    try:
        master = modbus_tcp.TcpMaster(host=host, port=port, timeout_in_sec=15.0)
        master.set_timeout(15.0)
        print("Connected to %s:%s ", host, port)
        print("read registers...")
        result = master.execute(slave=1, function_code=3, starting_address=0, quantity_of_x=2, data_format='<l')
        print("51AL1-1-KWHimp = " + str(byte_swap.byte_swap_32_bit(result[0])))
        result = master.execute(slave=1, function_code=3, starting_address=6403, quantity_of_x=2, data_format='<l')
        print("51AL2-1-KWHimp = " + str(byte_swap.byte_swap_32_bit(result[0])))
        result = master.execute(slave=1, function_code=3, starting_address=6405, quantity_of_x=2, data_format='<l')
        print("51AL3-1-KWHimp = " + str(byte_swap.byte_swap_32_bit(result[0])))
        result = master.execute(slave=1, function_code=3, starting_address=6407, quantity_of_x=2, data_format='<l')
        print("51AL4-1-KWHimp  = " + str(byte_swap.byte_swap_32_bit(result[0])))
        result = master.execute(slave=1, function_code=3, starting_address=6409, quantity_of_x=2, data_format='<l')
        print("51AL5-1-KWHimp = " + str(byte_swap.byte_swap_32_bit(result[0])))


        master.close()
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()
