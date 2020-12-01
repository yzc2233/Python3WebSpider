
import time
import pymysql

mysqlUser = {'qa2':{'host':'10.157.26.92','user':'marketing','password':'123456'},'stage':{'host':'10.157.24.94','user':'sephora_app','password':'123456'}}
env = 'stage'
mysqlhost = mysqlUser[env]['host']
mysqluser = mysqlUser[env]['user']
mysqlpassword = mysqlUser[env]['password']


# print(timestamp)

client_id_part1 = 'Android-Ag-PILIANGDAORUTAGSDevicetest1-'

with open(r'E:\SoftWare\JetBrains\IntellijCode\PythonCode\createorder\deviceuserimport.csv') as f:
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'user')
    cur = con.cursor()

    userids = f.readlines()
    for uid in userids:
        # print(str(uid).strip())
        try:
            timestamp = str(int(time.time()*1000))
            uid = uid.strip()
            print(uid)
            # sql = "insert into `user_device_status` (`client_id`, `user_id`, `supplier`, `status`, `create_time`, `update_time`) \
            # values('{0}','{1}','UM','1','2020-11-30 00:00:00','2020-11-30 00:00:00');".format(client_id_part1+timestamp,uid)
            # cur.execute(sql)
            # con.commit()
        except:
            print(uid,'插入数据失败。。。。。')
            continue

    cur.close()
    con.close()

