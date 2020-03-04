*** Settings ***
Library           DateTime
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
    Log    C2C帳戶 -> 幣值 : ${currency} 可用: ${available_money} 凍結: ${freeze_money}    WARN

Set Init Datetime 
    ${now_datetime} =      Get Current Date    local    exclude_millis=yes
    Set Global Variable    ${now_datetime}
    Log    執行時間 ${now_datetime}    WARN

Show New Otc Record On C2C Page
    ${record_datetime} =    Get Text    //tbody[@class='record-list']//tr[1]/td[1]
    ${record_datetime} =    Convert Date    ${record_datetime}   exclude_millis=yes  
    Log    執行時間 ${now_datetime}    WARN
    Log    記錄時間 ${record_datetime}   WARN
    Run Keyword If    '${record_datetime}' > '${now_datetime}'    Get All Otc Record On C2C Page 
    ...    ELSE    Log    No Record On C2C Page    WARN

Get All Otc Record On C2C Page
    ${count} =   Get Element Count  //td[text()='${record_datetime}']
    FOR    ${num}    IN RANGE   ${count}
        ${num} =  Evaluate    ${num}+1
        ${datetime} =  Get Text    (//td[text()='${first_column}']/..)[${num}]/td[1]
        ${currency} =  Get Text    (//td[text()='${first_column}']/..)[${num}]/td[2]
        ${number} =  Get Text    (//td[text()='${first_column}']/..)[${num}]/td[3]
        ${comment} =  Get Text    (//td[text()='${first_column}']/..)[${num}]/td[4]
        Log  實際 : ${datetime} ${currency} ${number} ${comment}    WARN
        Log  期待 : ${datetime} ${currency} ${number} ${comment}    WARN
    END

Goto Otc Record On C2C Page
    Wait Until Element Is Visible   //a[@href='/index.php?m=otcrecord']
    Click Element   //a[@href='/index.php?m=otcrecord']

