*** Settings ***
Library     AppiumLibrary
Library     WebSocketClient
Resource    ../../Resource/iOS/Common/App.robot
Resource    ../../Resource/iOS/Common/manipulate.robot
Resource    ../../Resource/iOS/Pages/Index/Index.robot
Resource    ../../Resource/iOS/Pages/Broadcast/Broadcast.robot
Resource    ../../Resource/iOS/Pages/Broadcast/Live/LiveSetting.robot
Resource    ../../Resource/iOS/Pages/Broadcast/Live/LiveRoom.robot
Resource    ../../Resource/iOS/Pages/Broadcast/Live/LiveClose.robot
Resource    ../../Resource/API/api.robot
Resource    ../../Resource/WebSocket/wsLive.robot

Suite Setup        App.Login With Email   broadcaster005  12345
Suite Teardown    App.Logout And Close

*** Variables ***

${setTitle} =    Password Room
${setBulletin} =    Autotest password room
${setPass} =    12345

*** Test Cases ***


首頁->直播->直播設定 應可成功設定密碼
    [Documentation]
    [Tags]  RAT
    Index.Click Live broadcast
    Broadcast.Click Live Broadcast
    LiveSetting.Input Subject  ${setTitle}
    LiveSetting.Input Bulletin Board  ${setBulletin}
    LiveSetting.Switch Room To Private And Set Pass  ${setPass}
    LiveSetting.Click Start Broadcast

開播後，房間資訊面板會顯示密碼
    [Documentation]
    [Tags]  RAT
    LiveRoom.Click Toolbox
    LiveRoom.Click Room Info Of Toolbox

    ${Title} =   LiveRoom.Get Title Of Room Info
    Log  ${Title}  level=Info  html=False  console=True  repr=False
    Should Be Equal  ${Title}  ${setTitle}  msg=相同  values=True  ignore_case=False

    ${Bulletin} =   LiveRoom.Get Bulletin Of Room Info
    Log  ${Bulletin}  level=Info  html=False  console=True  repr=False
    Should Be Equal  ${Bulletin}  ${setBulletin}  msg=相同  values=True  ignore_case=False

    ${Password} =   LiveRoom.Get Password Of Room Info
    Log  ${Password}  level=Info  html=False  console=True  repr=False
    Should Be Equal  ${Password}  ${setPass}  msg=相同  values=True  ignore_case=False
    LiveRoom.Click Save Of Room Info

API 使用者 首頁->首頁須顯示鎖頭
    api.Login Set Auth   tl-lisa   12345678
    ${id}=    api.Backend Get Identity With LoginId    broadcaster005
    ${tk}=    api.Login Set Auth   track0050   123456
    Log To Console    ${tk}
    Set Suite Variable    ${token}    ${tk}[token]
    Set Suite Variable    ${nonce}    ${tk}[nonce]
    ${res}=    api.Get Live List Home
    @{data}=  Set Variable   ${res}[data]
    FOR    ${value}    IN    @{data}
        run keyword if    '${value}[liveMasterId]' == '${id}'    Run Keywords
         ...    Set Suite Variable    &{roomInfo}    type=${value}[type]    roomId=${value}[roomId]    needPassword=${value}[needPassword]
         ...    AND    Log To Console    found: &{roomInfo}
    END
    Should Be True    ${roomInfo}[needPassword] == True

ws 使用者 進入該房間須輸入密碼，錯誤密碼不可進入
    ${ws}=    wsLive.WebSocket Connect  ${token}  ${nonce}
    Set Global Variable  ${ws}  ${ws}
    ${recv}=    wsLive.Join LiveRoom With Pass    ${ws}    ${roomInfo}[roomId]    1111
    Should Be Equal  '${recv}[payload][response][err]'  'ROOM_PASSWORD_MAY_BE_WRONG'  msg=密碼錯誤  values=True  ignore_case=False

ws 使用者 進入該房間須輸入密碼，正確密碼可進入
    ${recv}=    wsLive.Join LiveRoom With Pass    ${ws}    ${roomInfo}[roomId]    ${setPass}
    Log To Console  ${recv}[payload][data][fromUser][id]
    Log To Console  ${recv}[payload][data][fromUser][name]
    Log To Console  ${recv}[payload][data][targetUser][id]
    Log To Console  ${recv}[payload][data][targetUser][name]

從直播間得到人氣收益與開播時間，結束直播間
    ${LiveTime} =   LiveRoom.Get Live Time
    Log  ${LiveTime}  level=Info  html=False  console=True  repr=False
    ${LivePoints} =   LiveRoom.Get Live Points
    Log  ${LivePoints}  level=Info  html=False  console=True  repr=False
    LiveRoom.Exit

結束直播間頁面得到統計數據
    ${LiveTotalGift} =   LiveClose.Get Gift Revenue
    Log To Console  ${LiveTotalGift}

    ${LiveTotalHot} =   LiveClose.Get Live Hot
    Log To Console  ${LiveTotalHot}
    ${LiveTotalTime} =   LiveClose.Get Live Time

    Log  ${LiveTotalTime}  level=Info  html=True  console=True  repr=False
    Log To Console  ${LiveTotalTime}
    LiveClose.Exit





