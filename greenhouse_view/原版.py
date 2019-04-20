"""最开始的原版"""
import serial
import time
import pymysql
import re


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


def serial_00(port, ba, cmd, user_select):
    if cmd == '':
        cmd = '01 03 00 00 00 09 85 cc'

    if user_select == 2:
        conn = link_mysql()  # 连接数据库
        if conn:
            print(">>>   数据库连接成功!")
        else:
            print(">>>   数据库连接失败!")
            return

    cur = conn.cursor()
	# if exist table node ,delete table node and create new table node
    cur.execute('drop table if exists node')
    create_table = """create table node(id int primary key, d1 int, d2 int, d3 int, d4 int, d5 int, d6 int, d7 int)"""
    cur.execute(create_table)
  
    try:
        port = str(port.upper())
        ba = int(ba)
        ser_00 = serial.Serial(port=port, baudrate=ba, timeout=0)  # 打开端口

        ser_00.bytesize = serial.EIGHTBITS  # 8bit
        ser_00.stopbits = 1  # stopbits
        ser_00.parity = serial.PARITY_NONE  # 无校验

        print('>>>   设备打开成功!', '设备端口:', ser_00.port)  # 设备名称，端口号
        print("\n")

        id = 0  # 数据标记，第几组数据

        # TODO:可不可以只发送一次指令-no
        # hex_str = bytes.fromhex(cmd)
        # ser_00.write(hex_str)
        # hex_str = bytes.fromhex(cmd)  # 发送的指令，16进制 '01 03 00 00 00 09 85 cc'
        # ser_00.write(hex_str)

        while True:    
            hex_str = bytes.fromhex(cmd)
            ser_00.write(hex_str)
            
            res = ser_00.readall()  # 读取数据

            temp = res.hex()  # 源数据---把读取的数据转换为16进制

            # if temp == None or temp == '' or temp == '0'*46:
            # 	temp = '0'*46
            if temp == '':
            	temp = '0'*46

            """
            d1:   湿度
            d2:   温度
            d3_1: 土壤湿度一
            d3_2: 土壤湿度二
            d4:   PM2.5
            d5:   CO2浓度
            d6_1: 气体浓度一
            d6_2: 气体浓度二
            d7:   光照强度
            """

            d1 = temp[6:10]  # d1      6-9左闭右开
            # if d1 == '':
            #     d1 = '0'
            d1 = int(d1, 16)

            d2 = temp[10:14]  # d2
            # if d2 == '':
            #     d2 = '0'
            d2 = int(d2, 16)

            d3_1 = temp[14:18]  # d3_1
            # if d3_1 == '':
            #     d3_1 = '0'
            d3_1 = int(d3_1, 16)

            d3_2 = temp[18:22]  # d3_2

            d4 = temp[22:26]  # d4
            # if d4 == '':
            #     d4 = '0'
            d4 = int(d4, 16)

            d5 = temp[26:30]  # d5
            # if d5 == '':
            #     d5 = '0'
            d5 = int(d5, 16)

            d6_1 = temp[30:34]  # d6
            # if d6_1 == '':
            #     d6_1 = '0'
            d6_1 = int(d6_1, 16)

            d6_2 = temp[34:38]  # d6_2

            d7 = temp[38:42]  # d7
            # if d7 == '':
            #     d7 = '0'
            d7 = int(d7, 16)

            if user_select == 2:
                sql_word = 'insert into node values(%d, %d, %d, %d, %d, %d, %d, %d)' % (id, d1, d2, d3_1, d4, d5, d6_1, d7)
                add_data = cur.execute(sql_word)
                conn.commit()

            print(">>>   源数据是:", temp)
            print(">>>   第%d组数据-----湿度:%d   温度:%d   土壤湿度:%d   PM2.5:%d   CO2浓度:%d   气体浓度:%d   光照强度:%d"
                % (id, d1, d2, d3_1, d4, d5, d6_1, d7))

            print('\n')
            id += 1

            time.sleep(1.5)  # 延时1秒,在实际运行的时候取消延时,延时只为了调试方便

    except Exception as res:
        print('>>>   程序出错了:', res)


def link_mysql():  # d1, d2, d3_1, d4, d5, d6_1, d7

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
        if sql_password == '':
            continue
        else:
            break

    print(sql_ip, sql_port, sql_user, sql_password, sql_database)

    try:
        conn = pymysql.connect(host=sql_ip, port=int(sql_port), database=sql_database, user=sql_user, password=sql_password)
        return conn
        # sql_word = 'insert into node_data values(%d, %d, %d, %d, %d, %d, %d)' % (d1, d2, d3_1, d4, d5, d6_1, d7)
        # add_data = cur.execute(sql_word)
        # conn.commit()
    except:
        return False


def my_console(opt):

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

    serial_00(com, bot, cmd, user_select)


if __name__ == '__main__':

    opt = show()  # opt=1/2 1:仅调试 2:连接数据库
    my_console(opt)




