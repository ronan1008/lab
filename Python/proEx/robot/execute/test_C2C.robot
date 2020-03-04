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
${HOST}		www.proex.io
${URL}		http://${HOST}/
${SSLURL}	https://${HOST}/
${BW}	chrome
${NoGUI}	0

*** Test Cases ***

Test Login Web
	[Setup]	Login WebUI	${URL}	${BW}
	Login ProEx Web	softnextqcshock@gmail.com	Arborabc1234	6RJFVNCMKMOG62SU

Test Record C2C Info On C2C Account Page
    Goto C2C Account Page
    # return ${currency} ${available_money} ${freeze_money}
    Test Record On C2C Page    USDT
