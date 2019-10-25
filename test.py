# import tesserocr
# from PIL import Image
# image = Image.open('E:\SoftWare\Anaconda3\envs\mypython36\image.jpg')
# print(tesserocr.image_to_text(image))

# from flask import Flask
# app = Flask(__name__)
#
# @app.route("/")
# def hello():
#     return "Hello world!"
#
# if __name__ == "__main__":
#     app.run()

#
# import tornado.ioloop
# import tornado.web
#
# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("hello world!")
#
# def make_app():
#     return tornado.web.Application([
#         (r"/",MainHandler),
#     ])
#
# if __name__ == "__main__":
#     app = make_app()
#     app.listen(8888)
#     tornado.ioloop.IOLoop.current().start()

# from scrapyd_api import ScrapydAPI
# scrapyd = ScrapydAPI('http://localhost:6800')
# print(scrapyd.list_projects())
#
#
# import urllib.request
#
# response = urllib.request.urlopen('https://www.python.org')
# # print(response.read().decode('utf-8'))
# print(type(response))
# print(response.status)
# print(response.getheaders())
# print(response.getheader('Server'))
#response是一个 HTTPResposne 类型的对象，主要包含 read、readinto、getheader、getheaders、fileno 等方法，
# 以及 msg、version、status、reason、debuglevel、closed 等属性


# import urllib.parse
# import urllib.request
#
# data = bytes(urllib.parse.urlencode({'word1':'hello'}),encoding='utf-8')
# response = urllib.request.urlopen('http://httpbin.org/post',data=data)
# print(response.read())

# import urllib.request
#
# response = urllib.request.urlopen('http://httpbin.org/get',timeout=0.01)
# print(response.read())

# import socket
# import urllib.request
# import urllib.error
#
# try:
#     response = urllib.request.urlopen('http://httpbin.org/get',timeout=0.1)
# except urllib.error.URLError as e:
#     if isinstance(e.reason,socket.timeout):
#         print('TIME OUT')


# import urllib.request
#
# request = urllib.request.Request('https://python.org')
# response = urllib.request.urlopen(request)
# print(response.read().decode('utf-8'))
#
##验证页面
# from urllib.request import HTTPPasswordMgrWithDefaultRealm,HTTPBasicAuthHandler
# from urllib.error import URLError
# from urllib.request import build_opener #书中为导入次项
# username = 'DCadmin'
# password = 'q1w2e3r4'
# url = 'http://10.157.46.124:60014/login.html'
#
# p = HTTPPasswordMgrWithDefaultRealm()
# p.add_password(None,url,username,password)
# auth_handler = HTTPBasicAuthHandler(p)
# opener = build_opener(auth_handler)
#
# try:
#     result = opener.open(url)
#     html = result.read().decode('utf-8')
#     print(html)
# except URLError as e:
#     print('error:'+ str(e.reason))
#

# from urllib import request ,parse
#
# url = 'http://httpbin.org/post'
# headers = {#'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5;Window NT)',
#            'Host':'httpbin.org'
#            }
# dict = {'name':'Germey'}
# data = bytes(parse.urlencode(dict),encoding='utf8')
# req = request.Request(url=url,data=data,headers=headers,method='POST')
# req.add_header('User-Agent','Mozilla/4.0(compatible;MSIE 5.5;Window NT)')
# response = request.urlopen(req)
# print(response.read().decode('utf-8'))
from urllib.request import build_opener
from urllib.request import HTTPPasswordMgrWithDefaultRealm,HTTPBasicAuthHandler
from urllib.error import URLError

# username = 'username'
# password = 'password'
# url = 'http://localhost:5000/'
# p = HTTPPasswordMgrWithDefaultRealm()
# p.add_password(None,url,username,password)
# auth_handler = HTTPBasicAuthHandler(p)
# opener = build_opener(auth_handler)
#
# try:
#     result = opener.open(url)
#     html = result.read().decode('utf-8')
#     print(html)
# except URLError as e:
#     print(e.reason)

# #代理
# from urllib.error import URLError
# from urllib.request import ProxyHandler,build_opener
#
# proxy_handler = ProxyHandler({
#     'http':'http://127.0.0.1:9743',
#     'https':'http://127.0.0.1:9743'
# })
# opener = build_opener(proxy_handler)
# try:
#     response = opener.open("https://www.baidu.com")
#     print(response.read().decode('utf-8'))
# except URLError as e:
#     print(e.reason)

