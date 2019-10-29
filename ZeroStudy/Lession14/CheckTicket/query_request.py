import requests
from get_station import *
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

data = []  #保存整理好的车次信息
type_data = []  #保存分类后车次信息

def query(date,form_station,to_station):
    data.clear() #清空数据
    type_data.clear() #清空车次分类保存的数据
    headers = {'If-Modified-Since':'0','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.17 Safari/537.36',
               'X-Requested-With':'XMLHttpRequest','Cookie':'JSESSIONID=537D8878010B0E64F0518BB688798503; BIGipServerotn=837812746.24610.0000; BIGipServerpool_passport=250413578.50215.0000; RAIL_EXPIRATION=1572551466304; RAIL_DEVICEID=C3aUTdBb5by5Pzjau7aeNNdaZo4FJUs_wARhs4wPuihY24NKMn_E8qRYnC8lj2_il6okSYH7Yu-wAKkJAbU38oudE-awkJ49agPipIJmu5rMu2pEQIPqtrcjiroqUowyUhhYH-7qLF_GrIX2CHnm10EY1xrVnd4j; route=495c805987d0f5c8c84b14f60212447d; _jc_save_fromStation=%u4E0A%u6D77%2CSHH; _jc_save_toStation=%u5317%u4EAC%2CBJP; _jc_save_fromDate=2019-10-28; _jc_save_toDate=2019-10-28; _jc_save_wfdc_flag=dc'}

    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,form_station,to_station)

    response = requests.get(url,headers=headers)
    result = response.json()
    result = result['data']['result']

    if isStations() == True:
        stations = eval(read()) #读取所有车站并转换为dic类型
        if len(result) != 0:
            for i in result:
                tmp_list = i.split('|')
                from_station = list(stations.keys())[list(stations.values()).index(tmp_list[6])]
                to_station = list(stations.keys())[list(stations.values()).index(tmp_list[7])]
                seat = [
                    tmp_list[3],from_station,to_station,tmp_list[8],tmp_list[9],tmp_list[10],
                    tmp_list[32],tmp_list[31],tmp_list[30],tmp_list[21],tmp_list[23],tmp_list[33],
                    tmp_list[28],tmp_list[24],tmp_list[29],tmp_list[26]
                ]
                newseat = []
                for s in seat:
                    if s == '':
                        s = '--'
                    else:
                        s = s
                    newseat.append(s)
                data.append(newseat)
    return data

#获取高铁信息
def g_vehicle():
    if len(data) != 0:
        for g in data:
            i = g[0].startswith('G') #判断首字母是不是G
            if i:
                type_data.append(g)

#移除高铁信息
def r_g_vehicle():
    if len(data) != 0:
        for g in data:
            i = g[0].startswith('G') #判断首字母是不是G
            if i:
                type_data.remove(g)

#获取动车信息
def d_vehicle():
    if len(data) != 0:
        for d in data:
            i = d[0].startswith('D') #判断首字母是不是G
            if i:
                type_data.append(d)

#动车信息移除
def r_d_vehicle():
    if len(data) != 0:
        for d in data:
            i = d[0].startswith('D') #判断首字母是不是G
            if i:
                type_data.remove(d)


# 获取直达车信息的方法
def z_vehicle():
    if len(data) != 0:
        for z in data:  # 循环所有火车数据
            i = z[0].startswith('Z')  # 判断车次首字母是不是直达
            if i == True:  # 如果是将该条信息添加到直达数据中
                type_data.append(z)


# 移除直达车信息的方法
def r_z_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for z in data:
            i = z[0].startswith('Z')
            if i == True:  # 移除直达车信息
                type_data.remove(z)


# 获取特快车信息的方法
def t_vehicle():
    if len(data) != 0:
        for t in data:  # 循环所有火车数据
            i = t[0].startswith('T')  # 判断车次首字母是不是特快
            if i == True:  # 如果是将该条信息添加到特快车数据中
                type_data.append(t)


# 移除特快车信息的方法
def r_t_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for t in data:
            i = t[0].startswith('T')
            if i == True:  # 移除特快车信息
                type_data.remove(t)


# 获取快速车数据的方法
def k_vehicle():
    if len(data) != 0:
        for k in data:  # 循环所有火车数据
            i = k[0].startswith('K')  # 判断车次首字母是不是快车
            if i == True:  # 如果是将该条信息添加到快车数据中
                type_data.append(k)


# 移除快速车数据的方法
def r_k_vehicle():
    if len(data) != 0 and len(type_data) != 0:
        for k in data:
            i = k[0].startswith('K')
            if i == True:  # 移除快车信息
                type_data.remove(k)





