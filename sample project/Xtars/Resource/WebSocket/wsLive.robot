*** Settings ***
Library    WebSocketClient

*** Variables ***

${BASE_URL} =   http://testing-api.xtars.com

*** Keywords ***

WebSocket Connect
    [Arguments]	${token}    ${nonce}
    ${wsUrl}=    Set Variable    ws://testing-api.xtars.com/socket/websocket?token=${token}&nonce=${nonce}
    Log To Console  ${wsUrl}
    ${ws}=    WebSocketClient.Connect    ${wsUrl}
    [Return]    ${ws}

Join LiveRoom With Pass
    [Documentation]    直播間->聊聊天吧
    [Arguments]	${ws}    ${roomId}    ${pass}
    ${payload}=  Create Dictionary    code=${pass}
    ${body} =    Create Dictionary  topic=live_room:${roomId}   event=phx_join    payload=${payload}    ref=ref    join_ref=join_ref
    ${send}=    evaluate    json.dumps(${body})    json
    # Log To Console  ${send}
    WebSocketClient.Send  ${ws}  ${send}
    ${recv}=    WebSocketClient.Recv  ${ws}
    Log To Console  ${recv}


    ${dict}=    Evaluate    json.loads('${recv}')    json

    IF    '${dict}[payload][status]' == 'ok'
        ${recv}=    WebSocketClient.Recv  ${ws}
        ${dict}=    Evaluate    json.loads('${recv}')    json
    END
    [Return]    ${dict}


Join LiveRoom
    [Documentation]
    [Arguments]	${ws}    ${roomId}
    ${payload}=  Create Dictionary
    ${body} =    Create Dictionary  topic=live_room:${roomId}   event=phx_join    payload=${payload}    ref=ref    join_ref=join_ref
    ${send}=    evaluate    json.dumps(${body})    json
    Log To Console  ${send}
    WebSocketClient.Send  ${ws}  ${send}
    ${recv}=    WebSocketClient.Recv  ${ws}
    Log To Console  ${recv}  stream=STDOUT  no_newline=False
    ${dict}=    Evaluate    json.loads('${recv}')    json
    [Return]    ${dict}


