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

def window_capture():
    # 获取句柄窗口的大小信息
    hwnd = win32gui.FindWindow(None, "阴阳师 - MuMu模拟器")
    left, top, right, bot = get_window_rect(hwnd)
    width = right-left
    height = bot - top
    hWnd = hwnd
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hWnd, hWndDC)
    # 图像显示
    im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')
    im_opencv.shape = (height, width, 4)
    cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
    cv2.imwrite(".\images\screen.png", im_opencv, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 保存

def connect():
    try:
        os.system('adb connect 127.0.0.1:7555')
    except:
        print('连接失败')

def click(list):
    os.system('adb shell input tap %s %s' % (list[0], list[1]))

def screenshot():
    # nowa = int(round(time.time() * 1000))
    
    path = os.path.abspath('.') + '\images'
    
    # 原始方式
    # os.system('adb shell screencap /data/screen.png')
    # os.system('adb pull /data/screen.png %s' % path)

    # 改进方式1
    # os.system("adb shell screencap -p | sed 's/\\r$//' > " + path+"\screen.png")
    
    # 改进方式2
    # # 使用FindWindow查找指定title的窗口句柄 找不到返回None
    # hwnd = win32gui.FindWindow(None, '阴阳师 - MuMu模拟器')
    # app = QApplication(sys.argv)
    # screen = QApplication.primaryScreen()
    # # 如果hwnd是None 那么就会截取当前屏幕，否则就去截取指定窗口句柄的进程
    # img = screen.grabWindow(hwnd).toImage()
    # img.save(path+"\screen.png")

    # 改进方式3
    window_capture()

    # nowb = int(round(time.time() * 1000))
    # print(nowb-nowa)
    # global shuzu
    # shuzu.append(nowb-nowa)


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
    # global shuzu
    # shuzu =[]
    while 循环开始==1:
        screenshot()
        if Image_to_position("end.png"):
            # print("循环结束:")
            # print(shuzu)
            click(center)
            循环开始 =0
        elif Image_to_position("go.png"):
            # shuzu = []
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