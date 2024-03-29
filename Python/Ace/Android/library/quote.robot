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

Check Detail Info On Quote Page
    Wait Until Element Is Visible    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/tvQuotesDetailCurrency']
    ${ctoc} =    Get Element Attribute    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/tvQuotesDetailCurrency']    text
    ${price} =    Get Element Attribute    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/tvQuotesDetailPrice']    text
    ${volume} =    Get Element Attribute    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/tvQuotesDetailVolume']    text
    Log    幣種:${ctoc} 價格:${price} 數量:${volume}   WARN

Click Every Detail Of Banner On Quote Page
    ${count} =    Get Count Of Banner On Quote Page
    FOR    ${index}    IN RANGE    ${count}
        Sleep   0.5s
        ${currency} =    Get Element Attribute    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_item_layout' and @index='${index}']/*[@resource-id='com.asiainnovations.ace.taiwan:id/tvCurrencyName']    text
        Log    Check "${currency}" Detail   WARN
        Wait Until Element Is Visible    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_item_layout' and @index='${index}']
        Click Element    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_item_layout' and @index='${index}']
        Check Detail Info On Quote Page
        Click Back Button On Quote Page
    END

Check All Collections On Quote Page
    ${count}=     Get Matching Xpath Count    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/viewCollection']
    Log    ${count}    WARN
    FOR    ${index}    IN RANGE    ${count}
        Sleep   0.5s
        Click Element    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_item_layout' and @index='${index}']/*[@resource-id='com.asiainnovations.ace.taiwan:id/viewCollection']
        ${text} =    Get Element Attribute    xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_item_layout' and @index='${index}']/*[@resource-id='com.asiainnovations.ace.taiwan:id/tvCurrencyName']    text
        Log    Checked : ${text}    WARN
    END

Checked Collections On Quote Page
    [Arguments]	${Cryptocurrency}
    Click Element    xpath=//*[@text='${Cryptocurrency}']/following-sibling::*[@class='android.widget.CheckBox'][1]












