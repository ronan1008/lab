*** Settings ***
Documentation	首頁->我的
Resource    ../function/tool.robot
#Metadata			Version 0.1

*** Keywords ***
Click Advanced Settings On My Page
    [Documentation]    我的->進階設定
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="進階設定"]
    Click Element   //XCUIElementTypeStaticText[@name="進階設定"]

Click Logout On Advanced Settings Page
    [Documentation]    我的->進階設定->登出
    Swipe middle To Up On Page
    Wait Until Element Is Visible   //XCUIElementTypeApplication[@name="TL初樂"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[10]
    Click Element   //XCUIElementTypeApplication[@name="TL初樂"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[10]
    Sleep  1s


