import os
import sys
#
try :
    import pygame
except ImportError:
    print('pygame未安装，现在开始安装')
    os.system('activate mypython36&&pip install pygame')
    import pygame

# import pygame
# #初始化pygame
# pygame.init()
# #设置窗口size
# size = width,height = 320,240
# #设置显示窗口
# screen = pygame.display.set_mode(size)
#
# #执行死循环，确保窗口一直显示
# while True:
#     #检查事件
#     #遍历所有事件
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#
# #退出pygame
# pygame.quit()
#
# import sys
# import pygame
#
# pygame.init()
# size = width,height = 640,480
# screen = pygame.display.set_mode(size)
# color = (0,0,0)#设置背景颜色
#
# #加载图片
# ball = pygame.image.load('ball.png')
# #获取图片矩形区域
# ballrect = ball.get_rect()
#
# #设置移动的X轴、Y轴的距离
# speed = [5,5]
#
# #设置时钟
# clock = pygame.time.Clock()
#
# while True:
#     #每秒执行60次
#     clock.tick(120)
#
#     #检查事件
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#     #移动小球
#     ballrect = ballrect.move(speed)
#
#     #碰到左右边缘
#     if ballrect.left < 0 or ballrect.right > width:
#         speed[0] = -speed[0]
#
#     #碰到上下边缘
#     if ballrect.top < 0 or ballrect.bottom > height:
#         speed[1] = -speed[1]
#
#     #屏幕设置背景色
#     screen.fill(color)
#     #将图片画到窗口上
#     screen.blit(ball,ballrect)
#     #更新全部显示
#     pygame.display.flip()
#
# pygame.quit()
#


import pygame
import sys
import random

class Bird():
    def __init__(self):
        #鸟的矩形
        self.birdRect = pygame.Rect(65,50,50,50)

        #定义鸟的3种状态列表
        self.birdstatus = [pygame.image.load('1.png'),pygame.image.load('2.png'),pygame.image.load('dead.png')]
        self.status = 0 #默认飞行状态
        self.birdX = 120 # 小鸟所在X坐标
        self.birdY = 350 #小鸟所在Y坐标
        self.jump = False #默认情况小鸟自动降落
        self.jumpSpeed = 10 #跳跃高度
        self.gravity = 5 #重力
        self.dead = False #默认小鸟活着

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1 #速度递减，越来越慢
            self.birdY -= self.jumpSpeed #小鸟的Y坐标减小，小鸟上升
        else:
            self.gravity += 0.2 #重力递增，下降速度越来越快
            self.birdY += self.gravity #更改Y坐标
        self.birdRect[1] = self.birdY

class Pipeline():
    def __init__(self):
        self.wallx = 400 #管道所在的X轴坐标
        self.pineUp = pygame.image.load('top.png')
        self.pineDown = pygame.image.load('bottom.png')
    def updatePineline(self):
        #管道移动
        self.wallx -= 5  #管道X轴坐标递减
        #当管道运行到一定位置，即小鸟飞跃管道，分数加1，并且重置管道
        if self.wallx < -80:
            global score
            score += 1
            self.wallx = 400

def createMap():
    screen.fill((255,255,255))
    screen.blit(background,(0,0))

    #显示管道
    screen.blit(Pipeline.pineUp,(Pipeline.wallx,-300))
    screen.blit(Pipeline.pineDown,(Pipeline.wallx,500))
    Pipeline.updatePineline() #管道移动

    #显示小鸟
    if Bird.dead:
        Bird.status = 2 #撞管道状态
    elif Bird.jump:
        Bird.status = 1 #起飞状态
    screen.blit(Bird.birdstatus[Bird.status],(Bird.birdX,Bird.birdY)) #设置小鸟坐标和显示状态
    Bird.birdUpdate()
    #显示分数,设置颜色及坐标
    screen.blit(font.render('Score:'+str(score),-1,(255,255,255)),(100,50))
    pygame.display.update()

def checkdead():
    #上方管子的矩形位置
    upRect = pygame.Rect(Pipeline.wallx,-300,Pipeline.pineUp.get_width() - 10,Pipeline.pineUp.get_height())
    #下方管子的矩形位置
    downRect = pygame.Rect(Pipeline.wallx,500,Pipeline.pineDown.get_width()-10,Pipeline.pineDown.get_height())

    if upRect.colliderect(Bird.birdRect) or downRect.colliderect(Bird.birdRect) or Bird.birdY < 0 or Bird.birdY > 650:
        Bird.dead = True
        return  True
    else:
        return False



def getResult():
    final_text1 = 'Game Over'
    final_text2 = 'Your final score is: '+str(score)
    ft1_font = pygame.font.SysFont('Arial',70)#设置第一行文字字体
    ft1_surf = font.render(final_text1,1,(242,3,36))#设置第一行文字颜色
    ft2_font = pygame.font.SysFont('Arial',50)
    ft2_surf = font.render(final_text2,1,(253,177,6))
    #设置第一行文字显示位置
    screen.blit(ft1_surf,[screen.get_width()/2-ft1_surf.get_width()/2,100])
    #设置第二行文字位置
    screen.blit(ft2_surf,[screen.get_width()/2-ft2_surf.get_width()/2,200])
    pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    #初始化字体
    pygame.font.init()
    font = pygame.font.SysFont(None,50)
    size = width,height = 400,650
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    Pipeline = Pipeline()
    Bird = Bird()
    score = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not Bird.dead:
                Bird.jump = True
                Bird.gravity = 5
                Bird.jumpSpeed = 10

        background = pygame.image.load('background.png')

        if checkdead():
            getResult()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    print()
        else:
            createMap()

        createMap()

pygame.quit()


























