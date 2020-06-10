#!/bin/bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
xcode_version=`/usr/bin/xcodebuild -version`
if [ -z "$xcode_version" ]
then
    echo "Please install xcode first"
else
    #Cocoa 開發第三方套件管理工具
    brew install carthage
    brew tap wix/brew
    brew install wix/brew/applesimutils
    
    sudo xcode-select --install
    sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer


    #libimobiledevice(真機測試需要)
    brew install libimobiledevice

    #ios-deploy(真機測試需要)
    brew install ios-deploy
    gem install xcpretty
fi

if [ -z "`node -v`" ]
then
    brew install node
    node -v
    npm -v
    npm install appium-doctor -g
    appium-doctor --ios
else
    echo "nodejs had been installed"
    node -v
    npm -v
    appium-doctor --ios
fi