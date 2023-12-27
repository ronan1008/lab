*** Settings ***
Library     AppiumLibrary
Resource    ../../Resource/iOS/Common/App.robot
Resource    ../../Resource/iOS/Pages/Index/Index.robot
Resource    ../../Resource/iOS/Common/manipulate.robot
Test Setup       App.Login With Email   broadcaster005  12345
Test Teardown    App.Logout
*** Variables ***

*** Test Cases ***

首頁->熱門動態區->看更多
    [Documentation]    首頁熱門應顯示熱門動態區，點擊單張動態或「看更多」後可進到動態頁
    [Tags]  RAT
    Capture Page Screenshot    Index_002.png
    Index.Click Popular Activity Look More
    Capture Page Screenshot    PopularActivityLookmore_002.png
    manipulate.Return To Previous Page





