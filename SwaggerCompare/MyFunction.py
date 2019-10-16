import os
import json
import time
import requests
import getIP

#检查service文件夹是否存在，不存在则创建
def createServiceDir(service):
    isExist = os.path.exists(service)
    curDir = os.getcwd()
    service_APIJson_Dir = os.path.join(curDir,service,'APIJSON')
    service_APICompare_Dir = os.path.join(curDir,service,'APICompare')
    if not isExist:
        os.makedirs(service_APIJson_Dir)
        print(service_APIJson_Dir,'创建成功')
        os.makedirs(service_APICompare_Dir)
        print(service_APICompare_Dir,'创建成功')
    return service_APIJson_Dir,service_APICompare_Dir,isExist

#拉取最新的Swagger接口信息
def getAPIJosn(service):
    service_ip = getIP.getIP(service=service)
    service_swaggerUrl = service_ip+'/v2/api-docs'
    res = requests.get(service_swaggerUrl)
    res_json = json.loads(res.text)
    return res_json

#保存最新的Swagger接口信息
def saveAPIJosn(path,data):
    filetime = time.strftime('%Y%m%d',time.localtime())
    filename = filetime+'.json'
    filepath = os.path.join(path,filename)
    try:
        with open(filepath,'w',encoding='utf8') as file:
            json.dump(data,file,ensure_ascii=False,indent=4,sort_keys=True)
    except FileExistsError:
        filename = filetime+'_new'+'.json'
        filepath = os.path.join(path,filename)
        with open(filepath,'w',encoding='utf8') as file:
            json.dump(data,file,ensure_ascii=False,indent=4,sort_keys=True)
    return filepath

#获取最近两个Swagger接口信息文件路径
def getOldAndNewFilePath(path):
    DirFileList = os.listdir(path)
    oldFileName = DirFileList[-2]
    oldFilePath = os.path.join(path,oldFileName)
    newFileName = DirFileList[-1]
    newFilePath = os.path.join(path,newFileName)
    return oldFilePath,newFilePath

#获取接口Json文件中的接口路径
def getAPIList(data):
    APIList = []
    paths = list(data['paths'].keys())
    for path in paths:
        apitypelist = list(data['paths'][path].keys())
        for apitype in apitypelist:
            api = (apitype.upper(),path)
            APIList.append(api)
    return APIList

#对比两个接口列表获取新增数和删除数
def getAddAndDeleteCount(oldAPIList,newAPIList):
    addCount = 0 #新增接口数
    deleteCount = 0 #删除接口数
    addList = []
    deleteList = []
    for oldapi in oldAPIList:
    #删除接口
        if oldapi not in newAPIList:
            deleteList.append(oldapi)
            deleteCount += 1
    for newapi in newAPIList:
        if newapi not in oldAPIList:
            addList.append(newapi)
            addCount += 1
    return addCount,addList,deleteCount,deleteList