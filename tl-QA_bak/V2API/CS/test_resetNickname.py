# Milestone 29
import json
import requests
import pytest
from assistence import api
from assistence import initdata
from pprint import pprint
from datetime import datetime

def edit_user_nickName(prefix, nickname, header):
    api_name ='/api/v2/identity/myInfo'
    body = {
        "nickname": nickname,
        "sex": 1,
        "isPublicSexInfo": True,
        "description": "My name is Sana’a\nI like twice\nI love dancing\nHappy hope love peace",
        "birthday": 1569600123
    }
    res = api.apiFunction(prefix, header, api_name, 'put', body)
    return res


env = 'QA2'
test_parameter = {}
header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
initdata.set_test_data(env, test_parameter)
header['X-Auth-Token'] = test_parameter['backend_token']
header['X-Auth-Nonce'] = test_parameter['backend_nonce']

testData = [
    (             'admin query',         'backend_token',         'backend_nonce', "track2000", 2),
    (    'liveController query', 'liveController1_token', 'liveController1_nonce', "track2001", 2),
    (       'boradcaster query',     'broadcaster_token',     'broadcaster_nonce', "track2002", 4),
    ('Lack Of Necessary Params',         'backend_token',         'backend_nonce', "track2002", 4),
    (          'User Not Found',         'backend_token',         'backend_nonce', "track2003", 4),
    (              'Auth Error',             'err_token',             'err_nonce', "track2004", 4),
]
@pytest.mark.parametrize("scenario, token, nonce, account ,expected", testData)
def test_Reset_NickName_Count(scenario, token, nonce, account ,expected):
    header['X-Auth-Token'] = test_parameter['backend_token']
    header['X-Auth-Nonce'] = test_parameter['backend_nonce']
    user_id = api.search_user(test_parameter['prefix'],"track2000", header)
    result = api.user_login(test_parameter['prefix'], "track2000", '123456')
    header['X-Auth-Token'] = result['data']['token']
    header['X-Auth-Nonce'] = result['data']['nonce']
    reach_limit = False
    count = 0
    while not reach_limit :
        now_ts = datetime.now().timestamp()
        edit_nickname = '修改帳號' + str(now_ts)[-4:]
        res = edit_user_nickName(test_parameter['prefix'], edit_nickname, header)
        count += 1
        if res.status_code // 100 == 4:
            restext = json.loads(res.text)
            assert restext['Message'] == 'LIMIT_OF_NICKNAME_ADJUSTED_REACHED'
            reach_limit = True
    print("****")
    print(count)
    print("****")
    header['X-Auth-Token'] = test_parameter[token]
    header['X-Auth-Nonce'] = test_parameter[nonce]
    api_name = "/api/v2/cs/nickname/reset"
    if scenario == 'User Not Found': user_id ='abcd'
    body = {"userId": user_id}
    if scenario == 'Lack Of Necessary Params': body = None
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    restext = json.loads(res.text)
    if expected == 2:
        assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
        header['X-Auth-Token'] = result['data']['token']
        header['X-Auth-Nonce'] = result['data']['nonce']
        now_ts = datetime.now().timestamp()
        edit_nickname = '最後修改帳號' + str(now_ts)[-4:]
        res = edit_user_nickName(test_parameter['prefix'], edit_nickname, header)
        assert res.status_code // 100 == 2
    else:
        if scenario == 'Auth Error':
            assert res.status_code == 401
        elif scenario == 'User Not Found':
            assert res.status_code == 404
        elif scenario == 'Lack Of Necessary Params':
            assert res.status_code == 400
        else:
            assert res.status_code == 403
