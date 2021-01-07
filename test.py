
import time
import pymysql

mysqlUser = {'qa2':{'host':'10.157.26.92','user':'marketing','password':'123456'},'stage':{'host':'10.157.24.94','user':'sephora_app','password':'123456'}}
env = 'stage'
mysqlhost = mysqlUser[env]['host']
mysqluser = mysqlUser[env]['user']
mysqlpassword = mysqlUser[env]['password']


# print(timestamp)

# client_id_part1 = 'Android-Ag-PILIANGDAORUTAGSDevicetest1-'

# with open(r'F:\丝芙兰\压测\单服务压测2020-2021\Order\user_stage_1.csv','r+') as f:
#     con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'user')
#     cur = con.cursor()
#
#     userids = f.readlines()
#     for uidline in userids:
#         uid = uidline.split(',')[0]
#         # print(str(uid).strip())
#         try:
#             # timestamp = str(int(time.time()*1000))
#             uid = uid.strip()
#             print(uid)
#             sql = "SELECT order_id FROM order.orders WHERE user_id={uid} ORDER BY create_time LIMIT 1;".format(uid=uid)
#             # print(sql)
#             cur.execute(sql)
#             order_id = cur.fetchone()[0]
#             # print(order_id)
#         # con.commit()
#             data = "{old},{order_id}\n".format(old=uidline.strip(),order_id=order_id)
#             f.write(data)
#             # break
#         except:
#             print(uid,'查询order_id失败。。。。。')
#             continue
#
#     cur.close()
#     con.close()

