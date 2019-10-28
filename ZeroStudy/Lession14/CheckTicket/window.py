# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!

import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from query_request import *
from get_station import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow") #设置窗体名称
        MainWindow.resize(960, 786) #设置窗体大小
        MainWindow.setMinimumSize(QtCore.QSize(960,786)) #主窗体最小值
        MainWindow.setMaximumSize(QtCore.QSize(960,786)) #设置窗体最大值

        self.centralwidget = QtWidgets.QWidget(MainWindow) #设置主窗体的widget控件
        self.centralwidget.setObjectName("centralwidget")#设置对象名称

        #顶部图片
        self.label_title_img = QtWidgets.QLabel(self.centralwidget)
        self.label_title_img.setGeometry(QtCore.QRect(0, 0, 960, 141))
        self.label_title_img.setObjectName("label_title_img")
        title_img = QPixmap('img/bg1.png') #打开顶部位图
        self.label_title_img.setPixmap(title_img) #设置调色板

        #查询区域容器
        self.widget_query = QtWidgets.QWidget(self.centralwidget)
        self.widget_query.setGeometry(QtCore.QRect(0, 141, 960, 60))
        self.widget_query.setObjectName("widget_query")
        #开启自动填充背景
        self.widget_query.setAutoFillBackground(True)
        palette = QPalette() #调色板类
        #设置背景图片
        palette.setBrush(QPalette.Background,QtGui.QBrush(QtGui.QPixmap('img/bg2.png')))
        self.widget_query.setPalette(palette) #为控件设置对应的调色板即可

        self.label = QtWidgets.QLabel(self.widget_query)
        self.label.setGeometry(QtCore.QRect(30, 30, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget_query)
        self.label_2.setGeometry(QtCore.QRect(220, 30, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget_query)
        self.label_3.setGeometry(QtCore.QRect(410, 30, 54, 12))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.widget_query)
        self.pushButton.setGeometry(QtCore.QRect(610, 20, 91,31))
        self.pushButton.setObjectName("pushButton")

        self.textEdit = QtWidgets.QTextEdit(self.widget_query)
        self.textEdit.setGeometry(QtCore.QRect(80, 20, 104, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.widget_query)
        self.textEdit_2.setGeometry(QtCore.QRect(270, 20, 104, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.widget_query)
        self.textEdit_3.setGeometry(QtCore.QRect(460, 20, 104, 31))
        self.textEdit_3.setObjectName("textEdit_3")

        #车次选项
        self.widget_checkBox = QtWidgets.QWidget(self.centralwidget)
        self.widget_checkBox.setGeometry(QtCore.QRect(0, 220, 960, 80))
        self.widget_checkBox.setObjectName("widget")
        self.widget_checkBox.setAutoFillBackground(True)
        palette.setBrush(QPalette.Background,QtGui.QBrush(QtGui.QPixmap('img/bg3.png')))
        self.widget_checkBox.setPalette(palette)

        self.checkBox_D = QtWidgets.QCheckBox(self.widget_checkBox)
        self.checkBox_D.setGeometry(QtCore.QRect(258, 9, 63, 17))
        self.checkBox_D.setObjectName("checkBox_D")
        self.checkBox_G = QtWidgets.QCheckBox(self.widget_checkBox)
        self.checkBox_G.setGeometry(QtCore.QRect(100, 9, 70, 17))
        self.checkBox_G.setObjectName("checkBox_G")
        self.checkBox_Z = QtWidgets.QCheckBox(self.widget_checkBox)
        self.checkBox_Z.setGeometry(QtCore.QRect(415, 9, 63, 17))
        self.checkBox_Z.setObjectName("checkBox_Z")
        self.checkBox_T = QtWidgets.QCheckBox(self.widget_checkBox)
        self.checkBox_T.setGeometry(QtCore.QRect(572, 9, 63, 17))
        self.checkBox_T.setObjectName("checkBox_T")
        self.checkBox_K = QtWidgets.QCheckBox(self.widget_checkBox)
        self.checkBox_K.setGeometry(QtCore.QRect(730, 9, 63, 17))
        self.checkBox_K.setObjectName("checkBox_K")
        self.label_type = QtWidgets.QLabel(self.widget_checkBox)
        self.label_type.setGeometry(QtCore.QRect(30, 9, 65, 16))
        self.label_type.setObjectName("label_type")

        #分类图片
        self.label_train_img = QtWidgets.QLabel(self.centralwidget)
        self.label_train_img.setGeometry(QtCore.QRect(0, 256, 960, 60))
        self.label_train_img.setObjectName("label_train_img")
        train_img = QPixmap('img/bg4.png')
        self.label_train_img.setPixmap(train_img)

        #显示信息表格
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(0, 320, 960, 440))
        self.tableView.setObjectName("tableView")
        self.model = QStandardItemModel() #创建存储数据的模式
        #根据空间自动改变列宽度并且不可修改列宽度
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #设置表头不可见
        self.tableView.horizontalHeader().setVisible(False)
        #纵向表头不可见
        self.tableView.verticalHeader().setVisible(False)
        #设置表格内容文字大小
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView.setFont(font)
        #设置表格内容不可编辑
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #垂直滚动条始终开启
        self.tableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "车票查询"))
        self.checkBox_T.setText(_translate("MainWindow", "T-特快"))
        self.checkBox_K.setText(_translate("MainWindow", "K-快速"))
        self.checkBox_Z.setText(_translate("MainWindow", "Z-直达"))
        self.checkBox_D.setText(_translate("MainWindow", "D-动车"))
        self.checkBox_G.setText(_translate("MainWindow", "GC-高铁"))
        self.label_type.setText(_translate("MainWindow", "车次类型："))
        # self.label_title_img.setText(_translate("MainWindow", "TextLabel"))
        # self.label_train_img.setText(_translate("MainWindow", "TextLabel"))
        self.label.setText(_translate("MainWindow", "出发地："))
        self.label_2.setText(_translate("MainWindow", "目的地："))
        self.label_3.setText(_translate("MainWindow", "出发日："))
        self.pushButton.setText(_translate("MainWindow", "查询"))

        self.textEdit_3.setText(get_time())#触发日期显示当天日期
        self.pushButton.clicked.connect(self.on_click)#查询按钮指定单击事件的方法
        self.checkBox_G.stateChanged.connect(self.change_G)#高铁选中与取消事件
        self.checkBox_D.stateChanged.connect(self.change_D)#动车选中与取消事件
        self.checkBox_Z.stateChanged.connect(self.change_Z)#直达选中与取消事件
        self.checkBox_T.stateChanged.connect(self.change_T)#特快选中与取消事件
        self.checkBox_K.stateChanged.connect(self.change_K)#快车选中与取消事件

    #高铁复选框事件处理
    def change_G(self,state):
        #选中将高铁信息添加到最后要显示的数据中
        if state == QtCore.Qt.Checked:
            g_vehicle()
            #通过表格显示该车型数据
            self.displayTable(len(type_data),16,type_data)
        else:
            #取消选中状态将移除该数据
            r_g_vehicle()
            self.displayTable(len(type_data),16,type_data)

    def change_D(self,state):
        #选中将动车信息添加到最后要显示的数据中
        if state == QtCore.Qt.Checked:
            d_vehicle()
            #通过表格显示该车型数据
            self.displayTable(len(type_data),16,type_data)
        else:
            #取消选中状态将移除该数据
            r_d_vehicle()
            self.displayTable(len(type_data),16,type_data)

    def change_Z(self,state):
        #选中将直达车信息添加到最后要显示的数据中
        if state == QtCore.Qt.Checked:
            z_vehicle()
            #通过表格显示该车型数据
            self.displayTable(len(type_data),16,type_data)
        else:
            #取消选中状态将移除该数据
            r_z_vehicle()
            self.displayTable(len(type_data),16,type_data)

    def change_T(self,state):
        #选中将特快车信息添加到最后要显示的数据中
        if state == QtCore.Qt.Checked:
            t_vehicle()
            #通过表格显示该车型数据
            self.displayTable(len(type_data),16,type_data)
        else:
            #取消选中状态将移除该数据
            r_t_vehicle()
            self.displayTable(len(type_data),16,type_data)

    def change_K(self,state):
        #选中将快速车信息添加到最后要显示的数据中
        if state == QtCore.Qt.Checked:
            k_vehicle()
            #通过表格显示该车型数据
            self.displayTable(len(type_data),16,type_data)
        else:
            #取消选中状态将移除该数据
            r_k_vehicle()
            self.displayTable(len(type_data),16,type_data)

    #所有车次分类复选框取消勾选
    def checkBox_default(self):
        self.checkBox_G.setChecked(False)
        self.checkBox_D.setChecked(False)
        self.checkBox_Z.setChecked(False)
        self.checkBox_T.setChecked(False)
        self.checkBox_K.setChecked(False)

    #显示主窗体非法操作的消息提示框
    #title为提示框标题文字，message为提示信息
    def messageDialog(self,title,message):
        msg_box = QMessageBox(QMessageBox.Warning,title,message)
        msg_box.exec_()

    #展示车次信息的表格
    #train为共有多少列车，该参数作为表格的行
    #info为该车次的具体信息，例如有座、无座、卧铺等，该参数作为表格的列
    def displayTable(self,train,info,data):
        self.model.clear()
        for row in range(train):
            for column in range(info):
                #添加表格内容
                item = QStandardItem(data[row][column])
                #向表格存储模式中添加表格具体信息
                self.model.setItem(row,column,item)
        #设置表格存储数据的模式
        self.tableView.setModel(self.model)

    #查询按钮的单击事件
    def on_click(self):
        get_from = self.textEdit.toPlainText()#获取出发地
        get_to = self.textEdit_2.toPlainText()#获取到达地
        get_date = self.textEdit_3.toPlainText()#获取出发时间
        #判断车站文件是否存在
        if isStations() == True:
            stations = eval(read()) #读取所有车站并转换为dic类型
            #判断所有参数是否为空，以及出发地、目的地、出发日期
            cc = (is_valid_date(get_date))
            bb = (get_from in stations)
            aa = (get_to in stations)
            if get_from != '' and get_to != '' and get_date !='':
                #判断输入的车站名称是否存在，以及时间格式是否正确
                if get_from in stations and get_to in stations and is_valid_date(get_date):
                    #获取输入的日期是当前年初到现在一共过了多少天
                    inputYearDay = time.strptime(get_date,'%Y-%m-%d').tm_yday
                    #获取系统当前日期是当前年初到现在一共过了多少天
                    yearTody = time.localtime(time.time()).tm_yday
                    #计算时间差，也就是输入的日期减掉系统当前的日期
                    timeDifference = inputYearDay - yearTody
                    #判断时间差为0时证明是查询当天的查票
                    #以及29天以后的车票，12306要求只能查询30天以内的车票
                    if timeDifference >= 0 and timeDifference <= 28:
                        #在所有车站文件中找到对应的参数
                        from_station  =  stations[get_from]#出发地
                        to_station = stations[get_to]#目的地
                        #发起查询请求，并获取返回的信息
                        data = query(get_date,from_station,to_station)
                        self.checkBox_default() #调用取消勾选所有车次分类复选框
                        if len(data) != 0:#判断返回数据是否为空
                            #如果不为空数据就将车票信息显示在表格
                            self.displayTable(len(data),16,data)
                        else:
                            self.messageDialog('警告','没有返回的网络数据！')
                    else:
                        self.messageDialog('警告','超出查询日期的范围内','不可查询昨天的车票信息，以及29天以后的车票信息！')
                else:
                    self.messageDialog('警告','输入的站名不存在，或日期格式不正确！')
            else:
                self.messageDialog('警告','请填写车站名称！')
        else:
            self.messageDialog('警告','未下载车站查询文件！')


def show_MainWindow():
    app = QtWidgets.QApplication(sys.argv) #实例化QApplication类，作为GUI主程序入口
    MainWindow = QtWidgets.QMainWindow() #创建MainWindow类
    ui = Ui_MainWindow() #实例UI类
    ui.setupUi(MainWindow) #设置窗体UI
    MainWindow.show() #显示窗体
    sys.exit(app.exec_()) #当窗体创建完成，需要结束主循环过程

#获取系统当前时间并转换请求数据所需的格式
def get_time():
    #获取当前时间的时间戳
    now = int(time.time())
    #转换为其他日期格式，如：“%Y-%m-%d %H:%M:%S”
    timeStruct = time.localtime(now)
    strTime = time.strftime("%Y-%m-%d",timeStruct)
    return strTime

def is_valid_date(str):
    """判断是否是一个有效的日期字符串"""
    try:
        time.strptime(str,"%Y-%m-%d")
        return True
    except:
        return False


if __name__ == '__main__':
    if isStations() == False:
        getStation()
        show_MainWindow()
    else:
        show_MainWindow()