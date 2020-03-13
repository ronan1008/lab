*** Settings ***
Library    AppiumLibrary
Resource    ./library/navigation.robot
Resource    ./library/me.robot
Resource    ./library/home.robot
Resource    ./settings/login.robot

*** Variables ***
${host}    http://localhost:4723/wd/hub 
${platformName}		Android
${deviceName}		PNXGAM8932802833
${appPackage}	com.asiainnovations.ace.taiwan
${appActivity}	com.asiainnovations.ace.splash.SplashActivity

*** Test Cases ***
Login Ace On Android

      Open Ace App And Login
      Goto Home Tab On Home Page

#      Click Price Tab On Home Page
#      Click Gainers Tab On Home Page

#      Click Event Button On Home Page
#      Click Back Button In Event On Home Page

#      Click Crypto Card On Home Page
#      Click Back Button In Crypto Card On Home Page


#      Click Eye On Home Page
      Swipe Right To Left On Home Page
      Sleep    3s
      Swipe Left To Right On Home Page

*** comment ***
      Click Exchange Banner On Home Page
      Click Back Button On Home Page
      Click Top Banner On Home Page
      Click Back Button On Home Page
      Click Ace Launcher On Home Page
      Click Back Button On Home Page

 
 #    [Teardown]     Close Application






