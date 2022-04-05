# -*- encoding=utf8 -*-
#1280*720
import os,time
import cv2
import random
from datetime import datetime

from PyQt5.QtWidgets import QApplication
import sys
import win32gui

import numpy
import win32ui
import win32con

def get_window_rect(hwnd):
    '''
    获取窗口坐标
    :param hwnd: 句柄所在指针
    :return: 元组（rect.left, rect.top, rect.right, rect.bottom）
    '''
    import ctypes.wintypes
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        return rect.left, rect.top, rect.right, rect.bottom

def window_capture(name):
    # 获取指定窗口的句柄，win32gui.Findwindow(param1,param2) param1:需要传入窗口的类名 param2:需要传入窗口的标题
    # 这里的name为窗口标题，比如"阴阳师 - MuMu模拟器"
    hWnd = win32gui.FindWindow(None, name)
    # 使用自定义方法获取指定窗口的坐标
    left, top, right, bot = get_window_rect(hWnd )
    # 计算出窗口宽高
    width = right-left
    height = bot - top
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表 实际在内存开辟空间(将位图BitBlt至屏幕缓冲区(内存)，而不是将屏幕缓冲区替换成自己的位图。同时解决绘图闪烁等问题)
    neicunDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    # 为位图对象开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将位图对象保存到刚开辟的内存里
    neicunDC.SelectObject(saveBitMap)
    
    # 截取刚才保存到内存中的位图对象的指定范围信息，可以全部截取，然后将截取的这些信息保存在剪贴板
    # 剪贴板是Windows系统一段可连续的，可随存放信息的大小而变化的内存空间，用来临时存放交换信息，
    # 只能保留一份数据，每当新的数据传入，旧的便会被覆盖，平时使用的qq截图、微信截图就是将截好的图放置在剪贴板，然后在QQ/微信窗口粘贴才将截图从剪贴板中取出来
    # BitBle函数需要输入6个参数：
    # 第一参数(w1,w2),指在位图里显示的左上角顶点，一般为(0,0)，若不为(0,0)，应用位图无法覆盖的地方为黑色背景
    # 第二、第三参数width，height 最终截图的长宽(一般与上面设置的位图大小一致)
    # 第四参数指窗口的mfcDC。
    # 第五参数(x,y)指应用截图起点的逻辑坐标(设备坐标指相对于屏幕左上角为起点的坐标，逻辑坐标指相对于应用窗口左上角的坐标)。
    # 第六参数win32con.SRCCOPY，指用复制的方法截取，其他参数可百度光栅操作代码。
    # 整个逻辑是内存作为黑色背景墙，第二层为位图，第三层为我们需要截图的位置。
    # 所以BitBle的第一个参数是位图放置在黑色背景墙的位置(内存)，以黑色背景墙左上角为起点，(w1,w2)为位图左上角顶点的位置。放置好位图后，在位图上截图，截图的长为width，宽为height。截图的起始位置(相对于应用窗口左上角顶点的位置坐标)为(x，y)
    neicunDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    
    # 下面的操作都是对内存进行的，所以上述操作中创建内存空间，把位图放到内存空间中都是必要操作，别看下面没使用neicunDC就以为上面的操作没有用
    
    # 以下操作相当于手动实现cv2.imread()
    # 将位图每个像素的rg和B值转为一个整数 形成一个数组
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    # 将数组信息转为图片信息
    # 将numpy.ndarray转换为OpenCV图像的关键点就是numpy.ndarray中的每个元素的dtype应该为numpy.uint8
    global im_opencv
    im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')
    # 设置图片信息的宽高及通道数 这里通道数为4
    im_opencv.shape = (height, width, 4)
    # 将深度通道处理 否则后续使用MatchTemplate时会报错 如果不用MatchTemplate可以不做这一步 
    # 由于后续直接从内存取出来取比对cv2.imread读取到的数据 而cv2.imread读取到的图片颜色空间默认为BGR 所以这里在处理通道时，是BGRA2BGR
    im_opencv = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)

    # 最后一步 手动释放内存
    win32gui.DeleteObject(saveBitMap.GetHandle())
    neicunDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hWnd, hWndDC)

def connect():
    try:
        os.system('adb connect 127.0.0.1:7555')
    except:
        print('连接失败')

def click(list):
    os.system('adb shell input tap %s %s' % (list[0], list[1]))

def screenshot():
    nowa = int(round(time.time() * 1000))

    window_capture("阴阳师 - MuMu模拟器")

    nowb = int(round(time.time() * 1000))
    print(nowb-nowa)
    global shuzu
    shuzu.append(nowb-nowa)

def Image_to_position(image, m = 0):
    image_path = 'images/' + str(image)
    global im_opencv
    Image_to_position = cv2.imread(image_path, 1)
    methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED]
    image_x, image_y = Image_to_position.shape[:2]
    result = cv2.matchTemplate(im_opencv, Image_to_position, methods[m])
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