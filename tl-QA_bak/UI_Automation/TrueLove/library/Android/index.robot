*** Settings ***
Documentation	首頁
#Metadata			Version 0.1
*** Keywords ***
在 index 按下 首頁
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/homeFragment
    Click Element   id=com.extreamax.truelovelive:id/homeFragment

在 index 按下 活動
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/eventsFragment
    Click Element   id=com.extreamax.truelovelive:id/eventsFragment

在 index 按下 追蹤
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/homeFollowingFeedFragment
    Click Element   id=com.extreamax.truelovelive:id/homeFollowingFeedFragment

在 index 按下 我的
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/accountFragment
    Click Element   id=com.extreamax.truelovelive:id/accountFragment

在 index 按下 直播
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/showLiveAndCameraLayoutBtn
    Click Element   id=com.extreamax.truelovelive:id/showLiveAndCameraLayoutBtn

在 index 按下 放大鏡
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/searchBtn
    Click Element   id=com.extreamax.truelovelive:id/searchBtn

在 index 按下 鈴鐺
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/bellBtn
    Click Element   id=com.extreamax.truelovelive:id/bellBtn