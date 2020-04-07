*** Settings ***
Documentation	xxxx
#Metadata			Version 0.1
Resource    ../library/navigation.robot
Resource    ../library/me.robot
Library    ../tools/getTotp.py
*** Variables ***
${host}    http://localhost:4723/wd/hub

${platformName}		iOS
${deviceName}		ShockLee的iPhone11
${platformVersion}    13.3.1
${udid}    00008030-001825511404802E
${xcodeOrgId}    84B2274B58
#${bundleId}    com.asiainnovations.ace
${bundleId}    com.asiainnovations.ace-dev
${xcodeSigningId}    iPhone Developer
${automationName}    XCUITest

${googleAuth}   P4SIVMYMXBJ76PMV
*** Keywords ***
Open Ace On iOS
    Open Application    ${host}    platformName=${platformName}     deviceName=${deviceName}    udid=${udid}   xcodeOrgId=${xcodeOrgId}    bundleId=${bundleId}    xcodeSigningId=${xcodeSigningId}    automationName=${automationName}

Open Ace App And Login With Mobile
    Open Ace On iOS
    Goto Me Tab On Home Page
    Click Mobile Login On Me Page
    Input Tel Number In Mobile Login On Me Page    0936736561
    Input Password In Mobile Login On Me Page    Arborabc1234
    Click Login Button In Login On Me Page
    Input Google Auth In Login On Me Page    ${googleAuth}
    Click Login Button In Auth On Me Page    ${googleAuth}
