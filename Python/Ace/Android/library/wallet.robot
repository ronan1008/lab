*** Settings ***
Documentation	行情
#Metadata			Version 0.1

*** Keywords ***

Click Charge Cash On Trade Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_recharge
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_recharge

Click Withdraw Cash On Trade Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_withdraw
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_withdraw

Click Charge Coin On Trade Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_charging
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_charging

Click Withdraw Coin On Trade Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_coin
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_coin

Get Info In Charge Cash On Trade Page
    [Arguments]	${info}
    Wait Until Element Is Visible    xpath=//*[@text='${info}']/following-sibling::*[1]
    ${text} =    Get Element Attribute    xpath=//*[@text='${info}']/following-sibling::*[1]    text
    [return]    ${text}
    
Click Back Button On Trade page 
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/iv_back
    Click Element  id=com.asiainnovations.ace.taiwan:id/iv_back
























