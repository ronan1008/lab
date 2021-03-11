# Milestone 23.[New v2 API] 使用者撈取自己點數購買紀錄：GET /v2/identity/transactionList #1041
import json
import requests
import pytest
from assistence import api
from assistence import initdata
from pprint import pprint
from assistence import dbConnect
from assistence import sundry

env = 'QA2'
test_parameter = {}
header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
initdata.set_test_data(env, test_parameter)
header['X-Auth-Token'] = test_parameter['backend_token']
header['X-Auth-Nonce'] = test_parameter['backend_nonce']
result = api.user_login(test_parameter['prefix'], "track0005", '123456')
test_parameter['test_user_token'] = result['data']['token']
test_parameter['test_user_nonce'] = result['data']['nonce']
user_id_list=[]
user_id_list.append(api.search_user(test_parameter['prefix'],"track0005",header))
user_id_list.append(api.search_user(test_parameter['prefix'],"track0006",header))
#scenario, token, nonce, expect, yipay
test_data = [
    (           'user query',       'test_user_token',        'test_user_nonce', user_id_list[0], 2, True),
    (           'user query',       'test_user_token',        'test_user_nonce', user_id_list[0], 2, False),
    ('token/ nonce is wrong',             'err_token',              'err_nonce', user_id_list[1], 4, True),
    (            'No Record', 'liveController1_token',  'liveController1_nonce', user_id_list[1], 2, True),
]
# def setup_module():
#     header['X-Auth-Token'] = test_parameter['test_user_token']
#     header['X-Auth-Nonce'] = test_parameter['test_user_nonce']
#     sundry.yipay(test_parameter['prefix'], header, test_user_id, 'web.points.650000', True)

@pytest.mark.parametrize("scenario, token, nonce, user_id, expect, yipaySucc", test_data)
def test_transactionList(scenario, token, nonce,  user_id, expect, yipaySucc):
    header['X-Auth-Token'] = test_parameter['backend_token']
    header['X-Auth-Nonce'] = test_parameter['backend_nonce']
    sundry.yipay(test_parameter['prefix'], header, user_id, 'web.points.650000', yipaySucc)
    api_name = '/api/v2/identity/transactionList'
    header['X-Auth-Token'] = test_parameter[token]
    header['X-Auth-Nonce'] = test_parameter[nonce]
    res = api.apiFunction(test_parameter['prefix'], header, api_name , 'get', None)
    assert res.status_code // 100 == expect
    if expect == 2:
        restext = json.loads(res.text)
        if scenario == 'No Record':
            assert len(restext['data']) == 0
        elif scenario =='user query':
            pprint(restext)
            assert restext['data'][0]['purchaseType'] == 'yipay'
            assert restext['data'][0]['point']== 650000 and restext['data'][0]['amount']== 650000
            assert all([ x in restext['data'][0] for x in ['orderId', 'purchaseType', 'amount', 'point', 'createAt']]) == True
            transSucc_count = len(restext['data'])
            #超過20筆，有offset，帶著offset再query一次，一直query 直到沒有 offset
            if 'offset' in restext:
                assert restext['data'][-1]['orderId'] == restext['offset']
                offset=True
            else:
                offset=False
                print('Only One Page Record')
            while offset:
                api_name = '/api/v2/identity/transactionList?offset=' + str(restext['offset'])
                res = api.apiFunction(test_parameter['prefix'], header, api_name , 'get', None)
                restext = json.loads(res.text)
                transSucc_count += len(restext['data'])
                if 'offset' in restext:
                    assert restext['data'][-1]['orderId'] == restext['offset']
                    assert res.status_code // 100 == expect
                else:
                    offset=False
                    print('All Record Search Finished')

            sql = "select count(*) from purchase_order where consumer_user_id = \
                        '{}' and status = 1".format(user_id)

            [(db_result,)] = dbConnect.dbQuery(test_parameter['db'], sql , 'shocklee')
            assert db_result == transSucc_count

