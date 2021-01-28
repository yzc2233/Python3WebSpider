"""
    提供给他人可单独执行的脚本
"""
import sys
import json
import os
try:
    import requests
except:
    print('requests模块未安装，现在开始安装')
    os.system('pip install requests')
    import requests

try:
    import pymysql
except:
    print('requests模块未安装，现在开始安装')
    os.system('pip install pymysql')
    import pymysql

try:
    from bs4 import BeautifulSoup
except:
    print('bs4模块未安装，现在开始安装')
    os.system('pip install bs4')
    from bs4 import BeautifulSoup

try:
    from rediscluster import RedisCluster
except:
    print('rediscluster模块未安装，现在开始安装')
    os.system('pip install redis-py-cluster')
    from rediscluster import RedisCluster

# from configparser import ConfigParser
# import requests
# from clearwecharcache import clearwechatcache
# from clearwecharcache import clearcachemobiledefaultcard
# from GetIP import getIp

mysqlUser = {'qa2':{'host':'10.157.26.92','user':'marketing','password':'123456'},'stage':{'host':'10.157.24.94','user':'sephora_app','password':'123456'}
             ,'ebf':{'host':'10.157.24.252','user':'sephora_app','password':'123456'}}


def getIp(env='stage',service=''):
    service = service.lower()
    env = env.lower()

    if env == 'qa2':
        SwaggerURL = 'http://10.157.40.131:1111'
    elif env == 'stage':
        SwaggerURL = 'http://10.157.26.160:1111'
    elif env == 'ebf':
        SwaggerURL = 'http://10.157.40.13:1111'
    else:
        print('非QA2&Stage&EBF环境暂不支持，请谨慎操作')
        exit()

    res = requests.get(SwaggerURL)
    res.encoding = 'GB2312'
    soup = BeautifulSoup(res.text,'html.parser')
    ans = soup.find_all(['a','_blank'])

    ip = ''
    for an in ans:
        mlist = str(an.string)
        if mlist.find(service) >= 0:
            ipInfo = mlist.split('-')
            port = ipInfo[-1].split(':')
            ip = 'http://' + ipInfo[-2] +':' + port[-1]

    if ip == '':
        return '未找到对应Service的IP，请检查入参！'
        exit()
    else:
        return ip


def getUserInfo(mysqlhost,mysqluser,mysqlpassword,mobile):
    """根据手机号获取user_id"""
    print('*'*10,'根据手机号获取user_id','--开始','*'*10)
    user_id = None
    con = pymysql.connect(host=mysqlhost,user=mysqluser,password=mysqlpassword,database='user')
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
    con = pymysql.connect(host=mysqlhost,user=mysqluser,password=mysqlpassword,database='wechat')
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
    con = pymysql.connect(host=mysqlhost,user=mysqluser,password=mysqlpassword,database='user')
    cur = con.cursor()
    sql1 = "DELETE FROM user.user where mobile='{0}';".format(mobile)
    sql2 = "DELETE FROM user.user_profile where mobile='{0}';".format(mobile)
    sql3 = "DELETE FROM user.user_third_party_store where mobile='{0}';".format(mobile)
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
    con = pymysql.connect(host=mysqlhost,user=mysqluser,password=mysqlpassword,database='crmhub')
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
    con = pymysql.connect(host=mysqlhost,user=mysqluser,password=mysqlpassword,database='wechat')
    cur = con.cursor()
    sql1 = "DELETE FROM wechat_bind_mobile_list WHERE OpenId='{0}' AND MOBILE='{1}';".format(openId,mobile)
    # sql2 = "DELETE FROM wechat_bind_mobile_history where OpenId='{0}';".format(openId)
    sql3 = "DELETE FROM wechat_ba_bind where open_id='{0}';".format(openId)
    # sql4 = "DELETE FROM wechat_ba_bind_history where open_id='{0}';".format(openId)
    sql5 = "DELETE FROM  wechat_register_info WHERE OpenId='{0}';".format(openId)
    sql6 = "DELETE FROM monitor_wechat_user_access_history_log where OpenId='{0}';".format(openId)
    sql7 = "DELETE FROM wechat_mgm_register_bind_history where referral_open_id='{0}';".format(openId)
    cur.execute(sql1)
    # cur.execute(sql2)
    cur.execute(sql3)
    # cur.execute(sql4)
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
    con = pymysql.connect(host=mysqlhost,user=mysqluser,password=mysqlpassword,database='crmhub')
    cur = con.cursor()
    sql1 = "DELETE FROM omni_crm_wechat_register_info_log where OpenId='{0}';".format(openId)
    sql2 = "DELETE FROM omni_member_recommend WHERE referral_open_id='{0}';".format(openId)
    sql3 = "DELETE FROM omni_member_recommend_history WHERE referral_open_id='{0}';".format(openId)
    cur.execute(sql1)
    cur.execute(sql2)
    cur.execute(sql3)
    con.commit()
    cur.close()
    con.close()
    print('*'*10,'删除CRMHUB数据库中小程序对应注册信息','--结束','*'*10,'\n')

