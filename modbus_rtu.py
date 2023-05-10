import sys
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

# 创建Modbus RTU客户端
client = ModbusSerialClient(method='rtu', port='COM4', baudrate=11500, timeout=2)

# 连接Modbus RTU设备
if not client.connect():
    print('连接Modbus设备失败')
    sys.exit(1)

# 读取Modbus寄存器
result = client.read_holding_registers(address=1, count=2, unit=1)

# 判断读取是否成功
if result.isError():
    print('读取Modbus寄存器失败')
    sys.exit(1)

# 将Modbus响应数据解码
decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
print(decoder)
# 获取解码后的数据
value1 = decoder.decode_16bit_uint()
value2 = decoder.decode_16bit_uint()
print(value1,value2)
# 根据读取的值进行条件判断
if value1 > 100 and value2 < 50:
    print('条件满足')
else:
    print('条件不满足')

# 关闭Modbus RTU客户端连接
client.close()