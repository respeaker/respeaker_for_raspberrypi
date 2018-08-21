# 中文版Magic Mirror

[Magic Mirror](https://github.com/MichMich/MagicMirror)是一个非常受欢迎的开源项目，其目标是DIY极具科技感且可以日常使用的镜子。
这里我们将结合Magic Mirror和出门问问的语音SDK打造一个中文语音交互的魔境。

## 硬件
1. 树莓派（Raspberry Pi 3B)
2. ReSpeaker 4 Mic Linear Array（声卡，麦克风阵列）
3. HDMI显示器
4. 双向镜
5. 外框（需要一些木材自制）
6. SD卡

## 配置树莓派
1. 下载[定制的pi镜像](https://v2.fangcloud.com/share/7395fd138a1cab496fd4792fe5?folder_id=188000207913&lang=en)，
   里面内置ReSpeaker声卡驱动等，不要使用lite版本，因为需要桌面显示GUI,烧写SD卡（可以用[rufus](https://rufus.akeo.ie/)或[ether](https://etcher.io/))
   
2. 如果没有USB键盘或网线配合树莓派使用，在烧写完SD卡之后，第一启动SD之前，可以配置好WiFi和SSH。在SD卡的boot分区创建名为ssh的文件，以启用SSH，
   然后在创建`wpa_cupplicant.conf`，里面的内容模板如下，更新其中的`ssid`和`psk`
   
   ```
   country=CN
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1
   network={
	    ssid="WiFi SSID"
	    psk="password"
   }
   ```
   
3. 用SD卡启动树莓派，用树莓派的IP或者`raspberry.local`（需mDNS支持，Windows中要安装Bonjour）通过SSH访问树莓派。
   Windows中SSH客户端可以用[putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)

## 安装 Magic Mirror
1. 安装Magic Mirror软件，注意不要用apt安装node和npm，运行：

   ```
   bash -c "$(curl -sL https://raw.githubusercontent.com/MichMich/MagicMirror/master/installers/raspberry.sh)"
   ```
   这个命令会从github上克隆MagicMirror仓库到`~/MagicMirror`，安装node、npm和Magic Mirror的依赖。
   
2. 安装 Magic Mirror 的扩展模块 MMM-Remote-Control 和 MMM-kalliope

   ```
   cd ~/MagicMirror/modules
   git clone https://github.com/kalliope-project/MMM-kalliope.git
   git clone https://github.com/Jopyth/MMM-Remote-Control.git
   cd MMM-Remote-Control
   npm install
   ```
   然后在`~/MagicMirror/config/config.js`的`moddules`中添加 MMM-Remote-Control 和 MMM-kalliope 的配置
   ```
   {
       module: "MMM-kalliope",
       position: "upper_third",
       config: {
           title: "Kalliope"
       }
   },
   {
       module: 'MMM-Remote-Control'
       // uncomment the following line to show the URL of the remote control on the mirror
       // , position: 'bottom_left'
       // you can hide this module afterwards from the remote control itself
   },
   ```
   配置会在MagicMirror重启后生效。
   可以一下命令测试发送消息到MagicMirror
   ```
   curl -H "Content-Type: application/json" -X POST -d '{"notification":"KALLIOPE", "payload": "my message"}' http://localhost:8080/kalliope
   ```

3. 配置天气模块

   镜子上可以显示天气信息，但需要调用[OpenWeatherMap](https://home.openweathermap.org)的API，所以要注册OpenWeatherMap获取API key。
   获得key之后，填入`~/MagicMirror/config/config.js`
   
## 配置出门问问语音SDK
1. 克隆 `voice-engine/wenwen`

   ```
   cd ~
   git clone https://github.com/voice-engine/wenwen.git
   cd wenwen
   ```
2. 下载[出门问问Linux SDK](https://ai.chumenwenwen.com/pages/document/intro?id=download)，把压缩包中`lib`和`.mobvoi`解压到`wenwen`目录

   ```
    wenwen
    ├── .mobvoi
    ├── lib
    ├── assistant.py
    ├── offline.py
    └── player.py
   ```
3. 离线模式，运行`python offline.py`离线识别“开灯”、“关灯”、“播放音乐”等语音命令
4. 在线模式，在https://ai.chumenwenwen.com，注册出门问问开发者帐号，创建一个应用，获得应用的KEY，并填入`wenwen/assistan.py`
5. 运行`python wenwen/assistant.py`，用”你好问问“唤醒，然后语音对话

## 将Magic Mirror与问问结合
集成问问语音交互的代码就在这个仓库中，放在定制镜像的`~/respeaker`位置，运行以下命令进行配置

```
[ ! -d ~/respeaker ] && git clone https://github.com/respeaker/respeaker_for_raspberrypi.git ~/respeaker
cd respeaker
git pull origin master
cd magic_mirror_zh
ln -s ~/wenwen .
```

将出门问问应用的KEY填到`mirror.py`中，然后运行`python mirror.py`，就可以用“魔镜魔镜”唤醒镜子。


   
   
