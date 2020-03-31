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

Test Buy On Trade Page
    [tags]    stage    dev
    Goto Trading Tab On Home Page
    Choose Currency To Currency Exchange    TWD    ETH

    Click BuyIn On Trade Page
    Input Price On Trade Page    9999
    Click Up Button In Price On Trade Page    10
    Input Amount On Trade Page    3
    Click Up Button In Amount On Trade Page    10
    Click Buy Button On Trade Page

Test Sell On Trade Page
    [tags]    stage    dev
    Click SellOut On Trade Page
    Input Price On Trade Page    5000
    Click Down Button In Price On Trade Page    10
    Input Amount On Trade Page    1
    Click Down Button In Amount On Trade Page    10
    Click Sell Button On Trade Page







