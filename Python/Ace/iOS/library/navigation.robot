*** Settings ***
Documentation	分頁
#Metadata			Version 0.1

*** Keywords ***
Goto Home Tab On Home Page
    [Documentation]    Home 分頁
    Wait Until Element Is Visible    xpath=//XCUIElementTypeButton[@name="首頁"]
    Click Element    xpath=//XCUIElementTypeButton[@name="首頁"]

Goto Quotes Tab On Home Page
    [Documentation]    行情 分頁
    Wait Until Element Is Visible    xpath=//XCUIElementTypeButton[@name="行情"]
    Click Element    xpath=//XCUIElementTypeButton[@name="行情"]

Goto Trading Tab On Home Page
    [Documentation]    交易 分頁
    Wait Until Element Is Visible    xpath=//XCUIElementTypeButton[@name="交易"]
    Click Element    xpath=//XCUIElementTypeButton[@name="交易"]

Goto Wallet Tab On Home Page
    [Documentation]    錢包 分頁
    Wait Until Element Is Visible    xpath=//XCUIElementTypeButton[@name="錢包"]
    Click Element    xpath=//XCUIElementTypeButton[@name="錢包"]


Goto Me Tab On Home Page
    [Documentation]    我 分頁
    Wait Until Element Is Visible   xpath=//XCUIElementTypeButton[@name="我"]
    Click Element    xpath=//XCUIElementTypeButton[@name="我"]