# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette,QPixmap,QColor

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
        self.widget_query.setGeometry(QtCore.QRect(0, 141, 960, 150))
        self.widget_query.setObjectName("widget_query")
        #开启自动填充背景
        # self.widget_query.setAutoFillBackground(True)
        # palette = QPalette() #调色板类
        # #设置背景图片
        # palette.setBrush(QPalette.Background,QtGui.QBrush(QtGui.QPixmap('img/bg2.png')))
        # self.widget_query.setPalette(palette) #为控件设置对应的调色板即可

        #车次选项
        self.widget_checkBox = QtWidgets.QWidget(self.centralwidget)
        self.widget_checkBox.setGeometry(QtCore.QRect(0, 150, 960, 200))
        self.widget_checkBox.setObjectName("widget")

        #分类图片
        self.label_train_img = QtWidgets.QLabel(self.centralwidget)
        self.label_train_img.setGeometry(QtCore.QRect(0, 280, 960, 340))
        self.label_train_img.setObjectName("label_train_img")
        train_img = QPixmap('img/bg4.png')
        self.label_train_img.setPixmap(train_img)

        #显示信息表格
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(0, 540, 960, 786))
        self.tableView.setObjectName("tableView")

        #
        # self.label = QtWidgets.QLabel(self.widget_query)
        # self.label.setGeometry(QtCore.QRect(10, 20, 41, 20))
        # self.label.setObjectName("label")
        # self.label_2 = QtWidgets.QLabel(self.widget_query)
        # self.label_2.setGeometry(QtCore.QRect(320, 20, 41, 20))
        # self.label_2.setObjectName("label_2")
        # self.label_3 = QtWidgets.QLabel(self.widget_query)
        # self.label_3.setGeometry(QtCore.QRect(530, 20, 41, 20))
        # self.label_3.setObjectName("label_3")
        # self.pushButton = QtWidgets.QPushButton(self.widget_query)
        # self.pushButton.setGeometry(QtCore.QRect(730, 20, 41, 20))
        # self.pushButton.setObjectName("pushButton")
        #
        # self.textEdit = QtWidgets.QTextEdit(self.widget_query)
        # self.textEdit.setGeometry(QtCore.QRect(90, 20, 121, 20))
        # self.textEdit.setObjectName("textEdit")
        # self.textEdit_2 = QtWidgets.QTextEdit(self.widget_query)
        # self.textEdit_2.setGeometry(QtCore.QRect(370, 20, 121, 21))
        # self.textEdit_2.setObjectName("textEdit_2")
        # self.textEdit_3 = QtWidgets.QTextEdit(self.widget_query)
        # self.textEdit_3.setGeometry(QtCore.QRect(580, 20, 121, 21))
        # self.textEdit_3.setObjectName("textEdit_3")
        #
        #
        # self.checkBox_D = QtWidgets.QCheckBox(self.widget_checkBox)
        # self.checkBox_D.setGeometry(QtCore.QRect(200, 10, 140, 60))
        # self.checkBox_D.setObjectName("checkBox_D")
        # self.checkBox_G = QtWidgets.QCheckBox(self.widget_checkBox)
        # self.checkBox_G.setGeometry(QtCore.QRect(100, 10, 140, 60))
        # self.checkBox_G.setObjectName("checkBox_G")
        # self.checkBox_Z = QtWidgets.QCheckBox(self.widget_checkBox)
        # self.checkBox_Z.setGeometry(QtCore.QRect(290, 10, 140, 60))
        # self.checkBox_Z.setObjectName("checkBox_Z")
        # self.checkBox_T = QtWidgets.QCheckBox(self.widget_checkBox)
        # self.checkBox_T.setGeometry(QtCore.QRect(390, 10, 140, 60))
        # self.checkBox_T.setObjectName("checkBox_T")
        # self.checkBox_K = QtWidgets.QCheckBox(self.widget_checkBox)
        # self.checkBox_K.setGeometry(QtCore.QRect(490, 10, 140, 60))
        # self.checkBox_K.setObjectName("checkBox_K")
        # self.label_type = QtWidgets.QLabel(self.widget_checkBox)
        # self.label_type.setGeometry(QtCore.QRect(10, 10, 140, 60))
        # self.label_type.setObjectName("label_type")
        #
        MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 848, 23))
        # self.menubar.setObjectName("menubar")
        # self.menu = QtWidgets.QMenu(self.menubar)
        # self.menu.setObjectName("menu")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        # self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "车票查询"))
        # self.checkBox_T.setText(_translate("MainWindow", "T-特快"))
        # self.checkBox_K.setText(_translate("MainWindow", "K-快速"))
        # self.checkBox_Z.setText(_translate("MainWindow", "Z-直达"))
        # self.checkBox_D.setText(_translate("MainWindow", "D-动车"))
        # self.checkBox_G.setText(_translate("MainWindow", "GC-高铁"))
        # self.label_type.setText(_translate("MainWindow", "车次类型："))
        # # self.label_title_img.setText(_translate("MainWindow", "TextLabel"))
        # # self.label_train_img.setText(_translate("MainWindow", "TextLabel"))
        # self.label.setText(_translate("MainWindow", "出发地："))
        # self.label_2.setText(_translate("MainWindow", "目的地："))
        # self.label_3.setText(_translate("MainWindow", "出发日："))
        # self.pushButton.setText(_translate("MainWindow", "查询"))

def show_MainWindow():
    app = QtWidgets.QApplication(sys.argv) #实例化QApplication类，作为GUI主程序入口
    MainWindow = QtWidgets.QMainWindow() #创建MainWindow类
    ui = Ui_MainWindow() #实例UI类
    ui.setupUi(MainWindow) #设置窗体UI
    MainWindow.show() #显示窗体
    sys.exit(app.exec_()) #当窗体创建完成，需要结束主循环过程

if __name__ == '__main__':
    show_MainWindow()