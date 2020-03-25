*** Settings ***
Library    AppiumLibrary
Resource    ./settings/login.robot
Default Tags    prod
*** Variables ***

*** Test Cases ***
Test Login Ace On Android
    [Documentation]    登入ACE 使用 google 驗證
    Open Ace App And Login
