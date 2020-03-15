*** Settings ***
Documentation	行情
#Metadata			Version 0.1

*** Keywords ***
Click Banner On Quote Page
    [Arguments]	${Cryptocurrency}
    Wait Until Element Is Visible    xpath=//*[@resource-id='android:id/text1' and @text='${Cryptocurrency}']
    Click Element     xpath=//*[@resource-id='android:id/text1' and @text='${Cryptocurrency}']

