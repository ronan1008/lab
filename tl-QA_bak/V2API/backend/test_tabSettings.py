#milestone 28.[首頁改版][New API] 後台設定頁籤 (Tab) ：POST /v2/backend/tabSetting #1700
#milestone 28.[首頁改版][New API] 後台編輯頁籤 (Tab) ：PATCH /v2/backend/tabSetting/{{tab_id}} #1701
# pylint: disable=unbalanced-tuple-unpacking
import json
import requests
import pytest
from assistence import api
from assistence import initdata
from assistence import dbConnect
from pprint import pprint

class TabSetting:
    def __init__(self):
        self.test_parameter = {}
        self.prefix = ''

    def set_header(self, token, nonce):
        self.header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
        self.header['Content-Type'] = 'application/json'
        self.header['X-Auth-Token'] = self.test_parameter[token]
        self.header['X-Auth-Nonce'] = self.test_parameter[nonce]
        return self.header
    #  ( {"groupId":  1,"order": 1,"template": "HOT"} , {"groupId": 4,"order": 2,"template": "HOT"} , {"groupId": 4,"order": 3,"template": "HOT"} )
    def create_tab(self, header, tabs:list):
        api_name = "/api/v2/backend/tabSetting"
        body = {'data':[]}
        for tab in tabs:
            data = {"groupId": tab['groupId'], "order": tab['order'], "template": tab['template'],}
            data = {key: value for key, value in data.items() if value}
            body['data'].append(data)
        res = api.apiFunction(self.prefix, header, api_name, 'post',body)
        return res

    #( {"groupId":  1,"order": 1,"template": "HOT"} , {"groupId": 4,"order": 2,"template": "HOT"} , {"groupId": 4,"order": 3,"template": "HOT"} )
    def update_tab(self, header, edit_tabs:list):
        api_name = "/api/v2/backend/tabSetting"
        body = {'data':[]}
        for tab in edit_tabs:
            data = {"id": tab['id'], "groupId": tab['groupId'], "order": tab['order'], "template": tab['template'],}
            data = {key: value for key, value in data.items() if value}
            body['data'].append(data)
        res = api.apiFunction(self.prefix, header, api_name, 'patch',body)
        return res

class TestTab():
    env = 'QA2'
    test_parameter = {}
    initdata.set_test_data(env, test_parameter)
    tab = TabSetting()
    tab.test_parameter = test_parameter
    tab.prefix = test_parameter['prefix']
    tab_id_list = []

    @classmethod
    def setup_class(cls):
        sql = ["delete from tab_setting where template like '%test%'"]
        dbConnect.dbSetting(TestTab.test_parameter['db'], sql, 'shocklee')
    @classmethod
    def teardown_class(cls):
        pass


    tabs=[
           ( {"groupId":  1,"order": 1,"template": "test1"} , {"groupId": 4,"order": 2,"template": "test2"} , {"groupId": 4,"order": 3,"template": "test3"} ),
           ( {"groupId":  2,"order": 4,"template": "test4"} ,),
           ( {"groupId":  3,"order": 6,"template": "test6"} , {"groupId":    4,"order":    5,"template": "test5"} ),
           ( {"groupId":  3,"order": 1,"template": "test"} , {"groupId": None,"order":    2,"template": "test"} ), #缺 groupId
           ( {"groupId":  3,"order": 1,"template": "test"} , {"groupId":    4,"order": None,"template": "test"} ), #缺 order
           ( {"groupId":  3,"order": 1,"template": "test"} , {"groupId":    4,"order":    2,"template":  None} ), #缺 template
    ]
    create_tab_data=[
        #            scenario,                   token,                   nonce, expected,   *tabs
        (  'three groups query',         'backend_token',         'backend_nonce',        2, tabs[0]),
        (     'one group query', 'liveController1_token', 'liveController1_nonce',        2, tabs[1]), #之後改成 liveController1_token
        (  'two groups reverse', 'liveController2_token', 'liveController2_nonce',        2, tabs[2]),
        (     'Lack Of groupId',         'backend_token',         'backend_nonce',        4, tabs[3]),
        (       'Lack Of order',         'backend_token',         'backend_nonce',        4, tabs[4]),
        (    'Lack Of template',         'backend_token',         'backend_nonce',        4, tabs[5]),
        (          'auth error',             'err_token',             'err_nonce',        4, tabs[0]),
    ]
    @pytest.mark.parametrize("scenario, token, nonce, expected, tabs", create_tab_data)
    def test_create_tab(self, scenario, token, nonce, expected, tabs):
        header = self.tab.set_header(token, nonce)
        res = self.tab.create_tab(header, tabs)
        assert res.status_code // 100 == expected
        if expected == 2:
            restext = json.loads(res.text)
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
            #使用 identity 的 /api/v2/identity/tabSetting 來檢查欄位是否正確儲存
            api_name = "/api/v2/identity/tabSetting"
            res = api.apiFunction(TestTab.test_parameter['prefix'], header, api_name, 'get', None)
            restext = json.loads(res.text)
            if scenario == 'three groups query':
                assert len(restext['data']) == 3
                assert restext['data'][0]['order'] == tabs[0]['order']
                assert restext['data'][-1]['order'] == tabs[-1]['order']
                assert restext['data'][0]['groupId'] == tabs[0]['groupId']
                assert restext['data'][0]['template'] == tabs[0]['template']
            elif scenario == 'one group query':
                assert len(restext['data']) == 3+1
            elif scenario == 'two groups reverse':
                assert len(restext['data']) == 3+1+2
                assert restext['data'][-1]['order'] == tabs[0]['order']
                assert restext['data'][-2]['order'] == tabs[1]['order']
                assert restext['data'][-1]['template'] == tabs[0]['template']
                assert restext['data'][-2]['groupId'] == tabs[1]['groupId']
                TestTab.tab_id_list = [ restext['data'][i]['id'] for i in range(len(restext['data'])) ]
        else:
            if scenario.find('Lack Of') != -1:
                assert res.status_code == 400
            elif scenario.find('auth error') != -1:
                assert res.status_code == 401

    edit_tabs=[
        #base (                  {"groupId":  3,"order": 2,"template": "HOT"}  ,                         {"groupId": 4,"order": 1,"template": "COLD"} )
        ( {"id":  0, "groupId":  5,"order": 1,    "template": "testEdit1"} ,),
        ( {"id":  1, "groupId":  3,"order": 2,    "template": "testEdit2"} , {"id":     2, "groupId":  1,"order":    3,"template": "testEdit3"} ),
        ( {"id":  3, "groupId":  1,"order": 5,    "template": "testEdit4"} , {"id":     4, "groupId":  4,"order":    4,"template": "testEdit5"} ),
        ( {"id":  5, "groupId":  5,"order": None, "template": "testEdit6"} , {"id":     0, "groupId":  3,"order": None,"template": None } ),
        ( {"id":  0, "groupId":  3,"order": 1,    "template": "testEdit7"} , {"id":  None, "groupId":  3,"order": 2,"template": "testEdit8"} ), #缺 id
        ( {"id":  0, "groupId":  3,"order": 1,    "template": "testEdit9"} , {"id":  9999, "groupId":  3,"order": 2,"template": "testEdit10"} ), #id 不存在
    ]
    edit_tab_data=[
        #            scenario,                   token,                   nonce, expected,   *tabs
        ('change one of groupId template and reverse',         'backend_token',         'backend_nonce',        2, edit_tabs[0]),
        (               'change all of groupId order', 'liveController1_token', 'liveController1_nonce',        2, edit_tabs[1]),
        (           'change all with all and reverse',         'backend_token',         'backend_nonce',        2, edit_tabs[2]),
        (       'change all with require and reverse',         'backend_token',         'backend_nonce',        2, edit_tabs[3]),
        (                                'Lack Of Id',         'backend_token',         'backend_nonce',        4, edit_tabs[4]),
        (                          'Tab Id Not Found',         'backend_token',         'backend_nonce',        4, edit_tabs[5]),
        (                                'auth error',             'err_token',             'err_nonce',        4, edit_tabs[0]),
    ]
