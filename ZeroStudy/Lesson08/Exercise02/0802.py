
from GetHappy import gethappy

print('开始集福啦~~~')
MyhappyList = {'爱国福':0,'富强福':0,'和谐福':0,'友善福':0,'敬业福':0}

while True:
    fullflag = 0
    inputkey = input('按下<Enter>键获取五福,其他键退出程序')
    if inputkey == '':
        happy = gethappy()
        MyhappyList[happy] += 1
        print('获取到：',happy)
        print('当前拥有的福：')
        for i,n in MyhappyList.items():
            print(i,':',n,'  ',end='')
            if n != 0:
                fullflag += 1
        if fullflag >= 5:
            print('\n已集齐五福，退出程序')
            exit()
        print('\n')

    else:
        print('退出程序')
        exit()
