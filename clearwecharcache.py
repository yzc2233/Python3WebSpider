import sys
import requests
import GetIP


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
    env = sys.argv[1]
    # env = 'stage'
    openId = sys.argv[2]
    if len(sys.argv) < 4:
        mobile = '0'
    else:
        mobile = sys.argv[3]

    wechat_ip = GetIP.getIp(env,'sephora-wechatcenter-service')
    crmhub_ip = GetIP.getIp(env,'omni-crmhub-service')

    #清除微信账号相关缓存
    clearwechatcache(wechat_ip,openId,mobile,crmhub_ip)
