
*** Settings ***
Documentation	xxxx
#Metadata			Version 0.1

*** Variables ***
${host}    http://localhost:4723/wd/hub

${platformName}		iOS
${deviceName}		ShockLee的iPhone11
${platformVersion}    13.3.1
${udid}    00008030-001825511404802E
${xcodeOrgId}    84B2274B58
${bundleId}    com.asiainnovations.ace
${xcodeSigningId}    iPhone Developer
${automationName}    XCUITest

${googleAuth}   P4SIVMYMXBJ76PMV
*** Keywords ***
Open Ace App And Login
    Open Application    ${host}    platformName=${platformName}     deviceName=${deviceName}    udid=${udid}   xcodeOrgId=${xcodeOrgId}    bundleId=${bundleId}    xcodeSigningId=${xcodeSigningId}    automationName=${automationName}




