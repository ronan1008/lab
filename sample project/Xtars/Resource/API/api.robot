*** Settings ***
Library  RequestsLibrary
Library  Collections


*** Variables ***

${BASE_URL} =   http://testing-api.xtars.com

*** Keywords ***
Host Setting
    [Arguments]	${token}  ${nonce}
    ${headers} =    Create Dictionary    Content-Type    application/json    X-Auth-Token    ${token}    X-Auth-Nonce    ${nonce}
    Create Session    xtars    url=${BASE_URL}    headers=${headers}

Login Set Auth
    [Arguments]	${acc}  ${pass}
    Host Setting    ""    ""
    ${data} =    Create Dictionary  account=${acc}   password=${pass}
    ${res} =    POST On Session   xtars    /api/v2/identity/auth/login    json=${data}
    ${tk} =    Create Dictionary  token=${res.json()}[data][token]   nonce=${res.json()}[data][nonce]
    Set Global Variable    ${token}    ${tk}[token]
    Set Global Variable    ${nonce}    ${tk}[nonce]
    Host Setting    ${token}    ${nonce}
    [Return]    ${tk}

Get Live List Home
    ${res} =    Get On Session   xtars    /api/v2/live/list/home
    [Return]    ${res.json()}


Backend Get Identity With LoginId
    [Arguments]	${LoginId}
    ${data} =    Create Dictionary    keyword=${LoginId}    type=login_id
    ${res} =    POST On Session   xtars    /api/v2/backend/user/search    json=${data}
    Log To Console  ${res}
    [Return]    ${res.json()}[data][0][id]