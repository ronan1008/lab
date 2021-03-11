*** Settings ***
Documentation	首頁的nav bar
#Metadata			Version 0.1


*** Keywords ***
Click Home Button On Home Page
    [Documentation]    首頁->首頁
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="首 頁"]
    Click Element   //XCUIElementTypeButton[@name="首 頁"]

Click Activity Button On Home Page
    [Documentation]    首頁->活動
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="活 動"]
    Click Element   //XCUIElementTypeButton[@name="活 動"]

Click Live broadcast On Home Page
    [Documentation]    首頁->直播
    Wait Until Element Is Visible   //XCUIElementTypeApplication[@name="TL初樂"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTabBar/XCUIElementTypeButton[3]
    Click Element   //XCUIElementTypeApplication[@name="TL初樂"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTabBar/XCUIElementTypeButton[3]

Click Follow Button On Home Page
    [Documentation]    首頁->追蹤
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="追 蹤"]
    Click Element   //XCUIElementTypeButton[@name="追 蹤"]

Click My Button On Home Page
    [Documentation]    首頁->我的
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="我 的"]
    Click Element   //XCUIElementTypeButton[@name="我 的"]
