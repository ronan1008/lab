*** Settings ***
Documentation	front end page function control
...						include [TOMODIFY]
#Metadata			Version 0.1

*** Keywords ***
Goto Home Page
	[Documentation]	 點擊 首頁
    Wait Until Element Is Visible   //a[@href='/']    timeout=10
    Click Element  //a[@href='/']
Goto Exchange Page
    [Documentation]  點擊 幣幣交易
    Wait Until Element Is Visible   //a[@href="/exchange/btcpusdt"]    timeout=10
    Click Element  //a[@href="/exchange/btcpusdt"]

Goto Flat Page
    [Documentation]  點擊 場外交易
    Wait Until Element Is Visible   //a[@href="/index.php?c=trans"]    timeout=10
    Click Element  //a[@href="/index.php?c=trans"]

Goto IEO Page
    [Documentation]  點擊 IEO
    Wait Until Element Is Visible   //a[@href="/index.php?s=ieo&c=ieo&m=plan2"]    timeout=10
    Click Element  //a[@href="/index.php?s=ieo&c=ieo&m=plan2"]

Goto invitation list Page
    [Documentation]  點擊 邀請榜
    Wait Until Element Is Visible   //a[@href="/index.php?s=ieo&c=ieo&m=inviteBulletin"]    timeout=10
    Click Element  //a[@href="/index.php?s=ieo&c=ieo&m=inviteBulletin"]

Goto App Download Page
    [Documentation]  點擊 App下載
    Wait Until Element Is Visible   //a[@href="/index.php?m=download"]    timeout=10
    Click Element  //a[@href="/index.php?m=download"]

Goto Recharge and Withdraw Page
    [Documentation]  點擊 資產->充幣 提幣
    Wait Until Element Is Visible   //span[@class="icon icon-creditcard"]    timeout=10
    Mouse Over  //span[@class="icon icon-creditcard"]
    Wait Until Element Is Visible   //a[@href="/index.php?m=currency"]    timeout=10
    Click Element  //a[@href="/index.php?m=currency"]

Goto C2C Account Page
    [Documentation]  點擊 資產->C2C 帳戶
    Wait Until Element Is Visible   //span[@class="icon icon-creditcard"]    timeout=10
    Mouse Over  //span[@class="icon icon-creditcard"]
    Wait Until Element Is Visible   //a[@href="/index.php?m=otc"]    timeout=10
    Click Element  //a[@href="/index.php?m=otc"]

Goto Open Orders Page
    [Documentation]  點擊 訂單->當前委託
    Wait Until Element Is Visible   //span[@class="icon icon-file-text-o"]    timeout=10
    Mouse Over  //span[@class="icon icon-file-text-o"]
    Sleep   1s
    Wait Until Element Is Visible   //a[contains(@href,'/record/current/')]    timeout=10
    Click Element  //a[contains(@href,'/record/current/')]

Goto Order History Page
    [Documentation]  點擊 訂單->歷史委託
    Wait Until Element Is Visible   //span[@class="icon icon-file-text-o"]    timeout=10
    Mouse Over  //span[@class="icon icon-file-text-o"]
    Sleep   1s
    Wait Until Element Is Visible   //a[contains(@href,'/record/hisitroy/')]    timeout=10
    Click Element  //a[contains(@href,'/record/hisitroy/')]

Move To Account Page
    [Documentation]  移動到 帳號
    Wait Until Element Is Visible   //li/div[@class='name']/u[contains(@style,'text-decoration: inherit')]    timeout=10
    Mouse Over  //li/div[@class='name']/u[contains(@style,'text-decoration: inherit')]

Goto My Invitation Code Page
    [Documentation]  點擊 帳號->我的邀請碼
    Move To Account Page
    Wait Until Element Is Visible   //a[@href="/index.php?m=invite"]    timeout=10
    Click Element  //a[@href="/index.php?m=invite"]

Goto Account Security Page
    [Documentation]  點擊 帳號->帳號安全
    Move To Account Page
    Wait Until Element Is Visible   //a[@href="/index.php?m=safety"]    timeout=10
    Click Element  //a[@href="/index.php?m=invite"]

Goto Personal settings Page
    [Documentation]  點擊 帳號->個人設置
    Move To Account Page
    Wait Until Element Is Visible   //a[@href="/index.php?c=trans&m=card"]    timeout=10
    Click Element  //a[@href="/index.php?c=trans&m=card"]

Goto Sign Out Page
    [Documentation]  點擊 帳號->退出
    Move To Account Page
    Wait Until Element Is Visible   //a[@onclick="loginout()"]    timeout=10
    Click Element  //a[@onclick="loginout()"]

Change Language To CN
    [Documentation]  點擊 切換語系->簡體中文
    Wait Until Element Is Visible   //a[@href="/index.php?s=ieo&c=ieo&m=plan2"]
    Click Element  //a[@href="/index.php?s=ieo&c=ieo&m=plan2"]
Change Language To EN
    [Documentation]  點擊 切換語系->英文
    Wait Until Element Is Visible   //a[@href="/index.php?s=ieo&c=ieo&m=plan2"]
    Click Element  //a[@href="/index.php?s=ieo&c=ieo&m=plan2"]

