*** Settings ***
Documentation	flat page function control
Resource	./front_menu.robot

#Metadata			Version 0.1
*** Variables ***


*** Keywords ***
Test Record On C2C Page
	[Arguments]	${money}
    Wait Until Element Is Visible   //ul[@class='otc-wallet-list']/li/p[1]
    ${currency} =    Get Text    //ul[@class='otc-wallet-list']/li/p[contains(text(),'${money}')]
    ${available_money} =    Get Text     //ul[@class='otc-wallet-list']/li/p[contains(text(),'${money}')]/following-sibling::p[1]
    ${freeze_money} =    Get Text   //ul[@class='otc-wallet-list']/li/p[contains(text(),'${money}')]/following-sibling::p[2]
    Set Global Variable  ${currency}
    Set Global Variable  ${available_money}
    Set Global Variable  ${freeze_money}

Show New Otc Record On C2C Page
    ${first_column} =   Get Text    //tbody[@class='record-list']//tr[1]/td[1]
    ${count} =   Get Element Count  //td[text()='${first_column}']
    FOR    ${num}    IN RANGE   ${count}
        ${num} =  Evaluate    ${num}+1
        ${datetime} =  Get Text    (//td[text()='${first_column}']/..)[${num}]/td[1]
        ${currency} =  Get Text    (//td[text()='${first_column}']/..)[${num}]/td[2]
        ${number} =  Get Text    (//td[text()='${first_column}']/..)[${num}]/td[3]
        ${comment} =  Get Text    (//td[text()='${first_column}']/..)[${num}]/td[4]
        Log  ${datetime} ${currency} ${number} ${comment}    WARN
    END

(//td[text()='${first_column}']/..)[1]/td[1]
(//td[text()='${first_column}']/..)[1]/td[2]
(//td[text()='${first_column}']/..)[1]/td[3]
(//td[text()='${first_column}']/..)[1]/td[4]


Goto Otc Record On C2C Page
    Wait Until Element Is Visible   //a[@href='/index.php?m=otcrecord']
    Click Element   //a[@href='/index.php?m=otcrecord']