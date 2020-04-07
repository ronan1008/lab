*** Settings ***
Documentation	分頁
#Metadata			Version 0.1

*** Keywords ***

Click Email Login On Me Page
    [Documentation]    我->Email 登入
    Wait Until Element Is Visible    xpath=//XCUIElementTypeStaticText[@name="信箱登入"]
    Click Element    xpath=//XCUIElementTypeStaticText[@name="信箱登入"]  

Click Mobile Login On Me Page
    [Documentation]    我->電話 登入
    Wait Until Element Is Visible    xpath=//XCUIElementTypeStaticText[@name="手機登入"]
    Click Element    xpath=//XCUIElementTypeStaticText[@name="手機登入"]

Input Tel Number In Mobile Login On Me Page
    [Documentation]    我->電話 登入->輸入 電話
    [Arguments]	${tel_number}
    Wait Until Element Is Visible   xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextField
    Clear Text    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextField
    Input Text    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextField    ${tel_number}

Input Password In Mobile Login On Me Page
    [Documentation]    我->電話 登入->輸入 密碼
    [Arguments]	${Password}
    Wait Until Element Is Visible   xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeSecureTextField
    Input Text    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeSecureTextField    ${Password}

Click Login Button In Login On Me Page
    [Documentation]    我->電話orEmail 登入->登入
    Wait Until Element Is Visible    xpath=//XCUIElementTypeButton[@name="登入"]
    Click Element    xpath=//XCUIElementTypeButton[@name="登入"]
    Sleep    1s

Input Google Auth In Login On Me Page
    [Arguments]	${key}
    ${token}=  Run Keyword	get_totp_token	${key}
    Wait Until Element Is Visible    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTextField
    Input Text    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTextField    ${token}

Click Login Button In Auth On Me Page
    [Arguments]	${key}
    Wait Until Element Is Visible    xpath=//XCUIElementTypeButton[@name="送出"]
    Click Element    xpath=//XCUIElementTypeButton[@name="送出"]
    Sleep    2s
    ${status}=	Run Keyword And Return Status	Page Should Contain Element	xpath=//XCUIElementTypeButton[@name="送出"]
    ${token}=  Run Keyword	get_totp_token	${key}
	Run Keyword If	${status} == True	Run Keywords
 	...	Input Text  xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTextField    ${token}
 	...	AND    Click Element  xpath=//XCUIElementTypeButton[@name="送出"]