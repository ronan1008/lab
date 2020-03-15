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
#    Click Price Tab On Home Page
#      Click Gainers Tab On Home Page

#      Click Event Button On Home Page
#      Click Back Button In Event On Home Page

#      Click Crypto Card On Home Page
#      Click Back Button In Crypto Card On Home Page


#      Click Eye On Home Page
Test Click Home Page
    [Documentation]    切換到 首面 點擊 各個頁面
    Goto Home Tab On Home Page
    Click First Exchange Banner On Home Page
    Click Back Button On Home Page
    Click Second Exchange Banner On Home Page
    Click Back Button On Home Page
    Click third Exchange Banner On Home Page
    Click Back Button On Home Page

    Sleep    2s
    Swipe Right To Left On Home Page
    Sleep    2s

    Click First Exchange Banner On Home Page
    Click Back Button On Home Page
    Click Second Exchange Banner On Home Page
    Click Back Button On Home Page
    Click third Exchange Banner On Home Page
    Click Back Button On Home Page

    Sleep    2s
    Swipe Left To Right On Home Page
    Sleep    2s

*** comment ***
      Click Back Button On Home Page
      Click Top Banner On Home Page
      Click Back Button On Home Page
      Click Ace Launcher On Home Page
      Click Back Button On Home Page

 
 #    [Teardown]     Close Application






