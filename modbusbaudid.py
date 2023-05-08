# -*- coding: utf_8 -*-

# 2021-08-11 添加自动扫描COM口的程序 @1

import serial.tools.list_ports    #@1 获取COM口列表库

import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import time           #添加定时器
from time import *
import numpy as np

Baudrate = [9600,115200,19200,38400,57600]



# @1 start 获取现有COM口程序
ports = serial.tools.list_ports.comports()
for p in ports:
    print(p.device)
print(len(ports), 'ports found')

#time.sleep(1) #延时1s（可以不延时，方便看输出）
# @1 end


def mod(BAUDRATE,SlaveID):
    red = []
    alarm = ""
    try:
        # 设定串口为从站
        master = modbus_rtu.RtuMaster(serial.Serial(port='COM4',
                                                    baudrate=BAUDRATE, bytesize=8, parity='N', stopbits=1))
        master.set_timeout(0.05)  #50ms
        master.set_verbose(True)

        # 读保持寄存器
        red = master.execute(SlaveID, cst.READ_HOLDING_REGISTERS, 0, 2)  # 这里可以修改需要读取的功能码
        print(red)
        alarm = "正常"
       # return list(red), alarm
        return alarm

    except Exception as exc:
        #print(str(exc))
        alarm = (str(exc))
        

    return red, alarm  ##如果异常就返回[],故障信息


if __name__ == "__main__":

    print("开始扫描当前雷达站号和波特率，全部扫描结束时间为90S左右")
    print("雷达站号范围：1-100，波特率：9600、19200、38400、57600、115200")
    print("----------------------------------------")
    begin_time = time()
    for x in range(5):
        for y in range(1,2):
            z = mod(Baudrate[x],y)
            print(z)
            if z == '正常':
                print("当前波特率：",Baudrate[x],"当前站号：",y)
    end_time = time()
    run_time = end_time - begin_time
    print("查询运行时间：",run_time)

             
