import os
import json



import MyFunction as f

serviceList = ['WECHATCENTER-SERVICE']
service = serviceList[0]

#检查service文件夹是否存在，不存在则创建
APIJson_Dir,APICompare_Dir,service_isExist = f.createServiceDir(service)

##拉取最新的Swagger接口信息并保存
if service_isExist:
    APIJson = f.getAPIJosn(service)
    f.saveAPIJosn(APIJson_Dir,APIJson)
else:
    APIJson1 = f.getAPIJosn(service)
    f.saveAPIJosn(APIJson_Dir,APIJson1)
    APIJson2 = f.getAPIJosn(service)
    f.saveAPIJosn(APIJson_Dir,APIJson2)

#获取当前service最新的Json文件和上一文件
oldFilePath,newFilePath = f.getOldAndNewFilePath(APIJson_Dir)
with open(oldFilePath,'r',encoding='utf8') as file:
    oldFileData = json.load(file)
with open(newFilePath,'r',encoding='utf8') as file:
    newFileData = json.load(file)


#获取旧文件接口路径
oldAPIList = f.getAPIList(oldFileData)

#获取新文件接口路径
newAPIList = f.getAPIList(newFileData)

oldapiCount = len(oldAPIList)
newapiCount = len(newAPIList)

modifyCount = 0 #修改接口数
modifyContent = {"(1)路径":"","(2)上一版本入参":"","(3)当前版本入参":""}
modifyList = []

#获取接口新增和删除信息
addCount,addList,deleteCount,deleteList = f.getAddAndDeleteCount(oldAPIList,newAPIList)
difresults = {"新增接口详情":addList,"删除接口详情":deleteList,"编辑接口详情":modifyList}

#获取接口编辑信息
difFilename = os.path.basename(oldFilePath)[:-5]+'compare'+os.path.basename(newFilePath)[:-5]+'.json'
difFilepath = os.path.join(APICompare_Dir,difFilename)

for api in newAPIList:
    if api in oldAPIList:
        oldapiparameters = oldFileData['paths'][api[1]][api[0].lower()]['parameters']
        newapiparameters = newFileData['paths'][api[1]][api[0].lower()]['parameters']
        if oldapiparameters == newapiparameters:
            pass
        else:
            modifyContent['(1)路径'] = api[0] + api[1]
            modifyContent['(2)上一版本入参'] = oldapiparameters
            modifyContent['(3)当前版本入参'] = newapiparameters
            modifyList.append(modifyContent)
            modifyCount += 1

checkresult = {"1、上一版本接口个数":oldapiCount,"2、当前接口个数":newapiCount,
               "3、新增接口数":addCount,"4、删除接口数":deleteCount,"5、修改接口数":modifyCount,
               "6、检查结果":difresults}

#保存对比文件
with open(difFilepath,'w',encoding='utf8') as file:
    json.dump(checkresult,file,ensure_ascii=False,indent=4,sort_keys=True)

#显示对比结果
print("""
对比结果保存路径：%s
1、上一版本接口个数：%s
2、当前接口个数：%s
3、新增接口数：%s
4、删除接口数：%s
5、修改接口数：%s
6、检查结果：
""" %(difFilepath,oldapiCount,newapiCount,addCount,deleteCount,modifyCount),end='')
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
        print('\t\t\t(2)上一版本入参：',i['(2)上一版本入参'])
        print('\t\t\t(3)当前版本入参：',i['(3)当前版本入参'],'\n')
        seq += 1
else:
    print('\t\t无')