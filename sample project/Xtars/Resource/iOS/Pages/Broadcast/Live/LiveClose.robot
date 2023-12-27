*** Settings ***
Documentation	首頁->直播->Live->直播間->離開直播間->直播已結束

#Metadata			Version 0.1

*** Keywords ***

Get Live Time
    [Documentation]    直播已結束->本場開播時長
    ${checkPath} =   Set Variable    //XCUIElementTypeStaticText[@name="直播已結束"]
    Wait Until Page Contains Element  ${checkPath}  timeout=3s  error=None
    ${TimePath} =   Set Variable    //XCUIElementTypeStaticText[@name="本場開播時長"]/following-sibling::XCUIElementTypeStaticText
    ${LiveTime} =   Get Element Attribute   ${TimePath}    name
    [return]    ${LiveTime}

Get Gift Revenue
    [Documentation]    直播已結束->本場禮物收益
    ${checkPath} =   Set Variable    //XCUIElementTypeStaticText[@name="直播已結束"]
    Wait Until Page Contains Element  ${checkPath}  timeout=3s  error=None
    ${TimePath} =   Set Variable    //XCUIElementTypeStaticText[@name="本場禮物收益"]/following-sibling::XCUIElementTypeStaticText
    ${LiveTime} =   Get Element Attribute   ${TimePath}    name
    [return]    ${LiveTime}

Get Live Hot
    [Documentation]    直播已結束->本場開播人氣
    ${checkPath} =   Set Variable    //XCUIElementTypeStaticText[@name="直播已結束"]
    Wait Until Page Contains Element  ${checkPath}  timeout=3s  error=None
    ${TimePath} =   Set Variable    //XCUIElementTypeStaticText[@name="本場開播人氣"]/following-sibling::XCUIElementTypeStaticText
    ${LiveTime} =   Get Element Attribute   ${TimePath}    name
    [return]    ${LiveTime}

Exit
    [Documentation]    直播已結束->Exit
    ${checkPath} =   Set Variable    //XCUIElementTypeStaticText[@name="直播已結束"]
    Wait Until Page Contains Element  ${checkPath}  timeout=3s  error=None
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="buttonExit"]
    Click Element  	//XCUIElementTypeButton[@name="buttonExit"]