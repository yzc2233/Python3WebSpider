
import time
import pymysql

mysqlUser = {'qa2':{'host':'10.157.26.92','user':'marketing','password':'123456'},
             'stage':{'host':'10.157.24.94','user':'sephora_app','password':'123456'},
             'ebf':{'host':'10.157.24.252','user':'sephora_app','password':'123456'}}
env = 'stage'
mysqlhost = mysqlUser[env]['host']
mysqluser = mysqlUser[env]['user']
mysqlpassword = mysqlUser[env]['password']

##压测数据查询OrderId
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
#
#
# ##积分流水数据库记录build ES
# import requests
# import json
# con = pymysql.connect(user=mysqluser,host=mysqlhost,passwd=mysqlpassword,db='user',charset='utf8')
# cur = con.cursor()
# sql = "select  card_no,create_time,description,id,points,status,store_id,update_time from user.card_points_flow where card_no='8038254598' and status=1 order by update_time desc;"
# cur.execute(sql)
# data = cur.fetchall()
# # print(len(data))
# for i in data:
#     createTime = str(i[1])
#     updateTime = str(i[7])
#     if createTime == 'None':
#         createTime = updateTime
#     url = 'http://10.157.40.40:10003/v1/crm/elasticsearch/buildCardPointsFlowIndexList'
#     header = {'Content-Type':'application/json'}
#     body = {"head":{"token":"string","userId":"string"},"queryBody":[{"card_no":i[0],\
#        "createTime":createTime,"description":i[2],"id":i[3],"points":i[4],"status":i[5],"store_id":i[6],\
#         "updateTime":updateTime}]}
#     Response = requests.post(url=url,json=body,headers=header)
#     Response = json.loads(Response.text)
#     if Response['results']:
#         print(body,'成功')
#     else:
#         print(body,'失败')
#     # print(body)
# cur.close()
# con.close()
#


##压测数据创建线下订单

import requests,json
ticketNumber_base = '20210107'
count = 0
with open(r'F:\丝芙兰\压测\单服务压测2020-2021\Myaccount\对比压测\user_stage.csv') as f:
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'user')
    cur = con.cursor()

    userids = f.readlines()
    for uid in userids:
        # print(str(uid).strip())
        try:
            timestamp = str(int(time.time()*1000))
            uid = uid.split(',')[0]
            # print(uid)
            sql = "select card_no from user.user_profile where user_id={user_id} limit 1;".format(user_id=uid)
            cur.execute(sql)
            data = cur.fetchone()
            count += 1
            print(count)
            if not data:
                continue
            cardNo = data[0]
            ticketNumber = ticketNumber_base + timestamp
            # print(cardNo)
            url = 'http://10.157.26.186:10026/v1/omni/order/sync/offline-order/info'
            header = {'Content-Type':'application/json'}
            body = {
                "actualAmount": 118.50,
                "callBackURL": "callBackURL",
                "cardNo": cardNo,
                "discountAmount": 100.00,
                "productInfo": [
                    {
                        "price": 218.50,
                        "productBrandNameEN": "DIOR",
                        "productImageUrl": "products/2/7/7/0/9/9/1_n_new03504_",
                        "productName": "丝芙兰Excel1",
                        "productSize": "规格: 13 ml",
                        "productSkuCode": "VS1000842",
                        "quantity": 1
                    }
                ],
                "purchaseTime": "2020-10-15 11:03:42",
                "storeCode": "6011",
                "storeName": "杭州百货大楼店",
                "ticketNumber": ticketNumber,
                "totalAmount": 218.50,
                "totalQuantity": 1
            }
            # Response = requests.post(url=url,json=body,headers=header)
            # Response = json.loads(Response.text)
            # if not Response['results']:
            #     # print(uid,'成功')
            # #     pass
            # # else:
            #     print(uid,'失败')
        except:
            print(uid,'插入数据失败。。。。。')
            continue

    cur.close()
    con.close()
#
