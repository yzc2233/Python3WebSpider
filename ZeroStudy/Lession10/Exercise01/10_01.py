import os
import time
def createfile():
    filetime = time.strftime('%Y%m%d%H%M%S',time.localtime())
    filename = str(filetime) + '.txt'
    with open(filename,'w') as file:
        contain = filename+'\n'
        file.write(contain)

if __name__ == '__main__':
    count = int(input('请输入文件个数：'))
    for i in range(count):
        createfile()
        time.sleep(1)
    print('生成文件成功')
