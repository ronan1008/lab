*** Settings ***
Documentation	分頁
#Metadata			Version 0.1

*** Keywords ***
Click Top Banner On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/bannerViewPager
    Click Element  id=com.asiainnovations.ace.taiwan:id/bannerViewPager

Click Exchange Banner On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acb_login
    Click Element  id=com.asiainnovations.ace.taiwan:id/acb_login

Click Price Tab On Home Page
    Wait Until Element Is Visible   xpath=//*[@class='androidx.appcompat.app.ActionBar.Tab' and @index='0']
    Click Element  xpath=//*[@class='androidx.appcompat.app.ActionBar.Tab' and @index='0']

Click Gainers Tab On Home Page
    Wait Until Element Is Visible   xpath=//*[@class='androidx.appcompat.app.ActionBar.Tab' and @index='1']
    Click Element  xpath=//*[@class='androidx.appcompat.app.ActionBar.Tab' and @index='1']

Click Event Button On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/goEvent
    Click Element  id=com.asiainnovations.ace.taiwan:id/goEvent

Click Back Button In Event On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/iv_back
    Click Element  id=com.asiainnovations.ace.taiwan:id/iv_back

Click Crypto Card On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/goCard
    Click Element  id=com.asiainnovations.ace.taiwan:id/goCard

Click Back Button In Crypto Card On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/iv_back
    Click Element  id=com.asiainnovations.ace.taiwan:id/iv_back

Click Ace Launcher On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/goIeo
    Click Element  id=com.asiainnovations.ace.taiwan:id/goIeo

Click Eye On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acibChangeState
    Click Element  id=com.asiainnovations.ace.taiwan:id/acibChangeState

Click Back Button On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/tvBack
    Click Element  id=com.asiainnovations.ace.taiwan:id/tvBack




