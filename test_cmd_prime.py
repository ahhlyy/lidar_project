import serial.tools.list_ports
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from binascii import unhexlify
import time  # 添加定时器
from time import *
import numpy as np

Baudrate = [9600, 115200, 19200, 38400, 57600]
def find_serial_ports():
    """
    自动识别可用的串口号
    """
    ports = list(serial.tools.list_ports.comports())
    result = []
    for port in ports:
        result.append(port.device)
    return result

def choose_serial_port():
    """
    进行串口选择并返回选择的串口名称
    """
    serial_ports = find_serial_ports()
    if len(serial_ports) == 0:
        print("找不到可用的串口，请检查串口连接")
        return None
    else:
        print("可用串口列表:")
        for i, port in enumerate(serial_ports):
            print(f"{i+1}. {port}")
        while True:
            try:
                choice = int(input("请输入要选择的串口编号: "))
                if choice > 0 and choice <= len(serial_ports):
                    selected_port = serial_ports[choice - 1]
                    print(f"已选择串口: {selected_port}\n")
                    return selected_port
                else:
                    print("输入不正确，请重新输入")
            except ValueError:
                print("输入不正确，请重新输入")

# 测距配置
def mod_lidar(BAUDRATE, SlaveID):
    red = []
    alarm = ""
    master = establish_serial(selected_port, BAUDRATE)
    try:
        # 读保持寄存器
        red = master.execute(slave=SlaveID, function_code=cst.READ_HOLDING_REGISTERS, starting_address=0,
                             quantity_of_x=2)  # 这里可以修改需要读取的功能码
        print(red)
        alarm = "正常"

        return alarm

    except Exception as exc:
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息

def hexstr_to_bytes(hexstr):
    return bytes.fromhex(hexstr)

# 记下找到设备的雷达波特率
def find_lidar_baud():
    flag = False
    for x in range(5):
        for y in range(1, 5):
            z = mod_lidar(Baudrate[x], y)
            if z == '正常':
                baudrate = Baudrate[x]
                flag = True
                break
        if flag:
            break

    return baudrate

# 记下找到设备的雷达id值
def find_lidar_id():
    flag = False
    for x in range(5):
        for y in range(1, 5):
            z = mod_lidar(Baudrate[x], y)
            if z == '正常':
                id = y
                flag = True
                break
        if flag:
            break

    return id

# 输入新的波特率
def set_newbaud():
    # 获取用户输入的波特率
    print("请输入您想要设置的波特率:9600、19200、38400、57600、115200")
    check_baudnum = int(input())

    while check_baudnum not in Baudrate:
        print("波特率输入不正确,请重新输入")
        check_baudnum = int(input())

    new_baudrate = check_baudnum

    return new_baudrate

# 输入新的id
def set_newid():
    # 获取用户输入的id
    print("请输入您想要设置的id:1-255")
    check_idnum = int(input())

    while check_idnum not in range(256):
        print("id输入不正确,请重新输入")
        check_idnum = int(input())

    new_id = check_idnum

    return new_id

# 设定串口为从站
def establish_serial(selected_port, BAUDRATE):
    master = modbus_rtu.RtuMaster(
        serial.Serial(port=selected_port,
                      baudrate=BAUDRATE,
                      bytesize=8,
                      parity='N',
                      stopbits=1))
    master.set_timeout(0.05)  # 50ms
    master.set_verbose(True)

    return master

def read_registers():
    # 读取距离指令
    distance_cmd = master.execute(slave=id, function_code=cst.READ_HOLDING_REGISTERS, starting_address=0,
                             quantity_of_x=2)
    print(distance_cmd)

def write_register():
    # 写入id修改指令
    id_cmd = master.execute(slave=id, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x85,
                             output_value=new_id)
    print(id_cmd)

def read_run_hexinput():
    while True:
            try:
                cmd_hex = input("Modbus 指令输入(hex): ")
                cmd_bytes = hexstr_to_bytes(cmd_hex)
                response = send_modbus_cmd(cmd_bytes)
                if len(input_hex) == 0:
                    continue
                else:
                    break
            except ValueError:
                print("输入不正确，请重新输入")

if __name__ == "__main__":
    selected_port = choose_serial_port()
    baudrate = find_lidar_baud()
    id = find_lidar_id()
    master = establish_serial(selected_port, baudrate)
    new_baudrate = set_newbaud()
    new_id = set_newid()
    write_register()