*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1

Library		SeleniumLibrary
Resource	../../settings/browser_setting.robot


*** Variables ***
${HOST}		10minutemail.net/
${URL}		http://${HOST}/
${SSLURL}	https://${HOST}/
${BW}	chrome
${NoGUI}	0

*** Test Cases ***


Test Login 10minutemail And Return Email
	[Setup]	Login WebUI	${URL}	${BW}
    Sleep   5s
    Wait Until Element Is Visible  //input[@id='fe_text']  timeout=10
    ${email_address} =    Get Value    //input[@id='fe_text']  
    Set Global Variable    ${email_address}

Test Check 10minutemail And Click Mail Then Return Verfication Code
    Wait Until Element Is Visible   //table[@id='maillist']/tbody/tr/td[contains(text(),'ronan1008')]
    Click Element   //table[@id='maillist']/tbody/tr/td[contains(text(),'ronan1008')]
    Wait Until Element Is Visible   //div[@id='tab1']
    ${mailContent} =    Get Text    //div[@id='tab1']/div/div[@dir='ltr']
    ${getVerificationCode} =  Get Regexp Matches  ${mailContent}	testcode(..)   1
    Set Global Variable    ${email_address}



