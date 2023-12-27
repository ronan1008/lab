*** Settings ***
Documentation	首頁->直播->Live->Liveroom 設定頁面

#Metadata			Version 0.1

*** Keywords ***
Input Subject
    [Documentation]    Liveroom 設定頁面->主題
    [Arguments]	${text}
    ${path} =   Set Variable  //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeTextField
    Wait Until Element Is Visible   ${path}
    Input Text  ${path}  ${text}

Input Bulletin Board
    [Documentation]    Liveroom 設定頁面->佈告欄
    [Arguments]	${text}
    ${path} =   Set Variable  //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeTextView
    Wait Until Element Is Visible   ${path}
    Click Element  ${path}
    Click Element  	//XCUIElementTypeButton[@name="iconCloseSGrey2"]
    Input Text  ${path}  ${text}

Select From Main Sprint Activity
    [Documentation]    Liveroom 設定頁面->主衝刺活動
    [Arguments]	${activity}
    Wait Until Element Is Visible   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeOther
    Click Element   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeOther
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="${activity}"]
    Click Element   //XCUIElementTypeButton[@name="${activity}"]

Select From Sub Sprint Activity
    [Documentation]    Liveroom 設定頁面->副衝刺活動
    [Arguments]	${activity}
    Wait Until Element Is Visible   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeOther
    Click Element   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeOther
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="${activity}"]
    Click Element   //XCUIElementTypeButton[@name="${activity}"]

Click Start Broadcast
    [Documentation]    Liveroom 設定頁面->開始直播
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name=" 開始直播"]
    Click Element   //XCUIElementTypeButton[@name=" 開始直播"]


Switch Room To Private And Set Pass
    [Documentation]    Liveroom 設定頁面->公開房 開關
    [Arguments]	${pass}
    Wait Until Element Is Visible   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeSwitch
    Click Element   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeSwitch
    ${passPath} =   Set Variable  //XCUIElementTypeAlert[@name=" 設定房間密碼"]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeScrollView[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeSecureTextField
    Wait Until Element Is Visible   ${passPath}
    Input Text  ${passPath}  ${pass}
    Click Element   //XCUIElementTypeButton[@name="設定"]

