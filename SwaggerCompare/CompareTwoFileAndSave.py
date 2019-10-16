import os
import sys
import MyFunction as f

def CompareTwoFileAndSave(oldFilePath,newFilePath,APICompare_Dir):
    #获取两个文件的数据
    oldFileData,newFileData = f.getoldAndNewFiledata(oldFilePath,newFilePath)

    #获取旧文件接口路径
    oldAPIList = f.getAPIList(oldFileData)

    #获取新文件接口路径
    newAPIList = f.getAPIList(newFileData)

    #获取接口总数
    oldapiCount = len(oldAPIList)
    newapiCount = len(newAPIList)

    #获取接口新增和删除信息
    addCount,addList,deleteCount,deleteList = f.getAddAndDeleteCount(oldAPIList,newAPIList)

    #获取接口编辑信息
    modifyCount,modifyList = f.getmodifyresult(oldAPIList,newAPIList,oldFileData,newFileData)
    difresults = {"新增接口详情":addList,"删除接口详情":deleteList,"编辑接口详情":modifyList}

    #组合对比结果
    checkresult = {"1、上一版本接口个数":oldapiCount,"2、当前接口个数":newapiCount,
                   "3、新增接口数":addCount,"4、删除接口数":deleteCount,"5、修改接口数":modifyCount,
                   "6、检查结果":difresults}

    #保存对比结果
    difFilepath = f.savecompareresult(oldFilePath,newFilePath,APICompare_Dir,checkresult)

    #展示对比结果
    f.showCompareResults(difFilepath,checkresult)

if __name__ == '__main__':
    oldFilePath = sys.argv[1]
    newFilePath = sys.argv[2]
    if len(sys.argv) < 4:
        APICompare_Dir = os.getcwd()
    else:
        APICompare_Dir = sys.argv[3]
    CompareTwoFileAndSave(oldFilePath,newFilePath,APICompare_Dir)