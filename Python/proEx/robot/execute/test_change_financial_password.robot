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
    Goto Change Financial Password
    Change Pass On Change Financial Password Page   Arborabc5678    Arborabc8765    F125421771  6RJFVNCMKMOG62SU
    Sleep    2s
    Goto Account Security Page
    Goto Change Financial Password
    Change Pass On Change Financial Password Page   Arborabc8765    Arborabc5678    F125421771  6RJFVNCMKMOG62SU
