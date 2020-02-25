*** Settings ***
Documentation	front end page function control
#Metadata			Version 0.1

*** Keywords ***

Input Email On Forget Password Page
	[Arguments]	${username}
    Wait Until Element Is Visible   //input[@id='username']   timeout=10
    Input Text  //input[@id='username']  ${username}

Input Verification Code On Forget Password Page
    [Arguments]	${Verification}
    Wait Until Element Is Visible   //input[@class='mail_text']   timeout=10
    Input Text  //input[@class='mail_text']    ${Verification}

Click Get Verify Code On Forget Password Page
    Wait Until Element Is Visible   //button[@id='get_email_v']   timeout=10
    Click Element  //button[@id='get_email_v']  

Click Next On Forget Password Page
    Wait Until Element Is Visible   //button[@class='next-step']   timeout=10
    Click Element  //button[@class='next-step'] 


