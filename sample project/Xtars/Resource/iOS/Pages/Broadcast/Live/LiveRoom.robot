*** Settings ***
Documentation	首頁->直播->Live->直播間
Library    String
#Metadata			Version 0.1

*** Keywords ***
Chat Text
    [Documentation]    直播間->聊聊天吧
    [Arguments]	${text}
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="聊聊天吧"]   timeout=10s
    Click Element   //XCUIElementTypeButton[@name="聊聊天吧"]
    ${path} =   Set Variable    //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[6]/XCUIElementTypeTextView
    Input Text    ${path}    ${text}
    Click Element   //XCUIElementTypeButton[@name="iconAirplaneMPrimary"]

Exit
    [Documentation]    直播間->離開直播間
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="buttonExit"]
    Click Element   //XCUIElementTypeButton[@name="buttonExit"]
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="確定"]
    Click Element  	//XCUIElementTypeButton[@name="確定"]

Click Audience
    [Documentation]    直播間->陪伴區
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="buttonAudience"]    timeout=10s
    Click Element   //XCUIElementTypeButton[@name="buttonAudience"]

Click Bulletin
    [Documentation]    直播間->布告欄
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="buttonBulletinExpanded"]    timeout=10s
    Click Element   //XCUIElementTypeButton[@name="buttonBulletinExpanded"]

Click ReceivedGift
    [Documentation]    直播間->收禮明細
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="buttonReceivedGift"]    timeout=10s
    Click Element   //XCUIElementTypeButton[@name="buttonReceivedGift"]

Click Filter
    [Documentation]    直播間->濾鏡
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="buttonFilterSticker"]    timeout=10s
    Click Element   //XCUIElementTypeButton[@name="buttonFilterSticker"]

Click Toolbox
    [Documentation]    直播間->工具
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="buttonToolbox"]    timeout=10s
    Click Element   //XCUIElementTypeButton[@name="buttonToolbox"]

Click Share
    [Documentation]    直播間->分享
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="buttonShare"]    timeout=10s
    Click Element   //XCUIElementTypeButton[@name="buttonShare"]

Get Live Time
    [Documentation]    直播間->Live時間
    ${path} =   Set Variable    //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText[1]
    Wait Until Element Is Visible   ${path}    timeout=10s
    ${LiveTime} =   Get Element Attribute   ${path}    name
    [return]    ${LiveTime}

Get Live Points
    [Documentation]    直播間->Diamond
    ${PointsPath} =   Set Variable    //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText[2]
    Wait Until Element Is Visible   ${PointsPath}    timeout=10s
    ${LivePoints} =   Get Element Attribute   ${PointsPath}    name
    [return]    ${LivePoints}

Get Live Title
    [Documentation]    直播間->標題
    ${path}} =   Set Variable    //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeStaticText
    Wait Until Element Is Visible   ${path}    timeout=10s
    ${LivePoints} =   Get Element Attribute   ${path}    name
    [return]    ${LiveTitle}

Get Live Bulletin
    [Documentation]    直播間->佈告欄
    ${path} =   Set Variable        //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeTextView
    Wait Until Element Is Visible   ${path}    timeout=10s
    ${LiveBulletin} =   Get Element Attribute   ${path}    value
    [return]    ${LiveBulletin}


Click Violation List Of Toolbox
    [Documentation]    直播間->工具->違規名單
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="違規名單"]/preceding-sibling::XCUIElementTypeButton
    Click Element   //XCUIElementTypeStaticText[@name="違規名單"]/preceding-sibling::XCUIElementTypeButton

Click Room Control Of Toolbox
    [Documentation]    直播間->工具->場控列表
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="場控列表"]/preceding-sibling::XCUIElementTypeButton
    Click Element   //XCUIElementTypeStaticText[@name="場控列表"]/preceding-sibling::XCUIElementTypeButton

Click Room Info Of Toolbox
    [Documentation]    直播間->工具->房間資訊
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="房間資訊"]/preceding-sibling::XCUIElementTypeButton
    Click Element   //XCUIElementTypeStaticText[@name="房間資訊"]/preceding-sibling::XCUIElementTypeButton

Click Game Of Toolbox
    [Documentation]    直播間->工具->小遊戲
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="小遊戲"]/preceding-sibling::XCUIElementTypeButton
    Click Element   //XCUIElementTypeStaticText[@name="小遊戲"]/preceding-sibling::XCUIElementTypeButton

Click Mute Of Toolbox
    [Documentation]    直播間->工具->靜音
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="靜音"]/preceding-sibling::XCUIElementTypeButton
    Click Element   //XCUIElementTypeStaticText[@name="靜音"]/preceding-sibling::XCUIElementTypeButton

Click Camera Of Toolbox
    [Documentation]    直播間->工具->翻轉相機
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="翻轉相機"]/preceding-sibling::XCUIElementTypeButton
    Click Element   //XCUIElementTypeStaticText[@name="翻轉相機"]/preceding-sibling::XCUIElementTypeButton

Click Switch Mirror Of Toolbox
    [Documentation]    直播間->工具->切換鏡像
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="切換鏡像"]/preceding-sibling::XCUIElementTypeButton
    Click Element   //XCUIElementTypeStaticText[@name="切換鏡像"]/preceding-sibling::XCUIElementTypeButton

Click Beauty Face Of Toolbox
    [Documentation]    直播間->工具->美顏
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="美顏"]/preceding-sibling::XCUIElementTypeButton
    Click Element   //XCUIElementTypeStaticText[@name="美顏"]/preceding-sibling::XCUIElementTypeButton

Get Title Of Room Info
    [Documentation]    直播間->工具->房間資訊->主題
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="房間資訊"]
    ${TitlePath} =   Set Variable   //XCUIElementTypeStaticText[@name="主題"]/following-sibling::XCUIElementTypeTextField
    ${Title} =   Get Element Attribute  ${TitlePath}  value
    [return]    ${Title}

Get Bulletin Of Room Info
    [Documentation]    直播間->工具->房間資訊->佈告欄
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="房間資訊"]
    ${BulletinPath} =   Set Variable   //XCUIElementTypeStaticText[@name="佈告欄"]/following-sibling::XCUIElementTypeTextView
    ${Bulletin} =   Get Element Attribute  ${BulletinPath}  value
    [return]    ${Bulletin}

Get Password Of Room Info
    [Documentation]    直播間->工具->房間資訊->密碼
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="房間資訊"]
    ${PassPath} =   Set Variable   //XCUIElementTypeStaticText[contains(@name,'密碼')]
    ${PassStatement} =   Get Element Attribute  ${PassPath}  value
    ${words} =   String.Split String    ${PassStatement}    ：
    [return]    ${words}[1]


Click Save Of Room Info
    Wait Until Element Is Visible   //XCUIElementTypeStaticText[@name="房間資訊"]
    Click Element  //XCUIElementTypeButton[@name="儲存"]

