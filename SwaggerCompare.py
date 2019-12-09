import os

import sys
from myFunction import *
from Config import *

print('命令示例：python SwaggerCompare.py stage 1,2,3')
print('示例中的stage是与生产环境对比的环境，1,2,3是services序号，以下为各service序号(0代表以下所有services)')
for service in serviceList:
    print(serviceList.index(service),':',service)

def compareSingleService(service,env):
    #从swagger页面获取env环境API数据
    envApiList = getAPI(service,env)
    envData = {service:envApiList}
    #从swagger页面获取pr环境API数据
    prdApiList = getAPI(service,'prd')
    prdData = {service:prdApiList}
    #保存env环境API数据
    saveAPIJosn(serviceFileDir,env+'-'+service,envData)
    #保存prd环境API数据
    saveAPIJosn(serviceFileDir,'prd'+'-'+service,prdData)
    #对比两个文件
    prdLen,envLen,addCount,addList,deleteCount,deleteList = getAddAndDeleteCount(prdAPIList=prdApiList,envAPIList=envApiList)
    compare = showCompareResults(service,prdLen,envLen,addCount,addList,deleteCount,deleteList)
    AllCompareData.append(compare)
    #保存service对比结果
    saveAPIJosn(compareServiceFileDir,'compare'+'-'+service,compare)
    return compare

def main(DealServicesList,env):
    for service in DealServicesList:
        compareSingleService(service,env)
    #将service对比结果保存进对比汇总文件中
    saveAPIJosn(compareServiceFileDir,'AllServicesCompare',AllCompareData)
    #获取汇总结果Html
    allResultsHtml = allServicesResultHtml(AllCompareData)
    #保存Html
    ResultHtmlPath = saveHtml(compareServiceFileDir,'AllServicesCompare',allResultsHtml)
    os.startfile(ResultHtmlPath)
    print('对比结果汇总Html文件路径：' + ResultHtmlPath)


if __name__ == '__main__':
    env,realservicelist = gerInputArgus(serviceList)
    AllCompareData = []
    serviceFileDir,compareServiceFileDir = createServiceDir(env)
    main(env=env,DealServicesList=realservicelist)

