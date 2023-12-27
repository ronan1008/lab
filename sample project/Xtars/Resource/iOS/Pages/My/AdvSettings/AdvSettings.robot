*** Settings ***
Documentation	首頁->我的->進階設定
# Resource    ../function/tool.robot
Resource    ../../../Common/manipulate.robot
#Metadata			Version 0.1

*** Keywords ***
Click Logout
    [Documentation]    我的->進階設定->登出
    manipulate.Swipe middle To Up On Page
    Wait Until Element Is Visible   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[13]/XCUIElementTypeOther[2]/XCUIElementTypeOther
    Click Element   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[13]/XCUIElementTypeOther[2]/XCUIElementTypeOther
    Sleep  1s
