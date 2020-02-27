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


Test Release Buy In Flat Page
	Goto Flat Page
	Goto Release Page On Flat Page
    Select Trade Type On Release Page   buy
    Select Currency Type On Release Page    JPY
    Input Price On Release Page    20
    Input Number On Release Page    10
    Input Min Range On Release Page    1
    Input Max Range On Release Page    5    
    Input Pay Password On Release Page    Arborabc5678
    Select Pay Type On Release Page    wechatpay
    Input Submit On Release Page
    Sleep    2s
    Check Buyer Info On Flat Page   日本    softnextqcshock@gmail.com   9.9300  20.0000

Test Record C2C Info On C2C Account Page
    Goto C2C Account Page
