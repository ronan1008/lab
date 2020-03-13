*** Settings ***
Documentation	分頁
#Metadata			Version 0.1

*** Keywords ***
Click Email Login On Me Page
    Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/tv_email_login
    Click Element    id=com.asiainnovations.ace.taiwan:id/tv_email_login   

Click Mobile Login On Me Page
    Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/tv_phone_login
    Click Element    id=com.asiainnovations.ace.taiwan:id/tv_phone_login

Input Email In Email Login On Me Page
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
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acb_commit
    Click Element  id=com.asiainnovations.ace.taiwan:id/acb_commit
    