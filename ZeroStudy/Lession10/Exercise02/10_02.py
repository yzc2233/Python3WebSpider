import os

def createdir(count):
    for i in range(count):
        dirname = str(i+1)
        try:
            os.mkdir(dirname)
        except FileExistsError:
            print('文件夹',dirname,'已经存在，无法创建该文件')
        else:
            print('文件夹',dirname,'创建成功')

if __name__ == '__main__':
    count = int(input('请输入创建文件夹个数:'))
    createdir(count)
