*** Settings ***
Documentation	flat page function control
Resource	./front_menu.robot
...						include [TOMODIFY]
#Metadata			Version 0.1

*** Keywords ***

Goto Credit Card Management Page On Flat Page
    Wait Until Element Is Visible   //a[@href="/index.php?c=trans&m=card"]    timeout=10
    Click Element  //a[@href="/index.php?c=trans&m=card"]

Add Credit Card On Management Page
    Wait Until Element Is Visible  //div[@class='add add_bank_card']    timeout=10
    Click Element  //div[@class='add add_bank_card']

Add Bank Account On Credit Card Page
    Wait Until Element Is Visible    //i[@class='icon icon-unfold active']/preceding-sibling::input[@type='text']
    Click Element  //i[@class='icon icon-unfold active']/preceding-sibling::input[@type='text']
    Click Element  //ul/li[@pay_name='bank']
    Input Text  //input[@id='kh']   中國銀行
    Input Text  //input[@id='kh_address']   上海
    Input Text  //input[@id='card_number']   111144442222333
    Input Text  //input[@type='password']   Arborabc5678
    Click Element  //input[@type='button']

Add Wechat Account On Credit Card Page

Add Alipay Account On Credit Card Page

    ${count} =  Get Element Count   //ul/li/div[@class='number']
    Run Keyword If	'${count}}' > 1

$x("//ul/li/div[@class='number']")

$x("//ul/li/div/p[@onclick='deletePay(this)']")
