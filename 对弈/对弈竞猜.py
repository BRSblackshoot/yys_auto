# -*- encoding=utf8 -*-
#1280*720
import os,time
import cv2
import random
import easyocr 

def connect():
    try:
        os.system('adb connect 127.0.0.1:7555')
    except:
        print('连接失败')

def click(list):
    os.system('adb shell input tap %s %s' % (list[0], list[1]))

def back():
    os.system('adb shell input keyevent 4')

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

def 统计():
    global a
    a+=1
    print("==========================\n完成第%s次\n当前系统时间%s\n=========================="%(a,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())))

def screenshot(): 
    path = os.path.abspath('.') + '\images'
    # 改进方式1
    os.system("adb shell screencap -p | sed 's/\\r$//' > " + path+"\screen.png")

def 截图(): 
    path = os.path.abspath('.') + '\screenshot'
    name = "\\"+time.strftime("%m-%d-%H-%M-%S",time.localtime())+".png"
    print(name)
    os.system("adb shell screencap -p | sed 's/\\r$//' > " + path+name)

def ocr():
    #裁切
    img = cv2.imread("images/screen.png")
    # 裁切区域 裁剪坐标为[点1纵坐标:点2纵坐标, 点1横坐标:点2横坐标] 130-235 534-570 1105,531 1212,575
    img_hong = img[537:572,133:232]
    img_lan = img[531:575,1105:1212]

    try:
        #分别识别双方人数
        result1 = reader.readtext(img_hong)
        hong = int(result1[0][1])
        
        result2 = reader.readtext(img_lan)
        lan = int(result2[0][1])

        if(hong >= lan):
            return True
        else:
            return False
    except:
        #一旦发生异常 就无脑返回True 外部接收到了就无脑选红色方
        print("发生异常，无脑选左边了")
        print("此时识别到的红色为"+result1)
        print("此时识别到的蓝色为"+result2)
        return True

def run():
    #所有if判断之间是有隐含的顺序关系的 先后的判定顺序会影响整个脚本的逻辑
    while True:
        screenshot()
        # 启动游戏 进入对弈界面
        if Image_to_position("yys.png"):
            click(center)
        # 我的账号是渠道服 有时候会弹出选择账号的界面 此时单击账号头像 就能正常执行后续操作了
        if Image_to_position("zhanghao.png"):
            click(center)
        if Image_to_position("jinru.png"):
            click(center)
        if Image_to_position("tingzhong.png"):
            click(center)
        if Image_to_position("duiyianniu.png"):
            click(center)
        # 如果脚本24小时在线 那么在凌晨五点会发现町中出现百鬼夜行 对弈竞猜等界面没了 会导致程序卡住 所以要加这一层判断 自动返回庭院 重进町中
        if Image_to_position("yanjin.png"):
            click(随机数([1060,260]))

        #点开第一眼发现是领取奖励 那么领取 然后重新截图判断 两张图分别是界面显示领取奖励 和 点进去后再次点击屏幕返回对弈界面  (等待)
        if Image_to_position("jiangli1.png"):
            click(center)
            continue
        if Image_to_position("jiangli2.png"):
            click(center)
            continue

        #点开第一眼发现有下一局 直接点击下一局 然后重新截图判断 (等待)
        if Image_to_position("xiayiju.png"):
            click(center)
            time.sleep(1)
            continue
        
        # 如果是待投注状态 进行后续的判断和下注
        if Image_to_position("daitouzhu.png"):
            result = ocr()
            #根据result判断 决定投红 还是投蓝 然后两个分支分别去做
            if(result):
                #投红
                click(随机数([160,400]))
            else:
                #投蓝
                click(随机数([1130,400]))

        #如果当前界面是选择投钱的档位 就会有30W金币的档位 识别到这个大宝箱直接点击 然后等待一下 直接点押注 然后重新截图判断
        if Image_to_position("30.png"):
            click(center)
            time.sleep(1)
            click(随机数([1064,463]))
            time.sleep(1)
            click(随机数([756,432]))
            continue

        #只要检测到返回图标 说明之前要做的操作都完成了 直接点击 跳出循环 然后外部执行线程休眠2小时的操作
        if Image_to_position("jieshu.png"):
            click(center)
            统计()
            break
        
        #如果对弈竞猜处于已投注状态 则直接返回
        if Image_to_position("yitouzhu.png"):
            截图()
            back()

        #如果对弈竞猜处于休息状态 则直接返回
        if Image_to_position("xiuxi.png"):
            截图()
            back()
    
        #如果有人发送了协助之类的 直接点X
        if Image_to_position("jujuexiezhu.png"):
            click(center)
        #如果有人发送了协助之类的 直接点X
        if Image_to_position("tuichu.png"):
            click(center)

def limit():
    # 死循环 每间隔1分钟读取一次当前时间的小时数和分钟数 如果小时数为奇数 并且分钟数处于指定区间 才结束循环
    while True:
        H = time.strftime("%H",time.localtime())
        M = time.strftime("%M",time.localtime())
        if(int(H)%2==1):
            if(int(M)>45 and int(M)<50):
                break
        time.sleep(60)

if __name__ == '__main__':
    connect()
    # 用于统计 执行了多少次竞猜
    global a
    a=0
    # 初始化easyocr 默认安装的是 pytorch 的 cpu 版本 不支持GPU渲染 但是gpu参数默认为True 所以这里手动将gpu设置为False
    reader = easyocr.Reader(['ch_sim','en'],gpu=False)
    # 这个方法就是用来让我不用顾忌啥时候开程序 当分钟数处于指定区间 并且是小时数为奇数 才正式进入后续的操作任务 保证以后的每次竞猜都是在这个区间去读对弈阵容双方的下注人数
    # 不过假设现在是19:51 那就直接手动投了18:00-20:00这轮的对弈吧 因为脚本会一直等到21:46才正式进入后续操作 此时对应的是20:00-22:00的对弈
    limit()
    while True:
        # 现在的对弈都不是24小时了，比如这次是10：00~24：00，所以可以在每次循环时判断当前时间是否在区间内，如果不在那就直接休眠2小时
        H = time.strftime("%H",time.localtime())
        if int(H)>=0 and int(H)<10:
            time.sleep(2*60*60)
        else:
            now1=time.time()
            run()
            now2=time.time()
            #通过计算 确保整个循环大致以2小时为单位
            time.sleep(2*60*60-int((now2-now1)))