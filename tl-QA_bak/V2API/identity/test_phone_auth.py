#1484 [Update v1 API] 進行手機驗證：POST /api/v1/identity/phoneAuth 追加排除手機號碼第一碼的零
#1485 [Update v1 API] 取得註冊手機驗證碼：POST /api/v1/identity/phoneAuthCode 追加排除手機號碼第一碼的零
import json
import pytest
from assistence import api
from assistence import initdata
from assistence import dbConnect
from pprint import pprint
env = 'QA2'
test_parameter = {}
header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
initdata.set_test_data(env, test_parameter)

test_data = {
    # login_id , phone_number , expect_phone_number
    ('track5111', '0937855506', '937855506'),
    ('track5111',  '937855506', '937855506'),
}

@pytest.mark.parametrize("login_id, phone_number, expect_phone_number", test_data)
def test_phoneAuth(login_id, phone_number, expect_phone_number):

    #DB Query 先更新sms_history關於此電話的紀錄
    sqlStr =["UPDATE sms_history  SET phone_number = '111111111' WHERE phone_number LIKE '%{}%'".format(expect_phone_number)]
    print(sqlStr)
    dbConnect.dbSetting(test_parameter['db'], sqlStr, 'shocklee')

    #使用者 login，得到 token 與 nonce
    result = api.user_login(test_parameter['prefix'], login_id, '123456')
    header['X-Auth-Token'] = result['data']['token']
    header['X-Auth-Nonce'] = result['data']['nonce']

    #使用者發送驗證code
    api_name = '/api/v1/identity/phoneAuthCode'
    body = {
        "loginId": login_id,
        "phoneCountryCode": '+886',
        "phoneNumber": phone_number
    }
    res =  api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    assert res.status_code == 200

    #確認 sms_history 的 phone_number 欄位，有 expect_phone_number 這筆資料（不含零）
    sqlStr ="Select COUNT(*) From sms_history Where phone_number='{}'".format(expect_phone_number)
    db_result = dbConnect.dbQuery(test_parameter['db'], sqlStr , 'shocklee')
    assert db_result[0][0] == 1

    #DB Query 從 user_id 得到 activate_code、phone_num、country_code （確認activate不含零）
    sqlStr ="Select activate_code From identity Where login_id='{}'".format(login_id)
    db_result = dbConnect.dbQuery(test_parameter['db'], sqlStr , 'shocklee')
    activate_code = db_result[0][0].split('_')[0]
    activate_country_code = db_result[0][0].split('_')[1].split('-')[0]
    activate_mobile_num = db_result[0][0].split('_')[1].split('-')[1]
    assert activate_mobile_num == expect_phone_number

    #使用者傳送驗證code
    api_name = '/api/v1/identity/phoneAuth'
    body = {
        "activateCode": activate_code,
        "loginId": login_id,
        "phoneCountryCode": "+" + activate_country_code,
        "phoneNumber": phone_number,
        "pushToken": "string"
    }
    res =  api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    print(json.loads(res.text))
    assert res.status_code == 200

    #DB Query 從 identity 確認 phone_num 為 expect_phone_number
    sqlStr ="Select phone_number From identity Where login_id='track5111'"
    db_result = dbConnect.dbQuery(test_parameter['db'], sqlStr , 'shocklee')
    phone_query = db_result[0][0]
    assert phone_query == expect_phone_number
