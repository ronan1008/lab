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
    Sleep    3s
	Login ProEx Web	softnextqcshock@gmail.com	Arborabc1234	6RJFVNCMKMOG62SU
    Set Init Datetime

Test User A Record C2C Info On C2C Account Page
    Goto C2C Account Page
    Test Record On C2C Page    USDT
    Goto Otc Record On C2C Page
    Show New Otc Record On C2C Page