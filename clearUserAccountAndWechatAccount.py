import sys
import json
import pymysql
from configparser import ConfigParser
import requests
from clearwecharcache import clearwechatcache
from GetIP import getIp


def getUserInfo(mysqlhost,mysqluser,mysqlpassword,mobile):
    """获取user_id"""
    user_id = None
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'user')
    cur = con.cursor()
    sql = "select id from user where mobile='{0}' and status=1".format(mobile)
    cur.execute(sql)
    data = cur.fetchone()
    if data:
        user_id = data[0]
    cur.close()
    con.close()
    return user_id

def getWechatOpenId(mysqlhost,mysqluser,mysqlpassword,mobile):
    """获取小程序openId"""
    openIdList = []
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'wechat')
    cur = con.cursor()
    sql = "select OpenId from wechat.wechat_bind_mobile_list where Mobile='{0}';".format(mobile)
    cur.execute(sql)
    data = cur.fetchall()
    if data:
        for i in data:
            openIdList.append(i[0])
    cur.close()
    con.close()
    return openIdList

def clearUserRedisCache(myaccount_ip,user_id):
    """清除User中对应user_id的Redis缓存"""
    body = {"head": {"token": "string","userId": "string"},"queryBody": [user_id]}

    url = myaccount_ip + '/v1/myaccount/demo/userCache'
    res = requests.delete(url,json=body)
    response = json.loads(res.text)
    if response['results'] != str(user_id):
        print('清除CRMHUB手机号对应默认卡缓存失败',res.text)
    else:
        print('清除CRMHUB手机号对应默认卡缓存成功')

def db_delete_userRegister(mysqlhost,mysqluser,mysqlpassword,mobile):
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'user')
    cur = con.cursor()
    sql1 = "delete from user.user where mobile='{0}';".format(mobile)
    sql2 = "delete from user.user_profile where mobile='{0}';".format(mobile)
    sql3 = "delete from user.user_third_party_store where mobile='{0}';".format(mobile)
    cur.execute(sql1)
    cur.execute(sql2)
    cur.execute(sql3)
    con.commit()
    cur.close()
    con.close()

def db_delete_crmhubMobilemapping(mysqlhost,mysqluser,mysqlpassword,mobile):
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'crmhub')
    cur = con.cursor()
    sql1 = "DELETE  FROM crmhub.omni_card_mobile_mapping WHERE MOBILE='{0}';".format(mobile)
    cur.execute(sql1)
    con.commit()
    cur.close()
    con.close()


if __name__ == '__main__':
    #获取入参：环境、手机号
    # env = sys.argv[1]
    env = 'stage'
    # mobile = sys.argv[2]
    mobile = '16621790415'

    #获取所需service的IP
    myaccount_ip = getIp(env,'sephora-myaccount-service')
    wechatcenter_ip = getIp(env,'sephora-wechatcenter-service')
    crmhub_ip = getIp(env,'omni-crmhub-service')

    #获取数据库连接信息
    config =ConfigParser()
    config.read('properties.conf')
    mysqlhost = config['mysql_'+ env]['host']
    mysqluser = config['mysql_'+ env]['user']
    mysqlpassword = config['mysql_'+ env]['password']

    #获取user_id
    user_id = getUserInfo(mysqlhost,mysqluser,mysqlpassword,mobile)
    if user_id:
        print('手机号：%s对应user_id为：%s' %(mobile,user_id))
        #清除user中redis缓存
        clearUserRedisCache(myaccount_ip,user_id)

        # #user数据库清除相应记录
        # db_delete_userRegister(mysqlhost,mysqluser,mysqlpassword,mobile)




    else:
        print('手机号：%s不存在对应的user账号' %mobile)
    # print(user_id)
    #获取openId
    openIdList = getWechatOpenId(mysqlhost,mysqluser,mysqlpassword,mobile)
    if user_id:
        print('手机号：%s对应openId为：%s' %(mobile,openIdList))
    else:
        print('手机号：%s不存在对应的openId账号' %openIdList)
    # print(openIdList)



