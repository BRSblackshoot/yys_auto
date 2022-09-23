# -*- encoding=utf8 -*-
#1280*720
import os,time
import cv2
import random
from datetime import datetime
from plyer import notification #pip install plyer

def connect():
    try:
        os.system('adb connect 127.0.0.1:7555')
    except:
        print('连接失败')

def click(list):
    os.system('adb shell input tap %s %s' % (list[0], list[1]))

def screenshot(): 
    path = os.path.abspath('.') + '\images'
    # 改进方式1
    os.system("adb shell screencap -p | sed 's/\\r$//' > " + path+"\screen.png")

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
    i = 0
    while True:
        screenshot()
        if Image_to_position("yongwandaoju.png"):
            Image_to_position("zhuanhuan.png")
            print("道具刷完，切换到体力模式继续刷")
            click(center)
            time.sleep(1)
            click(center)
        if Image_to_position("tiaozhan.png"):
            i=i+1
            print("开始第{}次挑战".format(i))
            click(center)
        if Image_to_position("end.png"):
            click(center)
        if Image_to_position("end2.png"):
            click(center)
        if Image_to_position("shibai.png"):
            print("出现失败")
            click(center)
        if Image_to_position("jujuexiezhu.png"):
            print("出现协助悬赏，拒绝了")
            click(center)
        if Image_to_position("zhandou.png"):
            print("可能卡顿导致后续点击操作点在了空白地带，导致界面从战斗变回了场景，已经解决")
            click(center)
        if Image_to_position("yidashangxian.png"):
            print("已达体力挑战的999上限，任务结束")
            notification.notify(
                title = '阴阳师脚本',
                message = '已达体力挑战的999上限，任务结束',
                app_icon = None,
                timeout = 60,
            )
            break

if __name__ == '__main__':
    connect()
    time.sleep(1)
    run()