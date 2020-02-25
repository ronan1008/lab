*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1

Library		SeleniumLibrary
Resource	../settings/login_setting.robot
Resource	../settings/browser_setting.robot
Resource	../library/front_end/front_menu.robot
Resource	../library/front_end/flat.robot

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


Test Delete Account In Flat Page
	Goto Flat Page
	Goto Bank Card Management Page On Flat Page
	Delete Bank Info On Bank Card Management Page
	Delete Bank Info On Bank Card Management Page
