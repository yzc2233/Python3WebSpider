
import time
import pymysql

mysqlUser = {'qa2':{'host':'10.157.26.92','user':'marketing','password':'123456'},
             'stage':{'host':'10.157.24.94','user':'sephora_app','password':'123456'},
             'ebf':{'host':'10.157.24.252','user':'sephora_app','password':'123456'}}
env = 'ebf'
mysqlhost = mysqlUser[env]['host']
mysqluser = mysqlUser[env]['user']
mysqlpassword = mysqlUser[env]['password']

#
# # print(timestamp)
#
# client_id_part1 = 'Android-Ag-PILIANGDAORUTAGSDevicetest1-'
#
# with open(r'E:\SoftWare\JetBrains\IntellijCode\PythonCode\createorder\deviceuserimport.csv') as f:
#     con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'user')
#     cur = con.cursor()
#
#     userids = f.readlines()
#     for uid in userids:
#         # print(str(uid).strip())
#         try:
#             timestamp = str(int(time.time()*1000))
#             uid = uid.strip()
#             print(uid)
#             # sql = "insert into `user_device_status` (`client_id`, `user_id`, `supplier`, `status`, `create_time`, `update_time`) \
#             # values('{0}','{1}','UM','1','2020-11-30 00:00:00','2020-11-30 00:00:00');".format(client_id_part1+timestamp,uid)
#             # cur.execute(sql)
#             # con.commit()
#         except:
#             print(uid,'插入数据失败。。。。。')
#             continue
#
#     cur.close()
#     con.close()

import requests
import json
con = pymysql.connect(user=mysqluser,host=mysqlhost,passwd=mysqlpassword,db='user',charset='utf8')
cur = con.cursor()
sql = "select  card_no,create_time,description,id,points,status,store_id,update_time from user.card_points_flow where card_no='8038254598' and status=1 order by update_time desc;"
cur.execute(sql)
data = cur.fetchall()
# print(len(data))
for i in data:
    createTime = str(i[1])
    updateTime = str(i[7])
    if createTime == 'None':
        createTime = updateTime
    url = 'http://10.157.40.40:10003/v1/crm/elasticsearch/buildCardPointsFlowIndexList'
    header = {'Content-Type':'application/json'}
    body = {"head":{"token":"string","userId":"string"},"queryBody":[{"card_no":i[0],\
       "createTime":createTime,"description":i[2],"id":i[3],"points":i[4],"status":i[5],"store_id":i[6],\
        "updateTime":updateTime}]}
    Response = requests.post(url=url,json=body,headers=header)
    Response = json.loads(Response.text)
    if Response['results']:
        print(body,'成功')
    else:
        print(body,'失败')
    # print(body)
cur.close()
con.close()


