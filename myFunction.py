import os
import json
import time
import requests
import getIP
import cmdprintcolor
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from collections import OrderedDict

curDir = os.getcwd() #获取当前目录路径
TodayDate = str(datetime.date.today())   #获取当前日期

#检查service文件夹是否存在，不存在则创建
def createServiceDir(service,env='stage'):
    serviceFileDir = os.path.join(curDir,TodayDate,env,'ServicesAPI') #API数据文件目录
    compareServiceFileDir = os.path.join(curDir,TodayDate,env,'CompareResults') #对比结果文件目录
    #判断目录是否已存在
    isExist_data = os.path.exists(serviceFileDir)
    #不存在则创建
    if not isExist_data:
        os.makedirs(serviceFileDir)
    isExist_compare = os.path.exists(compareServiceFileDir)
    if not isExist_compare:
        os.makedirs(compareServiceFileDir)
    return serviceFileDir,compareServiceFileDir

#获取service对应的Html路径
def getSwaggerUrl(service,env='stage'):
    ip = getIP.getIP(service=service,env=env)
    url = ip + '/swagger-ui.html'
    return url

#从swagger页面获取API数据
def getApiList(service,env='stage'):
    #获取service对应的Html路径
    url = getSwaggerUrl(service,env)
    #设置FireFox驱动器路径
    DriverFlieDir = os.path.join(curDir,'geckodriver')
    #设置浏览器
    option = webdriver.firefox.options.Options()
    option.add_argument('-headless')#无头模式，后台打开浏览器
    browser = webdriver.Firefox(executable_path=DriverFlieDir,firefox_options=option)
    browser.get(url)
    wait = WebDriverWait(browser,10)
    wait.until(EC.presence_of_element_located((By.ID,'resources')))
    data = browser.page_source
    datahtml = BeautifulSoup(data,'lxml')
    ApiHtmlList = datahtml.select("ul > li > ul > li > ul > li .heading") #Api元素列表
    ApiList = []
    for ApiHtml in ApiHtmlList:
        Api = OrderedDict()
        Api_type = ApiHtml.h3.span.a.string
        Api_path = ApiHtml.find(class_='path').a.string
        Api_Note = ApiHtml.ul.li.a.span.p.string
        Api['Type'] = Api_type
        Api['Path'] = Api_path
        Api['Description'] = Api_Note
        ApiList.append(Api)
    browser.close()
    return ApiList

#保存最新的Swagger接口信息
def saveAPIJosn(path,name,data):
    filepath = os.path.join(path,name+'.json')
    with open(filepath,'w',encoding='utf8') as file:
        json.dump(data,file,ensure_ascii=False,indent=4)
    return filepath

#对比两个接口列表获取新增数和删除数
def getAddAndDeleteCount(prdAPIList,envAPIList):
    addCount = 0 #新增接口数
    deleteCount = 0 #删除接口数
    addList = []
    deleteList = []
    envLen = len(envAPIList)
    prdLen = len(prdAPIList)
    for oldapi in prdAPIList:
    #删除接口
        if oldapi not in envAPIList:
            deleteList.append(oldapi)
            deleteCount += 1
    for newapi in envAPIList:
        if newapi not in prdAPIList:
            addList.append(newapi)
            addCount += 1
    return prdLen,envLen,addCount,addList,deleteCount,deleteList


#显示对比结果
def showCompareResults(service,prdLen,envLen,addCount,addList,deleteCount,deleteList):
    compare = OrderedDict()
    compare['服务'] = service
    compare['当前环境接口总数'] = envLen
    compare['生产环境接口总数'] = prdLen
    compare['新增接口数'] = addCount
    compare['删除接口数'] = deleteCount
    compare['新增接口详情'] = addList
    compare['删除接口详情'] = deleteList
    compareresult = {service:compare}
    print('服务：'+service.upper()+'\n')
    print('\t当前环境接口总数：'+str(envLen))
    print('\t生产环境接口总数：'+str(prdLen))
    print('\t新增接口数：',end='')
    lightoutprint(addCount)
    print('\t删除接口数：',end='')
    lightoutprint(deleteCount)
    print('\t新增接口详情：')
    if addCount:
        for i in addList:
            print('\t\t',end='')
            for key,value in i.items():
                print(key + ':' + value +'\t',end='')
            print('\n')
    else:
        print('\t\t无')
    print('\n\t删除接口详情：')
    if deleteCount:
        for i in deleteList:
            print('\t\t',end='')
            for key,value in i.items():
                print(key + ':' + value +'\t',end='')
            print('\n')
    else:
        print('\t\t无')
    print('\n\n')
    return compare

def saveAllcompareresult(compareFileDir,compare,isNew=False):
    compareFilePath = os.path.join(compareFileDir,'AllServicesCompare','.josn')
    #保存对比文件
    if isNew:
        with open(compareFilePath,'w',encoding='utf8') as file:
            json.dump(compare,file,ensure_ascii=False,indent=4)
    else:
        with open(compareFilePath,'a',encoding='utf8') as file:
            json.dump(compare,file,ensure_ascii=False,indent=4)
    return compareFilePath

#判断是否高亮输出
def lightoutprint(count,highlight=0):
    if highlight != 0 or count > 0:
        cmdprintcolor.printYellowRed(str(count)+'\n')
        cmdprintcolor.resetColor()
    else:
        print(count)



