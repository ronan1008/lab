*** Settings ***
Documentation	首頁->直播

#Metadata			Version 0.1

*** Keywords ***
Click Photo Post
    [Documentation]    直播->照片
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="Camera button nor"]
    Click Element   //XCUIElementTypeButton[@name="Camera button nor"]


Click Live Broadcast
    [Documentation]    直播->Live
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="live button nor"]
    Click Element   //XCUIElementTypeButton[@name="live button nor"]


