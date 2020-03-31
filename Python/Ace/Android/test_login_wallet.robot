*** Settings ***
Library    AppiumLibrary
Resource    ./library/navigation.robot
Resource    ./library/me.robot
Resource    ./library/wallet.robot
Resource    ./settings/login.robot
Default Tags    prod
*** Variables ***

${googleAuth}   P4SIVMYMXBJ76PMV

*** Test Cases ***
Test Login Ace On Android
    [Documentation]    登入ACE 使用 手機 google 驗證
    Open Ace App And Login With Mobile

Test TWD Info On Wallet Page 
    Goto Wallet Tab On Home Page
    Click Eye Button On Wallet Page
    Check TWD Info On Wallet Page


Test Cash Withdraw On Wallet Page 
    [Documentation]    錢包->提領
    [tags]    stage    dev
    Goto Wallet Tab On Home Page
    Click Withdraw Cash On Wallet Page
    Choose Bank In Withdraw Cash On Wallet Page
    Input Cash Amount In Withdraw Cash On Wallet Page    100
    Click Next In Withdraw Cash On Wallet Page
    Input Cash Password In Withdraw Cash On Wallet Page    Arborabc5678
    Input Google Auth In Withdraw Cash On Wallet Page    ${googleAuth}
    Click Confirm Button In Withdraw Cash On Wallet Page
    Click Back Button On Wallet Page 

Test Check Info On Wallet Page  
    [Documentation]    錢包->入金
    Goto Wallet Tab On Home Page
    Click Charge Cash On Wallet Page
    Get Info In Charge Cash On Wallet Page    銀行資訊
    Get Info In Charge Cash On Wallet Page    匯款帳號
    Click Back Button On Wallet Page 

Test Show Charge Coin Info 
    [Documentation]    錢包->入幣
    Goto Wallet Tab On Home Page
    Click Charge Coin On Wallet Page
    Click Change Button In Charge Coin On Wallet Page
    Input Currency In Charge Coin Search Bar On Wallet Page    BTC
    Get Currency Address In Charge Coin On Wallet Page
    Click Change Button In Charge Coin On Wallet Page
    Input Currency In Charge Coin Search Bar On Wallet Page    ETH
    Get Currency Address In Charge Coin On Wallet Page
    Click Change Button In Charge Coin On Wallet Page
    Input Currency In Charge Coin Search Bar On Wallet Page    BCH
    Get Currency Address In Charge Coin On Wallet Page
    Click Back Button On Wallet Page 



Double Check TWD Info On Wallet Page 
    Goto Wallet Tab On Home Page
    Check TWD Info On Wallet Page


Test Show Coin Withdraw On Wallet Page
    [Documentation]    錢包->提幣
    [tags]    stage    dev
    Click Withdraw Coin On Wallet Page
    Choose Currency In Withdraw Coin On Wallet Page    BTC
    Input Coin Amount In Withdraw Coin On Wallet Page    0.0001
    Input Coin Address In Withdraw Coin On Wallet Page    sfsdfsdfsdfsdfsdfsdf
    Click Next In Withdraw Coin On Wallet Page
    Input Cash Password In Withdraw Coin On Wallet Page    Arborabc5678
    Input Google Auth In Withdraw Coin On Wallet Page    ${googleAuth}
    Click Confirm In Withdraw Coin On Wallet Page


*** comment ***

*** comment ***
robot -e stage -e dev test_login_wallet.robot 
robot -i prod test_login_wallet.robot