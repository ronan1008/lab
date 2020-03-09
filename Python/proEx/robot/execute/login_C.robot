*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1

Library		SeleniumLibrary
Resource	../settings/login_setting.robot
Resource	../settings/browser_setting.robot
Resource	../library/front_end/front_menu.robot
Resource	../library/front_end/flat.robot
Resource	../library/front_end/safety.robot

*** Variables ***
${HOST}		www.proex.io
${URL}		http://${HOST}/
${SSLURL}	https://${HOST}/
${BW}	chrome
${NoGUI}	0

*** Test Cases ***
Test User C Login Web
	[Setup]	open browser	${URL}	${BW}	
    Test Login ProEx Web Without Key    ns3401.test@gmail.com    Arborabc1234

Test Real Name Authentication
    Goto Real Name Authentication Page
    Input Personal Info On Authentication Page  陳小明  F12312312434