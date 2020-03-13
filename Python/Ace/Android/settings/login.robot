*** Settings ***
Documentation	xxxx
#Metadata			Version 0.1
Resource    ../library/navigation.robot
Resource    ../library/me.robot
Library    ../tools/getTotp.py
Library    ../tools/getGmailCode.py

*** Variables ***
${host}    http://localhost:4723/wd/hub 
${platformName}		Android
${deviceName}		PNXGAM8932802833
${appPackage}	com.asiainnovations.ace.taiwan
${appActivity}	com.asiainnovations.ace.splash.SplashActivity
${googleAuth}   P4SIVMYMXBJ76PMV
*** Keywords ***
Open Ace App And Login
    Open Application    ${host}    platformName=${platformName}     deviceName=${deviceName}    appPackage=${appPackage}   appActivity=${appActivity}
    Goto Me Tab On Home Page
    Click Mobile Login On Me Page
    Input Tel Number In Mobile Login On Me Page    0936736561
    Input Password In Mobile Login On Me Page    Arborabc1234
    Click Login Button In Mobile Login On Me Page
    Input Google Auth In Login On Me Page   ${googleAuth}
    Click Login Button In Auth On Me Page




