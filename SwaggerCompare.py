import os
import json
import sys
from myFunction import *

#
# serviceList = ['ALL service','COMMUNITY-CORE-SERVICE','CRM-SERVICE','FINANCE-SERVICE','INV-SERVICE',
#                'KOL-SERVICE','MARKETING-ACTIVITY-SERVICE','MESSAGES-SERVICE','MP-CMS-SERVICE',
#                'MYACCOUNT-PORTAL-SERVICE','MYACCOUNT-SERVICE','OFFLINE-SHOP-SERVICE','OMNI-CRMHUB-SERVICE',
#               # 'OMNI-MEMBER-MSG-SERVICE','OMNI-ORDERCENTER-SERVICE',
#                'ORDER-SERVICE','PIM-BACKEND',
#                'PRODUCT-SERVICE','PROMOTION-SERVICE','SEARCH-SERVICE',
#                'SHOP-CART-SERVICE','SOA-MANAGEMENT','OMS-SERVICE','WCS-SERVICE','WECHATCENTER-SERVICE']
# print('命令示例：python SwaggerCompare.py 1')
# print('示例中的1是service序号，以下为各service序号(0代表以下所有services)')
# for service in serviceList:
#     print(serviceList.index(service),':',service)

DealServicesList = ['MYACCOUNT-PORTAL-SERVICE']
env = 'qa2'

def main(DealServicesList):
    envFilePathList = []#生成的env文件路径列表
    prdFilePathList = []#生成的prd文件路径列表
    compareFilePathList = []#对比结果文件路径列表
    isNew = True
    for service in DealServicesList:
        # 创建相应文件夹
        serviceFileDir,compareServiceFileDir = createServiceDir(service,env)
        #从swagger页面获取env环境API数据
        envApiList = getApiList(service,env)
        envData = {service:envApiList}
        #从swagger页面获取pr环境API数据
        prdApiList = getApiList(service,'prd')
        prdData = {service:prdApiList}
        #保存env环境API数据
        envFileDir = saveAPIJosn(serviceFileDir,env+'-'+service,envData)
        envFilePathList.append(envFileDir)
        #保存prd环境API数据
        prdFileDir = saveAPIJosn(serviceFileDir,'prd'+'-'+service,prdData)
        prdFilePathList.append(prdFileDir)
        #对比两个文件
        prdLen,envLen,addCount,addList,deleteCount,deleteList = getAddAndDeleteCount(prdAPIList=prdApiList,envAPIList=envApiList)
        compare = showCompareResults(service,prdLen,envLen,addCount,addList,deleteCount,deleteList)
        #保存service对比结果
        compareFileDir = saveAPIJosn(compareServiceFileDir,'compare'+'-'+service,compare)
        compareFilePathList.append(compareFileDir)
        #将service对比结果保存进对比汇总文件中
        compareFilePath = saveAllcompareresult(compareFileDir,compare,isNew=isNew)
        isNew = False
    print('对比结果文件路径：' + compareFilePath)

    #
    # for service in realservicelist:
    #
    #
    #
    #     #对比两个文件保存结果并展示
    #     CompareTwoFileAndSave(oldFilePath,newFilePath,APICompare_Dir)
#
if __name__ == '__main__':
#     if len(sys.argv) == 1:
#         serviceIndex = int(input('请输入service序号：'))
#     else:
#         serviceIndex = int(sys.argv[1])
#     # serviceIndex = 19
#     realservicelist = []
#     if serviceIndex != 0:
#         realservicelist.append(serviceList[serviceIndex])
#     else:
#         realservicelist = serviceList[1:]
    main(DealServicesList)