# #Cookies
# import http.cookiejar,urllib.request
#
# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# for item in cookie:
#     print(item.name+"="+item.value)


# #输出保存Cookie文件-Mozilla 型浏览器的 Cookies 格式
# import http.cookiejar,urllib.request
# filename = 'cookie.txt'
# cookie = http.cookiejar.MozillaCookieJar(filename)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# cookie.save(ignore_discard=True,ignore_expires=True)

# #输出保存Cookie文件- LWP 格式的 Cookies文件
# import http.cookiejar,urllib.request
# filename = 'cookie.txt'
# cookie = http.cookiejar.LWPCookieJar(filename)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# cookie.save(ignore_discard=True,ignore_expires=True)

# ##读取并利用生成的Cookie文件
# import http.cookiejar,urllib.request
# cookie = http.cookiejar.LWPCookieJar()
# #调用 load 方法来读取本地的 Cookies 文件，获取到了 Cookies 的内容。
# #前提是我们首先生成了 LWPCookieJar 格式的 Cookies，并保存成文件
# cookie.load('cookie.txt',ignore_expires=True,ignore_discard=True)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# print(response.read().decode('utf-8'))
#

#异常
# from urllib import request,error
# try:
#     response = request.urlopen('https://cuiqingcai.com/index.htm')
# except error.URLError as e:
#     print(e.reason)
#

#HTTPError
from urllib import request,error
# try:
#     response = request.urlopen('https://cuiqingcai.com/index.htm')
# except error.HTTPError as e:
#     print(e.reason,e.code,e.headers,sep='\n')

# try:
#     response = request.urlopen('https://cuiqingcai.com/index.htm')
# except error.HTTPError as e:
#     print(e.reason,e.code,e.headers,sep='\n')
# except error.URLError as e:
#     print(e.reason)
# else:
#     print('Request Successfully')

# #异常reason返回duix
# import socket
# import urllib.request
# import urllib.error
#
# try:
#     response = urllib.request.urlopen('https://www.baidu.com', timeout=0.01)
# except urllib.error.URLError as e:
#     print(type(e.reason))
#     if isinstance(e.reason,socket.timeout):
#         print('Time Out')
#

#解析链接-urlparse
#实现URL的识别和分段
# from urllib.parse import urlparse
#
# result = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
# print(type(result),result)
# print(result.scheme,result[0],result.netloc,result[1])
#

# #解析链接-urlunparse
# from urllib.parse import urlunparse
# data = ['http','www.baidu.com','index.html','user','a=6','#comment']
# print(urlunparse(data))

# #解析链接-urlsplit
# #与urlparse类似，不再单独解析params，只返回5个结果， params 会合并到 path 中
# from urllib.parse import urlsplit
# result = urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
# print(result)
# print('\n',result.scheme,result[0])

# #解析链接-urlunsplit
# from urllib.parse import urlunsplit
# data = ['http', 'www.baidu.com', 'index.html', 'a=6', 'comment']
# print(urlunsplit(data))

# #解析链接-urljoin
# """
#     可以提供一个 base_url（基础链接）作为第一个参数，将新的链接作为第二个参数，
#     该方法会分析 base_url 的 scheme、netloc 和 path 这 3 个内容并对新链接缺失的部分进行补充，
#     最后返回结果
# """
# from urllib.parse import urljoin
#
# print(urljoin('http://baidu.com','FAQ.html'))
# print(urljoin('http://baidu.com','https://cuiqingcai.com/FAQ.html'))
# print(urljoin('http://baidu.com/about.html','https://cuiqingcai.com/FAQ.html'))
# print(urljoin('http://baidu.com/about.html','https://cuiqingcai.com/FAQ.html?question=2'))
# print(urljoin('http://baidu.com?wd=abc','https://cuiqingcai.com/index.php'))
# print(urljoin('http://baidu.com','?category=2#comment'))
# print(urljoin('http://baidu.com#comment','?category=2'))

# #解析链接-urlencode
# from urllib.parse import urlencode
#
# params = {
#     'name' : 'germey',
#     'age' : 22
# }
# base_url = 'http://www.baidu.com?'
# url = base_url + urlencode(params)
#
# print(url)

