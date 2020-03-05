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
${UploadImage}	/Users/shocklee/Documents/GitHub/workspace/Python/proEx/robot/library/tools/S__4390953.jpg

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

Test User A Release Sell In Flat Page
	Goto Flat Page
	Goto Release Page On Flat Page
    Select Trade Type On Release Page   sell
    Select Currency Type On Release Page    AUD
    Input Price On Release Page    9999
    Input Number On Release Page    20
    Input Min Range On Release Page    1
    Input Max Range On Release Page    10
    Input Pay Password On Release Page    Arborabc5678
    Select Pay Type On Release Page    bank
    Input Submit On Release Page
    Sleep    2s
    Check Seller Info On Flat Page   澳大利亚    softnextqcshock@gmail.com   9.9300  20.0000
    Log    UserA：發布賣幣->幣種: AUD 價格: 20 數量: 10 範圍:1~10 支付方式:bank   WARN

Test User A Record C2C Info After Release On C2C Account Page
    Goto C2C Account Page
    Test Record On C2C Page    USDT
    Goto Otc Record On C2C Page
    Show New Otc Record On C2C Page
    Goto Home Page

Test User B Login Web
	open browser	${URL}	${BW}	alias=B
    Sleep    3s
    Login ProEx Web	harry.hung@ace.io	1qaz@wsx	OVRXEBIF3AVI5TQC

Test User B Buy From A In Flat Page
    Goto Flat Page
    Click Buy Button On Seller Info
    Input Value And Password In Buy Window    2    zajack123
    Log    UserB：買幣->數量: 2 範圍:1~5 支付方式:bank   WARN
    Go To   ${URL}

Switch To User A To Confirm Record C2C Info After B Buy
	switch browser  A
    Goto C2C Account Page
    # return ${currency} ${available_money} ${freeze_money}
    Test Record On C2C Page    USDT
    Goto Otc Record On C2C Page
    Show New Otc Record On C2C Page
    Goto Home Page

Switch To User B Upload Image
    switch browser  B
    Goto Flat Page
    Upload Image On Receipt Windows
    Go To   ${URL}
    Log    UserB：上傳收據    WARN

Switch To User A To Confirm Record C2C Info After B Upload Image
	switch browser  A
    Goto C2C Account Page
    # return ${currency} ${available_money} ${freeze_money}
    Test Record On C2C Page    USDT
    Goto Otc Record On C2C Page
    Show New Otc Record On C2C Page
    Goto Home Page

Test User A Confirm B Trans On My Release Page
    Goto Flat Page
    Goto My Release Page On Flat Page
    Click First Detail On My Release Page
    Click First Confirm On Detail Page
    Log    UserA：將B的交易 已收款    WARN

Test User A To Confirm Record C2C Info After A Confirm B Trans
    Goto C2C Account Page
    # return ${currency} ${available_money} ${freeze_money}
    Test Record On C2C Page    USDT
    Goto Otc Record On C2C Page
    Show New Otc Record On C2C Page
    Goto Home Page

Test User A Take Off Order
    Goto Flat Page
    Goto My Release Page On Flat Page
    Click First Take Off On My Release Page
    Goto Home Page
    Log    UserA：將訂單下架    WARN

Test User A Record C2C Info After Take Off Order
    Goto C2C Account Page
    # return ${currency} ${available_money} ${freeze_money}
    Test Record On C2C Page    USDT
    Goto Otc Record On C2C Page
    Show New Otc Record On C2C Page
    Goto Home Page
