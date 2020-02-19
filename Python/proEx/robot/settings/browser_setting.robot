*** Settings ***
Documentation	Default browser setting for us
Library		String

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
	Login Climax Web
	

Login Register Page 
	[Documentation]	Using browser login our ui
	[Arguments]	${URL}	${BW}=firefox
	${BW}=	Convert To Lowercase	${BW}
	Run Keyword If	'${BW}' == 'firefox'	Open Firefox Browser for product	${URL}
	...	ELSE IF		'${BW}' == 'chrome'		Open Chrome Browser for product	${URL}
	...	ELSE IF		'${BW}' == 'safari'		Open Safari Browser for product	${URL}
	Maximize Browser Window
    Reload Page
	
	