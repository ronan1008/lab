*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1

Library		SeleniumLibrary
Resource	../settings/login_setting.robot
Resource	../settings/browser_setting.robot
Resource	../library/front_end/front_menu.robot
Resource	../library/front_end/flat.robot
Resource	../library/front_end/c2c_account.robot

*** Variables ***
${HOST}		www.proex.io/
${URL}		http://${HOST}/
${SSLURL}	https://${HOST}/
${BW}	chrome
${NoGUI}	0


*** Test Cases ***
Test User A Login Web
	[Setup]	open browser	${URL}	${BW}	alias=A
    Change Language To  CHS
	Change Language To  ENG
    Login ProEx Web	softnextqcshock@gmail.com	Arborabc1234	6RJFVNCMKMOG62SU