#清除CRMHUB手机号对应默认卡缓存
def clearcachemobiledefaultcard(crmhub_ip,mobile):
    print('*'*10,'清除CRMHUB手机号对应默认卡缓存','--开始','*'*10)
    clearcachemobiledefaultcard_url = crmhub_ip+'/v1/omni/crm/hub/cache/mobile/default/card?mobile='+mobile
    req = requests.delete(clearcachemobiledefaultcard_url)
    reqstatus = req.status_code
    if reqstatus != 200:
        print('清除CRMHUB手机号对应默认卡缓存,接口status：',reqstatus)
    else:
        print('清除CRMHUB手机号对应默认卡缓存成功')
    print('*'*10,'清除CRMHUB手机号对应默认卡缓存','--结束','*'*10,'\n')

#清除指定openId用户的微信登录注册信息缓存
def clearRegisterCached(wechat_ip,openId):
    print('*'*10,'清除指定openId用户的微信登录注册信息缓存','--开始','*'*10)
    clearRegisterCached_url = wechat_ip+'/v1/wechat/center/global/cached/clearRegisterCached?openId='+openId
    req = requests.get(clearRegisterCached_url)
    reqstatus = req.status_code
    if reqstatus != 200:
        print('清除指定openId用户的微信登录注册信息缓存接口失败,接口status：',reqstatus)
    else:
        print('清除指定openId用户的微信登录注册信息缓存成功')
    print('*'*10,'清除指定openId用户的微信登录注册信息缓存','--结束','*'*10,'\n')

#清除小程序登录注册时是否绑定过手机的状态缓存
def clearBindMobileStatusCached(wechat_ip,openId):
    print('*'*10,'清除小程序登录注册时是否绑定过手机的状态缓存','--开始','*'*10)
    clearBindMobileStatusCached_url = wechat_ip+'/v1/wechat/center/global/cached/clearBindMobileStatusCached?openId='+openId
    req = requests.get(clearBindMobileStatusCached_url)
    reqstatus = req.status_code
    if reqstatus != 200:
        print('清除小程序登录注册时是否绑定过手机的状态缓存,接口status：',reqstatus)
    else:
        print('清除小程序登录注册时是否绑定过手机的状态缓存成功')
    print('*'*10,'清除小程序登录注册时是否绑定过手机的状态缓存','--结束','*'*10,'\n')

#清除用户授权的手机是否已经绑定过当前账户的状态缓存
def clearCurrentAuthorizeMobileIsBindCached(wechat_ip,openId,mobile):
    print('*'*10,'清除用户授权的手机是否已经绑定过当前账户的状态缓存','--开始','*'*10)
    clearCurrentAuthorizeMobileIsBindCached_url = wechat_ip+'/v1/wechat/center/global/cached/clearCurrentAuthorizeMobileIsBindCached?openId='+openId+'&mobile='+mobile
    req = requests.get(clearCurrentAuthorizeMobileIsBindCached_url)
    reqstatus = req.status_code
    if reqstatus != 200:
        print('清除用户授权的手机是否已经绑定过当前账户的状态缓存,接口status：',reqstatus)
    else:
        print('清除用户授权的手机是否已经绑定过当前账户的状态缓存成功')
    print('*'*10,'清除用户授权的手机是否已经绑定过当前账户的状态缓存','--结束','*'*10,'\n')


#清除指定小程序用户当前绑定的活跃手机的缓存
def clearCurrentBindActiveMobileCached(wechat_ip,openId):
    print('*'*10,'清除指定小程序用户当前绑定的活跃手机的缓存','--开始','*'*10)
    clearCurrentBindActiveMobileCached_url = wechat_ip+'/v1/wechat/center/global/cached/clearCurrentBindActiveMobileCached?openId='+openId
    req = requests.get(clearCurrentBindActiveMobileCached_url)
    reqstatus = req.status_code
    if reqstatus != 200:
        print('清除指定小程序用户当前绑定的活跃手机的缓存,接口status：',reqstatus)
    else:
        print('清除指定小程序用户当前绑定的活跃手机的缓存成功')
    print('*'*10,'清除指定小程序用户当前绑定的活跃手机的缓存','--结束','*'*10,'\n')

def delUserCenterTpBindRedis(mobile):
    print('*'*10,'清除usercenter缓存开始','*'*10)
    r = RedisCluster(startup_nodes=nodes,decode_responses=True)
    rkey = "SOA:USERCENTER:SMS:LOGIN:{mobile}".format(mobile=mobile)
    r.delete(rkey)
    print('*'*10,'清除usercenter缓存结束','*'*10)

