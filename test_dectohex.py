
#dec = int(input("输入波特率: "))
# 将十进制转换为十六进制，并用0填充成8位
new_baudrate = hex(int(input("输入波特率: ")))[2:].zfill(8)

# 将十六进制字符串转换为两个字节的波特率高位和波特率低位
new_baudrate_highbyte = hex(int(new_baudrate[:4], 16))
new_baudrate_lowbyte = hex(int(new_baudrate[4:], 16))

# 输出结果
#print("Decimal number:", dec)
print("Hexadecimal string:", new_baudrate)
print("High byte:", new_baudrate_highbyte)
print("Low byte:", new_baudrate_lowbyte)