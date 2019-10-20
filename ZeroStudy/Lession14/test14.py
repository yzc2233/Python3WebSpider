


# import urllib.request
#
# res = urllib.request.urlopen('http://www.baidu.com')
# html = res.read()
# print(html)


# import urllib.request
# import urllib.parse
#
# data = bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf8')
# res = urllib.request.urlopen('http://httpbin.org/post',data=data)
# html = res.read()
# print(html)

#
# import urllib3
#
# #创建PoolManager对象用于处理与线程池的连接以及线程安全的所有细节
# http = urllib3.PoolManager()
# # res = http.request('GET','https://www.baidu.com')
# res = http.request('POST','http://httpbin.org/post',fields={'word':'hello'})
# print(res.data)
#

import requests
# res = requests.get('http://www.baidu.com')
# print(res.status_code)
# print(res.url)
# print(res.headers)
# print(res.cookies)
# print(res.text)
# print(res.content)

# res = requests.put('http://httpbin.org/put',data={'key':'value'})
# res = requests.delete('http://httpbin.org/delete')
# res = requests.get('http://httpbin.org/get')
# res = requests.options('http://httpbin.org/get')
#
#
# pyload = {'key1':'value1','key2':'value2'}
# res = requests.get('http://httpbin.org/get',params=pyload)
# print(res.content)


# import requests
# url = 'https://www.baidu.com'
#
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'}
# res = requests.get(url,headers=headers)
# print(res.content)
#
#

# import requests
#
# for a in range(0,50):
#     try:
#         res = requests.get('https://www.baidu.com',timeout=0.01)
#         print(res.status_code)
#     except Exception as e:
#         print('异常'+str(e))
#

# import requests
#
# proxy = {'http':'122.114.31.177:808',
#          'https':'122.114.31.177:8080'}
# res = requests.get('http://www.mingrisoft.com/',proxies=proxy)
# print(res.content)







































