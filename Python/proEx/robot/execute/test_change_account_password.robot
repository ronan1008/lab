*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1

Library		SeleniumLibrary
Resource	../settings/login_setting.robot
Resource	../settings/browser_setting.robot
Resource	../library/front_end/safety.robot
Resource	../library/front_end/front_menu.robot



*** Variables ***
${HOST}		www.proex.io
${URL}		http://${HOST}/
${SSLURL}	https://${HOST}/
${BW}	chrome
${NoGUI}	0

*** Test Cases ***

Test User A Login Web
	[Setup]	open browser	${URL}	${BW}	alias=A
    Login ProEx Web	softnextqcshock@gmail.com	Arborabc1234	6RJFVNCMKMOG62SU


Test Change Pass On Change Financial Password Page
    Goto Account Security Page
    Goto Change Account Password
    Change Pass On Change Account Password Page    Arborabc1234    Arborabc4321    6RJFVNCMKMOG62SU
    Sleep    3s
    Goto Home Page
    Login ProEx Web	softnextqcshock@gmail.com	Arborabc4321	6RJFVNCMKMOG62SU
    Goto Account Security Page
    Goto Change Account Password
    Change Pass On Change Account Password Page    Arborabc4321    Arborabc1234    6RJFVNCMKMOG62SU
