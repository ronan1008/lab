*** Settings ***
Library    AppiumLibrary
Resource    ../settings/settings.robot

*** Variables ***

*** Test Cases ***

Test Case: tl-30 : 註冊時，輸入電子信箱與密碼
    [Documentation]    登入TrueLove 使用 Email 登入
    在 Android 打開 TrueLove App 並 使用 Email 登入
    在


*** comment ***

Test Login With FB
    [Documentation]    登入TrueLove 使用 FB 登入
    Open TrueLove App And Login With FB On Android

Test Login With Line
    [Documentation]    登入TrueLove 使用 Line 登入
    Open TrueLove App And Login With Line On Android

