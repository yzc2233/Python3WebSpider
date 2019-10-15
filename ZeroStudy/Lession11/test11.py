# import sqlite3
# #连接到SQLite数据库
# #数据库文件是mrsoft.db，如果文件不存在，会自动在当前目录创建
# conn = sqlite3.connect('mrsoft.db')
# #创建一个Cursor
# cursor = conn.cursor()
# create_table_user_sql = 'create table user(id int(10) primary  key,name varchar(20))'
# #执行一条sql语句，创建user表
# try:
#     cursor.execute(create_table_user_sql)
# except sqlite3.OperationalError:
#     print('user表已存在')
# else:
#     print('user表创建成功')
# #关闭游标
# cursor.close()
# #关闭Connection
# conn.close()
#

#
# import sqlite3
# conn = sqlite3.connect('mrsoft.db')
# cursor = conn.cursor()
# try:
#     cursor.execute('insert into user(id,name) values ("1","MRSOFT")')
#     cursor.execute('insert into user(id,name) values ("2","Andy")')
#     cursor.execute('insert into user(id,name) values ("3","明日科技小助手")')
#     cursor.close()
#     conn.commit()
# except Exception as e:
#     print('新增数据错误:',e)
#     conn.rollback()
# finally:
#     conn.close()
# #
# import sqlite3
# conn = sqlite3.connect('mrsoft.db')
# cursor = conn.cursor()
# #使用问号作为占位符代替具体的数值，然后用一个元祖来替换问号（不要忽略元祖中最后的逗号）
# #使用占位符可以避免SQL注入的风险
# cursor.execute('select * from user where id > ?',(1,))
# data_first = cursor.fetchone()
# data_many = cursor.fetchmany(2)
# data_all = cursor.fetchall()
# print(data_first)
# print(data_many)
# print(data_all)
# cursor.close()
# conn.close()

# import sqlite3
# conn = sqlite3.connect('mrsoft.db')
# cursor = conn.cursor()
# cursor.execute('update user set name= ? where id = ?',('MR','1'))
# cursor.execute('select * from user ')
# data = cursor.fetchall()
# print(data)
# cursor.close()
# conn.commit()
# conn.close()
#
# import pymysql
# db = pymysql.connect('localhost','root','888888','mrsoft')
# cursor = db.cursor()
# # cursor.execute('select version()')
# # data = cursor.fetchall()
# # print(data)
# sql = """create table if not exists book(
#     id int(8) not null AUTO_INCREMENT,
#     name varchar(50) not null,
#     category varchar(50) not null,
#     price decimal(10,2) default null,
#     publish_time date default null,
#     PRIMARY KEY (id)
#     )ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
# """
# cursor.execute(sql)
# cursor.close()
# db.close()

#
# import pymysql
# conn = pymysql.connect('localhost','root','888888','mrsoft',charset='utf8')
# cur = conn.cursor()
# data = [('零基础学Python','Python','79.80','2018-5-20'),
#         ('Python从入门到精通','Python','69.80','2018-6-18'),
#         ('零基础学PHP','PHP','69.80','2017-5-21'),
#         ('PHP项目开发实战入门','PHP','79.80','2016-5-21'),
#         ('零基础学Java','Java','69.80','2017-5-21')]
# try:
#     cur.executemany('insert into book(name,category,price,publish_time) values (%s,%s,%s,%s)',data)
#     conn.commit()
# except Exception as e:
#     print('插入数据失败：',e)
#     conn.rollback()
# else:
#     cur.execute('select * from book')
#     data = cur.fetchall()
#     print(data)
# finally:
#     cur.close()
#     conn.close()







