*** Settings ***
Documentation	flat page function control
Resource	./front_menu.robot

#Metadata			Version 0.1
*** Variables ***
${UploadImage}	/Users/shocklee/Documents/GitHub/workspace/Python/proEx/robot/library/tools/S__4390953.jpg
${PayPassword}	Arborabc5678

*** Keywords ***

Goto Release Page On Flat Page
    Wait Until Element Is Visible   //a[@data-href='/index.php?c=trans&m=release']    timeout=10
    Click Element  //a[@data-href="/index.php?c=trans&m=release"]

Select Trade Type On Release Page
    [Arguments]	${type}
    Wait Until Element Is Visible   //span[@id='type-name']
    Click Element   //span[@id='type-name']
    Wait Until Element Is Visible   //p[@data-type='2']
    Run Keyword If  '${type}' == 'buy'    Click Element   //p[@data-type='1']
    Run Keyword If  '${type}' == 'sell'    Click Element   //p[@data-type='2']

Select Currency Type On Release Page
    [Arguments]	${currency}
    Click Element   //span[@id='currency']
    Wait Until Element Is Visible   //p[@data-countryid and text()='${currency}']
    Click Element   //p[@data-countryid and text()='${currency}']

Input Price On Release Page
    [Arguments]	${price}
    Input Text  //input[@id='price']  ${price}

Input Number On Release Page
    [Arguments]	${number}
    Input Text  //input[@id='nums']  ${number}

Input Min Range On Release Page
    [Arguments]	${min}
    Input Text  //input[@id='min']  ${min}
Input Max Range On Release Page
    [Arguments]	${max}
    Input Text  //input[@id='max']  ${max}

Input Pay Password On Release Page
    [Arguments]	${pass}
    Input Text  //input[@id='deal_psw']  ${pass}

Input Submit On Release Page
    Click Element   //button[@onclick='releaseC2C()']

Check Buyer Info On Flat Page
    [Arguments]	${country}  ${seller_name}  ${remain}   ${price}
    ${status} =    Run Keyword And Return Status    Page Should Contain Element    //content[@id='sell']//li/p[text() = '${country}']/following-sibling::p[text() = '${seller_name}']/following-sibling::p[text() = '${remain}']/following-sibling::p[text() = '${price}']    timeout=10
    Run Keyword If  '${status}' == 'True'  Log    資料正確     WARN
    Run Keyword If  '${status}' == 'False'  Log    發現錯誤    ERROR

Check Seller Info On Flat Page
    [Arguments]	${country}  ${buyer_name}   ${remain}   ${price}
    ${status} =    Run Keyword And Return Status    Page Should Contain Element   //content[@id='buy']//li/p[text() = '${country}']/following-sibling::p[text() = '${buyer_name}']/following-sibling::p[text() = '${remain}']/following-sibling::p[text() = '${price}']    timeout=10
    Run Keyword If  '${status}' == 'True'  Log    資料正確     WARN
    Run Keyword If  '${status}' == 'False'  Log    發現錯誤    ERROR

