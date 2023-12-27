*** Settings ***
Documentation	首頁->我的
Resource    AdvSettings/AdvSettings.robot

#Metadata			Version 0.1

*** Keywords ***
Click Advanced Settings
    [Documentation]    我的->進階設定
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="進階設定"]
    Click Element   //XCUIElementTypeStaticText[@name="進階設定"]