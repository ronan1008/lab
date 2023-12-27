*** Settings ***
Documentation	My->編輯個人檔案
#Metadata			Version 0.1

*** Keywords ***
在 My->編輯個人檔案 輸入 暱稱
    [Arguments]	${nickname}
    Wait Until Element Is Visible    //*[@text='暱稱']/following-sibling::*[@resource-id='com.extreamax.truelovelive:id/editText']
    Input Text   //*[@text='暱稱']/following-sibling::*[@resource-id='com.extreamax.truelovelive:id/editText']    ${nickname}
在 My->編輯個人檔案 輸入 簡介
    [Arguments]	${intro}
    Wait Until Element Is Visible    //*[@text='簡介']/following-sibling::*[@resource-id='com.extreamax.truelovelive:id/editText']
    Input Text   //*[@text='簡介']/following-sibling::*[@resource-id='com.extreamax.truelovelive:id/editText']    ${intro}

在 My->編輯個人檔案 選擇 生日
    [Arguments]	${birth}
    Wait Until Element Is Visible    //*[@text='生日']/following-sibling::*[@resource-id='com.extreamax.truelovelive:id/editText']
    Click Element   //*[@resource-id='com.extreamax.truelovelive:id/editText' and @text='請選擇生日']
    #手動更改
    Wait Until Element Is Visible    //*[@resource-id='com.extreamax.truelovelive:id/mtrl_picker_header_toggle']
    Click Element    //*[@resource-id='com.extreamax.truelovelive:id/mtrl_picker_header_toggle']
#TODO:
    Wait Until Element Is Visible     //*[@resource-id='com.extreamax.truelovelive:id/mtrl_picker_text_input_date']/*/*[@class='android.widget.EditText']
    Input Text     //*[@resource-id='com.extreamax.truelovelive:id/mtrl_picker_text_input_date']/*/*[@class='android.widget.EditText']     ${birth}

在 My->編輯個人檔案 選擇 性別

在 My->編輯個人檔案 按下 完成

在 My->編輯個人檔案 取消 暱稱


