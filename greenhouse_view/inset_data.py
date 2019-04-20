"""
这是测试用的代码，用来填充数据库nodedata的数据的
"""
import pymysql
import time
from decimal import Decimal

try:
    conn = pymysql.connect(host='localhost', port=3306, database='bsd', user='zgy', password='97zgy')
    cur = conn.cursor()
    cur.execute('delete from nodedata where 1=1')
    a = 1
    for i in range(1, 1000):
        i = i/3
        i = Decimal(i).quantize(Decimal('0.00'))
        i = str(i)
        sql_word = "insert into nodedata values(%d, %s, %s, %s, %s, %s, %s, %s,'com2')" % (a, i, i, i, i, i, i, i)
        try:
            cur.execute(sql_word)
            print('---before commit---', i)
            a += 1
            conn.commit()
            print('---affter commit---', i)
            print('\n')
        except Exception as err:
            print('出错', err)
            cur.rollback()
        time.sleep(1)
except Exception as s:
    print(s)
