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

Choose Country On Me Page
    [Documentation]    我->電話 登入->選擇區碼
    [Arguments]	${country}
    Wait Until Element Is Visible    xpath=//XCUIElementTypeStaticText[@name="+886"] 
    Click Element    xpath=//XCUIElementTypeStaticText[@name="+886"] 
    Wait Until Element Is Visible   xpath=//XCUIElementTypeSearchField[@name="搜尋"]
    Input Text  xpath=//XCUIElementTypeSearchField[@name="搜尋"]    ${country}
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="Taiwan"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="Taiwan"]

Click Register On Me Page
    [Documentation]    我->電話 登入->註冊
    Wait Until Element Is Visible    xpath=//XCUIElementTypeStaticText[@name="沒有帳號？請註冊"]
    Click Element    xpath=//XCUIElementTypeStaticText[@name="沒有帳號？請註冊"]

Click Get_verify_code On Me Page
    [Documentation]    我->電話 登入->註冊->取得驗證碼
    Wait Until Element Is Visible    xpath=//XCUIElementTypeStaticText[@name="取得簡訊驗證碼"]
    Click Element    xpath=//XCUIElementTypeStaticText[@name="取得簡訊驗證碼"]
    Sleep    30s

Input Tel Auth In Register On Me Page
    [Documentation]    我->電話 登入->註冊->輸入 驗證碼
    ${verify_code}=  Run Keyword	get_verification_code    [ACE]	
    Wait Until Element Is Visible   xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther[3]/XCUIElementTypeTextField
    Input Text  xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther[3]/XCUIElementTypeTextField    ${verify_code}

Click Cancel On Me Page
    [Documentation]    我->電話orEmail->取消
    Wait Until Element Is Visible    xpath=//XCUIElementTypeButton[@name="userModule btn close"]
    Click Element    xpath=//XCUIElementTypeButton[@name="userModule btn close"]

Input Tel Number In Mobile Login On Me Page
    [Documentation]    我->電話 登入->輸入 電話
    [Arguments]	${tel_number}
    Wait Until Element Is Visible   xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextField
    Clear Text    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextField
    Input Text    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextField    ${tel_number}

Input Email In Email Login On Me Page
    [Documentation]    我->Email 登入->輸入 mail
    [Arguments]	${Email}
    Wait Until Element Is Visible   xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextField
    Clear Text  xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextField
    Input Text  xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeTextField    ${Email}

Input Password In Email Login On Me Page
    [Documentation]    我->Email 登入->輸入 密碼
    [Arguments]	${Password}
    Wait Until Element Is Visible   xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeSecureTextField
    Input Text  xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeSecureTextField    ${Password}


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



Click Id Identify Authentication On Me Page
    [Documentation]    我->身份認證
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="身份驗證"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="身份驗證"] 

Click Security Center On Me Page
    [Documentation]    我->安全中心
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="安全中心"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="安全中心"] 

Click Login Password In Security Center On Me Page
    [Documentation]    我->安全中心->登入密碼
    Wait Until Element Is Visible   xpath=
    Click Element  xpath=

Click Bank Account On Me Page
    [Documentation]    我->銀行帳號
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="銀行帳號"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="銀行帳號"]

Click Coin Withdraw Address On Me Page
    [Documentation]    我->我的提幣地址
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="提幣地址"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="提幣地址"]

Click Invite Back On Me Page
    [Documentation]    我->邀請返佣
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="邀請返佣"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="邀請返佣"]

Click Announcement On Me Page
    [Documentation]    我->公告中心
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="公告中心"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="公告中心"]

Click System Settings On Me Page
    [Documentation]    我->系統設置
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="系統設置"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="系統設置"]

Click Logout In System Settings On Me Page
    [Documentation]    我->系統設置->登出
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="登出"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="登出"]

Click Question Reply On Me Page
    [Documentation]    我->問題回饋
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="問題回饋"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="問題回饋"]

Click Facebook On Me Page
    [Documentation]    我->Facebook
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="Facebook"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="Facebook"] 

Click Line On Me Page
    [Documentation]    我->Line@
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="Line@"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="Line@"]

Click Medium On Me Page
    [Documentation]    我->Medium
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="Medium"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="Medium"]

Click Telegram On Me Page
    [Documentation]    我->Telegram
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="Telegram"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="Telegram"]

Click Twitter On Me Page
    [Documentation]    我->Twitter
    Wait Until Element Is Visible   xpath=//XCUIElementTypeStaticText[@name="Twitter"]
    Click Element  xpath=//XCUIElementTypeStaticText[@name="Twitter"]


Click Back Button On Me Page
    [Documentation]    返回鍵
    Wait Until Element Is Visible   xpath=//XCUIElementTypeButton[@name="返回"]    timeout=10
    Click Element  xpath=//XCUIElementTypeButton[@name="返回"]