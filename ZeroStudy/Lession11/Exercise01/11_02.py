import pymysql

conn = pymysql.connect('localhost','root','888888','mrsoft')
cur = conn.cursor()
cur.execute("select `name`,price from book where price < %s and publish_time >= %s" %(70,'2017-01-01'))
data = cur.fetchall()
for book in data:
    print('图书：《%s》，价格：￥%s元' %(book[0],book[1]))
cur.close()
conn.close()

