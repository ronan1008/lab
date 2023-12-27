*** Settings ***
Documentation	登入
#Metadata			Version 0.1

*** Keywords ***
Click Login Button
    [Documentation]    登入頁面-登入->登入按鈕
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="登入"]
    Click Element   //XCUIElementTypeButton[@name="登入"]

Click Cancel Button If Exist
    [Documentation]    登入頁面-登入->取消(取消使用記憶帳號)
    ${back_status}=	Run Keyword And Return Status	Wait Until Element Is Visible   //XCUIElementTypeButton[@name="取消"]
    Run Keyword If	${back_status} == True   Click Element    //XCUIElementTypeButton[@name="取消"]
