*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1
Library		SeleniumLibrary

*** Variables ***


*** Test Cases ***
Login Minutemail And Return Email
    Sleep   5s
    Wait Until Element Is Visible  //input[@id='fe_text']  timeout=10
    ${email_address} =    Get Value    //input[@id='fe_text']
    Set Global Variable    ${email_address}

Check Minutemail And Click Mail Then Return Verfication Code
    Wait Until Element Is Visible   //table[@id='maillist']/tbody/tr/td[contains(text(),'ronan1008')]
    Click Element   //table[@id='maillist']/tbody/tr/td[contains(text(),'ronan1008')]
    Wait Until Element Is Visible   //div[@id='tab1']
    ${mailContent} =    Get Text    //div[@id='tab1']/div/div[@dir='ltr']
    ${getVerificationCode} =  Get Regexp Matches  ${mailContent}	testcode(..)   1
    Set Global Variable    ${getVerificationCode}



