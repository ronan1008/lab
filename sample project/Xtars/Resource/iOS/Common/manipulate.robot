*** Settings ***
Documentation	常用功能
#Metadata			Version 0.1

*** Keywords ***

Swipe middle To Up On Page
    [Documentation]   頁面由上往下動一次
    Sleep    1s
    Swipe By Percent    50    50    50    10    3000
    Sleep    1s

Swipe middle To Down On Page
    [Documentation]   頁面由下往上動一次
    Sleep    1s
    Swipe By Percent    50    50    50    100    3000
    Sleep    1s

Return To Previous Page
    [Documentation]   返回前一頁
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="返回"]
    Click Element   //XCUIElementTypeButton[@name="返回"]


Disable iCloud Key Chain
    Wait Until Element Is Visible   //XCUIElementTypeSheet[@name="您要在「iCloud鑰匙圈」中儲存此密碼，以便在所有裝置上與App和網站搭配使用嗎？"]
    Click Element   	//XCUIElementTypeButton[@name="稍後再說"]
