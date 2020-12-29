import sys
import pymysql
from rediscluster import RedisCluster

print("""例子：python userCenterClearThirdUserBind.py stage android qq UID_BEF8A31AD64F84C163820917F261FDB8
""")

def clearuserbindtplistAndhistory(unionId):
    conn = pymysql.connect(db_host,db_user,db_password,'usercenter')
    cur = conn.cursor()
    delsql1 = "delete FROM usercenter.user_bind_tp_list where union_id='{union_id}';".format(union_id=unionId,channel=channel)
    delsql2 = "delete FROM usercenter.user_bind_tp_history where union_id='{union_id}';".format(union_id=unionId,channel=channel)
    delsql3 = "delete FROM usercenter.user_bind_third_party_list where union_id='{union_id}';".format(union_id=unionId)
    delsql4 = "delete FROM usercenter.user_bind_third_party_history where union_id='{union_id}';".format(union_id=unionId)
    cur.execute(delsql1)
    cur.execute(delsql2)
    cur.execute(delsql3)
    cur.execute(delsql4)
    conn.commit()
    cur.close()
    conn.close()

def delUserCenterTpBindRedis(unionId):
    r = RedisCluster(startup_nodes=nodes,decode_responses=True)
    rkey = "SOA:USERCENTER:BIND:TP:{bindtype}:{unionId}".format(bindtype=bindtype,unionId=unionId)
    r.delete(rkey)

def getBindUserId(unionId):
    userIdList = []
    conn = pymysql.connect(db_host,db_user,db_password,'user')
    cur = conn.cursor()
    delsql1 = "select user_id FROM user.user_third_party_store where union_id='{union_id}';".format(union_id=unionId)
    cur.execute(delsql1)
    db_data = cur.fetchall()
    for item in db_data:
        userIdList.append(item[0])
    cur.close()
    conn.close()
    return userIdList

def clearuserthirdpartstore(unionId):
    conn = pymysql.connect(db_host,db_user,db_password,'user')
    cur = conn.cursor()
    delsql1 = "delete FROM user.user_third_party_store where union_id='{union_id}';".format(union_id=unionId)
    delsql2 = "delete FROM user.user_third_party_store_ex where union_id='{union_id}';".format(union_id=unionId)
    cur.execute(delsql1)
    cur.execute(delsql2)
    conn.commit()
    cur.close()
    conn.close()

def delUserThirdBindRedis(unionId,userIdList):
    r = RedisCluster(startup_nodes=nodes,decode_responses=True)
    rkey = "SOA:MYACCOUNT:LOGIN:SOCIAL:{bindtype}:UNIONID:{unionId}".format(bindtype=bindtype,unionId=unionId)
    r.delete(rkey)
    for uid in userIdList:
        rkey2 = "SOA:MYACCOUNT:USER:SOCIAL:BIND:{uid}".format(uid=uid)
        r.delete(rkey2)

if __name__ == '__main__':

    env = sys.argv[1]
    channel = sys.argv[2].upper()
    bindtype = sys.argv[3].upper()
    unionId = sys.argv[4]

    if env.lower()=='stage':
        env_IP = 'https://stageapi.sephora.cn'
        db_host = '10.157.24.94'
        db_user = 'sephora_app'
        db_password = '123456'
        nodes = [{'host':'10.157.24.45', 'port':6379},{'host':'10.157.24.46', 'port':6379},
                 {'host':'10.157.24.47', 'port':6379}, {'host':'10.157.24.54', 'port':6379},
                 {'host':'10.157.24.55', 'port':6379}]

    elif env.lower()=='qa2':
        env_IP = 'https://testapi.sephora.cn'
        db_host = '10.157.26.92'
        db_user = 'marketing'
        db_password = '123456'
        nodes = [{'host':'10.157.26.84', 'port':6379},{'host':'10.157.26.85', 'port':6379},
                 {'host':'10.157.26.86', 'port':6379}, {'host':'10.157.26.87', 'port':6379},
                 {'host':'10.157.26.88', 'port':6379}]
    elif env.lower()=='ebf':
        env_IP = 'https://ebfapi.sephora.cn'
        db_host = '10.157.24.252'
        db_user = 'sephora_app'
        db_password = '123456'
        nodes = [{'host':'10.157.46.44', 'port':6379},{'host':'10.157.46.45', 'port':6379}]
    else:
        print('环境输入错误，仅支持qa2/stage/ebf环境')
        exit()

    # 清除user_bind_tp_list、user_bind_tp_history对应unionId记录
    clearuserbindtplistAndhistory(unionId)
    # 清除usercenter第三方绑定关系
    delUserCenterTpBindRedis(unionId)
    # 获取uid
    userIdList = getBindUserId(unionId)
    #清除user表第三方绑定关系
    clearuserthirdpartstore(unionId)
    #清除user第三方redis缓存
    delUserThirdBindRedis(unionId,userIdList)
    print('已清除')