# #解析链接-parse_qs()
# from urllib.parse import parse_qs
#
# query = 'name=germey&age=22'
# print(parse_qs(query))

#解析链接-parse_qsl()
# from urllib.parse import parse_qsl
#
# query = 'name=germry&age=22'
# print(parse_qsl(query))

# #解析链接-quote()
# #将内容转化为 URL 编码的格式
# from urllib.parse import quote
#
# keyword = '壁纸'
# url = 'http://www.baidu.com?wd='  + quote(keyword)
# print(url)

# #解析链接-unquote()
# #进行 URL 解码
# from urllib.parse import unquote
#
# url = 'http://www.baidu.com?wd=%E5%A3%81%E7%BA%B8'
# print(unquote(url))

# #robotparse
# from urllib.robotparser import RobotFileParser
# from urllib.request import urlopen
# rp = RobotFileParser()
# print(rp.parse(urlopen('http://www.baidu.com/robots.txt').read().decode('utf-8').split('\n')))
#
# rp.set_url('http://www.jianshu.com/robots.txt')
# rp.read()
# print(rp.can_fetch('*','http://www.jianshu.com/p/b67554025d7d'))
# print(rp.can_fetch('*','http://www.jianshu.com/search?q=python&page=1&type=collections'))



#使用requests库

import requests

# r = requests.get('https://www.baidu.com')
# print(type(r))
# print(r.status_code)
# print(type(r.text))
# print(r.text)
# print(r.cookies)
#

# r = requests.post('http://httpbin.org/post')
# print(r.text)

# r = requests.put('http://httpbin.org/put')
# print(r.text)

# r = requests.delete('http://httpbin.org/delete')
# print(r.text)

# r = requests.head('http://httpbin.org/head')
# print(r.text)
#
# r = requests.options('http://httpbin.org/get')
# print(r.text)

# r = requests.get('http://httpbin.org/get')
# print(r.text)

# r = requests.get('http://httpbin.org/get?name=germey&age=23')
# print(r.text)

# data = {
#     'name':'germey',
#     'age': 22
# }
#
# r = requests.get('http://httpbin.org/get',params=data)
#
# print(r.text)

# r = requests.get('http://httpbin.org/get')
# print(type(r.text))
# print(r.json())
# print(type(r.json()))

import re

# headers = {'User-Agent':'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
# r = requests.get('https://www.zhihu.com/explore',headers=headers)
# print(r.text)
# pattern = re.compile('data-za-detail-view-id=".*">(.*?)</a>',re.S)
# titles = re.findall(pattern,r.text)
# print(titles)

import os

# r = requests.get('http://github.com/favicon.ico')
# # print(r.text)
# # print(r.content)
# filedir = os.path.dirname(os.path.realpath(__file__))
# with open(filedir+r'\favicon.ico','wb') as f:
#     f.write(r.content)

# r = requests.get('https://www.zhihu.com/explore')
# print(r.text)
#
# print('修改后\n')
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
#            }
# r1 = requests.get('https://www.zhihu.com/explore',headers=headers)
# print(r1.text)

# data = {'name':'germey','age':22}
# r = requests.post('http://httpbin.org/post',data=data)
# print(r.text)

# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
#                        }
# r = requests.get('http://www.jianshu.com',headers=headers)
# print(type(r.status_code),r.status_code)
# print(type(r.headers),r.headers)
# print(type(r.cookies),r.cookies)
# print(type(r.url),r.url)
# print(type(r.history),r.history)

# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
# r = requests.get('http://www.jianshu.com',headers=headers)
# exit() if not r.status_code == requests.codes.ok else print('Response Seccessfully')
#

# filedir = os.path.dirname(os.path.realpath(__file__))
# files = {'file':open(filedir+r'\favicon.ico','rb')}
# r = requests.post('http://httpbin.org/post',files=files)
# print(r.text)

