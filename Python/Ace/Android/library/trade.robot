*** Settings ***
Documentation	行情
#Metadata			Version 0.1

*** Keywords ***

Choose Currency To Currency Exchange
    [Arguments]	${currency1}    ${currency2}
    [Documentation]     左上角的匯率->上面欄位幣值->底下的詳情
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/tvTradingCurrencyName
    Click Element    id=com.asiainnovations.ace.taiwan:id/tvTradingCurrencyName
    Click Element    //*[@resource-id='android:id/text1' and @text='${currency1}']
    Click Element    //*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_item_layout']/*[@text='${currency2}']
    Log    選擇 ${currency1} -> ${currency2} 交易  WARN


Click BuyIn On Trade Page
    [Documentation]    買入 分頁
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/tvBuyBtn
    Click Element  id=com.asiainnovations.ace.taiwan:id/tvBuyBtn

Click SellOut On Trade Page
    [Documentation]    賣出 分頁
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/tvSellBtn
    Click Element  id=com.asiainnovations.ace.taiwan:id/tvSellBtn



Input Price On Trade Page
    [Documentation]    單價欄位
    [Arguments]	${price}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/etTradingPrice
    Input Text  id=com.asiainnovations.ace.taiwan:id/etTradingPrice    ${price}

Click Up Button In Price On Trade Page
    [Documentation]    單價欄位＋
    [Arguments]	${times}

    FOR    ${index}    IN RANGE    ${times}
        Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/viewAdd1
        Click Element  id=com.asiainnovations.ace.taiwan:id/viewAdd1
    END

Click Down Button In Price On Trade Page
    [Documentation]    單價欄位-
    [Arguments]	${times}

    FOR    ${index}    IN RANGE    ${times}
        Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/viewSub1
        Click Element  id=com.asiainnovations.ace.taiwan:id/viewSub1
    END

Input Amount On Trade Page
    [Documentation]    數量欄位
    [Arguments]	${amount}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/etTradingNum
    Input Text  id=com.asiainnovations.ace.taiwan:id/etTradingNum    ${amount}

Click Up Button In Amount On Trade Page
    [Documentation]    數量欄位+
    [Arguments]	${times}
    FOR    ${index}    IN RANGE    ${times}
        Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/viewAdd2
        Click Element  id=com.asiainnovations.ace.taiwan:id/viewAdd2
    END

Click Down Button In Amount On Trade Page
    [Documentation]    數量欄位-
    [Arguments]	${times}
    FOR    ${index}    IN RANGE    ${times}
        Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/viewSub2
        Click Element  id=com.asiainnovations.ace.taiwan:id/viewSub2
    END



Click Buy Button On Trade Page
    [Documentation]    買 按鈕
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/btnPostOrder
    Click Element  id=com.asiainnovations.ace.taiwan:id/btnPostOrder

Click Sell Button On Trade Page
    [Documentation]    賣 按鈕
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/btnPostOrder' and @index='21']
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/btnPostOrder' and @index='21']

Click Cancel Order Button On Trade Page
    [Documentation]    撤單
    [Arguments]	${number}
    ${number}=    Evaluate    ${number} - 1
    Wait Until Element Is Visible   xpath=//*[@class='android.view.ViewGroup' and @index='${number}']/*[@resource-id='com.asiainnovations.ace.taiwan:id/btnCancel']  
    Click Element  xpath=//*[@class='android.view.ViewGroup' and @index='${number}']/*[@resource-id='com.asiainnovations.ace.taiwan:id/btnCancel']  


Check List In My Order On Trade Page
    [Arguments]    ${type}    ${currency1}    ${currency2}    ${amount}    ${price}  

    ${float_leng}=    Set Variable If 
    ...    "${currency1}" == "BTC"    0.00000000
    ...    "${currency1}" == "ETH"    0.000000

    Page Should Contain Element    xpath=//*[@class='android.view.ViewGroup']/*[@text='${type}']/following-sibling::*[@text='${currency1}']/following-sibling::*[@text='/${currency2}']/following-sibling::*[@text='${float_leng}/${amount}']/following-sibling::*[@text='${price}']    loglevel=WARN
    Log    發現 該訂單：${type} ${currency1}/${currency2} 數量:${amount} 價格:${price}    WARN

Swipe middle To Up On Home Page
    Sleep    1s
    Swipe By Percent    50    50    50    10    5000
    Sleep    1s
