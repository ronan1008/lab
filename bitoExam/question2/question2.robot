*** Settings ***
Library    Selenium2Library
Library    RequestsLibrary
Library    DateTime
Library    RPA.Notifier
Library    ../../.venv/lib/python3.9/site-packages/robot/libraries/Collections.py
Library    ../../.venv/lib/python3.9/site-packages/robot/libraries/String.py
Suite Setup    Open Browser  https://www.bitopro.com/ns/fees  chrome
Suite Teardown    Teardown Actions


*** Variables ***
${BASE_URL}    https://api.bitopro.com/v3
${apiPath}		/provisioning/limitations-and-fees
${CERTIFICATE}    /opt/homebrew/etc/openssl@1.1/cert.pem


${slack_base_Url}    https://hooks.slack.com/
${slack_webhook_url}    https://hooks.slack.com/services/your/webhook/url
${CHANNEL}        general
*** Keywords ***

Send Message to Slack
    [Documentation]  我已經離開公司了，slack 帳號已經失效了。這段程式碼，沒有經過測試
    ${current_date}=    Get Current Date    result_format=%Y/%m/%d
    ${message}    Set Variable    ${current_date} 測試執行完畢
    ${payload}    Create Dictionary    text=${message}
    ${headers}    Create Dictionary    Content-Type=application/json

    create session  mysession   ${slack_base_Url}     headers=${headers}
    ${response}=    Post On Session    mysession   /services/your/webhook/url  data=${payload}   headers=${headers}
Teardown Actions
    Close Browser
    # Send Message to Slack
Get Page Level Rank
    [Documentation]  VIP 費用等級列表 欄位
    [Arguments]	${Num}
    Wait Until Element Is Visible    xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[1]/h4[2]
    ${Location}    Set Variable    ${${Num}+2}
    ${level_xpath}    Set Variable    xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/div[${Location}]/div[1]/span
    ${Level} =    Get Text    ${level_xpath}

    ${pre30_xpath}    Set Variable    xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/div[${Location}]/div[2]/span
    ${pre30} =    Get Text    ${pre30_xpath}

    ${operator_xpath}    Set Variable    xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/div[${Location}]/div[3]/span
    ${operator} =    Get Text    ${operator_xpath}

    ${pre1_xpath}    Set Variable    xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/div[${Location}]/div[4]/span
    ${pre1} =    Get Text    ${pre1_xpath}

    ${maker_taker_xpath}    Set Variable    xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/div[${Location}]/div[5]/span
    ${maker_taker} =    Get Text    ${maker_taker_xpath}

    ${maker_taker_discount20_xpath}    Set Variable    xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/div[${Location}]/div[6]/span
    ${maker_taker_discount20} =    Get Text    ${maker_taker_discount20_xpath}

    ${maker_taker_fee_xpath}    Set Variable    xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div/div[${Location}]/div[7]/span
    ${maker_taker_fee} =    Get Text    ${maker_taker_fee_xpath}

    ${dict} =	Create Dictionary	Level=${Level}	pre30=${pre30}	operator=${operator}    pre1=${pre1}	maker_taker=${maker_taker}    maker_taker_discount20=${maker_taker_discount20}    maker_taker_fee=${maker_taker_fee}
    Log To Console    ${dict}

    RETURN    ${dict}


