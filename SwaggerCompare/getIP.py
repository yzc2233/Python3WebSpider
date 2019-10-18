import sys
import os

try:
    import requests
except:
   print('requests模块未安装，现在开始安装')
   os.system('pip install requests')
   import requests

try:
    from bs4 import BeautifulSoup
except:
    print('bs4模块未安装，现在开始安装')
    os.system('pip install bs4')
    from bs4 import BeautifulSoup

def getIP(env='stage',service=''):
    env = env.lower()
    service = service.lower()

    if env == 'qa2':
        SwaggerURL = 'http://10.157.46.143:1111'
    elif env == 'stage':
        SwaggerURL = 'http://10.157.24.76:1111'
    elif env == 'prd':
        SwaggerURL = 'http://10.157.32.29:1111/'
    else:
        print('环境输入有误，请输入qa2、stage或prd')
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
            ip = 'http://' + ipInfo[-2] + ':' + port[-1]

    if ip == '':
        return '未找到对应Service的IP，请检查入参！'
        exit()
    else:
        return ip

if __name__ == '__main__':
    ip = getIP(env='stage',service='OMNI-CRMHUB-SERVICE')
    print(ip)