def delWechatCenterbindMobileStatusRedis(openId):
    print('*'*10,'清除wechatcenter-bindMobileStatus缓存开始','*'*10)
    r = RedisCluster(startup_nodes=nodes,decode_responses=True)
    rkey = "cache:wechat_center_user_bind_mobile_status:WECHAT_CENTER_USER_BIND_MOBILE_STATUS_{openId}".format(openId=openId)
    r.delete(rkey)
    print('*'*10,'清除wechatcenter-bindMobileStatus缓存开始','*'*10)

def clearwechatcache(wechat_ip,openId,mobile,crmhub_ip):
    #清除指定openId用户的微信登录注册信息缓存
    clearRegisterCached(wechat_ip,openId)
    #清除小程序登录注册时是否绑定过手机的状态缓存
    clearBindMobileStatusCached(wechat_ip,openId)
    #清除用户授权的手机是否已经绑定过当前账户的状态缓存
    clearCurrentAuthorizeMobileIsBindCached(wechat_ip,openId,mobile)
    #清除指定小程序用户当前绑定的活跃手机的缓存
    clearCurrentBindActiveMobileCached(wechat_ip,openId)
    #清除CRMHUB手机号对应默认卡缓存
    clearcachemobiledefaultcard(crmhub_ip,mobile)

if __name__ == '__main__':
    #获取入参：环境、手机号
    env = sys.argv[1].lower()
    mobile = sys.argv[2]
    switch_deluser = False
    try :
        deluser = sys.argv[3]
        if deluser == '1':
            switch_deluser = True
    except:
        pass

    if env.lower()=='stage':
        env_IP = 'https://stageapi.sephora.cn'
        # db_host = '10.157.24.94'
        # db_user = 'sephora_app'
        # db_password = '123456'
        nodes = [{'host':'10.157.24.45', 'port':6379},{'host':'10.157.24.46', 'port':6379},
                 {'host':'10.157.24.47', 'port':6379}, {'host':'10.157.24.54', 'port':6379},
                 {'host':'10.157.24.55', 'port':6379}]

    elif env.lower()=='qa2':
        env_IP = 'https://testapi.sephora.cn'
        # db_host = '10.157.26.92'
        # db_user = 'marketing'
        # db_password = '123456'
        nodes = [{'host':'10.157.26.84', 'port':6379},{'host':'10.157.26.85', 'port':6379},
                 {'host':'10.157.26.86', 'port':6379}, {'host':'10.157.26.87', 'port':6379},
                 {'host':'10.157.26.88', 'port':6379}]

    elif env.lower()=='ebf':
        env_IP = 'https://ebfapi.sephora.cn'
        # db_host = '10.157.24.252'
        # db_user = 'sephora_app'
        # db_password = '123456'
        nodes = [{'host':'10.157.46.44', 'port':6379},{'host':'10.157.46.45', 'port':6379}]
    else:
        print('环境输入错误，仅支持qa2/stage环境')
        exit()
    # env = 'stage'
    # mobile = '16621790415'

    #获取所需service的IP
    myaccount_ip = getIp(env,'sephora-myaccount-service')
    wechatcenter_ip = getIp(env,'sephora-wechatcenter-service')
    crmhub_ip = getIp(env,'omni-crmhub-service')

    #获取数据库连接信息
    # config =ConfigParser()
    # config.read('properties.conf')

    mysqlhost = mysqlUser[env]['host']
    mysqluser = mysqlUser[env]['user']
    mysqlpassword = mysqlUser[env]['password']

    #获取user_id
    user_id = getUserInfo(mysqlhost,mysqluser,mysqlpassword,mobile)
    # user_id = 258
    if user_id:
        #清除user中redis缓存
        clearUserRedisCache(myaccount_ip,user_id)

    delUserCenterTpBindRedis(mobile)

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
    # openIdList = ['ojmVG4_OjZjjD6F_19AeHNUGcW7o']
    if openIdList:
        #删除WECHATCENTER数据库中手机号对应注册信息
        for openId in openIdList:
            # 删除WECHATCENTER数据库中手机号对应注册信息
            db_delete_wechatRegister(mysqlhost,mysqluser,mysqlpassword,mobile,openId)

            # 删除CRMHUB数据库中小程序对应注册信息
            db_delete_CRMHUBWechatRegister(mysqlhost,mysqluser,mysqlpassword,openId)

            #删除小程序注册信息相关缓存
            clearwechatcache(wechatcenter_ip,openId,mobile,crmhub_ip)

            #清除wechatcenter-bindMobileStatus缓存开始
            delWechatCenterbindMobileStatusRedis(openId)