# r = requests.get('https://www.baidu.com')
# print(r.cookies)
# for key,value in r.cookies.items():
#     print(key+'='+value)
#
# headers = {
#     'Cookie': 'q_c1=31653b264a074fc9a57816d1ea93ed8b|1474273938000|1474273938000; d_c0="AGDAs254kAqPTr6NW1U3XTLFzKhMPQ6H_nc=|1474273938"; __utmv=51854390.100-1|2=registration_date=20130902=1^3=entry_date=20130902=1;a_t="2.0AACAfbwdAAAXAAAAso0QWAAAgH28HQAAAGDAs254kAoXAAAAYQJVTQ4FCVgA360us8BAklzLYNEHUd6kmHtRQX5a6hiZxKCynnycerLQ3gIkoJLOCQ==";z_c0=Mi4wQUFDQWZid2RBQUFBWU1DemJuaVFDaGNBQUFCaEFsVk5EZ1VKV0FEZnJTNnp3RUNTWE10ZzBRZFIzcVNZZTFGQmZn|1474887858|64b4d4234a21de774c42c837fe0b672fdb5763b0',
#     'Host': 'www.zhihu.com',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
# }
# r = requests.get('https://www.zhihu.com', headers=headers)
# print(r.text)
#

# cookies = 'q_c1=31653b264a074fc9a57816d1ea93ed8b|1474273938000|1474273938000; d_c0="AGDAs254kAqPTr6NW1U3XTLFzKhMPQ6H_nc=|1474273938"; __utmv=51854390.100-1|2=registration_date=20130902=1^3=entry_date=20130902=1;a_t="2.0AACAfbwdAAAXAAAAso0QWAAAgH28HQAAAGDAs254kAoXAAAAYQJVTQ4FCVgA360us8BAklzLYNEHUd6kmHtRQX5a6hiZxKCynnycerLQ3gIkoJLOCQ==";z_c0=Mi4wQUFDQWZid2RBQUFBWU1DemJuaVFDaGNBQUFCaEFsVk5EZ1VKV0FEZnJTNnp3RUNTWE10ZzBRZFIzcVNZZTFGQmZn|1474887858|64b4d4234a21de774c42c837fe0b672fdb5763b0'
# jar = requests.cookies.RequestsCookieJar()
# headers = {
#     'Host': 'www.zhihu.com',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
# }
# for cookie in cookies.split(';'):
#     key, value = cookie.split('=', 1)
#     jar.set(key, value)
# r = requests.get('http://www.zhihu.com', cookies=jar, headers=headers)
# print(r.text)


#正则表达式
import re

# #match方法
# content = 'Hello 123 4567 World_This is a Regex Demo'
# print(len(content))
# result = re.match('^Hello\s\d\d\d\s\d{4}\s\w{10}',content)
# print(result)
# print(result.group())
# print(result.span())
#
# #匹配目标
# content = 'Hello 1234567 World_This is a Regex Demo'
# results = re.match('^Hello\s(\d+)\sWorld(\w{4})',content)
# print(results)
# print(results.group())
# print(results.group(1))
# print(results.group(2))
# print(results.span())

# #通用匹配
# content = 'Hello 123 4567 World_This is a Regex Demo'
# results = re.match('^Hello.*Demo$',content)
# print(results)
# print(results.group())
# print(results.span())
#

# #贪婪与非贪婪
# content = 'Hello 1234567 World_This is a Regex Demo'
# results = re.match('^He.*(\d+).*Demo$',content)
# print(results)
# print(results.group(1))
#
# '''
# 贪婪匹配是尽可能匹配多的字符，非贪婪匹配就是尽可能匹配少的字符。
# 当 .? 匹配到 Hello 后面的空白字符时，再往后的字符就是数字了，
# 而 \d + 恰好可以匹配，那么这里 .? 就不再进行匹配，交给 \d+ 去匹配后面的数字。
# 所以这样 .*? 匹配了尽可能少的字符，\d+ 的结果就是 1234567 了
# '''
# results1 = re.match('^He.*?(\d+).*Demo$',content)
# print(results1)
# print (results1.group(1))
#
# #需要注意，如果匹配的结果在字符串结尾，.*? 就有可能匹配不到任何内容了，
# #因为它会匹配尽可能少的字符
# content = 'http://weibo.com/comment/kEraCN'
# results2 = re.match('http.*?comment/(.*?)',content)
# results3 = re.match('http.*?comment/(.*)',content)
# print('results2',results2.group(1))
# print('results3',results3.group(1))

