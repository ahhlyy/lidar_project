# -*- coding: utf_8 -*-

# 2023-05-06 添加自动扫描COM口并进行串口选择、显示修改ID、波特率的程序

import serial.tools.list_ports
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import time  # 添加定时器
from time import *
import numpy as np
import sys
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

Baudrate = [9600, 115200, 19200, 38400, 57600]


# 找出所有串口
def find_serial_ports():
    """
    自动识别可用的串口号
    """
    ports = list(serial.tools.list_ports.comports())
    result = []
    for port in ports:
        result.append(port.device)
    return result


# 选择串口
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


# 波特率高字节配置
def modifybaud_h(BAUDRATE, SlaveID, New_BAUDRATE):
    red = []
    alarm = ""
    master = establish_serial(selected_port, BAUDRATE)
    try:
        # 将十进制转换为十六进制，并用0填充成8位
        New_BAUDRATE_hex = hex(int(New_BAUDRATE))[2:].zfill(8)
        # 将十六进制字符串转换为两个字节的波特率高位和波特率低位
        New_BAUDRATE_H = hex(int(New_BAUDRATE_hex[:4], 16))
        NH = int(New_BAUDRATE_H, 16)

        # 写保持寄存器
        red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x83,
                             output_value=NH)  # 修改波特率高字节指令
        alarm = "正常"

        return alarm

    except Exception as exc:
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息


# 波特率低字节配置
def modifybaud_l(BAUDRATE, SlaveID, New_BAUDRATE):
    red = []
    alarm = ""
    master = establish_serial(selected_port, BAUDRATE)
    try:
        # 将十进制转换为十六进制，并用0填充成8位
        New_BAUDRATE_hex = hex(int(New_BAUDRATE))[2:].zfill(8)
        # 将十六进制字符串转换为两个字节的波特率高位和波特率低位
        New_BAUDRATE_L = hex(int(New_BAUDRATE_hex[4:], 16))
        NL = int(New_BAUDRATE_L, 16)

        # 写保持寄存器
        red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x84,
                             output_value=NL)  # 修改波特率低字节指令
        alarm = "正常"

        return alarm

    except Exception as exc:
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息


# id配置
def modifyid(BAUDRATE, SlaveID, New_SlaveID):
    red = []
    alarm = ""
    master = establish_serial(selected_port, BAUDRATE)    
    try:
        # 写保持寄存器
        red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x85,
                             output_value=New_SlaveID)  # 修改id指令
        alarm = "正常"

        return alarm

    except Exception as exc:
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息


# 保存配置
def savelidar(BAUDRATE, SlaveID):
    red = []
    alarm = ""
    master = establish_serial(selected_port, BAUDRATE)
    try:
        # 写保持寄存器
        red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x80,
                             output_value=0)  # 重启设备指令
        alarm = "正常"

        return alarm

    except Exception as exc:
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息


# 重启配置
def resetlidar(BAUDRATE, SlaveID):
    red = []
    alarm = ""
    master = establish_serial(selected_port, BAUDRATE)
    try:
        # 写保持寄存器
        red = master.execute(slave=SlaveID, function_code=cst.WRITE_SINGLE_REGISTER, starting_address=0x81,
                             output_value=1)  # 重启设备指令
        alarm = "正常"

        return alarm

    except Exception as exc:
        alarm = (str(exc))

    return red, alarm  # 如果异常就返回[],故障信息


# 主菜单页面
def main_menu():
    print("主菜单功能选择:")
    print("1.设备查找")
    print("2.设备测距")
    print("3.雷达配置")
    print("4.退出程序")
    print("----------------------------------------------------------")


# 设备测距子菜单页面1
def lidarmeasure_sub1_menu():
    print("示例,用空格分隔：")
    print("115200 1")
    print("----------------------------------------------------------")


# 设备测距子菜单页面2
def lidarmeasure_sub2_menu():
    print("测距子菜单功能选择:")
    print('{:>10}'.format('1.雷达测距'))
    print('{:>11}'.format('2.修改波特率'))
    print('{:>12}'.format('3.修改雷达id'))
    print('{:>11}'.format('4.返回主菜单'))
    print("----------------------------------------------------------")


# 雷达配置子菜单页面
def lidarsetting_sub_menu():
    print("配置子菜单功能选择:")
    print('{:>11}'.format('1.修改波特率'))
    print('{:>12}'.format('2.修改雷达id'))
    print('{:>11}'.format('3.返回主菜单'))
    print("----------------------------------------------------------")


