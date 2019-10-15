import os

try:
    import wx
except ImportError as e:
    print('wxPython包不存在，开始安装')
    os.system('activate mypython36')
    os.system('pip install -U wxPython')
    import wx
#
# class App(wx.App):
#     #初始化方法
#     def OnInit(self):
#         #创建窗口
#         frame = wx.Frame(parent=None,title='HelloPython')
#         #显示窗口
#         frame.Show()
#         return True #返回值
#
# if __name__ == '__main__':
#     #创建APP类的实例
#     app = App()
#     #调用APP类的MainLoop主循环方法
#     app.MainLoop()

# #初始化wx.App类
# app = wx.App()
# #定义一个顶级窗口
# frame = wx.Frame(None,title='Hello Python')
# #显示窗口
# frame.Show()
# #调用wx.App类的MainLoop()主循环方法
# app.MainLoop()
#
#
# class MyFrame(wx.Frame):
#     def __init__(self,parent,id):
#         wx.Frame.__init__(self,parent,id,title='创建StaticText类',pos=(100,100),size=(600,400))
#         #创建画板
#         panel = wx.Panel(self)
#         #创建标题并设置字体
#         title = wx.StaticText(panel,label='Python之禅——Tim Perters',pos=(100,20))
#         font = wx.Font(16,wx.DEFAULT,wx.FONTSTYLE_NORMAL,wx.NORMAL)
#         title.SetFont(font)
#         #创建文本
#         wx.StaticText(panel,label='Beautiful is better than ugly.',pos=(50,50))
#         wx.StaticText(panel,label='Explicit is better than implicit.',pos=(50,70))
#         wx.StaticText(panel,label='Simple is better than complex.',pos=(50,90))
#         wx.StaticText(panel,label='Complex is better than complicated.',pos=(50,110))
#         wx.StaticText(panel,label='Flat is better than nested.',pos=(50,130))
#         wx.StaticText(panel,label='Sparse is better than dense.',pos=(50,150))
#         wx.StaticText(panel,label='Readability counts.',pos=(50,170))
#         wx.StaticText(panel,label="Special cases aren't special enough to break the rules.",pos=(50,50))
#
# if __name__ == '__main__':
#     app = wx.App()
#     frame = MyFrame(parent=None,id=-1)
#     frame.Show()
#     app.MainLoop()


# #实现登录界面+确认、取消按钮
# class Myframe(wx.Frame):
#     def __init__(self,parent,id):
#         wx.Frame.__init__(self,parent,id,title='创建TextCtrl类',size=(400,300))
#         #创建面板
#         panel = wx.Panel(self)
#         #创建文本和输入框
#         self.title = wx.StaticText(panel,label='请输入用户名和密码',pos=(140,20))
#         self.label_user = wx.StaticText(panel,label='用户名：',pos=(50,50))
#         self.text_user = wx.TextCtrl(panel,pos=(100,50),size=(235,25),style=wx.TE_LEFT)
#         self.label_pwd = wx.StaticText(panel,pos=(50,90),label='密 码：')
#         self.text_pwd = wx.TextCtrl(panel,pos=(100,90),size=(235,25),style=wx.TE_PASSWORD)
#         self.bt_confirm = wx.Button(panel,label='确定',pos=(105,130))
#         self.bt_cancel = wx.Button(panel,label='取消',pos=(205,130))
#
#
# if __name__ == '__main__':
#     app = wx.App()
#     frame = Myframe(parent=None,id=-1)
#     frame.Show()
#     app.MainLoop()

#
# #使用BoxSizer实现简单的布局
# import wx
# class Myframe(wx.Frame):
#     def __init__(self,parent,id):
#         wx.Frame.__init__(self,parent,id,title='用户登录',size=(400,300))
#         #创建面板
#         panel = wx.Panel(self)
#         self.title = wx.StaticText(panel,label='请输入用户名和密码')
#         #添加容器，容器中控件按纵向排列
#         vsizer = wx.BoxSizer(wx.VERTICAL)
#         vsizer.Add(self.title,proportion=0,flag=wx.BOTTOM|wx.TOP|wx.ALIGN_CENTER,border=15)
#         panel.SetSizer(vsizer)
#
# if __name__ == '__main__':
#     app = wx.App()
#     frame = Myframe(parent=None,id=-1)
#     frame.Show()
#     app.MainLoop()


