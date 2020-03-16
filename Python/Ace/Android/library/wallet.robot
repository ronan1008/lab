*** Settings ***
Documentation	行情
#Metadata			Version 0.1
Library    ../tools/getTotp.py
*** Keywords ***

Click Charge Cash On Trade Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_recharge
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_recharge

Click Withdraw Cash On Trade Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_withdraw
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_withdraw

Click Charge Coin On Trade Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_charging
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_charging

Click Withdraw Coin On Trade Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_coin
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_coin

Get Info In Charge Cash On Trade Page
    [Arguments]	${info}
    Wait Until Element Is Visible    xpath=//*[@text='${info}']/following-sibling::*[1]    timeout=10
    ${text} =    Get Element Attribute    xpath=//*[@text='${info}']/following-sibling::*[1]    text
    Log    ${info}: ${text}   WARN
    
Choose Bank In Withdraw Cash On Trade Page
    Wait Until Element Is Visible   xpath=//*[@class='android.view.View' and @content-desc='選擇銀行帳戶']
    Click Element  xpath=//*[@class='android.view.View' and @content-desc='選擇銀行帳戶']
    Wait Until Element Is Visible   xpath=//*[@class='android.view.View' and @content-desc='確定']
    Click Element  xpath=//*[@class='android.view.View' and @content-desc='確定']

Input Cash Amount In Withdraw Cash On Trade Page
    [Arguments]	${cash_amount}
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.EditText' and @text='請填寫金額']
    Input Text    xpath=//*[@class='android.widget.EditText' and @text='請填寫金額']    ${cash_amount}

Click Next In Withdraw Cash On Trade Page
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.Button' and @content-desc='下一步']
    Click Element    xpath=//*[@class='android.widget.Button' and @content-desc='下一步']    

Input Cash Password In Withdraw Cash On Trade Page
    [Arguments]	${pass}
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.EditText' and @password='true']
    Input Text    xpath=//*[@class='android.widget.EditText' and @password='true']    ${pass}

Input Google Auth In Withdraw Cash On Trade Page
    ${token}=  Run Keyword	get_totp_token	${key}
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.EditText' and @password='false']
    Input Text    xpath=//*[@class='android.widget.EditText' and @password='false']    ${token}

Click Confirm Button In Withdraw Cash On Trade Page
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.Button' and @content-desc='提領確認']
    Click Element    xpath=//*[@class='android.widget.Button' and @content-desc='提領確認']    

Click Back Button On Trade page 
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/iv_back
    Click Element  id=com.asiainnovations.ace.taiwan:id/iv_back
























