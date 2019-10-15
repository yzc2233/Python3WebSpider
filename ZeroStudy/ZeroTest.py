
## 7.2.3
# class Geese:
#     """大雁类"""
#     def __init__(self):    #构造方法
#         print('我是大雁类！')
# wildGoose = Geese()   #创建大雁类的实例
#
# class Geese:
#     """大雁类"""
#     def __init__(self,beak,wing,claw):
#         print('我是大雁类！我又以下特征：')
#         print(beak)
#         print(wing)
#         print(claw)
# beak_1 = '喙的基部较高，长度和头部的长度几乎相等'
# wing_1 = '翅膀长而尖'
# claw_1 = '爪子是蹼状的'
# wildGoose = Geese(beak_1,wing_1,claw_1)

#7.2.4

# #Sample-1
# class Geese:
#     """大雁类"""
#     def __init__(self,beak,wing,claw):
#         print('我是大雁类！我有以下特征：')
#         print(beak)
#         print(wing)
#         print(claw)
#     def fly(self,state):
#         print(state)
# """************调用方法**********"""
# beak_1 = '喙的基部较高，长度和头部的长度几乎相等'
# wing_1 = '翅膀长而尖'
# claw_1 = '爪子是蹼状的'
# wildGoose = Geese(beak_1,wing_1,claw_1)
# wildGoose.fly('我飞行的时候，一会排个人字，一会排个一字')

# #Sample-1.2
# class Geese:
#     """大雁类"""
#     neck = '脖子较长'
#     wing = '振翅频率高'
#     leg = '腿位于身体的中心支点，行走自如'
#     def __init__(self):
#         print('我是大雁类！我有以下特征：')
#         print(Geese.neck)
#         print(Geese.wing)
#         print(Geese.leg)
# geese = Geese()
#
# class Cellphone:
#     def __init__(self):
#         self.__language = '手机默认语言为：英文'
#     @property
#     def cellphoelanguange(self):
#         return self.__language
#     @cellphoelanguange.setter
#     def cellphoelanguange(self,defaultlanguage):
#         self.__language = '将手机默认语言设置为' + defaultlanguage
#
# aa = Cellphone()
# print(aa.cellphoelanguange)
# aa.cellphoelanguange = 'fff'
# print(aa.cellphoelanguange)
#
# import random
# def checkCode():
#     checkcode = ''
#     for i  in range(0,4):
#         index = random.randrange(0,4)
#         if index != i and index + 1 != i:
#             checkcode += chr(random.randint(97,122)) #a~z小写字母
#         elif index + 1 == i:
#             checkcode += chr(random.randint(65,90))#A~Z大写字母
#         else:
#             checkcode += str(random.randint(1,9)) # 1-9数字
#     return checkcode
# a = checkCode()
# print('验证码',a)

# help('modules')
#
# #大乐透
# import random
# def getcode():
#     precode = ''
#     backcode = ''
#     code = ''
#     for i in range(0,5):
#         precode += '{:0>2d}'.format(random.randint(1,35))+' '
#     for i in range(0,2):
#         backcode += '{:0>2d}'.format(random.randint(1,12))+' '
#     code = precode + ' '*5 + backcode
#     print(code)
#
# def bighappy():
#     print('大乐透号码生成器')
#     count = int(input('请输入要生成的大乐透号码注数：'))
#     for i in range(0,count):
#         getcode()
#
#
# if __name__ == '__main__':
#     bighappy()
#
# #9.2.4
# #分苹果（每个人至少分到一个苹果）
# def division():
#     appcount = int(input('请输入苹果个数：'))
#     usercount = int(input('请输入小朋友人数：'))
#     #assert appcount > usercount,'苹果太少了，不够分~'
#     if appcount < usercount:
#         raise ValueError('苹果太少了，不够分~')
#     getcount = appcount // usercount
#     remaincount = appcount - getcount * usercount
#     if remaincount > 0:
#         print('每个小朋友分到%s个苹果，还剩余%s个' %(getcount,remaincount))
#     else:
#         print('每个小朋友分到%s个苹果，正好分完' %getcount)
#
# if __name__ == '__main__':
#     try:
#         division()
#     except ZeroDivisionError:
#         print('苹果不能分给0个小朋友哦')
#     except ValueError as e:
#         print('出错了，请输入正确的人数和苹果个数',e)

import this
























