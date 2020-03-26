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
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/first']/*[@index='2']
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/first']/*[@index='2']

Click Second Exchange Banner On Home Page
    [Documentation]    Home->上方匯率第二項
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/second']/*[@index='2']
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/second']/*[@index='2']

Click Third Exchange Banner On Home Page
    [Documentation]    Home->上方匯率第三項
    Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/third']/*[@index='2']
    Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/third']/*[@index='2']


Click Price Tab On Home Page
    [Documentation]    Home->價格榜
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.LinearLayout' and @index='0']
    Click Element  xpath=//*[@class='android.widget.LinearLayout' and @index='0']

Click Gainers Tab On Home Page
    [Documentation]    Home->漲跌榜
    Wait Until Element Is Visible   xpath=//*[@class='android.widget.LinearLayout' and @index='1']
    Click Element  xpath=//*[@class='android.widget.LinearLayout' and @index='1']

Click Event Button On Home Page
    [Documentation]    Home->活動專區
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/goEvent
    Click Element  id=com.asiainnovations.ace.taiwan:id/goEvent

Click Crypto Card On Home Page
    [Documentation]    Home->加密卡
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/goCard    
    Click Element  id=com.asiainnovations.ace.taiwan:id/goCard

Click Ace Launcher On Home Page
    [Documentation]    Home->代幣認購
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/goIeo
    Click Element  id=com.asiainnovations.ace.taiwan:id/goIeo

Click Eye On Home Page
    [Documentation]    Home->Eye
    Wait Until Element Is Visible   id=com.asiainnovations.ace.taiwan:id/acibChangeState
    Click Element  id=com.asiainnovations.ace.taiwan:id/acibChangeState

Swipe Right To Left On Home Page
    [Documentation]    Home->上方匯率的向右滑轉
    Sleep    1s
    Swipe    1000    560    0    560    5000
    Sleep    1s

Swipe Left To Right On Home Page
    [Documentation]    Home->上方匯率的向左滑轉
    Sleep    1s
    Swipe    0    560    1000    560    5000
    Sleep    1s


Click All Exchange In Price And Gainers Tab On Home Page
    [Documentation]    Home->價格榜(漲跌榜)->欄位
    Swipe By Percent    50    50    50    20
    ${count} =    Get Matching Xpath Count    //*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_container']
    FOR    ${index}    IN RANGE    ${count}
        Wait Until Element Is Visible   xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_container' and @index='${index}']
        Click Element  xpath=//*[@resource-id='com.asiainnovations.ace.taiwan:id/cl_container' and @index='${index}']
        Click Back Button On All Page
    END
    Swipe By Percent    50    50    50    80

Click Back Button On All Page
    [Documentation]    Home->其他返回
    Sleep    1s
    ${back_status1}=	Run Keyword And Return Status	Page Should Contain Element    //*[@resource-id='com.asiainnovations.ace.taiwan:id/ivBack']
    ${back_status2}=	Run Keyword And Return Status	Page Should Contain Element    //*[@resource-id='com.asiainnovations.ace.taiwan:id/tvBack']
    ${back_status3}=	Run Keyword And Return Status	Page Should Contain Element    //*[@resource-id='com.asiainnovations.ace.taiwan:id/back_btn']
	Run Keyword If	${back_status1} == True    Run Keywords
    ...    Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/iv_back
    ...    AND    Click Element    id=com.asiainnovations.ace.taiwan:id/iv_back
    ...    ELSE IF    ${back_status2} == True    Run Keywords
    ...    Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/tvBack
    ...    AND    Click Element    id=com.asiainnovations.ace.taiwan:id/tvBack
    ...    ELSE IF    ${back_status3} == True    Run Keywords
    ...    Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/back_btn
    ...    AND    Click Element    id=com.asiainnovations.ace.taiwan:id/back_btn
    ...    ELSE    Click Element At Coordinates    74    144
