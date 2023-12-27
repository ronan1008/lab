*** Settings ***
Documentation	我的頁面
Resource    ./edit_personal_file.robot
#Metadata			Version 0.1

*** Keywords ***
在 My 按下 訊息通知
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/notifications
    Click Element   id=com.extreamax.truelovelive:id/notifications

在 My 按下 已追蹤
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/followingStatusText
    Click Element   id=com.extreamax.truelovelive:id/followingStatusText

在 My 按下 編輯
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/editProfile
    Click Element   id=com.extreamax.truelovelive:id/editProfile

在 My 按下 我的點數
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/points_menu_item
    Click Element   id=com.extreamax.truelovelive:id/points_menu_item

在 My 按下 我的等級
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/level_menu_item
    Click Element   id=com.extreamax.truelovelive:id/level_menu_item

在 My 按下 進階設定
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/settings_menu_item
    Click Element   id=com.extreamax.truelovelive:id/settings_menu_item

在 My 按下 問題協助
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/help_menu_item
    Click Element   id=com.extreamax.truelovelive:id/help_menu_item

在 My 按下 名片管理
    Wait Until Element Is Visible     //*[@text='名片管理']/parent::*/parent::*
    Click Element   //*[@text='名片管理']/parent::*/parent::*

在 My 按下 粉絲名單
    Wait Until Element Is Visible     //*[@text='粉絲名單']/parent::*/parent::*
    Click Element   //*[@text='名片管理']/parent::*/parent::*

在 My 按下 動態管理
    Wait Until Element Is Visible     //*[@text='動態管理']/parent::*/parent::*
    Click Element   //*[@text='名片管理']/parent::*/parent::*

在 My 按下 收益報表
    Wait Until Element Is Visible     //*[@text='收益報表']/parent::*/parent::*
    Click Element   //*[@text='名片管理']/parent::*/parent::*

在 My 按下 收禮紀錄
    Wait Until Element Is Visible     //*[@text='收禮紀錄']/parent::*/parent::*
    Click Element   //*[@text='名片管理']/parent::*/parent::*

在 My 按下 回前一頁
    ${back_status1}=	Run Keyword And Return Status	Page Should Contain Element    //*[@resource-id='com.extreamax.truelovelive:id/backPressButton']
    ${back_status2}=	Run Keyword And Return Status	Page Should Contain Element    //*[@resource-id='com.extreamax.truelovelive:id/btnBack']
	Run Keyword If	${back_status1} == True    Click Element    id=com.extreamax.truelovelive:id/backPressButton
    ...    ELSE IF    ${back_status2} == True  Click Element    id=com.extreamax.truelovelive:id/btnBack
    ...    ELSE    Log    '找不到前一頁按鈕'   WARN


得到版本號
    Wait Until Element Is Visible     id=com.extreamax.truelovelive:id/version
#TODO: