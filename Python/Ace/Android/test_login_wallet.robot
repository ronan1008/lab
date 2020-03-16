*** Settings ***
Library    AppiumLibrary
Resource    ./library/navigation.robot
Resource    ./library/me.robot
Resource    ./library/wallet.robot
Resource    ./settings/login.robot

*** Variables ***

*** Test Cases ***
Test Login Ace On Android
    [Documentation]    登入ACE 使用 google 驗證
    Open Ace App And Login

Test Check Info On Wallet Page  
    Goto Wallet Tab On Home Page
    Click Charge Cash On Trade Page
    Get Info In Charge Cash On Trade Page    銀行資訊
    Get Info In Charge Cash On Trade Page    匯款帳號