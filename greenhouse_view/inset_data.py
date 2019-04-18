import pymysql
import time


try:
    conn = pymysql.connect(host='localhost', port=3306, database='bsd', user='zgy', password='97zgy')
    cur = conn.cursor()
    cur.execute('delete from nodedata where 1=1')
    for i in range(1, 1000):
        sql_word = "insert into nodedata values(%d, %d, %d, %d, %d, %d, %d, %d,'com2')" % (i, i, i, i, i, i, i, i)
        cur.execute(sql_word)
        conn.commit()
        time.sleep(1)
except Exception as s:
    print(s)
