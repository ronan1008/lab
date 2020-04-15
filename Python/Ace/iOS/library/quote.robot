*** Settings ***
Documentation	行情
#Metadata			Version 0.1

*** Keywords ***
Click Banner On Quote Page
    [Arguments]	${Cryptocurrency}
    Wait Until Element Is Visible    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView//XCUIElementTypeStaticText[@name="${Cryptocurrency}"]
    Click Element     xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView//XCUIElementTypeStaticText[@name="${Cryptocurrency}"]

Get Count Of Banner On Quote Page
    ${count} =    Get Matching Xpath Count    //XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell
    Log    ${count}   WARN
    [return]    ${count}

Click Detail Of Banner On Quote Page
    [Arguments]	${Cryptocurrency}
    Wait Until Element Is Visible    //XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable//XCUIElementTypeStaticText[@name="${Cryptocurrency}"]
    Click Element    //XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable//XCUIElementTypeStaticText[@name="${Cryptocurrency}"]



Click Back Button On Quote Page
    Wait Until Element Is Visible   xpath=//XCUIElementTypeButton[@name="返回"]
    Click Element  xpath=//XCUIElementTypeButton[@name="返回"]
    Sleep   0.5s

Check Detail Info On Quote Page
    Wait Until Element Is Visible    xpath=//XCUIElementTypeNavigationBar[@name="AIPriceDetailView"]/XCUIElementTypeStaticText/XCUIElementTypeStaticText[1]
    ${ctoc} =    Get Element Attribute    xpath=//XCUIElementTypeNavigationBar[@name="AIPriceDetailView"]/XCUIElementTypeStaticText/XCUIElementTypeStaticText[1]    name
    ${price} =    Get Element Attribute    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeStaticText[1]    name
    ${volume} =    Get Element Attribute    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeStaticText[8]    name
    Log    幣種:${ctoc} 價格:${price} 數量:${volume}   WARN


Click Every Detail Of Banner On Quote Page
    ${count} =    Get Count Of Banner On Quote Page
    FOR    ${index}    IN RANGE    ${count}
        ${index}=   Evaluate    ${index} + 1
        Sleep   1s
        ${currency} =    Get Element Attribute    //XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[${index}]/XCUIElementTypeStaticText[2]    name
        Log    Check "${currency}" Detail   WARN
        Wait Until Element Is Visible    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[${index}]
        Click Element    xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[${index}]
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












