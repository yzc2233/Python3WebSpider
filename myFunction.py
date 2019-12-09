import os
import json
import requests
import getIP
import cmdprintcolor
import datetime
import sys
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
from collections import OrderedDict

curDir = os.getcwd() #获取当前目录路径
TodayDate = str(datetime.date.today())   #获取当前日期

#检查service文件夹是否存在，不存在则创建
def createServiceDir(env='stage'):
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

# #从swagger页面获取API数据-太慢
# def getApiList(service,env='stage'):
#     #获取service对应的Html路径
#     url = getSwaggerUrl(service,env)
#     #设置FireFox驱动器路径
#     DriverFlieDir = os.path.join(curDir,'geckodriver')
#     #设置浏览器
#     option = webdriver.firefox.options.Options()
#     option.add_argument('-headless')#无头模式，后台打开浏览器
#     browser = webdriver.Firefox(executable_path=DriverFlieDir,firefox_options=option)
#     browser.get(url)
#     wait = WebDriverWait(browser,10)
#     wait.until(EC.presence_of_element_located((By.ID,'resources')))
#     data = browser.page_source
#     datahtml = BeautifulSoup(data,'lxml')
#     ApiHtmlList = datahtml.select("ul > li > ul > li > ul > li .heading") #Api元素列表
#     ApiList = []
#     for ApiHtml in ApiHtmlList:
#         Api = OrderedDict()
#         Api_type = ApiHtml.h3.span.a.string
#         Api_path = ApiHtml.find(class_='path').a.string
#         Api_Note = ApiHtml.ul.li.a.span.p.string
#         Api['Type'] = Api_type
#         Api['Path'] = Api_path
#         Api['Description'] = Api_Note
#         ApiList.append(Api)
#     browser.close()
#     return ApiList

#从swagger API接口获取API数据
def getAPI(service,env='stage'):
    typeList = ['GET','POST','PUT','DELETE']
    ApiList = []
    service_ip = getIP.getIP(service=service,env=env)
    url = service_ip+'/v2/api-docs'
    res = requests.get(url)
    res_json = json.loads(res.text)
    pathList = res_json['paths']
    for path in pathList.keys():

        for type in pathList[path].keys():
            Api = OrderedDict()
            Api_path = path
            Api_type = type.upper()
            Api_control = pathList[path][type]['tags'][0]
            Api_Note = pathList[path][type]['summary']
            Api['Control'] = Api_control
            Api['Type'] = Api_type
            Api['Path'] = Api_path
            Api['Description'] = Api_Note
            if Api_type in typeList:
                ApiList.append(Api)
    return ApiList

#保存最新的Swagger接口信息
def saveAPIJosn(path,name,data,type='.json'):
    filepath = os.path.join(path,name+type)
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

#判断是否高亮输出
def lightoutprint(count,highlight=0):
    if highlight != 0 or count > 0:
        cmdprintcolor.printYellowRed(str(count)+'\n')
        cmdprintcolor.resetColor()
        # print('\033[31m %s \033[0m' %count)
    else:
        print(count)

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

#创建所有Services对比结果汇总Html文件

def allServicesResultHtml(AllCompareData):
    satrtHtmlText = """<DOCTYPE HTML>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>所选Services对比结果汇总</title>
    </head>
    <body>
    <h1>所选Services对比结果汇总</h1>
    """
    bodyHtmlText = """"""
    for compareData in AllCompareData:
        bodyHtmlText += """<table border="1">
        <tr>
            <td><b>服务</b></td>
            <td><b>"""+compareData['服务']+"""</b></td>
        </tr>
        <tr>
            <td><b>当前环境接口总数</b></td>
            <td>"""+str(compareData['当前环境接口总数'])+"""</td>
        </tr>
        <tr>
            <td><b>生产环境接口总数</b></td>
            <td>"""+str(compareData['生产环境接口总数'])+"""</td>
        </tr>
        <tr>
            <td><b>新增接口数</b></td>"""
        if compareData['新增接口数']:
            bodyHtmlText += """<td style="color: red">"""+str(compareData['新增接口数'])+"""</td>"""
        else:
            bodyHtmlText += """<td>"""+str(compareData['新增接口数'])+"""</td>"""
        bodyHtmlText += """
        </tr>
        <tr>
            <td><b>删除接口数</b></td>"""
        if compareData['删除接口数']:
            bodyHtmlText += """<td style="color: red">"""+str(compareData['删除接口数'])+"""</td>"""
        else:
            bodyHtmlText += """<td>"""+str(compareData['删除接口数'])+"""</td>"""
        bodyHtmlText += """
        </tr>
        <tr>
            <td><b>新增接口详情</b></td>
            <td>
                <table border="1">"""
        if compareData['新增接口详情']:
            for add in compareData['新增接口详情']:
                bodyHtmlText += """
                    <tr>
                        <td><b>Control:</b>
                        """+add['Control']+"""
                        <b>Type:</b>
                        """+add['Type']+"""
                        <b>Path:</b>
                        """+add['Path']+"""
                        <b>Description:</b>
                        """+add['Description']+"""</td>
                    </tr>"""
        else:
            bodyHtmlText += """
                        无"""
        bodyHtmlText += """           
                </table>
            </td>
        </tr>
        <tr>
            <td border="1"><b>删除接口详情</b></td>
            <td>"""
        if compareData['删除接口详情']:
            for add in compareData['删除接口详情']:
                bodyHtmlText += """
                <table border="1">
                    <tr>
                        <td><b>Control:</b>
                        """+add['Control']+"""
                        <b>Type:</b>
                        """+add['Type']+"""
                        <b>Path:</b>
                        """+add['Path']+"""
                        <b>Description:</b>
                        """+add['Description']+"""</td>
                    </tr>"""
        else:
            bodyHtmlText += """
                        无"""
        bodyHtmlText += """
                </table>
            </td>
        </tr>
    </table>
    </br>
    </br>"""
    endHtmlText = """
    </body>
    </html>"""
    ResultHtml = satrtHtmlText+bodyHtmlText+endHtmlText
    return ResultHtml

#保存对比汇总Html文件
def saveHtml(path,name,data):
    filepath = os.path.join(path,name+'.html')
    with open(filepath,'w',encoding='utf8') as file:
        file.write(data)
    return filepath

#处理输入数据
def gerInputArgus(serviceList):
    envList = ['qa2','stage']
    if len(sys.argv) == 1:
        while True:
            inputdata = input('请输入正确的对比环境与service序号：')
            inputdata = inputdata.split(' ')
            if inputdata[0] not in envList:
                print('输入的环境有误，应该为qa2或者stage')
            elif len(inputdata) == 2:
                break
        env = inputdata[0]
        inservices = inputdata[1]
    else:
        env = sys.argv[1]
        inservices = sys.argv[2]
    inservicesList = inservices.split(',')
    realservicelist = []
    if '0' in inservicesList:
        realservicelist = serviceList[1:]
    else:
        for i in inservicesList:
            realservicelist.append(serviceList[int(i)])
    print(env,realservicelist)
    return env,realservicelist
