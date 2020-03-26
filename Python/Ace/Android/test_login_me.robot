*** Settings ***
Library    AppiumLibrary
Resource    ./library/navigation.robot
Resource    ./library/me.robot
Resource    ./library/wallet.robot
Resource    ./settings/login.robot
Default Tags    prod

*** Variables ***

*** Test Cases ***
Test Login Ace On Android
    [Documentation]    登入ACE 使用 google 驗證
    Open Ace App And Login

Test Click Me Page
    [Documentation]    切換到 我 點擊 各個頁面
    Goto Me Tab On Home Page
    Click Bank Account On Me Page
    Click Back Button On Me Page
    Click Coin Withdraw Address On Me Page
    Click Back Button On Me Page
    Click Invite Back On Me Page
    Click Back Button On Me Page
    Click Announcement On Me Page
    Click Back Button On Me Page
    Click System Settings On Me Page
    Click Back Button On Me Page
    Click Question Reply On Me Page
    Click Back Button On Me Page
