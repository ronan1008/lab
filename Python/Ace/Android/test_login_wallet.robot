*** Settings ***
Library    AppiumLibrary
Resource    ./library/navigation.robot
Resource    ./library/me.robot
Resource    ./library/wallet.robot
Resource    ./settings/login.robot

*** Variables ***

${googleAuth}   P4SIVMYMXBJ76PMV

*** Test Cases ***
Test Login Ace On Android
    [Documentation]    登入ACE 使用 google 驗證
    Open Ace App And Login


Test Cash Withdraw On Wallet Page 
    [Documentation]    錢包->提領 
    Goto Wallet Tab On Home Page
    Click Withdraw Cash On Trade Page
    Choose Bank In Withdraw Cash On Trade Page
    Input Cash Amount In Withdraw Cash On Trade Page    100
    Click Next In Withdraw Cash On Trade Page
    Input Cash Password In Withdraw Cash On Trade Page    Arborabc5678
    Input Google Auth In Withdraw Cash On Trade Page    ${googleAuth}
    Click Confirm Button In Withdraw Cash On Trade Page
    Click Back Button On Trade page 

Test Check Info On Wallet Page  
    [Documentation]    錢包->入金
    Goto Wallet Tab On Home Page
    Click Charge Cash On Trade Page
    Get Info In Charge Cash On Trade Page    銀行資訊
    Get Info In Charge Cash On Trade Page    匯款帳號
    Click Back Button On Trade page 

Test Show Charge Coin Info 
    [Documentation]    錢包->入幣
    Goto Wallet Tab On Home Page
    Click Charge Coin On Trade Page
    Click Change Button In Charge Coin On Trade Page
    Input Currency In Charge Coin Search Bar On Trade Page    BTC
    Get Currency Address In Charge Coin On Trade Page
    Click Change Button In Charge Coin On Trade Page
    Input Currency In Charge Coin Search Bar On Trade Page    ETH
    Get Currency Address In Charge Coin On Trade Page
    Click Change Button In Charge Coin On Trade Page
    Input Currency In Charge Coin Search Bar On Trade Page    BCH
    Get Currency Address In Charge Coin On Trade Page
    Click Back Button On Trade page 

Test Show Coin Withdraw On Wallet Page
    [Documentation]    錢包->提幣
    Click Withdraw Coin On Trade Page
    Choose Currency In Withdraw Coin On Trade Page    BTC
    Input Coin Amount In Withdraw Coin On Trade Page    0.0001
    Input Coin Address In Withdraw Coin On Trade Page    sfsdfsdfsdfsdfsdfsdf
    Click Next In Withdraw Coin On Trade Page
    Input Cash Password In Withdraw Coin On Trade Page    Arborabc5678
    Input Google Auth In Withdraw Coin On Trade Page    ${googleAuth}
    Click Confirm In Withdraw Coin On Trade Page



*** comment ***
