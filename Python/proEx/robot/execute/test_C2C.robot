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
#	Change Language To  CHS
#	Change Language To  ENG
	Login ProEx Web	softnextqcshock@gmail.com	Arborabc1234	6RJFVNCMKMOG62SU

Test Record C2C Info On C2C Account Page
    Goto C2C Account Page
    # return ${currency} ${available_money} ${freeze_money}
    Test Record On C2C Page    USDT
    ${init_currency}    Set Variable    ${currency}
    ${init_available_money}    Set Variable    ${available_money}
    ${init_freeze_money}    Set Variable    ${available_money}
    Log To Console	幣值: ${init_currency} 可用: ${init_available_money} 凍結: ${init_freeze_money}
