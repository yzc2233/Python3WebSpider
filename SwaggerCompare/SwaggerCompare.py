import os
import json
import sys
import MyFunction as f
import CompareTwoFileAndSave as c

serviceList = ['ALL service','COMMUNITY-CORE-SERVICE','CRM-SERVICE','FINANCE-SERVICE','INV-SERVICE',
               'KOL-SERVICE','MARKETING-ACTIVITY-SERVICE','MESSAGES-SERVICE','MP-CMS-SERVICE',
               'MYACCOUNT-PORTAL-SERVICE','MYACCOUNT-SERVICE','OFFLINE-SHOP-SERVICE','OMNI-CRMHUB-SERVICE',
               'ORDER-SERVICE','PIM-BACKEND','PRODUCT-SERVICE','PROMOTION-SERVICE','SEARCH-SERVICE',
               'SHOP-CART-SERVICE','SOA-MANAGEMENT','OMS-SERVICE','WCS-SERVICE','WECHATCENTER-SERVICE']
print('命令示例：python SwaggerCompare.py 1')
print('示例中的1是service序号，以下为各service序号(0代表以下所有services)')
for service in serviceList:
    print(serviceList.index(service),':',service)


def main(realservicelist):
    for service in realservicelist:
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

        #对比两个文件保存结果并展示
        c.CompareTwoFileAndSave(oldFilePath,newFilePath,APICompare_Dir)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        serviceIndex = int(input('请输入service序号：'))
    else:
        serviceIndex = int(sys.argv[1])
    # serviceIndex = 19
    realservicelist = []
    if serviceIndex != 0:
        realservicelist.append(serviceList[serviceIndex])
    else:
        realservicelist = serviceList[1:]
    main(realservicelist)