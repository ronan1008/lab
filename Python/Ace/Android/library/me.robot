*** Settings ***
Documentation	分頁
#Metadata			Version 0.1

*** Keywords ***
Click Email Login On Me Page
    [Documentation]    我->Email 登入
    Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/tv_email_login
    Click Element    id=com.asiainnovations.ace.taiwan:id/tv_email_login   

Click Mobile Login On Me Page
    [Documentation]    我->電話 登入
    Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/tv_phone_login
    Click Element    id=com.asiainnovations.ace.taiwan:id/tv_phone_login

Input Email In Email Login On Me Page
    [Documentation]    我->Email 登入->輸入 mail
    [Arguments]	${Email}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/aet_email
    Input Text  id=com.asiainnovations.ace.taiwan:id/aet_email    ${Email}

Input Password In Email Login On Me Page
    [Arguments]	${Password}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/aet_password
    Input Text  id=com.asiainnovations.ace.taiwan:id/aet_password    ${Password}

Input Tel Number In Mobile Login On Me Page
    [Arguments]	${tel_number}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/aet_phone
    Input Text  id=com.asiainnovations.ace.taiwan:id/aet_phone    ${tel_number}

Input Password In Mobile Login On Me Page
    [Arguments]	${Password}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/aet_password
    Input Text  id=com.asiainnovations.ace.taiwan:id/aet_password    ${Password}

Click Login Button In Email Login On Me Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acb_login
    Click Element  id=com.asiainnovations.ace.taiwan:id/acb_login

Click Login Button In Mobile Login On Me Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acb_login
    Click Element  id=com.asiainnovations.ace.taiwan:id/acb_login
    Sleep    1s

Input Google Auth In Login On Me Page
    [Arguments]	${key}
    ${token}=  Run Keyword	get_totp_token	${key}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/aet_vertify
    Input Text  id=com.asiainnovations.ace.taiwan:id/aet_vertify    ${token}

Click Login Button In Auth On Me Page
    [Arguments]	${key}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acb_commit
    Click Element  id=com.asiainnovations.ace.taiwan:id/acb_commit
    Sleep    2s
    ${status}=	Run Keyword And Return Status	Page Should Contain Element	id=com.asiainnovations.ace.taiwan:id/acb_commit
    ${token}=  Run Keyword	get_totp_token	${key}
	Run Keyword If	${status} == True	Run Keywords
 	...	Input Text  id=com.asiainnovations.ace.taiwan:id/aet_vertify    ${token}
 	...	AND    Click Element  id=com.asiainnovations.ace.taiwan:id/acb_commit

Click Id Identify Authentication On Me Page
    [Documentation]    我->身份認證
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/view_left'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/view_left'] 

Click Security Center On Me Page
    [Documentation]    我->安全中心
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/view_right'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/view_right'] 

Click Login Password In Security Center On Me Page
    [Documentation]    我->安全中心->登入密碼
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/actv_login_pass'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/actv_login_pass'] 

Click Bank Account On Me Page
    [Documentation]    我->銀行帳號
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='銀行帳號'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='銀行帳號'] 

Click Coin Withdraw Address On Me Page
    [Documentation]    我->我的提幣地址
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='我的提幣地址'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='我的提幣地址'] 

Click Invite Back On Me Page
    [Documentation]    我->邀請返佣
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='邀請返佣'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='邀請返佣'] 

Click Announcement On Me Page
    [Documentation]    我->公告中心
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='公告中心'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='公告中心']

Click System Settings On Me Page
    [Documentation]    我->系統設置
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='系統設置'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='系統設置'] 

Click Logout In System Settings On Me Page
    [Documentation]    我->系統設置->登出
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/tvExitLogin'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/tvExitLogin'] 


Click Question Reply On Me Page
    [Documentation]    我->問題回饋
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='問題回饋'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='問題回饋'] 

Click Facebook On Me Page
    [Documentation]    我->Facebook
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='FaceBook'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='FaceBook'] 

Click Line On Me Page
    [Documentation]    我->Line@
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='Line@'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='Line@'] 

Click Medium On Me Page
    [Documentation]    我->Medium
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='Medium'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='Medium']

Click Telegram On Me Page
    [Documentation]    我->Telegram
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='Telegram'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='Telegram']

Click Twitter On Me Page
    [Documentation]    我->Twitter
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='Twitter'] 
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/setting_left' and @text='Twitter'] 


Click Back Button On Me Page
    [Documentation]    返回鍵
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/iv_back    timeout=10
    Click Element  id=com.asiainnovations.ace.taiwan:id/iv_back