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

username = 'username'
password = 'password'
url = 'http://localhost:5000/'

p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None,url,username,password)
auth_handler = HTTPBasicAuthHandler(p)
opener = build_opener(auth_handler)

try:
    result = opener.open(url)
    html = result.read().decode('utf-8')
    print(html)
except URLError as e:
    print(e.reason)





















