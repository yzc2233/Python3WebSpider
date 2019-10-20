import requests
from get_station import *

data = []  #保存整理好的车次信息
type_data = []  #保存分类后车次信息

def query(data,form_station,to_station):
    data.clear() #清空数据
    type_data.clear() #清空车次分类保存的数据

    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(data,form_station,to_station)
    response = requests.get(url)
    result = response.json()
    result = result['data']['result']

    if isStation():
        stations = eval(read()) #读取所有车站并转换为dic类型
        if len(result) != 0:
            for i in result:
                tmp_list = i.split('|')
                from_station = list(stations.keys())[list(stations.values()).index(tmp_list[6])]
                to_station = list(stations.keys())[list(stations.values()).index(tmp_list[6])]
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

def g_vehicle():
    if len(data) != 0:
        for g in data:
            i = g[0].startwith('G') #判断首字母是不是G
            if i:
                type_data.append(g)

#移除高铁信息
def r_g_vehicle():
    if len(data) != 0:
        for g in data:
            i = g[0].startwith('G') #判断首字母是不是G
            if i:
                type_data.remove(g)

def d_vehicle():
    if len(data) != 0:
        for d in data:
            i = d[0].startwith('D') #判断首字母是不是G
            if i:
                type_data.append(d)


def r_d_vehicle():
    if len(data) != 0:
        for d in data:
            i = d[0].startwith('D') #判断首字母是不是G
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





