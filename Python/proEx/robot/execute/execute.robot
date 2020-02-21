*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1

Library		SeleniumLibrary
#Library		../library/DisplayLib.py
Resource	../settings/login_setting.robot
Resource	../settings/browser_setting.robot
Resource	../library/front_end/front_menu.robot
Resource	../library/front_end/flat.robot
#Suite Setup	DisplayLib.Start	${NoGUI}
#Suite Teardown	DisplayLib.Stop	${NoGUI}

*** Variables ***
${HOST}		www.proex.io/
${URL}		http://${HOST}/
${SSLURL}	https://${HOST}/
${BW}	chrome
${NoGUI}	0

*** Test Cases ***


Test Login ProEx Web
	[Setup]	Login WebUI	${URL}	${BW}
	Login ProEx Web	softnextqcshock@gmail.com	Arborabc1234	6RJFVNCMKMOG62SU


	
Test Add Account In Flat Page
	Goto Flat Page
	Goto Bank Card Management Page On Flat Page
	Add Bank Info On Bank Card Management Page
	Add Bank Account On Bank Info Page
	Sleep	5s
	Add Bank Info On Bank Card Management Page
	Add Wechat Account On Bank Info Page
	Sleep	5s
	Add Bank Info On Bank Card Management Page
	Add Alipay Account On Bank Info Page


Add Bank Info On Bank Card Management Page
	
#	[Teardown]	Close Browser