*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1

Library		SeleniumLibrary
Resource	../settings/browser_setting.robot
Resource	../library/tools/get10minutes.robot 

*** Variables ***
${HOST}		www.proex.io/
${URL}		http://${HOST}/
${MAILURL}	http://10minutemail.net//
${BW}	chrome
${NoGUI}	0

*** Test Cases ***

Test Input Email In Register Page
[Setup]	Login WebUI	${URL}	${BW}
    Test Login 10minutemail And Return Email 
    Login WebUI    ${MAILURL}   ${BW}
    Register ProEx Page    ${mail}  ${password}	${key} ${invite}


	



Register ProEx Page
	[Arguments]	${username}	${password}	${key} ${invite}
    [Setup]	Login WebUI	${URL}	${BW}
	Click Element	//div[@class='name']/a[@href='/index.php?m=register']
	Wait Until Element Is Visible  //input[@id='username']  timeout=10
	Input Text	//input[@id='username']	${username}
	Input Text	//input[@id='password']	${password}
	Input Text	//input[@id='confirm_password']	${password}
	Input Text	//input[@id='intro_user']	${invite}

Test Register Page

