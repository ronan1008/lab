*** Settings ***
Documentation	首頁的nav bar
#Metadata			Version 0.1
Resource   ../../Common/manipulate.robot

*** Keywords ***
Click Home Button
    [Documentation]    首頁->首頁
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="首 頁"]
    Click Element   //XCUIElementTypeButton[@name="首 頁"]

Click Activity Button
    [Documentation]    首頁->活動
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="活 動"]
    Click Element   //XCUIElementTypeButton[@name="活 動"]

Click Live broadcast
    [Documentation]    首頁->直播
    Wait Until Element Is Visible   //XCUIElementTypeTabBar[@name="標籤頁列"]/XCUIElementTypeButton[3]
    Click Element   //XCUIElementTypeTabBar[@name="標籤頁列"]/XCUIElementTypeButton[3]

Click Follow Button
    [Documentation]    首頁->追蹤
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="追 蹤"]
    Click Element   //XCUIElementTypeButton[@name="追 蹤"]

Click My Button
    [Documentation]    首頁->我的
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="我 的"]
    Click Element   //XCUIElementTypeButton[@name="我 的"]

Click Popular Activity Look More
    [Documentation]    首頁->熱門動態
    manipulate.Swipe middle To Up On Page
    manipulate.Swipe middle To Up On Page
    manipulate.Swipe middle To Up On Page
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="熱門動態"]
    Click Element   	xpath = (//XCUIElementTypeStaticText[@name="看更多"])[1]
    Sleep  2s  reason=None

