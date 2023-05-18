# 北醒Modbus协议在Python下实现功能配置

## 实验目的
 实现485接口系列雷达Modbus协议在Python上实现功能配置。
 本例程界面分为主菜单、测距子菜单、配置子菜单，功能如下：

+ 主菜单:
	+ 设备查找（扫描已经忘记波特率或站号的Modbus雷达设备）
	+ 设备测距（已知雷达设备的波特率和站号，进行多次测距，并能够选择修改雷达波特率和id）
	+ 雷达配置（未知设备波特率和站号，修改雷达波特率、雷达id、恢复出厂设置）
	+ 退出程序

## 测试环境

Window 10、Python 3.10.2

## Python库需求
* serial 串口库（自带）
* time 定时库（自带）
* modbus_tk（1.1.3）（需要安装）

<mark>注：</mark>本例程因为是自动扫描COM口，建议在使用的时候关闭其它无关的COM口

## Benewake(北醒) TF雷达接口及通讯协议说明

### 接口定义
![303920710259870](https://github.com/ahhlyy/lidar_project/assets/76689985/24ff54c4-fb21-48d8-bc20-58e12b6aa11e)

<center> 图1 TFmini-i-485 引脚线序图 </center>
 <br/>
<center>表1 TFmini-i -485引脚功能及连接说明</center>

<table >
    <tr>
        <th bgcolor=#DCDCDC width=26%>编号</th>
        <th bgcolor=#DCDCDC width=27%>颜色</th>
        <th bgcolor=#DCDCDC width=27%>引脚</th>
        <th bgcolor=#DCDCDC width=27%>功能</th>
    </tr>
    <tr>
        <td align="center">1</td>
        <td align="center">红色</td>
        <td align="center">VCC</td>
        <td align="center">供电</td>
    </tr>
    <tr>
        <td align="center">2</td>
        <td align="center">白色</td>
        <td align="center">RS485-B</td>
        <td align="center">RS485-B总线</td>
    </tr>
    <tr>
        <td align="center">3</td>
        <td align="center">绿色</td>
        <td align="center">RS485-A</td>
        <td align="center">RS485-A总线</td>
    </tr>
    <tr>
        <td align="center">4</td>
        <td align="center">N/A</td>
        <td align="center">/</td>
        <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">5</td>
        <td align="center">蓝色</td>
        <td align="center">/</td>
        <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">6</td>
        <td align="center">棕色</td>
        <td align="center">/</td>
        <td align="center">/</td>
    </tr>
    <tr>
        <td align="center">7</td>
        <td align="center">黑色</td>
        <td align="center">GND</td>
        <td align="center">地线</td>
    </tr>
</table>

<mark>注：</mark>RS485 和 CAN 接口为不同硬件版本，请勿将串口调试线与 RS485 或 CAN 总线混接，否则会导致雷达 MCU 损坏。

### Modbus通信协议说明
RS485 接口下默认为 Modbus 协议，具体通讯协议见表 2。波特率默认为 115200，地址默认为 0x01。
<center>表2 TFmini-i-485 通讯协议</center>
<style>
table {
margin: auto;
}
</style>
<table >
    <tr>
        <th bgcolor=#DCDCDC width=26%>项目</th>
        <th bgcolor=#DCDCDC width=26%>内容</th>
    </tr>
    <tr>
        <td align="center">通讯协议</td>
        <td align="center">RS485</td>

   </tr>
    <tr>
        <td align="center">波特率</td>
        <td align="center">115200</td>

   </tr>
    <tr>
        <td align="center">数据位</td>
        <td align="center">8</td>

   </tr>
    <tr>
        <td align="center">停止位</td>
        <td align="center">1</td>

   </tr>
    <tr>
        <td align="center">校验位</td>
        <td align="center">无</td>

   </tr>
</table>



### 功能码说明

![101255610254976](https://github.com/ahhlyy/lidar_project/assets/76689985/be06363f-d6bb-4e71-8846-ebf8b1831a92)

## 接线示意图

![300345210257474](https://github.com/ahhlyy/lidar_project/assets/76689985/26ef3b0e-2ba8-4685-a5ea-181890ee1319)
<mark>注：</mark>线路颜色仅供参考，具体参照实际线路颜色定义

## 库安装说明
确保已经完整安装Python(并安装PIP)
打开CMD窗口分别输入以下指令
```pyhton
pip install modbus_tk==1.1.3
```
<mark>注：</mark>为了防止程序运行错误，建议使用以上库版本

## 例程
已生成EXE文件，按上面介绍的接线方式接好后直接双击即可打开测试
![435604609248979](https://github.com/ahhlyy/lidar_project/assets/76689985/bad34922-0458-475a-83bf-4e9d5c4cd51f)

BW_TFMD_V1.0_20230511.exe文件链接：[https://github.com/ahhlyy/lidar_project/tree/main/dist](https://github.com/ahhlyy/lidar_project/tree/main/dist)

例程BW_TFMD_V1.0_20230511.py文件链接: [https://github.com/ahhlyy/lidar_project](https://github.com/ahhlyy/lidar_project)

## 运行与测试
双击EXE文件后例程运行：
* 设备查找功能演示

![551183111258657](https://github.com/ahhlyy/lidar_project/assets/76689985/e1ccd238-480b-430d-a420-30f8ae64e660)

<a id=1> </a>
* 已知雷达波特率和id，进行设备测距（波特率默认为 115200，地址默认为 0x01）

注：测距结束后，提供波特率和id的修改选项，可根据需要进行修改

![351984411253793](https://github.com/ahhlyy/lidar_project/assets/76689985/0620bdc4-216b-419d-9a52-b23c5c9f3975)

* 对雷达设备进行配置，如修改波特率、修改id、恢复出厂设置

注：当未知波特率和id时，对设备进行扫描，等待扫描完毕后（约200s），进行配置修改，若已知波特率和id，选择功能[2.设备测距](#1)进行配置修改则无需等待扫描设备时间
  
  * 修改波特率
  
![203593713247339](https://github.com/ahhlyy/lidar_project/assets/76689985/e549c7bb-30cb-4fa1-bb4d-d0b9947d6c44)

  * 修改id
  
![285854413240473](https://github.com/ahhlyy/lidar_project/assets/76689985/7795bf25-e773-4193-bcb2-d9cc6fd79f33)

  * 恢复出厂设置
  
![175455113231003](https://github.com/ahhlyy/lidar_project/assets/76689985/c4e2b25c-e678-4223-a8e3-f1c6f445146a)
  