Get API Level Rank
    [Documentation]  VIP 費用等級列表 api 欄位
    [Arguments]	${Num}
    ${headers}=  Create Dictionary  Content-Type=application/json  Accept=application/json
    Create Session    api    ${BASE_URL}    verify=${CERTIFICATE}
    ${response}       GET On Session    api    ${apiPath}    headers=${headers}
    Should Be Equal As Numbers    ${response.status_code}    200
    ${json_data}      Set Variable    ${response.json()}
    # Log To Console   ${json_data["tradingFeeRate"][${Num}]["rank"]}
    ${Level} =   Catenate    VIP   ${json_data["tradingFeeRate"][${Num}]["rank"]}
    Log To Console    ${Level}

    ${format_twdVolume}    Convert To Number	 ${json_data["tradingFeeRate"][${Num}]["twdVolume"]}
    ${format_twdVolume}    Evaluate    int(${format_twdVolume}) if "${format_twdVolume}".endswith(".0") else ${format_twdVolume}
    ${format_twdVolume}=      Format String     {:,}    ${format_twdVolume}

    ${twdVolumeSymbol}=    Run Keyword If    '${json_data["tradingFeeRate"][${Num}]["twdVolumeSymbol"]}' == '>='
    ...    Set Variable    ≥
    ...  ELSE
    ...    Set Variable    ${json_data["tradingFeeRate"][${Num}]["twdVolumeSymbol"]}
    ${pre30} =   Catenate    ${twdVolumeSymbol}   ${format_twdVolume}     TWD
    Log To Console    ${pre30}

    ${operator} =   Set Variable   ${json_data["tradingFeeRate"][${Num}]["rankCondition"]}


    Log To Console    ${operator}

    ${format_bitoAmount}    Convert To Number	${json_data["tradingFeeRate"][${Num}]["bitoAmount"]}
    ${format_bitoAmount}    Evaluate    int(${format_bitoAmount}) if "${format_bitoAmount}".endswith(".0") else ${format_bitoAmount}
    ${format_bitoAmount}=      Format String     {:,}    ${format_bitoAmount}
    ${bitoAmountSymbol}=    Run Keyword If    '${json_data["tradingFeeRate"][${Num}]["bitoAmountSymbol"]}' == '>='
    ...    Set Variable    ≥
    ...  ELSE
    ...    Set Variable    ${json_data["tradingFeeRate"][${Num}]["bitoAmountSymbol"]}
    ${pre1} =   Catenate    ${bitoAmountSymbol}   ${format_bitoAmount}    BITO
    Log To Console    ${pre1}


    # ${format_makerFee}    Evaluate    str(float(${json_data["tradingFeeRate"][${Num}]["makerFee"]}) * 100) + '%'
    # ${format_makerFee}    Evaluate    str(float(${json_data["tradingFeeRate"][${Num}]["makerFee"]}) * 100) + '%'
    # ${format_takerFee}    Evaluate    str(float(${json_data["tradingFeeRate"][${Num}]["takerFee"]}) * 100) + '%'
    ${format_makerFee}    Evaluate    str(round(float(${json_data["tradingFeeRate"][${Num}]["makerFee"]}) * 100,4)) + '%'
    ${format_takerFee}    Evaluate    str(round(float(${json_data["tradingFeeRate"][${Num}]["takerFee"]}) * 100,4)) + '%'
    # ${format_takerFee}    Evaluate    "{:.2%}".format(${json_data["tradingFeeRate"][${Num}]["takerFee"]})
    # ${format_bitoAmount}    Evaluate    float(${format_takerFee})

    ${maker_taker} =   Catenate    ${format_makerFee}  /  ${format_takerFee}
    Log To Console    ${maker_taker}

    # ${format_makerBitoFee}    Evaluate    str(float(${json_data["tradingFeeRate"][${Num}]["makerBitoFee"]}) * 100) + '%'
    # ${format_takerBitoFee}    Evaluate    str(float(${json_data["tradingFeeRate"][${Num}]["takerBitoFee"]}) * 100) + '%'

    ${format_makerBitoFee}    Evaluate    str(round(float(${json_data["tradingFeeRate"][${Num}]["makerBitoFee"]}) * 100,4)) + '%'
    ${format_takerBitoFee}    Evaluate    str(round(float(${json_data["tradingFeeRate"][${Num}]["takerBitoFee"]}) * 100,4)) + '%'

    ${maker_taker_discount20} =   Catenate    ${format_makerBitoFee}  /  ${format_takerBitoFee}
    Log To Console    ${maker_taker_discount20}

    ${format_gridBotMakerFee}    Evaluate    str(round(float(${json_data["tradingFeeRate"][${Num}]["gridBotMakerFee"]}) * 100,4)) + '%'
    ${format_gridBotTakerFee}    Evaluate    str(round(float(${json_data["tradingFeeRate"][${Num}]["gridBotTakerFee"]}) * 100,4)) + '%'

    ${maker_taker_fee} =   Catenate    ${format_gridBotMakerFee}  /  ${format_gridBotTakerFee}
    Log To Console    ${maker_taker_fee}

   ${dict} =	Create Dictionary	Level=${Level}	pre30=${pre30}	operator=${operator}    pre1=${pre1}	maker_taker=${maker_taker}    maker_taker_discount20=${maker_taker_discount20}    maker_taker_fee=${maker_taker_fee}
    Log To Console    ${dict}

    RETURN    ${dict}

