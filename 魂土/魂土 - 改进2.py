# -*- encoding=utf8 -*-
#1280*720
import os,time
import cv2
import random
from datetime import datetime

from PyQt5.QtWidgets import QApplication
import sys
import win32gui

def connect():
    try:
        os.system('adb connect 127.0.0.1:7555')
    except:
        print('连接失败')

def click(list):
    os.system('adb shell input tap %s %s' % (list[0], list[1]))

def screenshot():
    nowa = int(round(time.time() * 1000))
    
    path = os.path.abspath('.') + '\images'
    
    # 改进方式2
    # 使用FindWindow查找指定title的窗口句柄 找不到返回None
    hwnd = win32gui.FindWindow(None, '阴阳师 - MuMu模拟器')
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    # 如果hwnd是None 那么就会截取当前屏幕，否则就去截取指定窗口句柄的进程
    img = screen.grabWindow(hwnd).toImage()
    img.save(path+"\screen.png")

    nowb = int(round(time.time() * 1000))
    print(nowb-nowa)
    global shuzu
    shuzu.append(nowb-nowa)

def Image_to_position(image, m = 0):
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
        center=随机数(center)
        print(center)
        # return center
        return True
    else:
        return False

def 随机数(list):
    list[0]+=random.randint(0,5)
    list[1]+=random.randint(0,5)
    return list

def run():
    global 循环开始
    循环开始=1
    global shuzu
    shuzu =[]
    while 循环开始==1:
        screenshot()
        if Image_to_position("end.png"):
            print("循环结束:")
            print(shuzu)
            click(center)
            循环开始 =0
        elif Image_to_position("go.png"):
            shuzu = []
            click(center)
            

def 统计():
    print("==========================\n完成第%s次\n当前系统时间%s\n本次执行用时%s\n=========================="%(a,time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()),now2-now1))

#times 设置刷图次数
times = 120
a = 0

if __name__ == '__main__':
    connect()
    time.sleep(1)
    while times>=0:
        now1=datetime.now()
        run()
        times-=1
        a+=1
        now2=datetime.now()
        统计()