#
# #使用BoxSizer设置登录页面布局
# import wx
# class Myframe(wx.Frame):
#     def __init__(self,parent,id):
#         wx.Frame.__init__(self,parent,id,title='用户登录',size=(400,300))
#         panel = wx.Panel(self)
#
#         #创建确定和取消按钮
#         self.bt_confirm = wx.Button(panel,label='确定')
#         self.bt_cancel = wx.Button(panel,label='取消')
#
#         #创建文本，左对齐
#         self.title = wx.StaticText(panel,label='请输入用户和密码')
#         self.label_user = wx.StaticText(panel,label='用户名：')
#         self.text_user = wx.TextCtrl(panel,style=wx.TE_LEFT)
#         self.label_pwd = wx.StaticText(panel,label='密   码：')
#         self.text_pwd = wx.TextCtrl(panel,style=wx.TE_PASSWORD)
#
#         #添加容器，容器中的控件横向排列
#         hsizer_user = wx.BoxSizer(wx.HORIZONTAL)
#         hsizer_user.Add(self.label_user,proportion=0,flag=wx.ALL,border=5)
#         hsizer_user.Add(self.text_user,proportion=1,flag=wx.ALL,border=5)
#
#         hsizer_pwd = wx.BoxSizer(wx.HORIZONTAL)
#         hsizer_pwd.Add(self.label_pwd,proportion=0,flag=wx.ALL,border=5)
#         hsizer_pwd.Add(self.text_pwd,proportion=1,flag=wx.ALL,border=5)
#
#         hsizer_button = wx.BoxSizer(wx.HORIZONTAL)
#         hsizer_button.Add(self.bt_confirm,proportion=0,flag=wx.ALIGN_CENTER,border=5)
#         hsizer_button.Add(self.bt_cancel,proportion=0,flag=wx.ALIGN_CENTER,border=5)
#
#         #添加容器，容器中的控件纵向排列
#         vsizer_all = wx.BoxSizer(wx.VERTICAL)
#         vsizer_all.Add(self.title,proportion=0,flag=wx.BOTTOM|wx.TOP|wx.ALIGN_CENTER,border=15)
#         vsizer_all.Add(hsizer_user,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=45)
#         vsizer_all.Add(hsizer_pwd,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=45)
#         vsizer_all.Add(hsizer_button,proportion=0,flag=wx.ALIGN_CENTER|wx.TOP,border=15)
#
#         panel.SetSizer(vsizer_all)
#
# if __name__ == '__main__':
#     app = wx.App()
#     frame = Myframe(parent=None,id=-1)
#     frame.Show()
#     app.MainLoop()


#使用事件判断用户登录
import wx
class Myframe(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'用户登录',size=(400,300))

        panel = wx.Panel(self)

        self.title = wx.StaticText(panel,label='请输入用户名和密码')



        self.bt_confirme = wx.Button(panel,label='确定')
        self.bt_confirme.Bind(wx.EVT_BUTTON,self.OnclickSubmit)
        self.bt_cancel =  wx.Button(panel,label='取消')
        self.bt_cancel.Bind(wx.EVT_BUTTON,self.OnclickCancel)

        self.label_user = wx.StaticText(panel,label='用户名：')
        self.text_user = wx.TextCtrl(panel,style=wx.TE_LEFT)
        self.label_pwd = wx.StaticText(panel,label='密   码：')
        self.text_pwd = wx.TextCtrl(panel,style=wx.TE_PASSWORD)

        hsizer_user = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_user.Add(self.label_user,proportion=0,flag=wx.ALL,border=5)
        hsizer_user.Add(self.text_user,proportion=1,flag=wx.ALL,border=5)

        hsizer_pwd = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_pwd.Add(self.label_pwd,proportion=0,flag=wx.ALL,border=5)
        hsizer_pwd.Add(self.text_pwd,proportion=1,flag=wx.ALL,border=5)

        hsizer_bt = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_bt.Add(self.bt_confirme,proportion=0,flag=wx.ALL,border=5)
        hsizer_bt.Add(self.bt_cancel,proportion=1,flag=wx.ALL,border=5)

        hsizer_all = wx.BoxSizer(wx.VERTICAL)
        hsizer_all.Add(self.title,proportion=0,flag=wx.BOTTOM|wx.TOP|wx.ALIGN_CENTER,border=15)
        hsizer_all.Add(hsizer_user,proportion=0,flag=wx.EXPAND| wx.LEFT | wx.RIGHT,border=5)
        hsizer_all.Add(hsizer_pwd,proportion=0,flag=wx.EXPAND| wx.LEFT | wx.RIGHT,border=5)
        hsizer_all.Add(hsizer_bt,proportion=0,flag=wx.ALIGN_CENTER,border=5)

        panel.SetSizer(hsizer_all)

    def OnclickSubmit(self,event):
        message = ''
        #获取输入的用户名和密码
        usename = self.text_user.GetValue()
        pwd = self.text_pwd.GetValue()
        if usename == '' or pwd == '':
            message = '用户名或者密码不能为空'
        elif usename == 'mr' and pwd == 'mrsoft':
            message = '登陆成功'
        else:
            message = '用户名和密码不匹配'
        wx.MessageBox(message)



    def OnclickCancel(self,event):
        #清空用户名和密码
        self.text_user.SetValue('')
        self.text_pwd.SetValue('')


if __name__ == '__main__':
    app = wx.App()
    frame = Myframe(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
















