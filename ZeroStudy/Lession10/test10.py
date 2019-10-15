#10.1.1
#打开文件
# print('='*10,'蚂蚁庄园动态','='*10,'\n')
# file = open('message.txt','w')

# file = open('业务负责分组.png','rb')
# print(file)
# file.close()

# with open('message.txt','a+',encoding='utf-8') as file:
#     file.write('您使用了一张加速卡\n')
#     print('写入一条动态~')
#     file.flush()
# with open('message.txt','r',encoding='utf-8') as file:
#     contain = file.read()
#     print(contain)

# with open('message.txt','r',encoding='utf-8') as file:
#     number = 0
#     while True:
#         number += 1
#         line = file.readline()
#         if line == '':
#             break
#         print(number,line,end='')

with open('message.txt','r',encoding='utf-8') as file:
    lines = file.readlines()
    print(lines)
