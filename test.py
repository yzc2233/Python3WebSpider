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

#解析链接-urlunsplit
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

#robotparse
from urllib.robotparser import RobotFileParser
from urllib.request import urlopen
rp = RobotFileParser()
print(rp.parse(urlopen('http://www.baidu.com/robots.txt').read().decode('utf-8').split('\n')))

rp.set_url('http://www.jianshu.com/robots.txt')
rp.read()
print(rp.can_fetch('*','http://www.jianshu.com/p/b67554025d7d'))
print(rp.can_fetch('*','http://www.jianshu.com/search?q=python&page=1&type=collections'))



