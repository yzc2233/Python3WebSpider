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