# #修饰符
# #re.S加上后可以匹配节点与节点之间的换行
# content = '''Hello 1234567 World_This
# is a Regex Demo
# '''
# results = re.match('^He.*?(\d+).*Demo$',content)
# #print(results.group(1))
# results1 = re.match('^He.*?(\d+).*Demo$',content,re.S)
# print(results1.group(1))
#

# #转义匹配
# content = '(百度)www.baidu.com'
# results = re.match('\(百度\)www\.baidu\.com',content)
# print(results)
#

# #search
# content = 'Extra stings Hello 1234567 World_This is a Regex Demo Extra stings'
# result = re.match('Hello.*?(\d+).*?Demo', content)
# print(result)
# result1 = re.search('Hello.*?(\d+).*?Demo', content)
# print(result1)

html = '''<div id="songs-list">
<h2 class="title"> 经典老歌 </h2>
<p class="introduction">
经典老歌列表
</p>
<ul id="list" class="list-group">
<li data-view="2"> 一路上有你 </li>
<li data-view="7">
<a href="/2.mp3" singer="任贤齐">沧海一声笑 </a>
</li>
<li data-view="4" class="active">
<a href="/3.mp3" singer="齐秦">往事随风 </a>
</li>
<li data-view="6"><a href="/4.mp3" singer="beyond"> 光辉岁月 </a></li>
<li data-view="5"><a href="/5.mp3" singer="陈慧琳"> 记事本 </a></li>
<li data-view="5">
<a href="/6.mp3" singer="邓丽君"> 但愿人长久 </a>
</li>
</ul>
</div>'''
#
# results = re.search('<li.*?active.*?singer="(.*?)">(.*?)</a>',html,re.S)
# if results:
#     print(results.group(1),results.group(2),sep='')
#
# result1 = re.search('<li.*?singer="(.*?)">(.*?)</a>', html, re.S)
# if result1:
#     print(result1.group(1),result1.group(2),sep ='')
#
# result = re.search('<li.*?singer="(.*?)">(.*?)</a>', html)
# if result:
#     print(result.group(1), result.group(2))


# results = re.findall('<li.*?href="(.*?)".*?singer="(.*?)">(.*?)</a>', html, re.S)
# print(results)
# print(type(results))
# for result in results:
#     print(result)
#     print(result[0], result[1], result[2])
#
#

# #sub
# content = '54aK54yr5oiR54ix5L2g'
# content = re.sub('\d+', '', content)
# print(content)

# html = re.sub('<a.*?>|</a>', '', html)
# print(html)
# results = re.findall('<li.*?>(.*?)</li>', html, re.S)
# for result in results:
#     print(result.strip())


# #compile
# content1 = '2016-12-15 12:00'
# content2 = '2016-12-17 12:55'
# content3 = '2016-12-22 13:21'
# pattern = re.compile('\d{2}:\d{2}')
# result1 = re.sub(pattern, '', content1)
# result2 = re.sub(pattern, '', content2)
# result3 = re.sub(pattern, '', content3)
# print(result1, result2, result3)



from lxml import etree


text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''


# html = etree.parse('test.html',etree.HTMLParser())

# results = html.xpath('//*')
# print(results)
#
# results1 = html.xpath('//li')
# print(results1)
# print(results1[0])

# #//li 用于选中所有 li 节点，/a 用于选中 li 节点的所有直接子节点 a
# results2 = html.xpath('//li/a')
# print(results2)

# #取 ul 节点下的所有子孙 a 节点
# results3 = html.xpath('//ul//a')
# print(results3)

# results4 = html.xpath('//ul/a')
# print(results4)

#选中 href 属性为 link4.html 的 a 节点，然后再获取其父节点，然后再获取其 class 属性
# results4 = html.xpath('//a[@href="link4.html"]/../@class')
# print(results4)
#可以通过 parent:: 来获取父节点
# results5 = html.xpath('//a[@href="link4.html"]/parent::*/@class')
# print(results5)

# #选取 class 为 item-0 的 li 节点
# results6 = html.xpath('//li[@class="item-0"]')
# print(results6)

# # text 方法获取节点中的文本
# results7 = html.xpath('//li[@class="item-0"]/text()')
# print(results7)
#
# result8 = html.xpath('//li[@class="item-0"]/a/text()')
# print(result8)
#
# # html1 = etree.tostring(html)
# # print(html1.decode('utf-8'))
# result9 = html.xpath('//li[@class="item-0"]//text()')
# print(result9)

