# -*- coding: utf_8 -*-

# 2023-05-06 添加自动扫描COM口并进行串口选择、显示修改ID、波特率的程序

import serial.tools.list_ports
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import time  # 添加定时器
from time import *
import numpy as np

from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

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
                    print(f"已选择串口: {selected_port}")
                    return selected_port
                else:
                    print("输入不正确，请重新输入")
            except ValueError:
                print("输入不正确，请重新输入")


def modbaudid(BAUDRATE, SlaveID):
    red = []
    alarm = ""
    try:
        # 设定串口为从站
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=selected_port,
                          baudrate=BAUDRATE,
                          bytesize=8,
                          parity='N',
                          stopbits=1))
        master.set_timeout(0.05)  # 50ms
        master.set_verbose(True)

        # 读保持寄存器
        red = master.execute(slave=SlaveID, function_code=cst.READ_HOLDING_REGISTERS, starting_address=0,
                             quantity_of_x=2)  # 这里可以修改需要读取的功能码
        
        print(red)
        alarm = "正常"
        
        return alarm

    except Exception as exc:
        # print(str(exc))
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息


def modifybaudid(BAUDRATE, SlaveID, New_SlaveID):
    red = []
    alarm = ""
    try:
        # 设定串口为从站
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=selected_port,
                          baudrate=BAUDRATE,
                          bytesize=8,
                          parity='N',
                          stopbits=1))
        master.set_timeout(0.05)  # 50ms
        master.set_verbose(True)

        # 写保持寄存器
        red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x85,
                             output_value=New_SlaveID)  # 这里可以修改需要读取的功能码
        red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x80,
                             output_value=0)  # 这里可以修改需要读取的功能码

        # 读保持寄存器
        red = master.execute(slave=New_SlaveID, function_code=cst.READ_HOLDING_REGISTERS, starting_address=0,
                             quantity_of_x=2)  # 这里可以修改需要读取的功能码
        print(red)
        alarm = "正常"

        return alarm

    except Exception as exc:
        # print(str(exc))
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息


# 新建函数，进行设备波特率和 ID 的修改
def modify_modbaudid(BAUDRATE, SlaveID):
    new_baudrate = BAUDRATE
    new_id = SlaveID
    print("是否要修改波特率和ID? 1.是,修改波特率 2.是,修改id 3.是,修改波特率和id 4.否,输出空行")
    while True:
        try:
            chose = int(input("请输入要选择的操作: "))
            if chose == 1:
                # 获取用户输入的波特率
                print("请输入您想要设置的波特率：")
                new_baudrate = int(input())

            elif chose == 2:
                # 获取用户输入的ID
                print("请输入您想要设置的id:")
                new_id = int(input())

            elif chose == 3:
                # 获取用户输入的波特率和ID
                print("请输入您想要设置的波特率和ID:")
                new_baudrate = int(input())
                new_id = int(input())

            elif chose == 4:
                print(" ")

            else:
                print("输入不正确，请重新输入")

        except ValueError:
            print("输入不正确，请重新输入")         

        return new_baudrate, new_id


if __name__ == "__main__":
    selected_port = choose_serial_port()

    print("开始扫描当前雷达站号和波特率,全部扫描结束时间为90S左右")
    print("雷达站号范围:1-10,波特率:9600、19200、38400、57600、115200")
    print("----------------------------------------")
    
    begin_time = time()
    for x in range(5):
        for y in range(1, 5):     
            z = modbaudid(Baudrate[x], y)
            if z == '正常':
                print("当前波特率：", Baudrate[x], "当前站号：", y)
                id = y
                baudr = Baudrate[x]
                
    end_time = time()
    run_time = end_time - begin_time
    print("查询运行时间：", run_time)

    i = 1
    while i == 1:
        # 调用修改波特率和ID的函数，获取新的波特率和ID
        new_baudrate, new_id = modify_modbaudid(baudr, id)
        if new_baudrate != baudr:
            # 如果获取到了新的波特率，则修改设备的波特率
            z = modifybaudid(new_baudrate, id, new_id)
            if z == '正常':
                print("修改后的波特率：", new_baudrate)
            i = 0

        elif new_id != id:
            # 如果获取到了新的ID，则修改设备的ID
            z = modifybaudid(baudr, id, new_id)
            print("id已修改为:", new_id, "，请重启设备")
            i = 0

        elif new_baudrate != baudr and new_id != id:
            # 如果获取到了新的波特率和ID，则修改设备的波特率和ID
            z = modifybaudid(new_baudrate, id, new_id)
            if z == '正常':
                print("修改后的波特率和id:", new_baudrate, new_id)
            i = 0

        elif new_baudrate == baudr and new_id == id:
            print("未修改波特率和ID")
            i = 0

        else:
            print("出现异常")
            i = 0
             