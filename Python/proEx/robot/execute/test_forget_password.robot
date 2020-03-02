*** Settings ***

Documentation	xxxxx
Metadata			Version 0.1

Library		SeleniumLibrary
Library	    ../library/tools/getGmailCode.py
Resource	../settings/browser_setting.robot
Resource	../library/front_end/front_menu.robot
Resource	../library/front_end/forget_password.robot

*** Variables ***
${HOST}		www.proex.io
${URL}		http://${HOST}/
${SSLURL}	https://${HOST}/
${BW}	chrome
${NoGUI}	0
${IMAP_SERVER}    imap.gmail.com
${EMAIL}    softnextqcshock@gmail.com
${EMAIL_PASS}    Arborabc1234
*** Test Cases ***

Test Forget Password To Send Mail
    [Setup]	Login WebUI	${URL}	${BW}
    Change Language To  CHS
    Goto Forget Password Page
    Input Email On Forget Password Page    ${EMAIL}
    Click Get Verify Code On Forget Password Page
    Sleep   50s
    ${VERIFY_CODE} =    open_gmail_and_get_code    ${IMAP_SERVER}   ${EMAIL}     ${EMAIL_PASS}
    ${Email} =    open_gmail_and_get_content
    log    ${Email}    WARN
    Input Verification Code On Forget Password Page    ${VERIFY_CODE}
    Click Next On Forget Password Page