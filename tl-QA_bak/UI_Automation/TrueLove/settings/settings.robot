*** Settings ***
Documentation	xxxx
#Metadata			Version 0.1
Library    AppiumLibrary

*** Variables ***
${host}    http://localhost:4723/wd/hub

*** Keywords ***

Import Library From Device
    [Arguments]	${Type}

    Set Global Variable    ${Device}   ${Type}
    Import Resource    ${CURDIR}/../library/${Device}/login.robot
#    Import Resource    ${CURDIR}/../library/${Device}/My/my.robot
#    Import Resource  ${CURDIR}/../library/${Device}/index.robot

    Run Keyword If	'${Device}' == 'iOS'     Import Resource     ${CURDIR}/ios.robot
    ...     ELSE IF     '${Device}' == 'Android'     Import Resource     ${CURDIR}/android.robot


在 Android 打開 TrueLove
    Import Library From Device    Android
    Open Application    ${host}    platformName=${platformName}     deviceName=${deviceName}    appPackage=${appPackage}   appActivity=${appActivity}

在 iOS 打開 TrueLove
    Import Library From Device    iOS
    Open Application    ${host}    platformName=${ios_platformName}     deviceName=${ios_deviceName}    udid=${udid}   xcodeOrgId=${xcodeOrgId}    browserName=${browserName}    xcodeSigningId=${xcodeSigningId}    automationName=${ios_automationName}    autoWebview=${autoWebview}   startIWDP=${startIWDP}

Open TrueLove App And Login With FB On Android
    在 Android 打開 TrueLove
    在登入註冊頁面按下登入
    在登入頁面按下FB
    在歡迎頁面按下
    Sleep  7s

Open TrueLove App And Login With FB On iOS
    在 iOS 打開 TrueLove
    在登入註冊頁面按下登入
    Click Cancel Button If Exist On Login Page
    在登入頁面按下FB
    Click Authorize Button On FB Auth Page
    在歡迎頁面按下取消
    Sleep  5s

Open TrueLove App And Login With Line On Android
    在 Android 打開 TrueLove
    在登入註冊頁面按下登入
    在登入頁面按下LINE
    在LINE登入頁面按下許可
    在歡迎頁面按下取消
    Sleep  7s

Open TrueLove App And Login With Line On iOS
    在 iOS 打開 TrueLove
    Click Login Button On Login Welcome Page
    在登入頁面如果有取消按鈕就按下
    Click Line Button On Login Welcome Page
    Click Authorize Button On Line Auth Page
#    在歡迎頁面按下取消
    Sleep  2s

在 Android 打開 TrueLove App 並 使用 Email 登入
    [Arguments]	${acc}     ${pass}
    在 Android 打開 TrueLove
    在登入註冊頁面按下登入
    在登入頁面輸入帳號  ${acc}
    在登入頁面輸入密碼  ${pass}
    在登入頁面按下登入
#    在歡迎頁面按下取消
    Sleep  7s

Open TrueLove App And Login With Email On iOS
    [Arguments]	${acc}     ${pass}
    在 iOS 打開 TrueLove
    在登入註冊頁面按下登入
    在登入頁面如果有取消按鈕就按下
    在登入頁面輸入帳號  ${acc}
    在登入頁面輸入密碼  ${pass}
    在登入頁面按下登入
#    在歡迎頁面按下取消
    Sleep  2s

Logout TrueLove App On iOS
    Click My Button On Home Page
    Click Advanced Settings On My Page
    Click Logout On Advanced Settings Page
    Close Application






