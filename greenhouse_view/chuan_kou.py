"""
这是第一次成功的版本
最后查看时间2019-4-19-17:29

这是完善后的版本，暂时没有测试
2019-4-19-22:54

这是实验室准备测试的版本
2019-4-20-10:56
1.添加了str(d1)...
"""
import serial
import time
import pymysql
import re
from decimal import Decimal


def read_data(com, bot, cmd, user_select):
    opt = user_select
    # 选项是2就连接数据库
    if opt == 2:
        while True:
            sql_ip = input(">>>   请输入目标数据库IP地址(默认localhost):")
            if sql_ip == '' or sql_ip == 'localhost':
                sql_ip = 'localhost'
                break
            elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', sql_ip):
                break
            print(">>>   您输入的IP地址有误,请重新输入!")

        while True:
            sql_port = input(">>>   请输入目标数据库PORT(默认3306):")
            if sql_port == '':
                sql_port = 3306
                break
            if re.match(r'^\d{1,5}$', sql_port):
                break
            print(">>>   您输入的PORT有误,请重新输入！")

        sql_database = input(">>>   请输入目标数据库名称(默认bsd):")
        if sql_database == '':
            sql_database = 'bsd'

        sql_user = input(">>>   请输入数据库用户名(默认zgy):")
        if sql_user == '':
            sql_user = 'zgy'

        while True:
            sql_password = input(">>>   请输入数据库密码:")
            if sql_password != '':
                break

        print('>>>   IP地址--端口号--用户名--密码--数据库名', sql_ip, sql_port, sql_user, sql_password, sql_database)

        try:
            conn = pymysql.connect(host=sql_ip, port=int(sql_port), database=sql_database, user=sql_user, password=sql_password)
            cur = conn.cursor()
            cur.execute("""delete from nodedata where 1=1;""")           # 先删除传感器所有数据
        except Exception as res:
            print('>>>   数据库连接出错!', res)
            return
        print('>>>   数据库连接成功!')
        print('\n')

    # 打开串口
    try:
        com = str(com.upper())
        bot = int(bot)

        ser = serial.Serial(port=com, baudrate=bot, timeout=0)   # 打开端口
        ser.bytesize = serial.EIGHTBITS                          # 8bit
        ser.stopbits = 1                                         # 停止位
        ser.parity = serial.PARITY_NONE                          # 无校验
        ser_com = ser.port
        print('>>>   设备打开成功!', '设备端口:', ser_com)  # 设备名称，端口号
        print("\n")

        id = 1  # 数据标记，第几组数据

        while True:    
            hex_str = bytes.fromhex(cmd)
            ser.write(hex_str)
            res = ser.readall()                              # 读取数据
            temp = res.hex()                                    # 源数据---把读取的数据转换为16进制

            if temp == '':
                temp = '0'*46
            """d1:湿度   d2:温度  d3_1:土壤湿度  d4:PM2.5  d5:CO2浓度  d6_1:气体浓度  d7:光照强度"""

            d1 = temp[6:10]  # d1      6-9左闭右开
            d1 = int(d1, 16)

            d2 = temp[10:14]  # d2
            d2 = int(d2, 16)

            d3 = temp[14:18]  # d3
            d3 = int(d3, 16)

            d4 = temp[22:26]  # d4
            d4 = int(d4, 16)

            d5 = temp[26:30]  # d5
            d5 = int(d5, 16)

            d6 = temp[30:34]  # d6
            d6 = int(d6, 16)

            d7 = temp[38:42]  # d7
            d7 = int(d7, 16)

            d1 = d1/10
            d2 = d2/10
            d3 = d3/10
            d4 = d4/10
            d5 = d5/10
            d6 = d6/10
            d7 = d7/10

            d1 = Decimal(d1).quantize(Decimal('0.00'))
            d2 = Decimal(d2).quantize(Decimal('0.00'))
            d3 = Decimal(d3).quantize(Decimal('0.00'))
            d4 = Decimal(d4).quantize(Decimal('0.00'))
            d5 = Decimal(d5).quantize(Decimal('0.00'))
            d6 = Decimal(d6).quantize(Decimal('0.00'))
            d7 = Decimal(d7).quantize(Decimal('0.00'))

            d1 = str(d1)
            d2 = str(d2)
            d3 = str(d3)
            d4 = str(d4)
            d5 = str(d5)
            d6 = str(d6)
            d7 = str(d7)

            if opt == 2:
                sql_word = """insert into nodedata values(%d, %s, %s, %s, %s, %s, %s, %s, %s);""" % (id, d1, d2, d3, d4, d5, d6, d7, str(ser_com))
                cur.execute(sql_word)
                conn.commit()

            print(">>>   源数据是:", temp)
            print(">>>   第%d组数据---湿度:%d  温度:%d  土壤湿度:%d  PM2.5:%d  CO2浓度:%d  气体浓度:%d  光照强度:%d  COM端口:%s"
                % (id, d1, d2, d3, d4, d5, d6, d7, str(ser_com)))
            print('\n')
            id += 1
            time.sleep(1)  # 延时1秒,在实际运行的时候取消延时,延时只为了调试方便
    except Exception as res:
        print('>>>   程序出错了:', res)


def com_input(opt):
    user_select = opt
    while True:
        com = input(">>>   请输入COM端口号:")
        if re.match(r'^com\d+|COM\d+', com):
            break
        print(">>>   端口号输入错误,请重新输入!")

    while True:
        bot = input(">>>   请输入波特率:")
        if re.match(r'^\d+$', bot):
            break
        print(">>>   波特率输入错误,请重新输入!")

    cmd = input(">>>   请输入指令代码,默认='01 03 00 00 00 09 85 cc':")

    if cmd == '':
        cmd = '01 03 00 00 00 09 85 cc'
    read_data(com, bot, cmd, user_select)


def show():
    print(">>>   ------------------------------")
    print(">>>   ------------------------------")
    print(">>>   ------欢迎使用串口调试工具------")
    print(">>>   ------------------------------")
    print(">>>   ------------------------------")
    print(">>>   选项一:调试串口信息，不连接数据库")
    print(">>>   选项二:调试串口信息并且连接数据库")
    print(">>>   ------------------------------")

    while True:
        opt = input(">>>   请输入你的选项(1/2):")
        if opt == '1':
            print('>>>   您选择的是---单独调试串口信息，不连接数据库---')
            return 1
        elif opt == '2':
            print('>>>   您选择的是---调试串口信息，并且连接数据库---')
            return 2
        else:
            print('>>>   您输入的选项有误!请重新输入.')


if __name__ == '__main__':
    opt = show()  # return:int 1/2
    com_input(opt)





