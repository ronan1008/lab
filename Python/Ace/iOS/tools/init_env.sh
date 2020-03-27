#!/bin/bash
#brew install libimobiledevice --HEAD
TEAM_ID=''
deviceid=`idevice_id -l`
echo ${deviceid}
#通過USB 通道測試iOS 真機
brew install usbmuxd
#應用中如含有WebView
brew install ios-webkit-debug-proxy
npm i -g macaca-cli
brew install ideviceinstaller
brew install ios-webkit-debug-proxy
npm i macaca-ios -g
npm uninstall -g macaca-ios
# 安装有 TEAM_ID 的 macaca-ios
DEVELOPMENT_TEAM_ID=$TEAM_ID npm i macaca-ios -g
DEVELOPMENT_TEAM_ID=$TEAM_ID cnpm install app-inspector -g
