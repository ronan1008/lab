*** Settings ***
Documentation	分頁
#Metadata			Version 0.1

*** Keywords ***
Click Top Banner On Home Page
    [Documentation]    Home->Top Banner
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/bannerViewPager
    Click Element  id=com.asiainnovations.ace.taiwan:id/bannerViewPager

Click First Exchange Banner On Home Page
    [Documentation]    Home->上方匯率第一項
    Wait Until Element Is Visible   xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther
    Click Element  xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther

Click Second Exchange Banner On Home Page
    [Documentation]    Home->上方匯率第二項
    Wait Until Element Is Visible   xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell[2]/XCUIElementTypeOther
    Click Element  xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell[2]/XCUIElementTypeOther

Click Third Exchange Banner On Home Page
    [Documentation]    Home->上方匯率第三項
    Wait Until Element Is Visible   xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell[3]/XCUIElementTypeOther
    Click Element  xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell[3]/XCUIElementTypeOther


Click Price Tab On Home Page
    [Documentation]    Home->價格榜
    Wait Until Element Is Visible   xpath=(//XCUIElementTypeStaticText[@name="價格"])[1]
    Click Element  xpath=(//XCUIElementTypeStaticText[@name="價格"])[1]

Click Gainers Tab On Home Page
    [Documentation]    Home->漲跌榜
    Wait Until Element Is Visible   xpath=(//XCUIElementTypeStaticText[@name="漲跌"])[1]
    Click Element  xpath=(//XCUIElementTypeStaticText[@name="漲跌"])[1]

Click Event Button On Home Page
    [Documentation]    Home->活動專區
    Wait Until Element Is Visible   xpath=(//XCUIElementTypeButton[@name="static menu view event"])[1]
    Click Element  xpath=(//XCUIElementTypeButton[@name="static menu view event"])[1]

Click Crypto Card On Home Page
    [Documentation]    Home->加密卡
    Wait Until Element Is Visible   xpath=(//XCUIElementTypeButton[@name="static menu view card"])[1]
    Click Element  xpath=(//XCUIElementTypeButton[@name="static menu view card"])[1]

Click Ace Launcher On Home Page
    [Documentation]    Home->代幣認購
    Wait Until Element Is Visible   xpath=(//XCUIElementTypeButton[@name="static menu view IEO"])[1]
    Click Element  xpath=(//XCUIElementTypeButton[@name="static menu view IEO"])[1]

Click Eye On Home Page
    [Documentation]    Home->Eye
    Wait Until Element Is Visible   xpath=(//XCUIElementTypeButton[@name="home btn reveal"])[1]
    Click Element  xpath=(//XCUIElementTypeButton[@name="home btn reveal"])[1]

Swipe Right To Left On Home Page
    [Documentation]    Home->上方匯率的向右滑轉
    Sleep    1s
    Swipe By Percent    90    25    10    25
    Sleep    1s

Swipe Left To Right On Home Page
    [Documentation]    Home->上方匯率的向左滑轉
    Sleep    1s
    Swipe By Percent    10    25    90    25
    Sleep    1s


Click All Exchange In Price And Gainers Tab On Home Page
    [Documentation]    Home->價格榜(漲跌榜)->欄位
    Swipe By Percent    50    50    50    20
    ${count} =    Get Matching Xpath Count    //XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell
    FOR    ${index}    IN RANGE    ${count}
        ${index}=   Evaluate    ${index} + 1
        Wait Until Element Is Visible   xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[${index}]
        Click Element  xpath=//XCUIElementTypeApplication[@name="ACE-dev"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[${index}]
        Click Back Button On All Page
    END
    Swipe By Percent    50    50    50    80

Click Back Button On All Page
    [Documentation]    Home->其他返回
    Sleep    1s
    Wait Until Element Is Visible   xpath=//XCUIElementTypeButton[@name="返回"]
    Click Element  xpath=//XCUIElementTypeButton[@name="返回"]

