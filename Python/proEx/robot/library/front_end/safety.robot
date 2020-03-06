*** Settings ***
Documentation	安全配置頁面
#Metadata			Version 0.1
Library	../tools/getTotp.py

*** Keywords ***
Goto Change Financial Password
    Wait Until Element Is Visible   //button[contains(@onclick,'funds-pwd')]
    Click Element   //button[contains(@onclick,'funds-pwd')]
   

Change Pass On Change Financial Password Page
    [Arguments]    ${old_pass}     ${new_pass}     ${personal_id}    ${key}
    Input Text    //input[@id='bindtradepass-oldpass']    ${old_pass} 
    Input Text    //input[@id='bindtradepass-newpass']    ${new_pass} 
    Input Text    //input[@id='bindtradepass-confirmpass']    ${new_pass} 
    Input Text    //input[@id='bindtradepass-identityno']    ${personal_id}   
    ${token}=  Run Keyword	get_totp_token	${key}
	Input Text    //input[@id='bindtradepass-googlecode'] 	${token}
    Click Element    (//button[contains(@onclick,'saveModifyPwd')])[2]
    Log    Change Financial Password ${old_pass} To ${new_pass} Success   WARN

Goto Change Account Password
    Wait Until Element Is Visible   //button[contains(@onclick,'login-pwd')]
    Click Element   //button[contains(@onclick,'login-pwd')]
   
Change Pass On Change Account Password Page
    [Arguments]    ${old_pass}     ${new_pass}    ${key}
    Input Text    //input[@id='unbindloginpass-oldpass']    ${old_pass}
    Input Text    //input[@id='unbindloginpass-newpass']    ${new_pass}
    Input Text    //input[@id='unbindloginpass-confirmpass']    ${new_pass}
    ${token}=  Run Keyword	get_totp_token	${key}
	Input Text    //input[@id='unbindloginpass-googlecode'] 	${token}
    Click Element    (//button[contains(@onclick,'saveModifyPwd')])[1]
    Log    Change Account Password ${old_pass} To ${new_pass} Success   WARN


Goto Real Name Authentication Page
    Wait Until Element Is Visible   //button[contains(@onclick,'/index.php?m=verified')]
    Click Element   //button[contains(@onclick,'/index.php?m=verified')]

Input Personal Info On Authentication Page
    [Arguments]    ${name}     ${country}    ${passport}
    Input Text    //input[@id='bindrealinfo-realname']    ${name}


