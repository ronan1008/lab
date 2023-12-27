*** Settings ***
Library    AppiumLibrary
Resource   ../../Resource/iOS/Xtars.robot
Test Setup       Xtars.Login With Email  softnextqcshock@gmail.com  12345
Test Teardown    Xtars.Logout
*** Variables ***

*** Test Cases ***

Test Case Normal
    [Tags]  TEST
    [Documentation]    描述
    Do Something
    Log     WARN     HAPPYEND

Test Case Travel To USA With Setup And Teardown
    [Tags]  TEST
    [Documentation]    描述
    [Setup]    Take An Airplane To USA
    Go To NewYork
    Start Shopping
    Log     WARN     HAPPYEND
    [Teardown]    Take An Airplane To TAIWAN

*** comment ***
Test No Need
    [Documentation]    暫時不需要測試
    Do Something
