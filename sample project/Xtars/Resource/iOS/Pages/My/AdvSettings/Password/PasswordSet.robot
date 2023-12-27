*** Settings ***
Documentation	首頁->我的->進階設定->密碼設定

*** Keywords ***
Click Logout

Input Password
    [Documentation]    密碼設定->現在密碼
    Wait Until Element Is Visible
    Click Element
    Sleep  1s

Input New Password
    [Documentation]    密碼設定->設定新密碼
    Wait Until Element Is Visible
    Click Element
    Sleep  1s

Input Confirm Password
    [Documentation]    密碼設定->確認新密碼
    Wait Until Element Is Visible
    Click Element
    Sleep  1s
