*** Settings ***
Library    AppiumLibrary
Resource    ./library/navigation.robot
Resource    ./library/me.robot
Resource    ./library/home.robot
Resource    ./settings/login.robot

*** Variables ***

*** Test Cases ***
Test Login Ace On Android
    [Documentation]    登入ACE 使用 google 驗證
    Open Ace App And Login

Test Click Quote Page
    [Documentation]    切換到 行情 點擊 各個頁面
    Goto Quotes Tab On Home Page
    Click Banner On Quote Page    TWD






