# -*- encoding=utf8 -*-
#1280*720
import os,time
import cv2
import random
from datetime import datetime
import numpy as np

def connect():
    try:
        os.system('adb connect 127.0.0.1:7555')
    except:
        print('连接失败')

def click(list):
    os.system('adb shell input tap %s %s' % (list[0], list[1]))
    time.sleep(1)

def screenshot():
    path = os.path.abspath('.') + '\images'
    os.system('adb shell screencap /data/screen.png')
    os.system('adb pull /data/screen.png %s' % path)

def 随机数(list):
    list[0]+=random.randint(0,5)
    list[1]+=random.randint(0,5)
    return list

def 长按1():
    #屏幕下移
    os.system("adb shell input swipe 628 60 628 60 3000")

def 长按2():
    #屏幕上移
    os.system("adb shell input swipe 628 690 628 690 3000")

def 统计():
    print("==========================\n完成第%s次\n当前系统时间%s\n本次执行用时%s\n=========================="%(a,time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()),now2-now1))

def Image_to_position(image, m = 0):
    image_path = 'images/' + str(image)
    screen = cv2.imdecode(np.fromfile('images/screen.png', dtype=np.uint8),-1)
    # screen = cv2.imread('images/screen.png', 1)
    Image_to_position = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8),-1)
    # Image_to_position = cv2.imread(image_path, 1)
    methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED]
    image_x, image_y = Image_to_position.shape[:2]
    result = cv2.matchTemplate(screen, Image_to_position, methods[m])
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # print(max_val)
    if max_val > 0.9:
        global center
        center = [max_loc[0] + image_y / 2, max_loc[1] + image_x / 2]
        center=随机数(center)
        # return center
        return True
    else:
        return False

def 找入口():
    time.sleep(1)
    #截图
    screenshot()
    if Image_to_position("下一层入口.png"):
        print("找到入口 点击入口")
        click(center)
    #如果没找到 滑屏再找一次
    else:
        长按1()
        time.sleep(1)
        screenshot()
        # 滑屏之后基本都能找到
        if Image_to_position("下一层入口.png"):
            print("找到入口 点击入口")
            click(center)
        else:
            长按2()
            time.sleep(1)
            screenshot()
            if Image_to_position("下一层入口.png"):
                print("找到入口 点击入口")
                click(center)
            else:
                #退出重进 因为本次活动有迷雾机制
                click([59,54])
                time.sleep(1)
                click([674,377])

def 取消奖励弹窗():
    time.sleep(1)
    click([82,369])

def 遭遇战斗():
    print("遭遇战斗")
    # 等待一段时间判断战斗是否结束
    while True:
        time.sleep(5)
        screenshot()
        if Image_to_position("战斗结束.png"):
            print("战斗结束")
            click(center)
            break

def run():
    global 循环开始
    循环开始=1
    while 循环开始==1:
        print("新一轮循环")
        找入口()
        #点击下一层入口后 小人自动行走 并且会遭遇各种事件
        screenshot()
        if Image_to_position("遭遇战斗.png"):
            click(center)
            遭遇战斗()
            continue
        if Image_to_position("遭遇宝箱.png"):
            print("遭遇宝箱")
            Image_to_position("确认.png")
            click(center)
            # 接着屏幕显示获得的奖励 要点击空白处取消弹窗
            取消奖励弹窗()
            # 重新找入口
            continue
        if Image_to_position("遭遇云道.png"):
            print("遭遇云道")
            Image_to_position("取消云道.png")
            click(center)
            #穿过云道后可能拿到奖励 此时要点击空白处取消弹窗
            取消奖励弹窗()
            # 重新找入口
            continue
        if Image_to_position("遭遇答题.png"):
            print("遭遇答题")
            #点击第一个答案
            click([691,263])
            time.sleep(1)
            screenshot()
            if Image_to_position("答题获得奖励.png"):
                取消奖励弹窗()
                continue
            else:
                遭遇战斗()
                continue
        if Image_to_position("进入下一层.png"):
            print("进入下一层")
            Image_to_position("确认.png")
            click(center)
            time.sleep(1)
            screenshot()
            if Image_to_position("抉择资源.png"):
                Image_to_position("选定资源按钮.png")
                click(center)
                # 最后一次确认
                time.sleep(1)
                screenshot()
                Image_to_position("确认.png")
                click(center)
                

if __name__ == '__main__':
    connect()
    time.sleep(1)
    global a
    a = 0
    while True:
        now1=datetime.now()
        run()
        a+=1
        now2=datetime.now()
        统计()