Get Page Order Limit By
    [Documentation]     下單限制 交易對
    [Arguments]	${expect_pair}
    Wait Until Element Is Visible    xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[2]/h4
    FOR    ${i}    IN RANGE    1    50
        ${pair} =    Get Text     xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[2]/div/table/tbody/tr[${i}]/td[1]
        Log To Console    ${pair}

        ${counter}=    Run Keyword If    '${pair}'=='${expect_pair}'
        ...    Set Variable    ${i}
        Run Keyword If    '${pair}'=='${expect_pair}'    EXIT For Loop
    END
    Log To Console    ${counter}

    ${minOrder} =    Get Text    xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[2]/div/table/tbody/tr[${counter}]/td[2]
    ${minUnit} =    Get Text    xpath = //*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[2]/div/table/tbody/tr[${counter}]/td[3]
    ${dict} =	Create Dictionary	pair=${pair}	minimumOrderAmountWithBase=${minOrder}	minimumOrderNumberOfDigits=${minUnit}		# key=value syntax
    RETURN    ${dict}


Get API Order Limit By
    [Documentation]     下單限制 交易對 API
    [Arguments]	${expect_pair}
    ${headers}=  Create Dictionary  Content-Type=application/json  Accept=application/json
    Create Session    api    ${BASE_URL}    verify=${CERTIFICATE}
    ${response}       GET On Session    api    ${apiPath}    headers=${headers}
    Should Be Equal As Numbers    ${response.status_code}    200
    ${json_data}      Set Variable    ${response.json()}
    ${cnt}=    Get length    ${json_data["orderFeesAndLimitations"]}
    FOR    ${i}    IN RANGE    ${cnt}
        # Log To Console   ${json_data["orderFeesAndLimitations"][${i}]["pair"]}
        ${pair}    Set Variable    ${json_data["orderFeesAndLimitations"][${i}]["pair"]}
        ${counter}=    Run Keyword If    '${pair}'=='${expect_pair}'
        ...    Set Variable    ${i}
        Run Keyword If    '${pair}'=='${expect_pair}'    EXIT For Loop
    END
    ${pair}    Set Variable    ${json_data["orderFeesAndLimitations"][${counter}]["pair"]}
    ${minOrder}    Set Variable    ${json_data["orderFeesAndLimitations"][${counter}]["minimumOrderAmount"]}
    ${base}    Set Variable    ${json_data["orderFeesAndLimitations"][${counter}]["minimumOrderAmountBase"]}
    ${minUnit}    Set Variable    ${json_data["orderFeesAndLimitations"][${counter}]["minimumOrderNumberOfDigits"]}
    ${minOrder}    Convert To Number	${minOrder}
    ${minOrder}    Evaluate    int(${minOrder}) if "${minOrder}".endswith(".0") else ${minOrder}
    ${minOrder}=      Format String     {:,}    ${minOrder}

    ${minimumOrderAmountWithBase} =   Catenate    ${minOrder}     ${base}
    ${dict} =	Create Dictionary	pair=${pair}	minimumOrderAmountWithBase=${minimumOrderAmountWithBase}	minimumOrderNumberOfDigits=${minUnit}		# key=value syntax
    RETURN    ${dict}

