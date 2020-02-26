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
    Wait Until Element Is Visible   //input[@id='type']
    Click Element   //input[@id='type']
    Run Keyword If  '${type}' ==  'buy'    Click Element   //p[@data-type='1']
    Run Keyword If  '${type}' ==  'sell'    Click Element   //p[@data-type='2']

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

Select Pay Type On Release Page
    [Arguments]	${pay}
    Run Keyword If  '${pay}' ==  'bank'    Click Element   //input[@id='1']
    Run Keyword If  '${pay}' ==  'alipay'    Click Element   //input[@id='2']
    Run Keyword If  '${pay}' ==  'wechatpay'    Click Element   //input[@id='3']



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

