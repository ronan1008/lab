*** Settings ***
Documentation	分頁
#Metadata			Version 0.1

*** Keywords ***
Goto Home Tab On Home Page
      [Documentation]    Home 分頁
      Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/navigation_home
      Click Element    id=com.asiainnovations.ace.taiwan:id/navigation_home

Goto Quotes Tab On Home Page
      [Documentation]    行情 分頁
      Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/navigation_quotes
      Click Element    id=com.asiainnovations.ace.taiwan:id/navigation_quotes

Goto Trading Tab On Home Page
      [Documentation]    交易 分頁
      Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/navigation_trading
      Click Element    id=com.asiainnovations.ace.taiwan:id/navigation_trading

Goto Wallet Tab On Home Page
      [Documentation]    錢包 分頁
      Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/navigation_wallet
      Click Element    id=com.asiainnovations.ace.taiwan:id/navigation_wallet

Goto Me Tab On Home Page
      [Documentation]    我 分頁
      Wait Until Element Is Visible    id=com.asiainnovations.ace.taiwan:id/navigation_me
      Click Element    id=com.asiainnovations.ace.taiwan:id/navigation_me