# 主菜单驱动
def run_mainmenu():
    while True:
        main_menu()
        choice = int(input("请输入您的选择："))
        print("----------------------------------------------------------")

        if choice == 1:
            find_lidar()
        elif choice == 2:
            lidarmeasure_sub1_menu()
            run_measure_sub1menu()
        elif choice == 3:
            lidarsetting_sub_menu()
            run_set_submenu()
        elif choice == 4:
            break
        else:
            print("无效的选择，请重新输入。")   


# 测距驱动用户输入波特率
def run_measure_inputbaud():
    print("请先输入雷达波特率:")
    check_baudnum = int(input("波特率:"))
    while check_baudnum not in Baudrate:
        print("波特率输入格式不正确,请重新输入")
        print("----------------------------------------------------------")

    inputbaud = check_baudnum

    return inputbaud


# 测距驱动用户输入id
def run_measure_inputid():
    print("请先输入雷达id:")
    check_idnum = int(input("id:"))
    while check_idnum not in range(256):
        print("id输入格式不正确,请重新输入")
        print("----------------------------------------------------------")

    inputbaud = check_idnum

    return inputbaud


# 测距驱动用户输入波特率和id
def run_measure_inputbaudid():
    while True:
        print("请先输入雷达波特率和id:")
        input_str = input()
        input_list = input_str.split()
        if len(input_list) == 2 and input_list[0].isdigit() and input_list[1].isdigit():
            inputbaud = int(input_list[0])
            inputid = int(input_list[1])
            print("----------------------------------------------------------")
            break
        
        print("输入格式不正确，请重新输入")
        print("----------------------------------------------------------")

    return inputbaud, inputid


# 测距驱动1
def run_measure_sub1menu():
    while True:
        read = []
        info_baudid = run_measure_inputbaudid()
        inputbaud = info_baudid[0]
        inputid = info_baudid[1]
        master = establish_serial(selected_port, inputbaud)
        master.open()
        try:
            read = master.execute(slave=inputid, function_code=cst.READ_HOLDING_REGISTERS, starting_address=0,
                                  quantity_of_x=2)
        
        except modbus_rtu.ModbusInvalidResponseError as e:
            print("ModbusError: {}".format(e))
        
        master.close()

        if len(read) == 0:
            print("连接雷达设备失败,请重新检查波特率和id")
            print("----------------------------------------------------------")

        else:           
            print("连接雷达设备成功")
            print("当前雷达的测距结果为:", read)
            print("当前波特率：", inputbaud, "当前站号：", inputid)
            print("----------------------------------------------------------")
            correct_baud = inputbaud
            correct_id = inputid
            lidarmeasure_sub2_menu()
            #run_measure_sub2menu()
            while True:
                choice = int(input("测距子菜单下请输入您的选择："))
                print("----------------------------------------------------------")

                if choice == 1:
                    find_lidar()
                    lidarmeasure_sub2_menu()
                elif choice == 2:
                    #info_baudid = run_measure_inputbaudid()
                    #info_baudid = run_measure_sub1menu()
                    print("提示：当前的雷达的波特率为", info_baudid[0])
                    baudrate = info_baudid[0]
                    id = info_baudid[1]
                    new_baudrate = set_newbaud()
                    # 修改设备的波特率
                    modifybaud_h(baudrate, id, new_baudrate)
                    modifybaud_l(baudrate, id, new_baudrate)
                    savelidar(baudrate, id)
                    resetlidar(baudrate, id)
                    print("成功,波特率修改为:", new_baudrate)
                    print("----------------------------------------------------------")
                    #lidarmeasure_sub2_menu()
                    break
                    
                elif choice == 3:
                    #info_baudid = run_measure_inputbaudid()
                    print("提示：当前的雷达的站号为", info_baudid[1])
                    baudrate = info_baudid[0]
                    id = info_baudid[1]
                    new_id = set_newid()
                    # 修改设备的ID
                    modifyid(baudrate, id, new_id)
                    savelidar(baudrate, id)
                    resetlidar(baudrate, id)
                    print("成功,id修改为:", new_id)
                    print("----------------------------------------------------------")
                    #lidarmeasure_sub2_menu()
                    break
                    
                elif choice == 4:
                    break
                else:
                    print("无效的选择，请重新输入。")            
            break
    return correct_baud, correct_id




