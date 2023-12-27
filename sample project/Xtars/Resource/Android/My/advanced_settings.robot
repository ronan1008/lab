*** Settings ***
Documentation	My->進階設定
#Metadata			Version 0.1

*** Keywords ***
在 My->進階設定 按下 登出
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/logoutButton
    Click Element   id=com.extreamax.truelovelive:id/logoutButton


