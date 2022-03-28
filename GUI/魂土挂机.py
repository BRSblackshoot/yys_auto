# -*- coding: utf-8 -*-

from PyQt5 import QtCore,QtWidgets 

import os,time
import cv2
import random
from datetime import datetime
import sys
import subprocess

from threading import Thread

import inspect
import ctypes

class Ui_MainWindow(object):
    #定义全局变量
    kaiguan =0
    次数=0
    对局次数=0
    now1=0
    now2=0

    #别人写好的自定义函数，用于实现停止指定子线程
    def _async_raise(self,tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    #封装上面写的自定义函数 
    def stop_thread(self,thread):
        self._async_raise(thread.ident, SystemExit)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(359, 340)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(12, 60, 241, 251))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(270, 300, 77, 12))
        self.label_2.setObjectName("label_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(13, 33, 241, 22))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(270, 30, 77, 161))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget1)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_3.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #关联按钮和函数
        self.pushButton.clicked.connect(self.init)
        self.pushButton_2.clicked.connect(self.star)
        self.pushButton_3.clicked.connect(self.end)
        self.pushButton_4.clicked.connect(self.textEdit.clear)

        #禁用按钮，避免用户误触
        self.pushButton_3.setEnabled(False)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "自动挂魂土"))
        self.label_2.setText(_translate("MainWindow", "版本:V1.0"))
        self.label.setText(_translate("MainWindow", "刷图次数"))
        self.pushButton.setText(_translate("MainWindow", "初始化"))
        self.pushButton_2.setText(_translate("MainWindow", "开始"))
        self.pushButton_3.setText(_translate("MainWindow", "停止"))
        self.pushButton_4.setText(_translate("MainWindow", "清空"))

    def init(self):
        try:
            subprocess.run("adb connect 127.0.0.1:7555",shell=True)
            self.textEdit.append("连接成功")
            #使用全局变量 需要声明
            global kaiguan
            global 次数
            kaiguan=1
            #读到的是字符串格式
            次数=self.lineEdit.text()
            if 次数 == "":
                次数=40
                self.textEdit.append("未给定刷图次数，预设为40次")
            elif 次数 =="0":
                次数=10000
                self.textEdit.append("给定刷图次数为“无限”")
            else:
                self.textEdit.append("给定刷图次数为%s" %(次数))
                次数=int(次数)
        except:
            self.textEdit.append("连接失败")

    def star(self):
        global kaiguan
        global 对局次数
        global t
        if kaiguan==1:
            对局次数=0
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(True)
            t = Thread(target=self.执行循环)
            t.start()
        else:
            self.textEdit.append("还未初始化脚本，请点击初始化按钮连接模拟器")
    
    def 执行循环(self):
        global 次数
        global now1
        global now2
        global 对局次数

        while 次数>=0:
            now1=datetime.now()
            self.run()
            次数=次数-1
            对局次数=对局次数+1
            now2=datetime.now()
            self.统计()

    def click(self,list):
        subprocess.run('adb shell input tap %s %s' % (list[0], list[1]),shell=True)
        # os.system('adb shell input tap %s %s' % (list[0], list[1]))

    def screenshot(self):
        path = os.path.abspath('.') + '\images'
        subprocess.run("adb shell screencap /data/screen.png",shell=True)
        # os.system('adb shell screencap /data/screen.png')
        subprocess.run('adb pull /data/screen.png %s' % path,shell=True)
        # os.system('adb pull /data/screen.png %s' % path)

    def Image_to_position(self,image, m = 0):
        image_path = 'images/' + str(image)
        screen = cv2.imread('images/screen.png', 1)
        Image_to_position = cv2.imread(image_path, 1)
        methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED]
        image_x, image_y = Image_to_position.shape[:2]
        result = cv2.matchTemplate(screen, Image_to_position, methods[m])
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print(max_val)
        if max_val > 0.9:
            global center
            center = [max_loc[0] + image_y / 2, max_loc[1] + image_x / 2]
            center=self.随机数(center)
            print(center)
            # return center
            return True
        else:
            return False

    def 随机数(self,list):
        list[0]+=random.randint(0,5)
        list[1]+=random.randint(0,5)
        return list

    def run(self):
        global 循环开始
        循环开始=1
        while 循环开始==1:
            self.screenshot()
            if self.Image_to_position("end.png"):
                self.click(center)
                循环开始 =0
            elif self.Image_to_position("go.png"):
                self.click(center)

    def 统计(self):
        self.textEdit.append("==========================\n完成第%s次\n当前系统时间%s\n本次执行用时%s"%(对局次数,time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()),now2-now1))
        #令指定控件自动翻滚到最新的记录
        self.textEdit.ensureCursorVisible()

    def end(self):
        global t
        # os.system('adb kill-server')
        subprocess.run('adb kill-server',shell=True)
        
        self.stop_thread(t)
        self.textEdit.append("脚本已停止")
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(False)
        global kaiguan
        global 次数
        global now1
        global now2
        global 对局次数

        kaiguan =0
        次数=0
        对局次数=0
        now1=0
        now2=0

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

