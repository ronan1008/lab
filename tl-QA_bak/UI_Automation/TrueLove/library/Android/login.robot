*** Settings ***
Documentation	登入頁面
#Metadata			Version 0.1

*** Keywords ***
在登入註冊頁面按下登入
    Wait Until Element Is Visible    id=com.extreamax.truelovelive:id/loginButton
    Click Element   id=com.extreamax.truelovelive:id/loginButton

在登入頁面按下FB
    Wait Until Element Is Visible    id=com.extreamax.truelovelive:id/facebookLoginButton
    Click Element   id=com.extreamax.truelovelive:id/facebookLoginButton

在登入頁面按下LINE
    Wait Until Element Is Visible    id=com.extreamax.truelovelive:id/line_login_btn
    Click Element   id=com.extreamax.truelovelive:id/line_login_btn

在歡迎頁面按下取消
    Wait Until Element Is Visible    id=com.extreamax.truelovelive:id/btn_skip
    Click Element   id=com.extreamax.truelovelive:id/btn_skip

在LINE登入頁面按下許可
    Wait Until Element Is Visible    //*[@class='android.widget.Button' and @text='許可']
    Click Element   //*[@class='android.widget.Button' and @text='許可' ]

在登入頁面輸入帳號
    [Documentation]    登入頁面->帳號欄位
    [Arguments]	${account}
    Wait Until Element Is Visible   //*[@resource-id='com.extreamax.truelovelive:id/editText' and @password='false']
    Input Text   //*[@resource-id='com.extreamax.truelovelive:id/editText' and @password='false']   ${account}

在登入頁面輸入密碼
    [Documentation]    登入頁面->密碼欄位
    [Arguments]	${password}
    Wait Until Element Is Visible   //*[@resource-id='com.extreamax.truelovelive:id/editText' and @password='true']
    Input Text   //*[@resource-id='com.extreamax.truelovelive:id/editText' and @password='true']    ${password}

在登入頁面按下登入
    [Documentation]    登入頁面->登入按鈕
    Wait Until Element Is Visible    id=com.extreamax.truelovelive:id/loginButton
    Click Element   id=com.extreamax.truelovelive:id/loginButton


