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

Test User A Login Web
	[Setup]	open browser	${URL}	${BW}	alias=A
    Login ProEx Web	softnextqcshock@gmail.com	Arborabc1234	6RJFVNCMKMOG62SU
Test User A Record C2C Info On C2C Account Page
    Goto C2C Account Page
    # return ${currency} ${available_money} ${freeze_money}
    Test Record On C2C Page    USDT
    ${init_currency}    Set Variable    ${currency}
    ${init_available_money}    Set Variable    ${available_money}
    ${init_freeze_money}    Set Variable    ${freeze_money}
    Log To Console	初始值->幣值: ${init_currency} 可用: ${init_available_money} 凍結: ${init_freeze_money}
    Show New Otc Record On C2C Page

Test User A Release Buy In Flat Page
	Goto Flat Page
	Goto Release Page On Flat Page
    Select Trade Type On Release Page   buy
    Select Currency Type On Release Page    JPY
    Input Price On Release Page    20
    Input Number On Release Page    10
    Input Min Range On Release Page    1
    Input Max Range On Release Page    5
    Input Pay Password On Release Page    Arborabc5678
    Select Pay Type On Release Page    bank
    Input Submit On Release Page
    Sleep    2s
    Check Buyer Info On Flat Page   日本    softnextqcshock@gmail.com   9.9300  20.0000

Test User A Record C2C Info After Release On C2C Account Page
    Goto C2C Account Page
    # return ${currency} ${available_money} ${freeze_money}
    Test Record On C2C Page    USDT
    ${after_currency}    Set Variable    ${currency}
    ${after_available_money}    Set Variable    ${available_money}
    ${after_freeze_money}    Set Variable    ${freeze_money}
    Log To Console	發布後->幣值: ${after_currency} 可用: ${after_available_money} 凍結: ${after_freeze_money}
    Show New Otc Record On C2C Page

Test User B Login Web
	open browser	${URL}	${BW}	alias=B
    Login ProEx Web	harry.hung@ace.io	1qaz@wsx	OVRXEBIF3AVI5TQC

Test User B Sell To A In Flat Page
    Goto Flat Page
    Click Sell Button On Buyer Info
    Input Value And Password In Sell Window    2    zajack123
    Go To   ${URL}

Switch To User A Upload Image
    switch browser  A
    Goto Flat Page
    Goto My Release Page On Flat Page
    Click First Detail On My Release Page


    Upload Image On Receipt Windows
    Go To   ${URL}


Switch To User A To Confirm Record C2C Info After B Sell
	switch browser  A
    Goto C2C Account Page
    # return ${currency} ${available_money} ${freeze_money}
    Test Record On C2C Page    USDT
    ${after_currency}    Set Variable    ${currency}
    ${after_available_money}    Set Variable    ${available_money}
    ${after_freeze_money}    Set Variable    ${freeze_money}
    Log To Console	UserA：UserB購買後->幣值: ${after_currency} 可用: ${after_available_money} 凍結: ${after_freeze_money}
    Log    UserA：UserB購買後->幣值: ${after_currency} 可用: ${after_available_money} 凍結: ${after_freeze_money}
    Show New Otc Record On C2C Page
    Goto Home Page

Test User B Sell To A In Flat Page
    Goto Flat Page
    Click Buy Button On Seller Info
    Input Value And Password In Sell Window        2    zajack123
    Go To   ${URL}

Switch To User A To Confirm Record C2C Info After B Sell
	switch browser  A
    Goto C2C Account Page
    # return ${currency} ${available_money} ${freeze_money}
    Test Record On C2C Page    USDT
    ${after_currency}    Set Variable    ${currency}
    ${after_available_money}    Set Variable    ${available_money}
    ${after_freeze_money}    Set Variable    ${freeze_money}
    Log To Console	UserA：UserB購買後->幣值: ${after_currency} 可用: ${after_available_money} 凍結: ${after_freeze_money}
    Log    UserA：UserB購買後->幣值: ${after_currency} 可用: ${after_available_money} 凍結: ${after_freeze_money}
    Show New Otc Record On C2C Page
    Goto Home Page


<button onclick="buy_sell_alert(this,'USDT')" price="20.0000000000" coin_name="USDT" min="1.0000000000" max="5.0000000000" nums="9.9300000000" cid="204" currency="JPY" type="2">賣出</button>

Test Compare Before And After On C2C Account Page




	switch browser  B