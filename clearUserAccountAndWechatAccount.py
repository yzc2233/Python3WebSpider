import sys
import json
import pymysql
from configparser import ConfigParser
import requests
from clearwecharcache import clearwechatcache
from clearwecharcache import clearcachemobiledefaultcard
from GetIP import getIp


def getUserInfo(mysqlhost,mysqluser,mysqlpassword,mobile):
    """根据手机号获取user_id"""
    print('*'*10,'根据手机号获取user_id','--开始','*'*10)
    user_id = None
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'user')
    cur = con.cursor()
    sql = "select id from user where mobile='{0}' and status=1".format(mobile)
    cur.execute(sql)
    data = cur.fetchone()
    if data:
        user_id = data[0]
        print('手机号：%s对应user_id为：%s' %(mobile,user_id))
    else:
        print('手机号：%s未找到对应账号' %(mobile))
    cur.close()
    con.close()
    print('*'*10,'根据手机号获取user_id','--结束','*'*10,'\n')
    return user_id

def getWechatOpenId(mysqlhost,mysqluser,mysqlpassword,mobile):
    """获取手机号对应小程序openId"""
    print('*'*10,'获取手机号对应小程序openId','--开始','*'*10)
    openIdList = []
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'wechat')
    cur = con.cursor()
    sql = "select OpenId from wechat.wechat_bind_mobile_list where Mobile='{0}';".format(mobile)
    cur.execute(sql)
    data = cur.fetchall()
    if data:
        for i in data:
            openIdList.append(i[0])
        print('手机号：%s对应openId为：%s' %(mobile,openIdList))
    else:
        print('手机号：%s不存在对应的openId账号' %mobile)
    cur.close()
    con.close()
    print('*'*10,'获取手机号对应小程序openId','--结束','*'*10,'\n')
    return openIdList

def clearUserRedisCache(myaccount_ip,user_id):
    """清除User中对应user_id的Redis缓存"""
    print('*'*10,'清除User中对应user_id的Redis缓存','--开始','*'*10)
    body = {"head": {"token": "string","userId": "string"},"queryBody": [user_id]}
    url = myaccount_ip + '/v1/myaccount/demo/userCache'
    res = requests.delete(url,json=body)
    response = json.loads(res.text)
    if response['results'] != str(user_id):
        print('清除CRMHUB手机号对应默认卡缓存失败',res.text)
    else:
        print('清除CRMHUB手机号对应默认卡缓存成功')
    print('*'*10,'清除User中对应user_id的Redis缓存','--结束','*'*10,'\n')

def db_delete_userRegister(mysqlhost,mysqluser,mysqlpassword,mobile):
    """user数据库删除相应用户记录"""
    print('*'*10,'user数据库删除相应用户记录','--开始','*'*10)
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
    print('*'*10,'user数据库删除相应用户记录','--结束','*'*10,'\n')

def db_delete_crmhubMobilemapping(mysqlhost,mysqluser,mysqlpassword,mobile):
    """CRMHUB数据库删除相应手机号卡号绑定关系"""
    print('*'*10,'CRMHUB数据库删除相应手机号卡号绑定关系','--开始','*'*10)
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'crmhub')
    cur = con.cursor()
    sql1 = "DELETE  FROM crmhub.omni_card_mobile_mapping WHERE MOBILE='{0}';".format(mobile)
    cur.execute(sql1)
    con.commit()
    cur.close()
    con.close()
    print('*'*10,'CRMHUB数据库删除相应手机号卡号绑定关系','--结束','*'*10,'\n')

def db_delete_wechatRegister(mysqlhost,mysqluser,mysqlpassword,mobile,openId):
    """删除WECHATCENTER数据库中手机号对应注册信息"""
    print('*'*10,'删除WECHATCENTER数据库中手机号对应注册信息','--开始','*'*10)
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'wechat')
    cur = con.cursor()
    sql1 = "DELETE FROM wechat_bind_mobile_list WHERE OpenId='{0}' AND MOBILE='{1}';".format(openId,mobile)
    sql2 = "delete from wechat_bind_mobile_history where OpenId='{0}';".format(openId)
    sql3 = "delete from wechat_ba_bind where open_id='{0}';".format(openId)
    sql4 = "delete from wechat_ba_bind_history where open_id='{0}';".format(openId)
    sql5 = "DELETE FROM  wechat_register_info WHERE OpenId='{0}';".format(openId)
    sql6 = "delete from monitor_wechat_user_access_history_log where OpenId='{0}';".format(openId)
    sql7 = "delete from wechat_mgm_register_bind_history where referral_open_id='{0}';".format(openId)
    cur.execute(sql1)
    cur.execute(sql2)
    cur.execute(sql3)
    cur.execute(sql4)
    cur.execute(sql5)
    cur.execute(sql6)
    cur.execute(sql7)
    con.commit()
    cur.close()
    con.close()
    print('*'*10,'删除WECHATCENTER数据库中手机号对应注册信息','--结束','*'*10,'\n')


def db_delete_CRMHUBWechatRegister(mysqlhost,mysqluser,mysqlpassword,openId):
    """删除CRMHUB数据库中小程序对应注册信息"""
    print('*'*10,'删除CRMHUB数据库中小程序对应注册信息','--开始','*'*10)
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'crmhub')
    cur = con.cursor()
    sql1 = "delete from omni_crm_wechat_register_info_log where OpenId='{0}';".format(openId)
    sql2 = "DELETE FROM omni_member_recommend WHERE referral_open_id='{0}';".format(openId)
    sql3 = "DELETE FROM omni_member_recommend_history WHERE referral_open_id='{0}';".format(openId)
    cur.execute(sql1)
    cur.execute(sql2)
    cur.execute(sql3)
    con.commit()
    cur.close()
    con.close()
    print('*'*10,'删除CRMHUB数据库中小程序对应注册信息','--结束','*'*10,'\n')

if __name__ == '__main__':
    #获取入参：环境、手机号
    env = sys.argv[1]
    mobile = sys.argv[2]
    switch_deluser = False
    try :
        deluser = sys.argv[3]
        if deluser == '1':
            switch_deluser = True
    except:
        pass

    # env = 'stage'
    # mobile = '16621790415'

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
        #清除user中redis缓存
        clearUserRedisCache(myaccount_ip,user_id)

    if switch_deluser:
        #user数据库清除相应记录
        db_delete_userRegister(mysqlhost,mysqluser,mysqlpassword,mobile)
        # #clearUserRedisCache(myaccount_ip,user_id) #

        #清除CRMHUB中手机号对应卡记录
        db_delete_crmhubMobilemapping(mysqlhost,mysqluser,mysqlpassword,mobile)
        #清除CRMHUB手机号对应默认卡缓存
        clearcachemobiledefaultcard(crmhub_ip,mobile)

    # print(user_id)
    #获取openId
    openIdList = getWechatOpenId(mysqlhost,mysqluser,mysqlpassword,mobile)
    if openIdList:
        #删除WECHATCENTER数据库中手机号对应注册信息
        for openId in openIdList:
            # 删除WECHATCENTER数据库中手机号对应注册信息
            db_delete_wechatRegister(mysqlhost,mysqluser,mysqlpassword,mobile,openId)

            # 删除CRMHUB数据库中小程序对应注册信息
            db_delete_CRMHUBWechatRegister(mysqlhost,mysqluser,mysqlpassword,openId)

            #删除小程序注册信息相关缓存
            clearwechatcache(wechatcenter_ip,openId,mobile,crmhub_ip)




