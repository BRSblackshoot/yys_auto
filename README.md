# yys_auto
用来玩阴阳师的各种小程序，比如挂机魂土、挂机各种爬塔活动，全都是源码，练手之作，仅供学习参考
# 魂土
初版：
基于python+opencv+adb 挂机刷魂土的，刷魂十或者别的御魂估计也行，只要都有类似的开始战斗图标

改动1：配合sed命令，将adb截图直接保存在本地，但是速度提升有限
```python
# 挂机程序启动时第一轮战斗 截图17次 平均耗时1603毫秒
[1635, 1661, 1819, 1815, 1190, 1687, 1943, 1820, 2040, 1431, 1910, 1604, 1207, 1433, 1258, 1431, 1368]

# 挂机程序启动后第二轮战斗 截图16次 平均耗时1693毫秒
[1936, 1679, 1910, 2290, 1717, 2167, 1964, 2042, 1369, 1594, 1846, 1445, 1324, 1348, 1321, 1144]

```
改动2：抛弃adb截图，使用PyQt获取模拟器的画面，效果提升显著
```python
# 挂机程序启动时第一轮战斗 截图40次 平均耗时441毫秒
[463, 490, 450, 469, 506, 475, 515, 490, 454, 470, 190, 262, 338, 458, 473, 507, 474, 501, 433, 474, 397, 504, 490, 287, 394, 443, 508, 580, 456, 481, 268, 372, 373, 500, 392, 502, 551, 471, 367, 448]

# 挂机程序启动后第二轮战斗 截图37次 平均耗时490毫秒
[428, 772, 495, 633, 668, 543, 691, 642, 640, 467, 479, 512, 560, 456, 504, 647, 432, 459, 484, 267, 242, 372, 453, 486, 524, 422, 476, 308, 348, 403, 627, 498, 474, 492, 429, 444, 388]

```

改动3：直接使用win32的方法获取模拟器的画面，去掉中间商PyQt，速度提升显著，基本算是0延迟了
```python
# 挂机程序启动时第一轮战斗 截图95次 平均耗时10.6毫秒
[8, 6, 11, 13, 9, 9, 10, 10, 10, 13, 36, 8, 10, 8, 17, 8, 12, 11, 12, 11, 8, 11, 9, 8, 8, 17, 7, 9, 10, 8, 9, 10, 10, 11, 16, 17, 9, 13, 10, 8, 9, 11, 11, 15, 17, 8, 10, 8, 9, 9, 10, 10, 10, 11, 8, 9, 12, 13, 10, 10, 10, 20, 10, 9, 8, 9, 9, 9, 17, 10, 10, 18, 10, 10, 9, 10, 9, 10, 9, 10, 14, 10, 7, 9, 8, 10, 8, 8, 11, 8, 9, 10, 8, 11, 11]

# 挂机程序启动后第二轮战斗 截图89次 平均耗时11.0毫秒
[11, 31, 9, 9, 12, 11, 24, 11, 10, 10, 16, 9, 11, 14, 16, 8, 8, 11, 9, 9, 9, 9, 11, 14, 13, 12, 10, 8, 8, 8, 10, 14, 11, 11, 12, 10, 9, 8, 11, 10, 8, 19, 9, 9, 10, 10, 12, 9, 14, 9, 13, 11, 17, 14, 13, 11, 10, 10, 9, 8, 12, 12, 9, 10, 8, 11, 17, 8, 10, 9, 10, 9, 9, 8, 9, 8, 11, 10, 11, 8, 12, 10, 7, 8, 12, 8, 10, 23, 10]

```

改动4：考虑到后续操作是`cv2.matchTemplate`，因此在调用win32API的基础上，可以不再保存截图，而是使用全局变量直接传递图片数据给`cv2.matchTemplate`
后续操作中，增加了`cv2.cvtColor`等操作，去掉了IO等操作，单次截图速度处于合理的浮动范围，但是可以看到截图频率变高了，这是因为`cv2.matchTemplate`操作中省去了一次`cv2.imread()`，令全局流程耗时降低，整体速度是提升的
```python
# 挂机程序启动时第一轮战斗 截图102次 平均耗时10.4毫秒
[14, 9, 9, 19, 16, 10, 8, 8, 9, 9, 7, 8, 13, 9, 13, 7, 9, 10, 9, 13, 8, 9, 8, 10, 9, 10, 9, 10, 10, 8, 9, 9, 13, 9, 14, 8, 11, 10, 8, 9, 10, 7, 11, 9, 14, 9, 10, 10, 11, 9, 17, 9, 10, 10, 11, 11, 12, 10, 8, 9, 16, 16, 13, 22, 9, 9, 13, 10, 9, 11, 13, 10, 14, 13, 11, 9, 10, 11, 11, 11, 12, 9, 9, 9, 8, 11, 9, 9, 9, 9, 8, 12, 8, 12, 10, 8, 10, 11, 11, 10, 9, 10]

# 挂机程序启动后第二轮战斗 截图93次 平均耗时12.0毫秒
[13, 14, 7, 9, 14, 9, 8, 9, 9, 7, 8, 9, 15, 13, 40, 13, 10, 26, 13, 12, 14, 14, 13, 10, 20, 14, 10, 10, 11, 12, 15, 13, 9, 11, 8, 13, 9, 18, 13, 11, 13, 23, 14, 13, 32, 13, 19, 15, 9, 11, 11, 10, 12, 16, 17, 12, 7, 9, 9, 10, 9, 11, 13, 8, 9, 8, 9, 12, 11, 10, 13, 14, 8, 10, 11, 9, 11, 10, 9, 11, 18, 14, 10, 8, 9, 11, 11, 8, 9, 9, 9, 8, 8]

```

## 对比选择
对比几种方式，可以发现，速度最快的是方式六手动调用win32 api获取图片数据并使用全局变量传递数据，但是adb可以配合模拟器后台运行，而win32 api要求软件不能后台运行且不能最小化，所以要根据实际需求进行选取

# GUI
在魂土程序的基础上，学习用PYQT5做界面，魂土挂机.py就是把功能源码嵌入界面，魂土挂机-信号.py就是在把功能嵌入界面后基于信号解决界面阻塞问题
后面我又基于魂土挂机-信号.py玩了一下pyinstaller，有兴趣可以试一试
# 不见岳
本来是想玩一玩AI的，训练一下，但是突然发现活动和上次铃彦姬的塔不一样，不需要决策，扒拉一下屏幕，点一下终点就完事了，官方小人会自己跑向终点，就用python+opencv+adb实现功能
做得挺简单的，遇到答题我直接摆烂点第一个，遇到迷雾我就退出重进（23333 别问 问就是懒得写复杂的）
不过借机学了一些python快速获取屏幕截图的方法，比如win32接口，但是这个源码没放出来，等下次阴阳师出爬塔活动再说吧（咕）