#    @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.parametrize("scenario, token, nonce, expected, edit_tabs", edit_tab_data)
    def test_update_tab(self, scenario, token, nonce, expected, edit_tabs):
        tab_data = []
        x= self.__class__.tab_id_list
        for tab in edit_tabs:
            tab_data.append({ key:(x[val] if key=='id' and val is not None and val < len(x)  else val) for key, val in tab.items()},)
        header = self.tab.set_header(token, nonce)
        #print(tab_data)
        res = self.tab.update_tab(header, tab_data)
        assert res.status_code // 100 == expected
        if expected == 2:
            restext = json.loads(res.text)
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
            #使用 identity 的 /api/v2/identity/tabSetting 來檢查欄位是否正確儲存
            api_name = "/api/v2/identity/tabSetting"
            res = api.apiFunction(TestTab.test_parameter['prefix'], header, api_name, 'get', None)
            restext = json.loads(res.text)
            # print("/n")
            # pprint(restext)
            assert restext['data'][0]['order'] == 1 and restext['data'][0]['order'] < restext['data'][1]['order']

            if scenario == "change one of groupId template and reverse" :
                assert restext['data'][0]['groupId'] == edit_tabs[0]['groupId']
                assert restext['data'][0]['template'] == edit_tabs[0]['template']
                assert restext['data'][0]['groupId'] == edit_tabs[0]['groupId']
                assert restext['data'][0]['template'] == edit_tabs[0]['template']
            elif scenario == 'change all of groupId order':
                assert restext['data'][1]['groupId'] == edit_tabs[0]['groupId']
                assert restext['data'][1]['template'] == edit_tabs[0]['template']
                assert restext['data'][2]['groupId'] == edit_tabs[1]['groupId']
                assert restext['data'][2]['template'] == edit_tabs[1]['template']
            elif scenario == 'change all with all and reverse':
                assert restext['data'][3]['groupId'] == edit_tabs[1]['groupId']
                assert restext['data'][3]['template'] == edit_tabs[1]['template']
                assert restext['data'][4]['groupId'] == edit_tabs[0]['groupId']
                assert restext['data'][4]['template'] == edit_tabs[0]['template']
            elif scenario == 'change all with require and reverse':
                assert restext['data'][5]['groupId'] == edit_tabs[0]['groupId']
                assert restext['data'][5]['template'] == edit_tabs[0]['template']
                assert restext['data'][0]['groupId'] == edit_tabs[1]['groupId']
                assert restext['data'][0]['template'] == "testEdit1"
        else:
            restext = json.loads(res.text)
            if scenario == "Lack Of Id" or scenario == "Tab Id Not Found" :
                assert res.status_code == 400
            else:
                assert res.status_code == 401
