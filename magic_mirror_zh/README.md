# Magic Mirror with Voice Assistant

[Magic Mirror](https://github.com/MichMich/MagicMirror) is a super popular open source modular smart mirror project.
In this guide, we use ReSpeaker 4 Mic Linear Array to add voice interface to a Magic Mirror.

[>>中文版](magic_mirror_zh.md)

## Hardware
1. Raspberry Pi 3B
2. ReSpeaker 4 Mic Linear Array（sound card）
3. HDMI display
4. two way mirror
5. frame
6. SD card

![](https://user-images.githubusercontent.com/948283/44985869-7d8a7480-afb4-11e8-9aed-97a93384348d.jpg)

## Setup Raspberry Pi
1. Download [a customized pi image](https://v2.fangcloud.com/share/7395fd138a1cab496fd4792fe5?folder_id=188000207913&lang=en)，
   which includes the sound card's driver and some voice related packages (Do not use the lite version for we need desktop enviroment to show GUI).
   We can write the image to a SD card with [rufus](https://rufus.akeo.ie/) (very tiny but only for windows) or [ether](https://etcher.io/).

2. If you don't have any extra keyboard to access and configure the Raspberry Pi， you can setup WiFi configuratio and enable SSH before first time boot.
   To do that, Juse add a file named `ssh` to the boot partition of the SD card, which enables SSH, and then create a file named `wpa_supplicant.conf` with the following content, replace `ssid` and `psk` with yours
   
   ```
   country=GB
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1
   network={
	    ssid="WiFi SSID"
	    psk="password"
   }
   ```
   
3. Power on your Pi， use Pi's IP or `raspberry.local`（requires mDNS support， need to install Bonjour on Windows） to login via ssh
   (On Windows, [putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) is a handy ssh client).

## Install Magic Mirror
1. To install Magic Mirror software package， just run：

   ```
   bash -c "$(curl -sL https://raw.githubusercontent.com/MichMich/MagicMirror/master/installers/raspberry.sh)"
   ```
   This command will clone MagicMirror repository from github to `~/MagicMirror`， install node, npm and other dependencies.

   >Note: Do not use `apt install` to install node and npm, node and npm in the deb repository is kind of outdated. Remove them if already installed.
   
2. Install Magic Mirror modules: MMM-Remote-Control and MMM-kalliope

   ```
   cd ~/MagicMirror/modules
   git clone https://github.com/kalliope-project/MMM-kalliope.git
   git clone https://github.com/Jopyth/MMM-Remote-Control.git
   cd MMM-Remote-Control
   npm install
   ```
   and then add the configuration of MMM-Remote-Control and MMM-kalliope to `moddules` of `~/MagicMirror/config/config.js` 
   ```
   {
       module: "MMM-kalliope",
       position: "upper_third",
       config: {
           title: "",
           max: 1
       }
   },
   {
       module: 'MMM-Remote-Control'
       // uncomment the following line to show the URL of the remote control on the mirror
       // , position: 'bottom_left'
       // you can hide this module afterwards from the remote control itself
   },
   ```
   restart MagicMirror to enable the new configuration.
   Use the following command to test if we can send a message to MagicMirror
   ```
   curl -H "Content-Type: application/json" -X POST -d '{"notification":"KALLIOPE", "payload": "my message"}' http://localhost:8080/kalliope
   ```

3. Configure Weather module

   By default, a weather module using [OpenWeatherMap](https://home.openweathermap.org) is included， we need sign up OpenWeatherMap to get a API key and
   fill the key to `~/MagicMirror/config/config.js`
   
## Set Google Assistant
1. Go to [Introduction to the Google Assistant Library](https://developers.google.com/assistant/sdk/guides/library/python/) to install and setup Google Assistant Library

2. After authorization, we can just run [mirror_with_google_assistant.py](mirror_with_google_assistant.py) to start the Google Assistant for the Mirror.


![](https://user-images.githubusercontent.com/948283/44985871-7e230b00-afb4-11e8-860b-7b3ce3f57585.jpg)

![](https://user-images.githubusercontent.com/948283/44985870-7e230b00-afb4-11e8-8c97-d61494bfca42.jpg)

## To do
As we are using a 4 Mic Linear Array, we are able to detect sound Direction of Arrial (DOA) which can be used to provide some creative functions. We can use beamforming to enhance a specific direction's sound.
