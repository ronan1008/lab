*** Settings ***
Library    AppiumLibrary
Resource    ../settings/settings.robot
Resource    ../Library/Android/index.robot
Resource    ../Library/Android/My/my.robot

*** Test Cases ***

Test Case: tl-30 : 註冊時，輸入電子信箱與密碼
    在 Android 打開 TrueLove App 並 使用 Email 登入     broadcaster009      123456

Test Case tl-xx : 暫時
    在 index 按下 我的
    在 My 按下 編輯
    在 My 按下 回前一頁
    在 My 按下 名片管理
    在 My 按下 回前一頁
    在 My 按下 我的點數
    在 My 按下 回前一頁
    在 My 按下 收益報表
    在 My 按下 回前一頁