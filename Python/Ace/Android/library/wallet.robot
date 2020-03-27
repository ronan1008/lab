*** Settings ***
Documentation	行情
#Metadata			Version 0.1
Library    ../tools/getTotp.py
*** Keywords ***

Click Charge Cash On Wallet Page
    [Documentation]    錢包->入金
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_recharge
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_recharge

Click Withdraw Cash On Wallet Page
    [Documentation]    錢包->提領
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_withdraw
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_withdraw

Click Charge Coin On Wallet Page
    [Documentation]    錢包->入幣
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_charging
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_charging

Click Withdraw Coin On Wallet Page
    [Documentation]    錢包->提幣
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/atv_coin
    Click Element  id=com.asiainnovations.ace.taiwan:id/atv_coin

Get Info In Charge Cash On Wallet Page
    [Documentation]    錢包->入金->入金資訊
    [Arguments]	${info}
    Wait Until Element Is Visible    xpath=//*[@text='${info}']/following-sibling::*[1]    timeout=10
    ${text} =    Get Element Attribute    xpath=//*[@text='${info}']/following-sibling::*[1]    text
    Log    ${info}: ${text}   WARN
    
Choose Bank In Withdraw Cash On Wallet Page
    [Documentation]    錢包->提領->選擇銀行帳戶
    Wait Until Element Is Visible   xpath=//*[@class='android.view.View' and @text='選擇銀行帳戶']
    Click Element  xpath=//*[@class='android.view.View' and @text='選擇銀行帳戶']
    Sleep    3s
    Click Element At Coordinates    980    1240

Input Cash Amount In Withdraw Cash On Wallet Page
    [Documentation]    錢包->提領->提領金額
    [Arguments]	${cash_amount}
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.EditText' and @index='0']
    Input Text    xpath=//*[@class='android.widget.EditText' and @index='0']    ${cash_amount}

Click Next In Withdraw Cash On Wallet Page
    [Documentation]    錢包->提領->下一步
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.Button' and @text='下一步']
    Click Element    xpath=//*[@class='android.widget.Button' and @text='下一步']    

Input Cash Password In Withdraw Cash On Wallet Page
    [Documentation]    錢包->提領->現金密碼
    [Arguments]	${pass}
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.EditText' and @password='true']
    Input Text    xpath=//*[@class='android.widget.EditText' and @password='true']    ${pass}

Input Google Auth In Withdraw Cash On Wallet Page
    [Arguments]	${key}
    [Documentation]    錢包->提領->google auth
    ${token}=  Run Keyword	get_totp_token	${key}
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.EditText' and @password='false']
    Input Text    xpath=//*[@class='android.widget.EditText' and @password='false']    ${token}

Click Confirm Button In Withdraw Cash On Wallet Page
    [Documentation]    錢包->提領->確認
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.Button' and @text='提領確認']
    Click Element    xpath=//*[@class='android.widget.Button' and @text='提領確認']    



Click Change Button In Charge Coin On Wallet Page
    [Documentation]    錢包->入幣->更改
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/tv_change
    Click Element    id=com.asiainnovations.ace.taiwan:id/tv_change

Input Currency In Charge Coin Search Bar On Wallet Page
    [Documentation]    錢包->入幣->輸入幣種
    [Arguments]	${currency}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acet_coin
    Input Text    id=com.asiainnovations.ace.taiwan:id/acet_coin    ${currency} 
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/sectionBodyRL
    Click Element    id=com.asiainnovations.ace.taiwan:id/sectionBodyRL

Get Currency Address In Charge Coin On Wallet Page
   [Documentation]    錢包->入幣->輸入幣種->入幣地址
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/tvAddress
    ${currency} =    Get Element Attribute    id=com.asiainnovations.ace.taiwan:id/tvCoinName    text
    ${address} =    Get Element Attribute    id=com.asiainnovations.ace.taiwan:id/tvAddress    text
    Log    ${currency}: ${address}   WARN

Choose Currency In Withdraw Coin On Wallet Page
    [Documentation]    錢包->提幣->選擇幣種
    [Arguments]	${currency}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/tvSelectCoin
    Click Element    id=com.asiainnovations.ace.taiwan:id/tvSelectCoin
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acet_coin
    Input Text       id=com.asiainnovations.ace.taiwan:id/acet_coin    ${currency}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/sectionBodyRL
    Click Element    id=com.asiainnovations.ace.taiwan:id/sectionBodyRL
    

Input Coin Amount In Withdraw Coin On Wallet Page
    [Documentation]    錢包->提幣->提幣數量
    [Arguments]	${amount}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/et_money_num
    Input Text    id=com.asiainnovations.ace.taiwan:id/et_money_num    ${amount}

Input Coin Address In Withdraw Coin On Wallet Page
    [Documentation]    錢包->提幣->提幣地址
    [Arguments]	${address}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/et_withdraw
    Input Text    id=com.asiainnovations.ace.taiwan:id/et_withdraw    ${address}

Click Next In Withdraw Coin On Wallet Page
    [Documentation]    錢包->提幣->下一步
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acb_next
    Click Element    id=com.asiainnovations.ace.taiwan:id/acb_next   

Input Cash Password In Withdraw Coin On Wallet Page
    [Documentation]    錢包->提幣->資金密碼
    [Arguments]	${pass}
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/et_trade_pass
    Input Text    id=com.asiainnovations.ace.taiwan:id/et_trade_pass   ${pass}

Input Google Auth In Withdraw Coin On Wallet Page
    [Arguments]	${key}
    [Documentation]    錢包->提幣->Google Auth
    ${token}=    Run Keyword    get_totp_token    ${key}
    Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/et_phone_verify_code
    Input Text  id=com.asiainnovations.ace.taiwan:id/et_phone_verify_code    ${token}

Click Confirm In Withdraw Coin On Wallet Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acb_next
    Click Element    id=com.asiainnovations.ace.taiwan:id/acb_next   

Click Back Button On Wallet Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/iv_back
    Click Element  id=com.asiainnovations.ace.taiwan:id/iv_back

Click Eye Button On Wallet Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acib_visiable
    Click Element  id=com.asiainnovations.ace.taiwan:id/acib_visiable

Check TWD Info On Wallet Page
    [Documentation]    TWD可用餘額    TWD處理中    TWD總資產
    ${TWD_avail} =    Get Element Attribute    id=com.asiainnovations.ace.taiwan:id/tv_capital_balance    text
    ${TWD_proce} =    Get Element Attribute    id=com.asiainnovations.ace.taiwan:id/tv_total    text
    ${TWD_total} =    Get Element Attribute    id=com.asiainnovations.ace.taiwan:id/tv_total_assets    text
    ${TWD_digit_total} =    Get Element Attribute    id=com.asiainnovations.ace.taiwan:id/atv_my_captial    text
    Log    TWD可用餘額 ${TWD_avail}    WARN
    Log    TWD處理中 ${TWD_proce}    WARN
    Log    TWD可用餘額 ${TWD_total}    WARN
    Log    ${TWD_digit_total}    WARN





























