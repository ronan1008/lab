#milestone 27. [首頁改版][New API] GET 使用者獲取頁籤列表：GET /v2/identity/tabSetting #1702
import json
import requests
import pytest
from assistence import api
from assistence import initdata
from assistence import dbConnect
from pprint import pprint

class Tab():
    def __init__(self):
        env = 'QA2'
        test_parameter = {}
        initdata.set_test_data(env, test_parameter)
        self.test_parameter = test_parameter
        self.prefix = test_parameter['prefix']
        self.api_name=''

    def set_header(self, token, nonce):
        self.header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
        self.header['Content-Type'] = 'application/json'
        self.header['X-Auth-Token'] = self.test_parameter[token]
        self.header['X-Auth-Nonce'] = self.test_parameter[nonce]
        return self.header

    def user_show_tab_list(self, header):
        api_name = "/api/v2/identity/tabSetting"
        res = api.apiFunction(self.prefix, header, api_name, 'get', None)
        return res

class TestTag():
    env = 'QA2'
    test_parameter = {}
    tab = Tab()
    test_parameter = tab.test_parameter

    #NOTE: 僅為測試資料，未來有API 可以新增修改刪除時，不需要了
    @classmethod
    def setup_class(cls):
        sql_list = []
        sql_list.append("insert into tab_setting (id, tag_group_id, template, `order`, created_at, updated_at, create_user_id, update_user_id) values (1, 1, 'templete-1', 3, '2032-12-31 23:59:59', '2032-12-31 23:59:59','774ab73f-6aa6-4ed1-a991-609d7db7d1a3','774ab73f-6aa6-4ed1-a991-609d7db7d1a3')")
        sql_list.append("insert into tab_setting (id, tag_group_id, template, `order`, created_at, updated_at, create_user_id, update_user_id) values (2, 2, 'templete-2', 2, '2032-12-31 23:59:59', '2032-12-31 23:59:59','774ab73f-6aa6-4ed1-a991-609d7db7d1a3','774ab73f-6aa6-4ed1-a991-609d7db7d1a3')")
        sql_list.append("insert into tab_setting (id, tag_group_id, template, `order`, created_at, updated_at, create_user_id, update_user_id) values (3, 3, 'templete-3', 4, '2032-12-31 23:59:59', '2032-12-31 23:59:59','774ab73f-6aa6-4ed1-a991-609d7db7d1a3','774ab73f-6aa6-4ed1-a991-609d7db7d1a3')")
        sql_list.append("insert into tab_setting (id, tag_group_id, template, `order`, created_at, updated_at, create_user_id, update_user_id) values (4, 4, 'templete-4', 1, '2032-12-31 23:59:59', '2032-12-31 23:59:59','774ab73f-6aa6-4ed1-a991-609d7db7d1a3','774ab73f-6aa6-4ed1-a991-609d7db7d1a3')")
        sql_list.append("insert into tab_setting (id, tag_group_id, template, `order`, created_at, updated_at, create_user_id, update_user_id) values (5, 5, 'templete-5', 5, '2032-12-31 23:59:59', '2032-12-31 23:59:59','774ab73f-6aa6-4ed1-a991-609d7db7d1a3','774ab73f-6aa6-4ed1-a991-609d7db7d1a3')")
        sql_list.append("insert into tab_setting (id, tag_group_id, template, `order`, created_at, updated_at, create_user_id, update_user_id) values (6, 1, 'templete-1', 6, '2032-12-31 23:59:59', '2032-12-31 23:59:59','774ab73f-6aa6-4ed1-a991-609d7db7d1a3','774ab73f-6aa6-4ed1-a991-609d7db7d1a3')")
        dbConnect.dbSetting(cls.test_parameter['db'], sql_list, 'shocklee')

    #NOTE: 僅為測試資料，未來有API 可以新增修改刪除時，不需要了
    @classmethod
    def teardown_class(cls):
        sql_list =["DELETE FROM tab_setting WHERE created_at='2032-12-31 23:59:59'"]
        dbConnect.dbSetting(cls.test_parameter['db'], sql_list, 'shocklee')

    test_list_data=[
        ('User header'        ,            'user_token',            'user_nonce', 2),
        ('broadcaster header' ,     'broadcaster_token',     'broadcaster_nonce', 2),
        ('liveController'     , 'liveController1_token', 'liveController1_nonce', 2),
        ('auth error'         ,             'err_token',             'err_nonce', 4),
    ]

    @pytest.mark.parametrize("scenario, token, nonce, expected", test_list_data)
    def test_user_show_tab_list(self, scenario, token, nonce, expected):
        header = self.tab.set_header(token, nonce)
        res = self.tab.user_show_tab_list(header)
        assert res.status_code // 100 == expected
        if expected == 2:
            restext = json.loads(res.text)
            pprint(restext)
            assert restext['data'][-1]['order'] >= restext['data'][-2]['order']
            assert restext['data'][0]['order'] <= restext['data'][1]['order']
            assert all([ item in restext['data'][-1] for item in ['id', 'order', 'groupId', 'template']]) == True
        else:
            assert res.status_code == 401


