#! /bin/bash
function helpmenu {
     echo "usage: $0 [options1] [options2]" >&2
     echo " " >&2
     echo "options1:" >&2
     echo "         -a   (appium) [start|stop|restart] " >&2
     echo "         -d   (device) [iOS|Android] " >&2
     echo "options2:" >&2
     echo "         -l   show app list in device" >&2
     echo "         -i   show device info" >&2
     echo "         -x   execute Apple Xcode or Android uiautomatorviewer" >&2
     echo "         -r   restart adb server(android only)" >&2
     echo " " >&2
     echo " Appium : " >&2
     echo "      執行Appium : sh $0 -a start" >&2
     echo "      停止Appium : sh $0 -a stop" >&2
     echo "      重啟Appium : sh $0 -a restart" >&2
     echo " iOS : " >&2
     echo "      執行iOS裝置的Xcode         :  sh  $0 -d iOS -x" >&2
     echo "      顯示iOS裝置的自動化資訊    :  sh  $0 -d iOS -i" >&2
     echo "      顯示iOS裝置的所有 app 列表 :  sh  $0 -d iOS -l" >&2
     echo "      檢查iOS的自動化環境        :  sh  $0 -d iOS -c" >&2
     echo " Android : " >&2

     echo "      執行Android裝置的UIAutomator   :  sh  $0 -d Android -x" >&2
     echo "      重啟Android的adb Command       :  sh  $0 -d Android -r" >&2
     echo "      顯示Android裝置的自動化資訊    :  sh  $0 -d Android -i" >&2
     echo "      顯示Android裝置的所有 app 列表 :  sh  $0 -d Android -l" >&2
     echo "      檢查Android的自動化環境        :  sh  $0 -d Android -c" >&2
}
optspec=":a:d:clixr"
while getopts "$optspec" optchar
do
	case $optchar in
    	a)
			appium=$OPTARG;
			;;
		d)
			device=$OPTARG;
			;;
        c)
			check="1";
			;;
		l)
			show_app_list="1";
			;;
		i)
			show_info="1";
			;;
		x)
			execute="1";
			;;
		r)
			restart_adb="1";
			;;
	    *)
			helpmenu
			exit
			;;
	esac
done


if [ "$appium" == "start" ]; then
    appium&
    if [ $? -eq 0 ]; then
        echo "Appium Start Success."
        exit 0
    else
        echo "Appium Start Failed!"
        exit 1
    fi

elif [ "$appium" == "stop" ]; then
    appium_pid=`ps aux | grep [a]ppium | grep -v 'exclude' | awk '{print $2}'`
    if [ -z "$appium_pid" ];then
        echo 'No Appium Process Founded'
        exit 0
    else
        kill -2 $appium_pid
        if [ $? -eq 0 ]; then
            echo "Appium Stop Success."
            exit 0
        else
            echo "Appium Stop Failed!"
            exit 1
        fi
    fi

elif [ "$appium" == "restart" ]; then
    appium_pid=`ps aux | grep [a]ppium | grep -v 'exclude' | awk '{print $2}'`
    if [ -z "$appium_pid" ];then
        echo 'No Appium Process Founded'
        exit 0
    else
        kill -2 $appium_pid
        if [ $? -eq 0 ]; then
            echo "Appium Stop Success."
        else
            echo "Appium Stop Failed!"
            exit 1
        fi
    fi
    appium&
    if [ $? -eq 0 ]; then
        echo "Appium Start Success."
        exit 0
    else
        echo "Appium Start Failed!"
        exit 1
    fi
fi

# For iOS
if [ "$device" == "iOS" ]; then
    computer_name=`scutil --get ComputerName`
    ios_device_cmd=`instruments -s devices | grep -v "Simulator\|Devices\|null\|$computer_name"`
    if [ -z "$ios_device_cmd" ];then
        device_num=0
    else
        device_num=`echo $ios_device_cmd|wc -l`
    fi
    if [ "$device_num" -eq "0" ] || [ "$device_num" -gt "1" ];then
        echo "No devices founded"
        exit 1
    fi
    deviceName=`echo $ios_device_cmd | awk -F '[][]' '{print $1}'`
    udid=`echo $ios_device_cmd | awk -F '[][]' '{print $2}'`
    platformVersion=`echo $ios_device_cmd | awk -F '[()]' '{print $2}'`
    tl_bundleId=`ios-deploy --id $udid --list_bundle_id | grep -i 'truelovelive'`
    wv_bundleId=`ios-deploy --id $udid --list_bundle_id | grep -i 'waviilive'`
    if [ "$execute" == "1" ]; then
        # 執行 xcode
        cd /usr/local/lib/node_modules/appium/node_modules/appium-webdriveragent
        xcodebuild -project WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination "id=$udid" test
    elif [ "$show_app_list" == "1" ]; then
        # 秀出所有 app 列表
        ios-deploy --id $udid --list_bundle_id
    elif [ "$check" == "1" ]; then
        # 檢查環境
        appium-doctor --ios

    elif [ "$show_info" == "1" ]; then
        # 秀出資訊
        if [ $device_num -eq 1 ];then
            echo "platformName       : iOS"
            echo "deviceName         : $deviceName"
            echo "platformVersion    : $platformVersion"
            echo "udid               : $udid"
            echo "xcodeOrgId         : 3EV5247FNZ"
            echo "bundleId(True Love): $tl_bundleId"
            echo "bundleId(Wavii)    : $wv_bundleId"
            echo "xcodeSigningId     : iPhone Developer"
            echo "automationName     : XCUITest"
cat << EOF
{
  "host": "http://localhost:4723/wd/hub",
  "platformName": "iOS",
  "deviceName": "$deviceName",
  "platformVersion": "$platformVersion",
  "udid": "$udid",
  "xcodeOrgId": "3EV5247FNZ",
  "bundleId": "$tl_bundleId",
  "bundleId": "$wv_bundleId",
  "xcodeSigningId": "iPhone Developer",
  "automationName": "XCUITest"
}
EOF
        else
            echo "沒有手機或是超過一台手機連接"
        fi
    else
        helpmenu
    fi

# For Android
elif [ "$device" == "Android" ]; then

    if [ "$execute" == "1" ];then

        /Users/$USER/Library/Android/sdk/tools/bin/uiautomatorviewer

    elif [ "$restart_adb" == "1" ]; then

        adb kill-server
        adb start-server

    elif [ "$show_info" == "1" ]; then
        udid=`adb devices | grep 'device$' | awk '{print $1}'`
        appPackage=`adb shell dumpsys window | grep mCurrentFocus | awk -F '/' '{print $1}' | awk '{print $3}'`
        appActivity=`adb shell dumpsys window | grep mCurrentFocus | awk -F '/' '{print $2}' | sed 's/}//g'`
        echo "host         : http://localhost:4723/wd/hub"
        echo "platformName : Android"
        echo "deviceName   : $udid"
        echo "appPackage   : $appPackage"
        echo "appActivity  : $appActivity"

cat << EOF
{
  "host": "http://localhost:4723/wd/hub",
  "platformName": "Android",
  "deviceName": "$udid",
  "appPackage": "$appPackage",
  "appActivity": "$appActivity"
}
EOF

    elif [ "$check" == "1" ]; then
        appium-doctor --android
    else
        helpmenu
    fi
else
    helpmenu
fi

