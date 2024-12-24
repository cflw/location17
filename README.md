# Location17

适用于iOS 17.x的虚拟定位程序。由于iOS 17.x之后修改定位方式发生变化，以前的虚拟定位程序均已失效，于是仿照location-cleaned写了一个新的虚拟定位程序。

![](./主窗口图.png)

特点：
* 支持iOS 17.x（测试可用的iOS版本：17.5.1~17.7、18.0~18.2）
* 离线使用，无需联网
* 地址管理功能，提前保存地址信息，需要时直接定位到保存的地址
* **没有**地图选点功能，请自行通过其他地图服务获取坐标数据

许可证：
* ![cc-by-nc-image](https://licensebuttons.net/l/by-nc/4.0/88x31.png) [知识共享-署名-非商业性使用 4.0](https://creativecommons.org/licenses/by-nc/4.0/legalcode.zh-hans)

我不是location-cleaned的作者，请不要询问我有关location-cleaned的问题。

## 使用方法

1、下载/克隆本仓库到本地电脑。

2、确保电脑中已安装Python3和第三方库：
* [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)
* [async-tkinter-loop](https://github.com/insolor/async-tkinter-loop)

```
pip install pymobiledevice3 async-tkinter-loop
```

3、数据线连接苹果手机，确保手机已启用开发者模式，且手机处于解锁状态。

4、进入仓库目录，**管理员权限**执行：

```
pythonw 程序.py
```

会弹出程序窗口，开始使用吧。

## 常见问题

**点【修改定位】后，手机定位在修改位置和实际位置反复横跳**

iOS 17之后的系统具有非常快的定位矫正，目前没有完美解决办法。Location17的做法是点【修改定位】后频繁向手机发送修改定位命令使位置固定，又因为系统自动矫正，看到的现象就是定位反复横跳。根据观察，手机定位到修改位置的时间大概占【修改定位】期间的90%以上，基本能用。

**点【还原定位】后手机定位没有还原**

还原定位有延迟，稍等一会就行。如果急着还原定位可以重启手机。

**修改的定位和实际位置有偏差**

由于国家安全原因，国内地图服务给的坐标是偏移的，偏移量几百米不等，偏移方向不固定，也没有纠正算法（出现即违法），所以修改的定位和实际位置有偏差，需要微调。

**没有显示手机**

可以打开iTunes查看是否显示手机，如果iTunes没有显示手机，那么Location17一样不会显示手机。

## 附：获取坐标方法

打开百度地图拾取坐标系统：https://api.map.baidu.com/lbsapi/getpoint/index.html

在地图上点击，会显示对应坐标。
