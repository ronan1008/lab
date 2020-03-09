*** Settings ***
Documentation	安全配置頁面
#Metadata			Version 0.1
Library	../tools/getTotp.py

*** Variables ***
${UploadImage}	/Users/shocklee/Documents/GitHub/workspace/Python/proEx/robot/library/tools/S__4390953.jpg


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
    [Arguments]    ${name}     ${passport}
    Wait Until Element Is Visible   //input[@id='bindrealinfo-realname']
    Input Text    //input[@id='bindrealinfo-realname']    ${name}
    Click Element    //u[@class='icon icon-unfold']
    Wait Until Element Is Visible    //p[@data-cid='81']
    Click Element    //p[@data-cid='81']
    Input Text    //input[@id='bindrealinfo-identityno']    ${passport}
    Choose File   //input[@onchange='file(event,this,1)']   ${UploadImage}
    Sleep    2s
    Choose File   //input[@onchange='file(event,this,3)']   ${UploadImage}
    Sleep    2s
    Click Element   //button[@onclick='saveRealName()']
