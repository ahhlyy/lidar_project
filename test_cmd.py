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
def mod_distance(BAUDRATE, SlaveID):
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

# 记下找到设备的雷达波特率
def find_lidar_baud():
    flag = False
    for x in range(5):
        for y in range(1, 5):
            z = mod_distance(Baudrate[x], y)
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
            z = mod_distance(Baudrate[x], y)
            if z == '正常':
                id = y
                flag = True
                break
        if flag:
            break

    return id

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

# 将十六进制字符串转换为字节串
def hexstr_to_bytes(hexstr):
    return bytes.fromhex(hexstr)

# 发送Modbus指令并接收响应
def send_modbus_cmd(cmd):
    baudrate = find_lidar_baud()
    master = establish_serial(selected_port, baudrate)
    master.flushInput()
    master.executeflushOutput()
    master.write(cmd)
    time.sleep(0.1)
    response = master.read_all()
    return response


# 读取Modbus寄存器
def read_register(addr, reg_num):
    id = find_lidar_id()
    # modbus设备的地址为2位十六进制数，寄存器的编号4位十六进制数
    cmd = hexstr_to_bytes(f'01 03 {addr:02X} {reg_num:04X} 0002')
    response = send_modbus_cmd(cmd)
    if len(response) < 5:
        raise Exception('No response receiveIDd')
    if response[1] != 0x03:
        raise Exception(f'Response error: {response.hex()}')
    data_len = response[2]
    if len(response) != data_len + 5:
        raise Exception(f'Response length error: {response.hex()}')
    reg_value = int.from_bytes(response[3:5], byteorder='big')
    return reg_value


# 写入Modbus寄存器
def write_register(addr, reg_num, value):
    # modbus设备的地址为2位十六进制数，寄存器的编号4位，对寄存器读写操作的值4位
    cmd = hexstr_to_bytes(f'01 06 {addr:04X} {reg_num:04X} {value:04X}')
    response = send_modbus_cmd(cmd)
    if len(response) < 5:
        raise Exception('No response received')
    if response[1] != 0x06:
        raise Exception(f'Response error: {response.hex()}')
    reg_addr = int.from_bytes(response[2:4], byteorder='big')
    reg_value = int.from_bytes(response[4:6], byteorder='big')
    return (reg_addr, reg_value)

# 读取输入的十六进制指令并执行
def read_run_hexinput():
    while True:
        cmd_hex = input('Modbus 指令输入(hex): ')
        try:
            cmd_bytes = hexstr_to_bytes(cmd_hex)
            response = send_modbus_cmd(cmd_bytes)
            print('响应为:', response.hex())
        except Exception as e:
            print('Error:', str(e))
 '''
 
 
 '''           
def read_modbus():
        baudrate = find_lidar_baud()
        id = find_lidar_id()
        master = establish_serial(selected_port, baudrate)
        red = master.execute(slave=id, function_code=cst.READ_HOLDING_REGISTERS, starting_address=0,
                             quantity_of_x=2)  # 这里可以修改需要读取的功能码
        print(red)

# 读取寄存器
def read_register1(slave_id, address, length):
    baudrate = find_lidar_baud()
    master = establish_serial(selected_port, baudrate)
    data = master.execute(slave_id, cst.READ_HOLDING_REGISTERS, address, length)
    return data

# 写入寄存器
def write_register1(slave_id, address, value):
    baudrate = find_lidar_baud()
    master = establish_serial(selected_port, baudrate)
    master.execute(slave_id, cst.WRITE_SINGLE_REGISTER, address, output_value=value)

# 循环读取和写入寄存器
def run()
    while True:
        # 从终端输入十六进制指令
        cmd = input("请输入指令（例如：030100000001CRC）：")
        cmd_bytes = unhexlify(cmd)

        # 解析指令中的从站地址、寄存器地址和数据
        slave_id = cmd_bytes[1]
        r_address = int.from_bytes(cmd_bytes[2:4], byteorder='big')
        if cmd.startswith('06'):
            value = int.from_bytes(cmd_bytes[4:6], byteorder='big')
            write_register(slave_id, r_address, value)
            print("写入成功")
        elif cmd.startswith('03'):
            length = int.from_bytes(cmd_bytes[4:6], byteorder='big')
            data = read_register(slave_id, r_address, length)
            print("读取成功：" + str(data))
        else:
            print("指令格式不正确")

if __name__ == "__main__":
    selected_port = choose_serial_port()
    read_run_hexinput()
    run()