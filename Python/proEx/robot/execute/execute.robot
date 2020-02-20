*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1

Library		SeleniumLibrary
#Library		../library/DisplayLib.py
Resource	../settings/login_setting.robot
Resource	../settings/browser_setting.robot
Resource	../library/front_end/front_menu.robot
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

Test Every Web Page
	Goto Home Page
	Goto IEO Page
	Goto C2C Account Page
	Goto Open Orders Page
	Goto Order History Page
	Goto Personal settings Page
	Goto Recharge and Withdraw Page
	Goto Flat Page
	Goto App Download Page
	Goto Account Security Page
	Goto Sign Out Page

#	[Teardown]	Close Browser