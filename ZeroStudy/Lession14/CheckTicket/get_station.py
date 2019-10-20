import requests
import re
import os

def getStation():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9114'
    response = requests.get(url,verify=True) #请求并验证

    #获取所需要的车站名称
    stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)',response.text)
    stations = dict(stations)
    stations = str(stations)
    write(stations)

def write(stations):
    with open('station.text','w',encoding='utf8') as file:
        file.write(stations)

def read():
    with open('station.text','r',encoding='utf8') as file:
        data = file.readline()
        return data

def isStations():
    isStations = os.path.exists('station.text')
    return isStations



