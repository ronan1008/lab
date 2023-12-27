*** Settings ***
Library    WebSocketClient

Resource    ../../Resource/API/api.robot
Resource    ../../Resource/WebSocket/wsLive.robot

*** Variables ***

${BASE_URL} =   http://testing-api.xtars.com

*** Test Cases ***
使用者登入
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

ws 觀眾進入該房間須輸入密碼，錯誤密碼不可進入
    ${ws}=    wsLive.WebSocket Connect  ${token}  ${nonce}
    Set Global Variable  ${ws}  ${ws}
    ${recv}=    wsLive.Join LiveRoom With Pass    ${ws}    ${roomInfo}[roomId]    1111
    Should Be Equal  '${recv}[payload][response][err]'  'ROOM_PASSWORD_MAY_BE_WRONG'  msg=密碼錯誤  values=True  ignore_case=False

ws 觀眾進入該房間須輸入密碼，正確密碼可進入
    ${recv}=    wsLive.Join LiveRoom With Pass    ${ws}    ${roomInfo}[roomId]    2222
    Log To Console  ${recv}[payload][data][fromUser][id]
    Log To Console  ${recv}[payload][data][fromUser][name]
    Log To Console  ${recv}[payload][data][targetUser][id]
    Log To Console  ${recv}[payload][data][targetUser][name]


