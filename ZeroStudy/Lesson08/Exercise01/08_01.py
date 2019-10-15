import sys

#sys.path.append('E:/SoftWare/JetBrains/IntellijCode/PythonCode/Python3WebSpider/ZeroStudy/Lesson08/Exercise01')

from MyMoudle.Create_lotto import Create_lotto

print('大乐透号码生成器')
while True:
    times = input('请输入要生成的大乐透号码注数：')
    try:
        times = int(times)
        break
    except:
        print('请输入正确的数量')

lottoCodeList = Create_lotto(times)
for lottoCode in lottoCodeList:
    print(lottoCode)






