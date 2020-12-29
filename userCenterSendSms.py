import sys
import requests
import json
from rediscluster import RedisCluster

print('''请求命令Sample:python userCenterSendSms.py stage android 14444404547 forget
场景（账号密码注册：REGIST；忘记密码：FORGET；手机验证码登录：SMS；账号密码登录：PWD；联合登录绑定手机：SOCIALBIND；
用户手机号身份验证：TELREGISTED；用户留资：COMPLETETEL；邮箱登录绑定手机：EMAILBIND）
''')
#
scenedict = {'REGIST':'账号密码注册','FORGET':'忘记密码','SMS':'手机验证码登录','PWD':'账号密码登录','SOCIALBIND':'联合登录绑定手机',\
             'TELREGISTED':'用户手机号身份验证','COMPLETETEL':'用户留资','EMAILBIND':'邮箱登录绑定手机'}

def getcaptcha(identification,imageType=1):
    headers = {'channel':channel}
    url = env_IP + '/v1/usercenter/verification/captcha?imageType={imageType}&identification={identification}'.format(imageType=imageType,identification=identification)
    res = requests.get(url,headers=headers)
    response = json.loads(res.text)
    if response['errorCode']:
        print('获取图形验证码失败，错误：',response)
        exit()
    codeToken = response['results']['codeToken']
    # print(codeToken)
    return codeToken

def getcaptchacodeByRedis(codeToken):
    r = RedisCluster(startup_nodes=nodes,decode_responses=True)
    rkey = 'cache:usercenter_captcha_token:usercenter_captcha_token_{channel}_{codeToken}'.format(channel=channel,codeToken=codeToken)
    code = r.get(rkey)[1:5]
    rkey2 = "cache:usercenter_sms_send:usercenter_sms_send_{mobile}_{scene}".format(mobile=mobile,scene=scene)
    # r.delete(rkey2)
    # print(code)
    return code


def verificatecaptcha(identification,code,codeToken):
    headers = {'channel':channel}
    url = env_IP + '/v1/usercenter/verification/captcha?identification={identification}&code={code}&codeToken={codeToken}'.format(identification=identification,code=code,codeToken=codeToken)
    res = requests.post(url,headers=headers)
    response = json.loads(res.text)
    if response['errorCode']:
        print('校验图形验证码失败，错误：',response)
        exit()
    rtoken = response['results']['rtoken']
    # print(rtoken)
    return rtoken

def usercentersendSms(rToken):
    headers = {'channel':channel}
    url = env_IP + '/v1/usercenter/verification/smsCode?rToken={rToken}&scene={scene}'.format(rToken=rToken,scene=scene)
    res = requests.post(url,headers=headers)
    response = json.loads(res.text)
    if response['errorCode']:
        print('发送短信验证码失败，错误：',response)
        exit()

def getSmsCodeByRedis(mobile,channel,scene):
    r = RedisCluster(startup_nodes=nodes,decode_responses=True)
    rkey = 'cache:usercenter_telephone_smscode:usercenter_telephone_smscode_{mobile}_{channel}_{scene}'.format(mobile=mobile,channel=channel,scene=scene)
    # print(code)
    SmsCode = r.get(rkey)
    if not SmsCode:
        r = RedisCluster(startup_nodes=nodes2,decode_responses=True)
        SmsCode = r.get(rkey)[1:7]
    else:
        SmsCode = r.get(rkey)[1:7]
    return SmsCode


if __name__ == '__main__':
    env = sys.argv[1]
    channel = sys.argv[2].upper()
    mobile = sys.argv[3]
    scene = sys.argv[4].upper()

    if env.lower()=='stage':
        env_IP = 'https://stageapi.sephora.cn'
        nodes = [{'host':'10.157.24.45', 'port':6379},{'host':'10.157.24.46', 'port':6379},
                 {'host':'10.157.24.47', 'port':6379}, {'host':'10.157.24.54', 'port':6379},
                 {'host':'10.157.24.55', 'port':6379}]
    elif env.lower()=='qa2':
        env_IP = 'https://testapi.sephora.cn'
        nodes = [{'host':'10.157.26.84', 'port':6379},{'host':'10.157.26.85', 'port':6379},
                 {'host':'10.157.26.86', 'port':6379}, {'host':'10.157.26.87', 'port':6379},
                 {'host':'10.157.26.88', 'port':6379}]
    elif env.lower()=='ebf':
        env_IP = 'https://ebfapi.sephora.cn'
        nodes = [{'host':'10.157.46.44', 'port':6379},{'host':'10.157.46.45', 'port':6379}]
    elif env.lower()=='prd':
        env_IP = 'https://api.sephora.cn'
        nodes = [{'host':'10.157.32.78', 'port':6479},
                 {'host':'10.157.32.79', 'port':6479},{'host':'10.157.32.80', 'port':6479},
                 {'host':'10.157.32.65', 'port':6479},{'host':'10.157.32.66', 'port':6479},
                 {'host':'10.157.32.69', 'port':6479}]
        nodes2 = [{'host':'10.157.32.78', 'port':6379}]
    else:
        print('环境输入错误，仅支持qa2/stage/ebf环境')


    #获取图形验证码codeToken
    codeToken = getcaptcha(mobile)
    #redis获取图形验证码
    code = getcaptchacodeByRedis(codeToken)
    #校验图形验证码获取rtoken
    rtoken = verificatecaptcha(mobile,code,codeToken)
    #发送短信验证码
    usercentersendSms(rtoken)
    #redis获取短信验证码
    SmsCode = getSmsCodeByRedis(mobile,channel,scene)
    print('手机号{mobile}在{channel}渠道，{scene}场景，发送短信验证码为：{SmsCode}，对应rtoken为：{rtoken}'.format(mobile=mobile,channel=channel,scene=scenedict[scene],SmsCode=SmsCode,rtoken=rtoken))