*** Test Cases ***
Case 1 : Check VIP Rank List By 0
    [Documentation]
    ${pageDict}=    Get Page Level Rank    0
    ${apiDict}=    Get API Level Rank    0
    Dictionaries Should Be Equal    ${pageDict}    ${apiDict}

Case 2 : Check VIP Rank List By 1
    [Documentation]
    ${pageDict}=    Get Page Level Rank    1
    ${apiDict}=    Get API Level Rank    1
    Dictionaries Should Be Equal    ${pageDict}    ${apiDict}


Case 3 : Check VIP Rank List By 2
    [Documentation]
    ${pageDict}=    Get Page Level Rank    2
    ${apiDict}=    Get API Level Rank    2
    Dictionaries Should Be Equal    ${pageDict}    ${apiDict}


Case 4 : Check VIP Rank List By 3
    [Documentation]
    ${pageDict}=    Get Page Level Rank    3
    ${apiDict}=    Get API Level Rank    3
    Dictionaries Should Be Equal    ${pageDict}    ${apiDict}


Case 5 : Check VIP Rank List By 4
    [Documentation]
    ${pageDict}=    Get Page Level Rank    4
    ${apiDict}=    Get API Level Rank    4
    Dictionaries Should Be Equal    ${pageDict}    ${apiDict}

Case 6 : Check VIP Rank List By 5
    [Documentation]
    ${pageDict}=    Get Page Level Rank    5
    ${apiDict}=    Get API Level Rank    5
    Dictionaries Should Be Equal    ${pageDict}    ${apiDict}


Case 7 : Check Order Limit By ADA/TWD
    ${pageResult_dict}=   Get Page Order Limit By    ADA/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    ADA/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}
Case 8 : Check Order Limit By APE/TWD
    ${pageResult_dict}=   Get Page Order Limit By    APE/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    APE/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}
Case 9 : Check Order Limit By BCH/TWD
    ${pageResult_dict}=   Get Page Order Limit By    BCH/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    BCH/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}
Case 10 : Check Order Limit By BITO/TWD
    ${pageResult_dict}=   Get Page Order Limit By    BITO/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    BITO/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}

Case 11 :Check Order Limit By BNB/TWD
    ${pageResult_dict}=   Get Page Order Limit By    BNB/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    BNB/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}

Case 12 :Check Order Limit By BTC/TWD
    ${pageResult_dict}=   Get Page Order Limit By    BTC/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    BTC/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}
Case 13 :Check Order Limit By DOGE/TWD
    ${pageResult_dict}=   Get Page Order Limit By    DOGE/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    DOGE/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}
Case 14 :Check Order Limit By EOS/TWD
    ${pageResult_dict}=   Get Page Order Limit By    EOS/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    EOS/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}
Case 15 :Check Order Limit By ETH/TWD
    ${pageResult_dict}=   Get Page Order Limit By    ETH/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    ETH/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}
Case 16:Check Order Limit By GADT/TWD
    ${pageResult_dict}=   Get Page Order Limit By    GADT/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    GADT/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}
Case 17 :Check Order Limit By LTC/TWD
    ${pageResult_dict}=   Get Page Order Limit By    LTC/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    LTC/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}
Case 18 :Check Order Limit By MATIC/TWD
    ${pageResult_dict}=   Get Page Order Limit By    MATIC/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    MATIC/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}
Case 19 :Check Order Limit By MV/TWD
    ${pageResult_dict}=   Get Page Order Limit By    MV/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    MV/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}
Case 20 :Check Order Limit By SHIB/TWD
    ${pageResult_dict}=   Get Page Order Limit By    SHIB/TWD
    Log To Console    ${pageResult_dict}
    ${apiResult_dict}=    Get API Order Limit By    SHIB/TWD
    Log To Console    ${apiResult_dict}
    Dictionaries Should Be Equal    ${pageResult_dict}    ${apiResult_dict}