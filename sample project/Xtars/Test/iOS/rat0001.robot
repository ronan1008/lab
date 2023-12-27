*** Settings ***
Library    AppiumLibrary
Resource   ../../Resource/iOS/Common/App.robot

*** Variables ***

*** Test Cases ***

開啟 Xtars 使用 Email 登入
    [Documentation]    登入TrueLove 使用 Email 登入
    [Tags]  RAT
    App.Login With Email  broadcaster005  12345
    App.Logout


EXAMPLE
    [Tags]  WARN
    App.Login With Email  broadcaster005  12345
    App.Logout

*** comment ***

Test Login With FB
    [Documentation]    登入TrueLove 使用 FB 登入
    Open TrueLove App And Login With FB
    Logout TrueLove App

Test Login With Line
   [Documentation]    登入TrueLove 使用 Line 登入
   Open TrueLove App And Login With Line


