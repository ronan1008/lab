# Milestone 23.<重置簡訊次數 API> 於「忘記密碼 > 使用手機號碼」發送驗證碼次數達上限後，無法用 API 重置簡訊次數 #1221
import json
import requests
import pytest
from assistence import api
from assistence import initdata
from pprint import pprint
#設定好預設的環境
env = 'QA2'
#設定好header
header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
#設定set_test_data的parameters
test_parameter = {}
#初始化所有acc token 與 nonce : test_parameter['xxxx']
# backend_acc, backend_nonce, backend_token, broadcaster1_acc...
initdata.set_test_data(env, test_parameter)
#設定 backend 的 token 與 nonce 給 header
header['X-Auth-Token'] = test_parameter['backend_token']
header['X-Auth-Nonce'] = test_parameter['backend_nonce']

def test_get_user_phone_num():
    api_name = '/api/v2/backend/giftCategory/list'
    #帶入 prefix userid header
    user_id = api.search_user(test_parameter['prefix'], 'happy', header)
    api_name = '/api/v2/backend/user/' + user_id

    res = api.apiFunction(test_parameter['prefix'], header, api_name , 'get', None)
    if res.status_code // 100 == 2:
        restext = json.loads(res.text)
        assert restext['phoneNumber'] == '937855506'
        assert restext['phoneCountryCode'] == '886'
        phoneNumber = restext['phoneNumber']
        phoneCountryCode = restext['phoneCountryCode']
        country_phone = phoneCountryCode+ "-" + phoneNumber

        del header['X-Auth-Token']
        del header['X-Auth-Nonce']
        header['Content-Type'] = 'application/json'

        flag = True
        while flag:
            api_name = '/api/v2/identity/password/send'
            data = {
                "source":"mobile",
                "identifier":country_phone,
            }

            res = api.apiFunction(test_parameter['prefix'], header, api_name , 'post', data)
            print('-------------')
            print(data)
            print(res.text)
            print(res.status_code)
            print('-------------')
            if res.status_code // 100 == 4:
                restext = json.loads(res.text)
                assert restext['Message'] == "WEEKLY_LIMIT_OF_MOBILE_SMS_SENT_REACHED"
                flag = False

        header['X-Auth-Token'] = test_parameter['backend_token']
        header['X-Auth-Nonce'] = test_parameter['backend_nonce']
        api_name = '/api/v2/cs/sms/reset'
        data = {
            "phonenumbers": [ "+" + phoneCountryCode + phoneNumber ]
        }
        res = api.apiFunction(test_parameter['prefix'], header, api_name , 'post', data)
        assert res.status_code // 100 == 2
        if res.status_code // 100 == 2:
            del header['X-Auth-Token']
            del header['X-Auth-Nonce']
            header['Content-Type'] = 'application/json'
            api_name = '/api/v2/identity/password/send'
            data = {
                "source":"mobile",
                "identifier":country_phone,
            }
            res = api.apiFunction(test_parameter['prefix'], header, api_name , 'post', data)
            assert res.status_code // 100 == 2

