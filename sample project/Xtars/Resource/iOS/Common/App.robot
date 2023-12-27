*** Settings ***
Documentation	iOS
#Metadata			Version 0.1
Library    AppiumLibrary
Resource    ../../../Settings/ios.robot
Resource    ../Pages/Xtars.robot
Resource    ../Pages/Login.robot
Resource    ../Pages/Index/Index.robot
Resource    ../Pages/My/My.robot
Resource    ../Pages/My/AdvSettings/AdvSettings.robot
Resource    manipulate.robot

*** Variables ***
${host}    http://localhost:4723/wd/hub

*** Keywords ***
Open App
    Open Application    ${host}    platformName=${ios_platformName}     deviceName=${ios_deviceName}    udid=${udid}    bundleId=${bundleId}    xcodeOrgId=${xcodeOrgId}    xcodeSigningId=${xcodeSigningId}    automationName=${ios_automationName}    newCommandTimeout=${newCommandTimeout}

Logout If Entrance Without Login Page
    [Documentation]    如果登入的時候，沒有看到版本號，進行登出
    ${present}=    Run Keyword And Return Status    Element Should Be Visible   xpath= //XCUIElementTypeStaticText[contains(@name,'版本號')]
    Run Keyword If    ${present} == True    Log To Console    Starting Login
    ...    ELSE     Logout

Login With FB
    Open App
    Xtars.Click Login Button
    # Welcome.Click Login Button
    # Welcome.Click Cancel
    # Welcome.Click Cancel Button If Exist
    # Welcome.Click FB Button
    # Welcome.Click Authorize Button On FB
    # Welcome.Click Skip Button
    Sleep  5s

Login With Line
    Open App
    Welcome.Click Login Button
    Welcome.Click Cancel Button If Exist
    Welcome.Click Line Button
    Welcome.Click Authorize Button On Line
    Sleep  2s

Login With Email
    [Arguments]	${acc}     ${pass}
    Open App
    Logout If Entrance Without Login Page
    Xtars.Click Login Button
    Login.Cancel Login Popup
    Login.Input Account    ${acc}
    Login.Input Password    ${pass}
    Login.Click Login Button
    manipulate.Disable iCloud Key Chain
    Sleep  10s

Logout
    Log To Console    Starting Logout
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="首 頁"]    timeout=15s
    Index.Click My Button
    My.Click Advanced Settings
    AdvSettings.Click Logout

Close
    Close Application

Logout And Close
    Logout
    Close
