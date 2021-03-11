*** Settings ***
Documentation	登入
#Metadata			Version 0.1

*** Keywords ***
Click Login Button On Login Welcome Page
    Wait Until Element Is Visible    accessibility_id=login_btn
    Click Element   accessibility_id=login_btn

Click FB Button On Login Welcome Page
    Wait Until Element Is Visible    //XCUIElementTypeButton[@name="buttonFacebookLogin"]
    Click Element   //XCUIElementTypeButton[@name="buttonFacebookLogin"]

Click Line Button On Login Welcome Page
    Wait Until Element Is Visible    //XCUIElementTypeButton[@name="buttonLineLogin"]
    Click Element   //XCUIElementTypeButton[@name="buttonLineLogin"]

Click Skip Button On Login Welcome Page
    ${back_status}=	Run Keyword And Return Status	Wait Until Element Is Visible   Wait Until Element Is Visible   //XCUIElementTypeStaticText[contains(@name,"跳過")]
    Run Keyword If	${back_status} == True   Click Element    Wait Until Element Is Visible   //XCUIElementTypeStaticText[contains(@name,"跳過")]
    ...	ELSE    sleep   10s

Click Authorize Button On Line Auth Page
    Wait Until Element Is Visible    //*[@class='android.widget.Button' and @text='許可']
    Click Element   //*[@class='android.widget.Button' and @text='許可' ]

Click Authorize Button On FB Auth Page
    [Documentation]    點完FB->跳出「TL初樂」想要使用..->繼續->打開->繼續
    Wait Until Element Is Visible    //XCUIElementTypeButton[@name="繼續"]
    Click Element   //XCUIElementTypeButton[@name="繼續"]
    Sleep  0.5s
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="打開"]
    Click Element   //XCUIElementTypeButton[@name="打開"]
    Sleep  0.5s
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="繼續"]
    Click Element   //XCUIElementTypeButton[@name="繼續"]



Input Account On Login Page
    [Documentation]    登入頁面-登入->帳號欄位
    [Arguments]	${account}
    Wait Until Element Is Visible   //XCUIElementTypeApplication[@name="TL初樂"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTextField
    Input Text   //XCUIElementTypeApplication[@name="TL初樂"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTextField   ${account}

Input Password On Login Page
    [Documentation]    登入頁面-登入->密碼欄位
    [Arguments]	${password}
    Wait Until Element Is Visible   //XCUIElementTypeApplication[@name="TL初樂"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeSecureTextField
    Input Text   //XCUIElementTypeApplication[@name="TL初樂"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeSecureTextField    ${password}

Click Login Button On Login Page
    [Documentation]    登入頁面-登入->登入按鈕
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="登入"]
    Click Element   //XCUIElementTypeButton[@name="登入"]

在登入頁面如果有取消按鈕就按下
    [Documentation]    登入頁面-登入->取消(取消使用記憶帳號)
    ${back_status}=	Run Keyword And Return Status	Wait Until Element Is Visible   //XCUIElementTypeButton[@name="取消"]
    Run Keyword If	${back_status} == True   Click Element    //XCUIElementTypeButton[@name="取消"]
