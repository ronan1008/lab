*** Settings ***
Documentation	Default browser setting for us
Library		String
Library	../library/tools/getTotp.py

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
	Wait Until Element Is Visible  //span[@class='icon icon-close safety_announcemen_close']  timeout=10
	Click Element	//span[@class='icon icon-close safety_announcemen_close']

confirm_password