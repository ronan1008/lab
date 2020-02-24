*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1
Library		SeleniumLibrary
Resource  ../settings/browser_setting.robot

*** Variables ***
${HOST}		www.proex.io/
${URL}		http://${HOST}/
${MAILURL}	http://10minutemail.net//
${BW}	chrome
${NoGUI}	0
${username}   softnextqcshock@gmail.com
${password}	  Arborabc1234
*** Test Cases ***

Test Register In Register Page
	open browser	${URL}	${BW}	alias=tab1
	open browser	${MAILURL}	${BW}	alias=tab2
	switch browser  tab2
	Sleep   5s
    Wait Until Element Is Visible  //input[@id='fe_text']  timeout=10
    ${email_address} =    Get Value    //input[@id='fe_text']
    Set Global Variable    ${email_address}
	switch browser  tab1
    Click Element	//div[@class='name']/a[@href='/index.php?m=register']
	Wait Until Element Is Visible  //input[@id='username']  timeout=10
	Input Text	//input[@id='username']	${username}
	Input Text	//input[@id='password']	${password}
	Input Text	//input[@id='confirm_password']	${password}
	#Input Text	//input[@id='intro_user']	${invite}=''
	Click Element	//button[@id='e_v']
	switch browser  tab2
	Sleep  30s  reason=None
	Wait Until Element Is Visible   //table[@id='maillist']/tbody/tr/td[contains(text(),'ronan1008')]
    Click Element   //table[@id='maillist']/tbody/tr/td[contains(text(),'ronan1008')]
    Wait Until Element Is Visible   //div[@id='tab1']
    ${mailContent} =    Get Text    //div[@id='tab1']/div/div[@dir='ltr']
    ${getVerificationCode} =  Get Regexp Matches  ${mailContent}	testcode(..)   1
    Set Global Variable    ${getVerificationCode}
	switch browser  tab1
	Input Text	//input[@id='verify']	${getVerificationCode}
