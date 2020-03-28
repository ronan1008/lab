#!/bin/bash

java_version=`java --version | head -1 | awk '{print $2}'`

if [ -z "$java_version" ]
then
    echo "Download Java : https://www.oracle.com/java/technologies/javase-jdk13-downloads.html"
    echo "Download Android Studio : https://developer.android.com/studio"
    echo "在android studio 裡面的 Configure->SDK Manager\nAndroid SDK->SDK Tools 把 Hide Obsolete Packages 取消\n安裝Android SDK Tooks(Obsolete)"
else
    javaHome=`/usr/libexec/java_home`

cat << EOF >> $HOME/.bash_profile
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=\$PATH:\$ANDROID_HOME/tools
export PATH=\$PATH:\$ANDROID_HOME/tools/bin
export PATH=\$PATH/:\$ANDROID_HOME/platform-tools
export JAVA_HOME=$javaHome
export PATH=\$JAVA_HOME/bin:\$PATH
EOF
    source $HOME/.bash_profile
fi

nodejs_version=`node -v`

if [ -z "$nodejs_version" ]
then
    brew install node
    node -v
    npm -v
    npm install appium-doctor -g
    appium-doctor --android
else
    echo "nodejs had been installed"
    node -v
    npm -v
    appium-doctor --android
fi
