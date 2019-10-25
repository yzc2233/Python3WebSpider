import os
import json
import time
import requests
import getIP
import cmdprintcolor

#检查service文件夹是否存在，不存在则创建
def createServiceDir(service):
    curDir = os.getcwd()
    servicepath = os.path.join(curDir,'Services',service)
    isExist = os.path.exists(servicepath)
    service_APIJson_Dir = os.path.join(servicepath,'APIJSON')
    service_APICompare_Dir = os.path.join(servicepath,'APICompare')
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
    if len(os.listdir(path)) == 1:
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


def getoldAndNewFiledata(oldFilePath,newFilePath):
    with open(oldFilePath,'r',encoding='utf8') as file:
        oldFileData = json.load(file)
    with open(newFilePath,'r',encoding='utf8') as file:
        newFileData = json.load(file)
    return oldFileData,newFileData

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

#字典对比
def compareDic(dic_old,dic2_new):
    """对比两个字典的区别，以dic_old为主体进行对比，dic2_new新增key、删除key、value变更"""
    # dic_old = dict(dic_old)
    # dic2_new = dict(dic2_new)
    dict1 = {'a':2,'b':2,'c':3,'d':4}
    dict2 = {'a':1,'b':2,'c':5,'e':6,'g':4}
    #新增的key
    addDictList = []
    addkey = list(dict2.keys()-dict1.keys())
    for key in addkey:
        addDict = {key:dict2[key]}
        addDictList.append(addDict)
    print(addDictList)
    #删除的key
    delDictList = []
    delkey = list(dict1.keys()-dict2.keys())
    for key in delkey:
        delDict = {key:dict1[key]}
        delDictList.append(delDict)
    # 字典值不同
    allkey = dict1.keys() & dict2.keys()
    modifyDictList = [({'Key':k, '原值':dict1[k], '当前值':dict2[k]}) for k in allkey if dict1[k] != dict2[k]]
    diffResult = {'新增key列表':addDictList,'删除key列表':delDictList,'编辑key列表':modifyDictList}
    return diffResult

#对比接口入参列表
def compareParametersList(list_old,list_new):
    list_old =  list(list_old)
    list_new = list(list_new)
    oldParameter = []
    for i in list_old:
        x = {i['in']:i['name']}
        oldParameter.append(x)
    print(oldParameter)
    newParameter = []
    for i in list_new:
        x = {i['in']:i['name']}
        newParameter.append(x)
    print(newParameter)
    addParameList = list(x for x in newParameter if x not in oldParameter)
    delParameList = list(x for x in oldParameter if x not in newParameter)
    difflist = {'新增参数':addParameList,'删除参数':delParameList}
    return difflist

#获取接口编辑对比结果
def getmodifyresult(oldAPIList,newAPIList,oldFileData,newFileData):
    modifyCount = 0 #修改接口数
    modifyContent = {"(1)路径":"","(2)上一版本入参":"","(3)当前版本入参":""}
    modifyList = []
    #获取接口编辑信息
    for api in newAPIList:
        if api in oldAPIList:
            if 'parameters' in oldFileData['paths'][api[1]][api[0].lower()].keys():
                oldapiparameters = oldFileData['paths'][api[1]][api[0].lower()]['parameters']
                newapiparameters = newFileData['paths'][api[1]][api[0].lower()]['parameters']
                if oldapiparameters == newapiparameters:
                    pass
                else:
                    print('修改后')
                    for apiparameter in oldapiparameters:
                        pass



                    # modifyContent['(1)路径'] = api[0] + api[1]
                    # modifyContent['(2)上一版本入参'] = oldapiparameters
                    # modifyContent['(3)当前版本入参'] = newapiparameters
                    # modifyList.append(modifyContent)
                    # modifyCount += 1
    return modifyCount,modifyList

def savecompareresult(oldFilePath,newFilePath,APICompare_Dir,checkresult):
    difFilename = os.path.basename(oldFilePath)[:-5]+'compare'+os.path.basename(newFilePath)[:-5]+'.json'
    difFilepath = os.path.join(APICompare_Dir,difFilename)
    #保存对比文件
    with open(difFilepath,'w',encoding='utf8') as file:
        json.dump(checkresult,file,ensure_ascii=False,indent=4,sort_keys=True)
    return difFilepath

#判断是否高亮输出
def lightoutprint(count,highlight=0):
    if highlight != 0 or count > 0:
        cmdprintcolor.printYellowRed(str(count)+'\n')
        cmdprintcolor.resetColor()
        # print("\033[1;31;40m%s\033[0m" %count)
    else:
        print(count)

#显示对比结果
def showCompareResults(difFilepath,checkresult):
    addcount = checkresult['3、新增接口数']
    deltecount = checkresult['4、删除接口数']
    modifycount = checkresult['5、修改接口数']
    print("""对比结果保存路径：%s
1、上一版本接口个数：%s
2、当前接口个数：%s
""" %(difFilepath,checkresult['1、上一版本接口个数'],checkresult['2、当前接口个数']),end='')
    print("3、新增接口数：",end='')
    lightoutprint(addcount)
    print('4、删除接口数：',end='')
    lightoutprint(deltecount)
    print('5、修改接口数：',end='')
    lightoutprint(modifycount)
    print("6、检查结果：")
    print('\t新增接口详情：')
    if len(checkresult['6、检查结果']['新增接口详情']):
        for i in checkresult['6、检查结果']['新增接口详情']:
            print('\t\t',i[0],'\t',i[1])
    else:
        print('\t\t无')
    print('\n\t删除接口详情：')
    if len(checkresult['6、检查结果']['删除接口详情']):
        for i in checkresult['6、检查结果']['删除接口详情']:
            print('\t\t',i[0],'\t',i[1])
    else:
        print('\t\t无')
    print('\n\t编辑接口详情：')
    if len(checkresult['6、检查结果']['编辑接口详情']):
        seq = 1
        for i in checkresult['6、检查结果']['编辑接口详情']:
            print('\t\t编辑接口：',seq)
            print('\t\t\t(1)路径：',i['(1)路径'])
            print('\t\t\t(2)上一版本入参：',i['(2)上一版本入参'],'\n')
            print('\t\t\t(3)当前版本入参：',i['(3)当前版本入参'],'\n\n')
            seq += 1
    else:
        print('\t\t无')
    print('\n\n')



