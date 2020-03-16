*** Settings ***
Documentation	行情
#Metadata			Version 0.1

*** Keywords ***
Click Banner On Quote Page
    [Arguments]	${Cryptocurrency}
    Wait Until Element Is Visible    xpath=//*[@resource-id='android:id/text1' and @text='${Cryptocurrency}']
    Click Element     xpath=//*[@resource-id='android:id/text1' and @text='${Cryptocurrency}']

Get Count Of Banner On Quote Page
    ${count} =    Get Matching Xpath Count    //*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_item_layout']
    Log    ${count}   WARN
    [return]    ${count}

Click Detail Of Banner On Quote Page
    [Arguments]	${Cryptocurrency}
    Click Element    //*[@text='${Cryptocurrency}' and @resource-id='com.asiainnovations.ace.taiwan:id/tvCurrencyName']

Click Back Button On Quote Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/tvBack
    Click Element  id=com.asiainnovations.ace.taiwan:id/tvBack

Click Every Detail Of Banner On Quote Page
    ${count} =    Get Count Of Banner On Quote Page
    FOR    ${index}    IN RANGE    ${count}
        ${currency} =    Get Element Attribute    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_item_layout' and @index='${index}']/*[@resource-id='com.asiainnovations.ace.taiwan:id/tvCurrencyName']    text
        Log    Check "${currency}" Detail   WARN
        Click Element    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_item_layout' and @index='${index}']
        Click Back Button On Quote Page
    END




















