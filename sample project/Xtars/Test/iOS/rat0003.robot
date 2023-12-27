*** Settings ***
Library     AppiumLibrary
Resource    ../../Resource/iOS/Common/App.robot
Resource    ../../Resource/iOS/Common/manipulate.robot
Resource    ../../Resource/iOS/Pages/Index/Index.robot
Resource    ../../Resource/iOS/Pages/Broadcast/Broadcast.robot
Resource    ../../Resource/iOS/Pages/Broadcast/Live/LiveSetting.robot
Resource    ../../Resource/iOS/Pages/Broadcast/Live/LiveRoom.robot
Resource    ../../Resource/iOS/Pages/Broadcast/Live/LiveClose.robot


Test Setup       App.Login With Email   broadcaster005  12345
Test Teardown    App.Logout
*** Variables ***

*** Test Cases ***

首頁->直播->直播設定->直播間得到人氣收益與開播時間
    [Documentation]    直播間設定
    [Tags]  RAT
    Index.Click Live broadcast
    Broadcast.Click Live Broadcast
    LiveSetting.Input Subject  Shock Auto Test
    LiveSetting.Input Bulletin Board  Welcome To My Home
    LiveSetting.Select From Main Sprint Activity  牛轉乾坤
    LiveSetting.Select From Sub Sprint Activity  頂聲對決
    LiveSetting.Click Start Broadcast
    LiveRoom.Chat Text  大家好
    LiveRoom.Chat Text  今天好冷
    LiveRoom.Chat Text  希望你們都平安
    Sleep  15s  reason=None
    ${LiveTime} =   LiveRoom.Get Live Time
    Log  ${LiveTime}  level=Info  html=False  console=True  repr=False
    ${LivePoints} =   LiveRoom.Get Live Points
    Log  ${LivePoints}  level=Info  html=False  console=True  repr=False
    LiveRoom.Exit
    ${LiveTotalGift} =   LiveClose.Get Gift Revenue
    Log  ${LiveTotalGift}  level=Info  html=True  console=True  repr=False
    ${LiveTotalHot} =   LiveClose.Get Live Hot
    Log  ${LiveTotalHot}  level=Info  html=True  console=True  repr=False
    ${LiveTotalTime} =   LiveClose.Get Live Time
    Log  ${LiveTotalTime}  level=Info  html=True  console=True  repr=False
    LiveClose.Exit