Click Sell Button On Buyer Info
    Wait Until Element Is Visible   (//button[@type='2' and @price='20.0000000000' and @nums='9.9300000000'and @coin_name='USDT' and @currency='JPY'])[1]
    Click Element  (//button[@type='2' and @price='20.0000000000' and @nums='9.9300000000'and @coin_name='USDT' and @currency='JPY'])[1]

Click Buy Button On Seller Info
    Wait Until Element Is Visible   (//button[@type='1' and @price='20.0000000000' and @nums='9.9300000000'and @coin_name='USDT' and @currency='AUD'])[1]
    Click Element  (//button[@type='1' and @price='20.0000000000' and @nums='9.9300000000'and @coin_name='USDT' and @currency='AUD'])[1]

Input Value And Password In Buy Window
    [Arguments]	${number}   ${password}
    [Documentation]    輸入數量在買入USDT視窗
    Input Text  //input[@id='buy_amount']   ${number}
    Click Element   //button[@data-type='1']
    Wait Until Element Is Visible   //p[@class='buy_pay_password']
    Input Text  (//input[@type='password'])[1]  ${password}
    Click Element   //p[@class='buy_pay_password']

Input Value And Password In Sell Window
    [Arguments]	${number}   ${password} ${type}
    [Documentation]    輸入數量在賣出USDT
    Input Text  //input[@id='sell_amount']   ${number}
    Click Element   //button[@data-type='2']
    Wait Until Element Is Visible   //p[@onclick='submitOrder(this)']
    Input Text  (//input[@type='password'])[3]  ${password}
    Select Pay Type In Sell Window  ${type}
    Click Element   //p[@onclick='submitOrder(this)']

Select Pay Type In Sell Window
    [Arguments]	${type}
    Run Keyword If  '${type}' == 'bank'    Click Element   //input[@id='bank']/following-sibling::label
    Run Keyword If  '${type}' == 'alipay'    Click Element   //input[@id='zfb']/following-sibling::label
    Run Keyword If  '${type}' == 'wechatpay'    Click Element   //input[@id='wx']/following-sibling::label

Upload Image On Receipt Windows
    Click Element  (//a[@class='upload_voucher'])[1]
    Sleep  1s
    Choose File    //input[@id='upload1']    ${UploadImage}
    Sleep  3s
    Click Element  (//button[@class='update_voucher_submit'])
    Sleep  1s

Goto My Release Page On Flat Page
    Wait Until Element Is Visible   //a[@data-href='/index.php?c=trans&m=myRelease']
    Click Element   //a[@data-href='/index.php?c=trans&m=myRelease']

Click First Detail On My Release Page
    Wait Until Element Is Visible   (//a[contains(@href,'myReleaseDetail')])[1]
    Click Element   (//a[contains(@href,'myReleaseDetail')])[1]

Click First Confirm On Detail Page
    Wait Until Element Is Visible   (//a[contains(@onclick,'paid')])[1]
    Click Element   (//a[contains(@onclick,'paid')])[1]

Click First Take Off On My Release Page
    Wait Until Element Is Visible    (//a[@href='javascript:void(0)'])[1]
    Click Element    (//a[@href='javascript:void(0)'])[1]

Select Pay Type On Release Page
    [Arguments]	${pay}
    Run Keyword If  '${pay}' == 'bank'    Click Element   //input[@id='one']/..
    Run Keyword If  '${pay}' == 'alipay'    Click Element   //input[@id='two']/..
    Run Keyword If  '${pay}' == 'wechatpay'    Click Element   //input[@id='three']/..

Goto Bank Card Management Page On Flat Page
    Wait Until Element Is Visible   //span[@class='icon icon-creditcardalt']/parent::a[@href='/index.php?c=trans&m=card']    timeout=10
    Click Element  //span[@class='icon icon-creditcardalt']/parent::a[@href='/index.php?c=trans&m=card']

Delete Bank Info On Bank Card Management Page
    ${delCount} =  Get Element Count   //p[@onclick='deletePay(this)']
    Run Keyword If  ${delCount} > 1    run keywords
    ...    Click Element    (//ul/li/div/p[@onclick='deletePay(this)'])[1]
    ...	AND		Wait Until Element Is Visible    //input[@id='deal_password']
    ...	AND		Input Text   //input[@id='deal_password']    ${PayPassword}
    ...	AND		Wait Until Element Is Visible    (//button[@type='button'])[4]
    ...	AND     Sleep   1s
    ...	AND		Click Element    (//button[@type='button'])[4]
    Sleep   2s

Add Bank Info On Bank Card Management Page
    Wait Until Element Is Visible  //section//div[@class='add add_bank_card']    timeout=10
    Click Element  //section//div[@class='add add_bank_card']

Add Bank Account On Bank Info Page
    Wait Until Element Is Visible    //i[contains(@class,'icon icon-unfold')]/preceding-sibling::input[@type='text']
    Sleep	1s
    Click Element  //i[contains(@class,'icon icon-unfold')]/preceding-sibling::input[@type='text']
    Click Element  //ul/li[@pay_name='bank']
    Input Text  //input[@id='kh']   玉山銀行
    Input Text  //input[@id='kh_address']   上海
    Input Text  //input[@id='card_number']   1111222233334444
    Input Text  //input[@type='password']   ${PayPassword}
    Click Element  //div[@class='text']/preceding-sibling::button[@type='button']

Add Wechat Account On Bank Info Page
    Wait Until Element Is Visible    //i[contains(@class,'icon icon-unfold')]/preceding-sibling::input[@type='text']
    Sleep	1s
    Click Element  //i[contains(@class,'icon icon-unfold')]/preceding-sibling::input[@type='text']
    Wait Until Element Is Visible   //ul/li[@pay_name='wxpay']
    Click Element  //ul/li[@pay_name='wxpay']
    Input Text    //input[@id='account']  wxpay1234567
    Choose File    //input[@id='upload']  ${UploadImage}
    Sleep	5s
    Input Text    (//div[@class='input-box']/input[@class='password'])[2]   ${PayPassword}
    Click Element  //div[@class='text']/preceding-sibling::button[@type='button']

Add Alipay Account On Bank Info Page
    Wait Until Element Is Visible    //i[contains(@class,'icon icon-unfold')]/preceding-sibling::input[@type='text']
    Sleep	1s
    Click Element  //i[contains(@class,'icon icon-unfold')]/preceding-sibling::input[@type='text']
    Wait Until Element Is Visible   //ul/li[@pay_name='alipay']
    Click Element  //ul/li[@pay_name='alipay']
    Input Text    //input[@id='account']  alipay123456
    Choose File    //input[@id='upload']  ${UploadImage}
    Sleep	5s
    Input Text    (//div[@class='input-box']/input[@class='password'])[2]   ${PayPassword}
    Click Element  //div[@class='text']/preceding-sibling::button[@type='button']



    