#!/bin/bash

#java version
java_version=`java --version | head -1 | awk '{print $2}'`

if [ -z "$java_version" ]
then
    echo "Download Java : https://mac.filehorse.com/download-java-development-kit/14709/"
    echo "Download Android Studio : https://developer.android.com/studio"
    echo "在android studio 裡面的 Configure->SDK Manager\nAndroid SDK->SDK Tools 把 Hide Obsolete Packages 取消\n安裝Android SDK Tooks(Obsolete)"
else
    javaHome=`/usr/libexec/java_home`
fi

#java home
java_home=`grep "JAVA_HOME" /$HOME/.bash_profile`

if [ -z "$java_home" ]
then
cat << EOF >> $HOME/.bash_profile
export JAVA_HOME=$javaHome
export PATH=\$JAVA_HOME/bin:\$PATH
EOF
else
    echo "JAVA_HOME had been setted"
fi

#android home
andro_home=`grep "ANDROID_HOME" /$HOME/.bash_profile`

if [ -z "$andro_home" ]
then
cat << EOF >> $HOME/.bash_profile
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=\$PATH:\$ANDROID_HOME/tools
export PATH=\$PATH:\$ANDROID_HOME/tools/bin
export PATH=\$PATH/:\$ANDROID_HOME/platform-tools
EOF
else
    echo "ANDROID_HOME had been setted"
fi

source $HOME/.bash_profile

#node js
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
