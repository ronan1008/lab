*** Settings ***
Documentation	Default browser setting for us
Library		String
Library	../library/tools/getTotp.py

*** Variables ***
${HOST}		www.proex.io
${URL}		http://${HOST}/
${MAILURL}	http://10minutemail.net//
${BW}	chrome
${NoGUI}	0
${password}	  Arborabc1234

*** Keywords ***

#############################################
#	Browser configuarion
#############################################
#############################################

Open Firefox Browser for product
	[Arguments]	${URL}
	${profile}=	Evaluate	sys.modules['selenium.webdriver'].FirefoxProfile()	sys
	Call Method	${profile}	set_preference	intl.accept_languages	en
	#Call Method	${profile}	set_preference	dom.disable_beforeunload	true
	# disable browser ask unsave page when close
	Call Method	${profile}	set_preference	browser.tabs.warnOnClose	true
	# disable browser ask unsave page when close
	Create WebDriver	Firefox	firefox_profile=${profile}
	Go To	${URL}

Open Chrome Browser for product
	[Arguments]	${URL}
	${chromeprofile} =	Evaluate	sys.modules['selenium.webdriver'].ChromeOptions()	sys
	Call Method	${chromeprofile}	add_argument	disable-gpu
	Call Method	${chromeprofile}	add_argument	--disable-extensions
	Create WebDriver	Chrome	chrome_options=${chromeprofile}
	Go To	${URL}

Open Safari Browser for product
	[Arguments]	${URL}
	Open Browser  ${URL}  browser=safari

Login WebUI
	[Documentation]	Using browser login our ui
	[Arguments]	${URL}	${BW}=firefox
	${BW}=	Convert To Lowercase	${BW}
	Run Keyword If	'${BW}' == 'firefox'	Open Firefox Browser for product	${URL}
	...	ELSE IF		'${BW}' == 'chrome'		Open Chrome Browser for product	${URL}
	...	ELSE IF		'${BW}' == 'safari'		Open Safari Browser for product	${URL}

Login ProEx Web
	[Arguments]	${username}	${password}	${key}
	Click Element	//div[@class='name']/a[@href='/index.php?m=login']
	Wait Until Element Is Visible  //input[@id='username']  timeout=10
	Input Text	//input[@id='username']	${username}
	Input Text	//input[@id='password']	${password}
	Click Element	//button[@class='login_btn']
	Wait Until Element Is Visible  //input[@class='mail_text']  timeout=10
	${token}=  Run Keyword	get_totp_token	${key}
	Input Text	//input[@class='mail_text']	${token}
	Click Element	//button[@class='login_send']
#	Wait Until Element Is Visible  //span[@class='icon icon-close safety_announcemen_close']  timeout=10
#	Click Element	//span[@class='icon icon-close safety_announcemen_close']

Change Language To
    [Arguments]     ${Lang}
	${status}=	Run Keyword And Return Status	Page Should Contain Element    //div[contains(text(),'简体中文')]
	Run Keyword If	'${status}' == 'True'    Mouse Over  //div[contains(text(),'简体中文')]
	...	ELSE IF		'${status}' == 'False'	 Mouse Over  //div[contains(text(),'English')]
	Sleep  2s
	Run Keyword If	'${Lang}' == 'CHS'	run keywords
	...	Wait Until Element Is Visible	//p[contains(text(),'简体中文')]
	...	AND     Click Element  //p[contains(text(),'简体中文')]
	Run Keyword If	'${Lang}' == 'ENG'	run keywords
	...	Wait Until Element Is Visible	//p[contains(text(),'English')]
	...	AND     Click Element  //p[contains(text(),'English')]
	Sleep  3s

Test Register In Register Page
	open browser	${MAILURL}	${BW}	alias=tab2
	open browser	${URL}	${BW}	alias=tab1
	switch browser  tab2
	Sleep   5s
    Wait Until Element Is Visible  //input[@id='fe_text']  timeout=10
    ${email_address} =    Get Value    //input[@id='fe_text']
    Set Global Variable    ${email_address}
	switch browser  tab1
    Click Element	//div[@class='name']/a[@href='/index.php?m=register']
	Wait Until Element Is Visible  //input[@id='username']  timeout=10
	Input Text	//input[@id='username']	${email_address}
	Input Text	//input[@id='password']	${password}
	Input Text	//input[@id='confirm_password']	${password}
	#Input Text	//input[@id='intro_user']	${invite}=''
	Click Element	//button[@id='e_v']
	switch browser  tab2
	Sleep  5s  reason=None
	Wait Until Element Is Visible   //table[@id='maillist']/tbody/tr/td[contains(text(),'ProEx')]	timeout=90
    Click Element   //table[@id='maillist']/tbody/tr/td[contains(text(),'ProEx')]
    Wait Until Element Is Visible   //div[@id='tab1']
    ${getVerificationCode} =    Get Text    (//span[@style='color:#e4007f;font-weight:bold;'])[2]
   # ${getVerificationCode} =  Get Regexp Matches  ${mailContent}	testcode(..)   1
    Set Global Variable    ${getVerificationCode}
	switch browser  tab1
	Input Text	//input[@id='verify']	${getVerificationCode}
	Click Element	//input[@class='check_protocol']
	Sleep	0.2s
	Click Element	//button[@class='reg_submit']
	Sleep	2s
	Wait Until Page Contains Element	//button[@class="login_btn"]	timeout=10
	Log    Register ${email_address} success!    WARN
#	[Teardown]	Close All Browsers
