*** Settings ***
Library    AppiumLibrary
Resource    ./library/navigation.robot
Resource    ./library/me.robot
Resource    ./library/trade.robot
Resource    ./settings/login.robot
Default Tags    prod
*** Variables ***

*** Test Cases ***
Test Login Ace On Android
    [Documentation]    登入ACE 使用 手機 google 驗證
    Open Ace App And Login With Mobile


Test Sell On Trade Page
    [tags]    stage    dev
    Goto Trading Tab On Home Page
    Choose Currency To Currency Exchange    TWD    ETH

    Click SellOut On Trade Page
    Input Price On Trade Page    12000
    Click Down Button In Price On Trade Page    3
    Click Up Button In Price On Trade Page  3
    Input Amount On Trade Page    1
    Click Down Button In Amount On Trade Page    3
    Click Up Button In Amount On Trade Page  3
    Click Sell Button On Trade Page
    Swipe middle To Up On Home Page
    Check List In My Order On Trade Page    賣    ETH    TWD    1.000000    12,000.0
    Click Cancel Order Button On Trade Page    1



Test Buy On Trade Page
    [tags]    stage    dev
    Goto Trading Tab On Home Page
    Choose Currency To Currency Exchange    TWD    BTC

    Click BuyIn On Trade Page
    Input Price On Trade Page    66666
    Click Up Button In Price On Trade Page    2
    Click Down Button In Price On Trade Page  2
    Input Amount On Trade Page    1
    Click Up Button In Amount On Trade Page    2
    Click Down Button In Amount On Trade Page  2
    Click Buy Button On Trade Page
    Swipe middle To Up On Home Page
    Check List In My Order On Trade Page    買    BTC    TWD    1.00000000    66,666.0
    Click Cancel Order Button On Trade Page    1

