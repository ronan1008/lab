*** Settings ***
Library    AppiumLibrary
Library    ./tools/smsParser.py
Resource    ./library/navigation.robot
Resource    ./library/me.robot
Resource    ./settings/login.robot
Default Tags    prod
*** Variables ***


*** Test Cases ***
Test Register Ace On Android
    [Documentation]    註冊ACE，確認發送手機驗證碼
    Open Ace On Android
    Click Mobile Login On Me Page
    Click Register On Me Page
    Sleep    1s
    Choose Country On Me Page    Canada
    Input Tel Number In Register On Me Page    8192724632
    Click Get_verify_code On Me Page
    Input Tel Auth In Register On Me Page
    Click Cancel On Me Page






