# Milestone 23.[New v2 API] 後台撈取使用者點數購買紀錄：GET /v2/backend/user/transactionList/{user_id} #1026
# Milestone 27.後台撈取使用者點數購買紀錄 API purchaseType 定義修正 #1642
# Milestone 27.[Enhancement] 後台撈取使用者點數購買紀錄，回應中需要追加「消費點數」 #1628

import json
import requests
import datetime
import time
import pytest
from assistence import api
from assistence import initdata
from pprint import pprint
from assistence import dbConnect
from assistence import sundry

env = 'QA2'
test_parameter = {}
header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}

idList=[]

now_datetime = datetime.datetime.now() # 目前時間的 datetime object
b1hours_datetime = now_datetime - datetime.timedelta(hours = 1) # 目前時間少1hours object
b1hours_timestamp = int(b1hours_datetime.timestamp()) # 將 object 轉成 timestamp
b7days_datetime = now_datetime - datetime.timedelta(days = 7) # 目前時間少7days object
b7days_timestamp = int(b7days_datetime.timestamp()) # 將 object 轉成 timestamp
now_timestamp = int(now_datetime.timestamp()) # 將 object 轉成 timestamp
now_timestamp = now_timestamp + 100

initdata.set_test_data(env, test_parameter)
header['X-Auth-Token'] = test_parameter['backend_token']
header['X-Auth-Nonce'] = test_parameter['backend_nonce']
test_user_id = api.search_user(test_parameter['prefix'],"track0050",header)
def setup_module():
    #test_user_id = api.search_user(test_parameter['prefix'],"track0050",header)
    #產生乙禾網路交易紀錄
    sundry.yipay(test_parameter['prefix'], header, test_user_id, 'web.points.650000', True)
    #產生後台加點交易紀錄
    time.sleep(1)
    sundry.remittance(test_parameter['prefix'], header, test_user_id)
#scenario, token, nonce, st_time, end_time, item, page, expect

testData = [
    #權限限定 : ADMIN, BUSINESS_MANAGER, ROLE_LIVE_CONTROLLER

    (          'admin query', test_user_id,        'backend_token',         'backend_nonce', b1hours_timestamp,    now_timestamp, 5, 1, 2),
    (       'business query', test_user_id,        'project_token',         'project_nonce', b1hours_timestamp,             None, 10, 1, 2),
    ('live controller query', test_user_id,'liveController1_token', 'liveController1_nonce',              None,    now_timestamp, 15, 1, 2),
    (    'boradcaster query', test_user_id,    'broadcaster_token',     'broadcaster_nonce',              None,             None, 10, 1, 4),
    (           'user query', test_user_id,           'user_token',            'user_nonce', b1hours_timestamp,    now_timestamp, 10, 1, 4),
    (    'token nonce wrong', test_user_id,            'err_token',             'err_nonce',              None,             None, 10, 1, 4),
]

@pytest.mark.parametrize("scenario, test_user_id, token, nonce, st_time, end_time, item, page, expect", testData)
def test_transaction_list(scenario, test_user_id, token, nonce, st_time, end_time, item, page, expect):
    #GET /v2/backend/user/transactionList/df5bdc75-7482-4fb2-834e-68dcc477d3af?startTime=1590012345&endTime=1690012345&item=20&page=1
    api_name = '/api/v2/backend/user/transactionList/' + test_user_id
    parameters_dict = {'startTime' : st_time, 'endTime' : end_time, 'item' : item, 'page' : page,}
    api_name = api.dict_to_url_get(api_name, parameters_dict)
    header['X-Auth-Token'] = test_parameter[token]
    header['X-Auth-Nonce'] = test_parameter[nonce]
    res = api.apiFunction(test_parameter['prefix'], header, api_name , 'get', None)
    assert res.status_code // 100 == expect
    if expect == 2:
        restext = json.loads(res.text)
        if st_time is None:
            st_time = b7days_timestamp
        elif end_time is None:
            end_time = now_timestamp
        count = len(restext['data'])
        assert count <= item
        assert all([ x in restext['data'][-1] for x in ['orderId', 'purchaseType', 'amount', 'points', 'status', 'createAt']]) == True
        assert st_time < restext['data'][-1]['createAt'] # 最後一筆資料 比 startTime 大
        assert restext['totalCount'] != None
        assert restext['data'][0]['createAt'] < end_time # 第一筆資料 比 endTime 小
        assert restext['data'][0]['createAt'] > restext['data'][1]['createAt'] # 第一筆比第二筆大
        assert restext['data'][0]['purchaseType'] == '匯款儲值' # 最新的資料是 yipay
        assert restext['data'][1]['purchaseType'] == '乙禾網路' # 第二筆資料是 乙禾網路
        assert restext['data'][0]['points'] == 100
        assert restext['data'][0]['amount'] == 30.0
        assert restext['data'][1]['points'] == 650000
        assert restext['data'][1]['amount'] == 100000.0