# 测距驱动2
def run_measure_sub2menu():
    while True:
        choice = int(input("测距子菜单下请输入您的选择："))
        print("----------------------------------------------------------")

        if choice == 1:
            measure_lidar()
            lidarmeasure_sub2_menu()
        elif choice == 2:
            #info_baudid = run_measure_inputbaudid()
            info_baudid = run_measure_sub1menu()
            print("提示：当前的雷达的波特率为", info_baudid[0], ",站号为", info_baudid[1])
            baudrate = info_baudid[0]
            id = info_baudid[1]
            new_baudrate = set_newbaud()
            # 修改设备的波特率
            modifybaud_h(baudrate, id, new_baudrate)
            modifybaud_l(baudrate, id, new_baudrate)
            savelidar(baudrate, id)
            resetlidar(baudrate, id)
            print("成功,波特率修改为:", new_baudrate)
            print("----------------------------------------------------------")
            lidarmeasure_sub2_menu()
        elif choice == 3:
            info_baudid = run_measure_sub1menu()
            baudrate = info_baudid[0]
            id = info_baudid[1]
            new_id = set_newid()
            # 修改设备的ID
            modifyid(baudrate, id, new_id)
            savelidar(baudrate, id)
            resetlidar(baudrate, id)
            print("成功,id修改为:", new_id)
            print("----------------------------------------------------------")
            lidarmeasure_sub2_menu()
        elif choice == 4:
            break
        else:
            print("无效的选择，请重新输入。")


# 配置驱动
def run_set_submenu():
    while True:
        choice = int(input("配置子菜单下请输入您的选择："))
        print("----------------------------------------------------------")
        
        if choice == 1:
            baudrate, id = find_lidar_baudid()
            new_baudrate = set_newbaud()
            # 修改设备的波特率
            modifybaud_h(baudrate, id, new_baudrate)
            modifybaud_l(baudrate, id, new_baudrate)
            savelidar(baudrate, id)
            resetlidar(baudrate, id)
            print("成功,波特率修改为:", new_baudrate)
            print("----------------------------------------------------------")
            lidarsetting_sub_menu()
        elif choice == 2:
            baudrate, id = find_lidar_baudid()
            new_id = set_newid()
            # 修改设备的ID
            modifyid(baudrate, id, new_id)
            savelidar(baudrate, id)
            resetlidar(baudrate, id)
            print("成功,id修改为:", new_id)
            print("----------------------------------------------------------")
            lidarsetting_sub_menu()
        elif choice == 3:
            break
        else:
            print("无效的选择，请重新输入。")

    return choice


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


# 记下找到设备的雷达波特率和id值
def find_lidar_baudid():
    flag = False
    for x in range(5):
        for y in range(1, 5):
            z = mod_lidar(Baudrate[x], y)
            if z == '正常':
                print("当前修改设备的波特率：", Baudrate[x], "当前站号：", y)
                baudrate = Baudrate[x]
                id = y
                flag = True
                break
        if flag:
            break

    return baudrate, id


# 查找雷达设备
def find_lidar():
    print("开始扫描当前雷达站号和波特率,全部扫描结束时间为90S左右")
    print("雷达站号范围:1-10,波特率:9600、19200、38400、57600、115200")
    print("----------------------------------------------------------")

    begin_time = time()
    flag = False
    for x in range(5):
        for y in range(1, 5):
            z = mod_lidar(Baudrate[x], y)
            if z == '正常':
                print("测距成功")
                print("当前波特率：", Baudrate[x], "当前站号：", y)
                baudrate = Baudrate[x]
                id = y
                flag = True
                break
        if flag:
            break

    end_time = time()
    run_time = end_time - begin_time
    print("查询运行时间：", run_time, "\n")

    return baudrate, id


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


def endfunction():
    print("操作完毕\n 1.对设备轮询测距\n 2.结束")
    while True:
        try:
            tag = int(input("请输入要选择的操作: "))
            if tag == 1:
                # 对设备轮询测距
                begin_time = time()
                print("对设备测距")
                for x in range(5):
                    for y in range(1, 5):
                        z = mod_lidar(Baudrate[x], y)
                        if z == '正常':
                            print("当前波特率：", Baudrate[x], "当前站号：", y)
                            baudrate1 = Baudrate[x]
                            id1 = y

                end_time = time()
                run_time = end_time - begin_time
                print("查询运行时间：", run_time, "\n")
                lidarfunc(baudrate1, id1)

                break

            elif tag == 2:
                # 结束
                print(" ")
                break

            else:
                print("输入不正确，请重新输入")

        except ValueError:
            print("输入不正确，请重新输入")


if __name__ == "__main__":
    selected_port = choose_serial_port()
    run_mainmenu()

    #find_lidar()
    #endfunction()
