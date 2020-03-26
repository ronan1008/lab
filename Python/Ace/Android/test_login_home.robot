*** Settings ***
Library    AppiumLibrary
Resource    ./library/navigation.robot
Resource    ./library/me.robot
Resource    ./library/home.robot
Resource    ./settings/login.robot
Default Tags    prod
*** Variables ***

*** Test Cases ***
Test Login Ace On Android
    [Documentation]    登入ACE 使用 google 驗證
    Open Ace App And Login

Test Click Home Page
    [Documentation]    切換到 首面 點擊 各個頁面
    Goto Home Tab On Home Page
    


Test Price And Gainers Tab On Home Page 
    [Documentation]    切換 價格榜 點擊匯率 在切換到 漲跌榜 點擊匯率
    Click Price Tab On Home Page
    Click All Exchange In Price And Gainers Tab On Home Page
    Click Gainers Tab On Home Page
    Click All Exchange In Price And Gainers Tab On Home Page

Test Top Exchange Banner On Home Page
    [Documentation]    點擊上面Bar 的三種匯率，向右滑動 在點擊三種匯率，再向左滑動
    Click First Exchange Banner On Home Page
    Click Back Button On All Page
    Click Second Exchange Banner On Home Page
    Click Back Button On All Page
    Click third Exchange Banner On Home Page
    Click Back Button On All Page

    Swipe Right To Left On Home Page

    Click First Exchange Banner On Home Page
    Click Back Button On All Page
    Click Second Exchange Banner On Home Page
    Click Back Button On All Page
    Click third Exchange Banner On Home Page
    Click Back Button On All Page

    Swipe Left To Right On Home Page

    Click Eye On Home Page

*** comment ***
Test Event Crypto Card Ace Launcher On Home Page
    [Documentation]    點擊  Ace代幣認購  加密卡兌換  活動專區
#    Click Ace Launcher On Home Page
#    Click Back Button On All Page
    Click Crypto Card On Home Page
    Click Back Button On All Page
    Click Event Button On Home Page
    Click Back Button On All Page




 
 #    [Teardown]     Close Application






