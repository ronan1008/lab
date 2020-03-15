*** Settings ***
Documentation	分頁
#Metadata			Version 0.1

*** Keywords ***
Click Top Banner On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/bannerViewPager
    Click Element  id=com.asiainnovations.ace.taiwan:id/bannerViewPager

Click First Exchange Banner On Home Page
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/first']/*[@index='2']
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/first']/*[@index='2']

Click Second Exchange Banner On Home Page
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/second']/*[@index='2']
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/second']/*[@index='2']

Click Third Exchange Banner On Home Page
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/third']/*[@index='2']
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/third']/*[@index='2']


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
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/iv_back    timeout=10
    Click Element  id=com.asiainnovations.ace.taiwan:id/iv_back

Click Crypto Card On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/goCard    
    Click Element  id=com.asiainnovations.ace.taiwan:id/goCard

Click Back Button In Crypto Card On Home Page
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/iv_back    timeout=10
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

Swipe Right To Left On Home Page
    Swipe    1000    560    0    560    5000

Swipe Left To Right On Home Page
    Swipe    0    560    1000    560    5000



