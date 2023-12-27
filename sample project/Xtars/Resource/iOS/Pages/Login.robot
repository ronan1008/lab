*** Settings ***
Documentation	登入
#Metadata			Version 0.1

*** Keywords ***
Cancel Login Popup
    Sleep  3s  reason=None
    Tap    ${None}    118    167

# Click Login Button
#     Wait Until Element Is Visible    accessibility_id=login_btn
#     Click Element   accessibility_id=login_btn

Click FB Button
    Wait Until Element Is Visible    //XCUIElementTypeButton[@name="buttonFacebookLogin"]
    Click Element   //XCUIElementTypeButton[@name="buttonFacebookLogin"]

Click Line Button
    Wait Until Element Is Visible    //XCUIElementTypeButton[@name="buttonLineLogin"]
    Click Element   //XCUIElementTypeButton[@name="buttonLineLogin"]

Click Skip Button
    ${back_status}=	Run Keyword And Return Status	Wait Until Element Is Visible   Wait Until Element Is Visible   //XCUIElementTypeStaticText[contains(@name,"跳過")]
    Run Keyword If	${back_status} == True   Click Element    Wait Until Element Is Visible   //XCUIElementTypeStaticText[contains(@name,"跳過")]
    ...	ELSE    sleep   10s

Click Authorize Button On Line
    Wait Until Element Is Visible    //*[@class='android.widget.Button' and @text='許可']
    Click Element   //*[@class='android.widget.Button' and @text='許可' ]

Click Authorize Button On FB
    [Documentation]    點完FB->跳出「TL初樂」想要使用..->繼續->打開->繼續
    Wait Until Element Is Visible    //XCUIElementTypeButton[@name="繼續"]
    Click Element   //XCUIElementTypeButton[@name="繼續"]
    Sleep  0.5s
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="打開"]
    Click Element   //XCUIElementTypeButton[@name="打開"]
    Sleep  0.5s
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="繼續"]
    Click Element   //XCUIElementTypeButton[@name="繼續"]

Input Account
    [Documentation]    登入頁面-登入->帳號欄位
    [Arguments]	${account}
    Wait Until Element Is Visible   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeTextField
    Input Text   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeTextField   ${account}

Input Password
    [Documentation]    登入頁面-登入->密碼欄位
    [Arguments]	${password}
    Wait Until Element Is Visible   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeSecureTextField
    Input Text   //XCUIElementTypeApplication[@name="Xtars Live"]/XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeSecureTextField    ${password}

Click Login Button
    [Documentation]    登入頁面-登入->登入按鈕
    Wait Until Element Is Visible   //XCUIElementTypeButton[@name="登入"]
    Click Element   //XCUIElementTypeButton[@name="登入"]