#获取所有 li 节点下所有 a 节点的 href 属性
# result10 = html.xpath('//li/a/@href')
# print(result10)


# #属性多值匹配
# text = '''
# <li class="li li-first"><a href="link.html">first item</a></li>
# '''
# html = etree.HTML(text)
# results = html.xpath('//li[@class="li"]/a/text()')
# print(results)
#
# results1 = html.xpath('//li[contains(@class,"li")]/a/text()')
# print(results1)



# #多属性匹配
# text = '''
# <li class="li li-first" name="item"><a href="link.html">first item</a></li>
# '''
# html = etree.HTML(text)
# results = html.xpath('//li[contains(@class,"li") and @name="item"]/a/text()')
# print(results)

#按序选择
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
# html = etree.HTML(text)
# results = html.xpath('//li[1]/a/text()')
# print(results)
# results1 = html.xpath('//li[last()]/a/text()')
# print(results1)
# results2 = html.xpath('//li[position()<3]/a/text()')
# print(results2)
# results3 = html.xpath('//li[last()-2]/a/text()')
# print(results3)

#节点轴选择
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html"><span>first item</span></a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
# html = etree.HTML(text)
# #调用了 ancestor 轴,是第一个 li 节点的所有祖先节点，包括 html、body、div 和 ul
# results = html.xpath('//li[1]/ancestor::*')
# print(results)
# #只有 div 这个祖先节点
# results1 = html.xpath('//li[1]/ancestor::*/div')
# print(results1)
# # 调用了 attribute 轴,li 节点的所有属性值
# results2 = html.xpath('//li[1]/attribute::*')
# print(results2)
# #调用了 child 轴
# results3 = html.xpath('//li[1]/child::a[@href="link1.html"]')
# print(results3)
# #调用了 descendant 轴，可以获取所有子孙节点
# results4 = html.xpath('//li[1]/descendant::span')
# print(results4)
# #调用了 following 轴，可以获取当前节点之后的所有节点
# results5 = html.xpath('//li[1]/following::*[2]')
# print(results5)
# #调用了 following-sibling 轴，可以获取当前节点之后的所有同级节点
# results6 = html.xpath('//li[1]/following-sibling::*')
# print(results6)






#BeautifulSoup

from bs4 import BeautifulSoup

# soup = BeautifulSoup('<p>Hello</p>','lxml')
# print(soup.p.string)

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# soup = BeautifulSoup(html,'lxml')
# #prettify() 方法把要解析的字符串以标准的缩进格式输出,
# #，输出结果里面包含 body 和 html 节点
# print(soup.prettify(),'\n\n')
# print(soup.title.string)

#节点选择器
# soup = BeautifulSoup(html,'lxml')
# print(soup.title)
# print(type(soup.title))
# print(soup.title.string)
# print(soup.head)
# print(soup.p)

# #获取名称
# soup = BeautifulSoup(html,'lxml')
# #name 属性获取节点的名称
# print(soup.title.name)
# print(soup.p.name)

# #获取属性
# soup = BeautifulSoup(html,'lxml')
# #调用 attrs 获取所有属性
# print(soup.p.attrs)
# print(soup.p.attrs['name'])
# print(soup.p.attrs['class'])
#
# print(soup.p['name'])
# print(soup.p['class'])

# #获取内容
# soup = BeautifulSoup(html,'lxml')
# print(soup.p.string)

# #嵌套选择
# html = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# """
# soup =  BeautifulSoup(html,'lxml')
# print(soup.head.title)
# print(type(soup.head.title))
# print(soup.head.title.string)


#关联选择
html = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <p class="story">
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">
                <span>Elsie</span>
            </a>
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
            and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            and they lived at the bottom of a well.
        </p>
        <p class="story">...</p>
"""
soup = BeautifulSoup(html,'lxml')
#contents 属性得到的结果是直接子节点的列表
# print(soup.p.contents)
#可以调用 children 属性得到相应的结果
# print(soup.p.children)
# for i,child in enumerate(soup.p.children):
#     print(i,child)

#得到所有的子孙节点
# print(soup.p.descendants)
# for i,child in enumerate(soup.p.descendants):
#     print(i,child)

#获取某个节点元素的父节点
# print(soup.a.parent)

#获取所有的祖先节点
# print(type(soup.a.parents))
# print(list(enumerate(soup.a.parents)))

html = """
<html>
    <body>
        <p class="story">
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">
                <span>Elsie</span>
            </a>
            Hello
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
            and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            and they lived at the bottom of a well.
        </p>
