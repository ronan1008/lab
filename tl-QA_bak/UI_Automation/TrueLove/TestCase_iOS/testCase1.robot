*** Settings ***
Library    AppiumLibrary
Resource    ./settings/settings.robot

*** Variables ***

*** Test Cases ***

Test Login With Email
    [Documentation]    登入TrueLove 使用 Email 登入
    Open TrueLove App And Login With Email
    Logout TrueLove App

*** comment ***

Test Login With FB
    [Documentation]    登入TrueLove 使用 FB 登入
    Open TrueLove App And Login With FB
    Logout TrueLove App

Test Login With Line
   [Documentation]    登入TrueLove 使用 Line 登入
   Open TrueLove App And Login With Line


