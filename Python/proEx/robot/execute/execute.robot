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
Test User B Login Web
	open browser	${URL}	${BW}	alias=B
    Login ProEx Web	harry.hung@ace.io	1qaz@wsx	OVRXEBIF3AVI5TQC
Test User B Sell To A In Flat Page
    Goto Flat Page
    Click Sell Button On Buyer Info
    Input Value And Password In Sell Window    2    zajack123
    Go To   ${URL}