"""

# #获取同级的节点（也就是兄弟节点）
# soup = BeautifulSoup(html,'lxml')
# print('Next Sibling',soup.a.next_sibling)
# print('Prev Sibling', soup.a.previous_sibling)
# print('Next Siblings', list(enumerate(soup.a.next_siblings)))
# print('Prev Siblings', list(enumerate(soup.a.previous_siblings)))
#


#提取信息

html = """
<html>
    <body>
        <p class="story">
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">Bob</a><a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
        </p>
"""
# soup = BeautifulSoup(html,'lxml')
# print('Next Sibling:')
# print(type(soup.a.next_sibling))
# print(soup.a.next_sibling)
# print(soup.a.next_sibling.string)
# print('Parent:')
# print(type(soup.a.parents))
# print(list(soup.a.parents)[0])
# print(list(soup.a.parents)[0].attrs['class'])



#find_all
#查询所有符合条件的元素，可以给它传入一些属性或文本来得到符合条件的元素
#find_all(name , attrs , recursive , text , **kwargs)
html='''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''
# soup = BeautifulSoup(html,'lxml')
# # print(soup.find_all(name='ul'))
# # print(type(soup.find_all(name='ul')[0]))
#
# for ul in soup.find_all(name='ul'):
#     print(ul.find_all(name='li'))
#     for li in ul.find_all(name='li'):
#         print(li.string)



#attrs
#传入一些属性来进行查询
html='''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1" name="elements">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''
# soup = BeautifulSoup(html,'lxml')
# # print(soup.find_all(attrs={'id':'list-1'}))
# # print(soup.find_all(attrs={'name':'elements'}))
#
# #于一些常用的属性，比如 id 和 class 等，我们可以不用 attrs 来传递
# print(soup.find_all(id='list-1'))
# print(soup.find_all(class_='element'))
#


#text
#text 参数可用来匹配节点的文本，传入的形式可以是字符串，可以是正则表达式对象

import re
html='''
<div class="panel">
    <div class="panel-body">
        <a>Hello, this is a link</a>
        <a>Hello, this is a link, too</a>
    </div>
</div>
'''
# soup = BeautifulSoup(html,'lxml')
# print(soup.find_all(text=re.compile('link')))
#

#find
#返回的是单个元素，也就是第一个匹配的元素
html='''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''
# soup = BeautifulSoup(html,'lxml')
# print(type(soup.find(name='ul')))
# print(soup.find(name='ul'))
# print(soup.find(class_='list'))

#find_parents 和 find_parent：前者返回所有祖先节点，后者返回直接父节点。

#find_next_siblings 和 find_next_sibling：前者返回后面所有的兄弟节点，
# 后者返回后面第一个兄弟节点。

#find_previous_siblings 和 find_previous_sibling：前者返回前面所有的兄弟节点，
# 后者返回前面第一个兄弟节点。

#find_all_next 和 find_next：前者返回节点后所有符合条件的节点，
# 后者返回第一个符合条件的节点。

#find_all_previous 和 find_previous：前者返回节点前所有符合条件的节点，
# 后者返回第一个符合条件的节点。



#CSS 选择器

html = '''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''

# soup = BeautifulSoup(html,'lxml')
# print(soup.select('.panel .panel-heading'))
# print(soup.select('ul li'))
# print(soup.select('#list-2 .element'))
# print(type(soup.select('ul')[0]))

#select 方法同样支持嵌套选择，例如我们先选择所有 ul 节点，再遍历每个 ul 节点选择其 li 节点

soup = BeautifulSoup(html,'lxml')
# for ul in soup.select('ul'):
#     # print(ul.select('li'))
#     print(ul['id'])
#     print(ul.attrs['id'])
#
#
# for li in soup.select('li'):
#     print('Get text',li.get_text())
#     print('String',li.string)
#

print( 'a' in 'a')

aa = '这是A对test.py进行的修改'





