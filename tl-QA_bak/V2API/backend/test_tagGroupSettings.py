#milestone 28.[首頁改版] 後台新增標籤群組 (Tag Group)：POST /v2/backend/tagGroup #1756
#milestone 28.[首頁改版] 後台編輯標籤群組 (Tag Group)：PATCH /v2/backend/tagGroup #1757
#milestone 28.[首頁改版] 後台撈取標籤群組列表 (Tag Group)：GET /v2/backend/tagGroup/list #1758
#/backend 底下的 API，需要有以下權限 :ROLE_ADMIN	BUSINESS_MANAGER	ROLE_BUSINESS_MANAGER	LIVE_CONTROLLER	ROLE_LIVE_CONTROLLER
# pylint: disable=unbalanced-tuple-unpacking
import json
import requests
import pytest
from backend.test_tagSettings import Tag
from backend.test_tabSettings import TabSetting
from assistence import api
from assistence import initdata
from assistence import dbConnect
from pprint import pprint

class TagGroup():
    def __init__(self):
        self.test_parameter = {}
        self.prefix = ''

    def set_header(self, token, nonce):
        self.header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
        self.header['Content-Type'] = 'application/json'
        self.header['X-Auth-Token'] = self.test_parameter[token]
        self.header['X-Auth-Nonce'] = self.test_parameter[nonce]
        return self.header

    #POST 後台新增標籤群組 (Tag Group)
    def create_tagGroup(self, label, tag_type, header):
        api_name = "/api/v2/backend/tagGroup"
        body = {'label':label ,
                'type': tag_type,
        }
        body = {key : val for key,val in  body.items() if val is not None}
        res = api.apiFunction(self.prefix, header, api_name, 'post',body)
        return res

    #GET 後台撈取標籤群組列表 (Tag Group):typeFilter, item, page
    def read_tagGroup_list(self, header, **kwargs):
        api_name = "/api/v2/backend/tagGroup/list"
        api_name = api.dict_to_url_get(api_name, kwargs)
        res = api.apiFunction(self.prefix, header, api_name, 'get', None)
        return res

    #PATCH 後台編輯標籤群組 (Tag Group)
    def edit_tagGroup(self, tag_group_id, label, tag_type, header):
        api_name = "/api/v2/backend/tagGroup/" + str(tag_group_id)
        body = {'label':label ,
                'type': tag_type,
        }
        body = {key : val for key,val in  body.items() if val is not None}
        res = api.apiFunction(self.prefix, header, api_name, 'patch', body)
        return res
    #PATCH 後台刪除標籤群組
    def delete_tagGroup(self, tag_id, header):
        api_name = "/api/v2/backend/tagGroup/" + str(tag_id)
        res = api.apiFunction(self.prefix, header, api_name, 'delete', None)
        return res



class TestTagGroup():
    env = 'QA2'
    test_parameter = {}
    initdata.set_test_data(env, test_parameter)
    tagGP = TagGroup()
    tagGP.test_parameter = test_parameter
    tagGP.prefix = test_parameter['prefix']
    tagGp_idList = []

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass
        # sql_list =["DELETE FROM tag_group WHERE label like '%標籤群組'"]
        # dbConnect.dbSetting(cls.test_parameter['db'], sql_list, 'shocklee')

    test_create_tagGroup=[
         #                  scenario,                   token,                   nonce,             label, group_type,  expected
        (           'backend query' ,         'backend_token',         'backend_nonce',    '第一組標籤群組',     'user',        2),
        (          'backend query2' ,         'backend_token',         'backend_nonce',    '第二組標籤群組',   'custom',        2),
        (    'liveController query' , 'liveController1_token', 'liveController1_nonce',    '第三組標籤群組',   'custom',        2),
        ('LACK_OF_NECESSARY_PARAMS' ,         'backend_token',         'backend_nonce',  '缺乏參數標籤群組',         '',        4),
        (              'auth error' ,             'err_token',             'err_nonce',  '權限錯誤標籤群組',      'user',       4),
    ]

    @pytest.mark.parametrize("scenario, token, nonce, label, group_type,  expected", test_create_tagGroup)
    def test_backend_create_tagGroup(self, scenario, token, nonce, label, group_type,  expected):
        header = self.tagGP.set_header(token, nonce)
        res = self.tagGP.create_tagGroup(label, group_type, header)
        assert res.status_code // 100 == expected
        if expected == 2:
            restext = json.loads(res.text)
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
        else:
            restext = json.loads(res.text)
            if scenario == 'LACK_OF_NECESSARY_PARAMS':
                assert res.status_code == 400
            elif scenario == 'auth error':
                assert res.status_code == 401

    test_read_tagGroup_list=[
         #                  scenario,               token,                    nonce,    typeFilter,    item, page, expected
        (   'backend_userFilter' ,         'backend_token',         'backend_nonce',        'user',       2,     1,   2),
        ( 'controller_allFilter' , 'liveController1_token', 'liveController1_nonce',          None,       3,     1,   2),
        (   'backend_full_query' ,         'backend_token',         'backend_nonce',          None,    None,  None,   2),
        (           'auth error' ,             'err_token',             'err_nonce',        'user',       3,     1,   4),
    ]

    @pytest.mark.parametrize("scenario, token, nonce, typeFilter, item, page, expected", test_read_tagGroup_list)
    def test_backend_read_tagGroup_list(self, scenario, token, nonce, typeFilter, item, page, expected):
        header = self.tagGP.set_header(token, nonce)
        res = self.tagGP.read_tagGroup_list(header,typeFilter=typeFilter, item=item, page=page)
        assert res.status_code // 100 == expected
        if expected == 2:
            restext = json.loads(res.text)
            count = len(restext['data'])
            if item is not None:  assert count <= item
            if scenario == 'backend_userFilter':
                assert restext['data'][0]['type'] == 'user'
                assert restext['data'][0]['label'] == '第一組標籤群組'
            elif scenario == 'controller_allFilter':
                assert restext['data'][0]['type'] == 'custom'
                assert restext['data'][0]['label'] == '第三組標籤群組'
            assert restext['data'][0]['id'] > restext['data'][1]['id']
            assert restext['totalCount'] != None
            #尋找 label 帶有標籤 文字
            if scenario == 'backend_full_query':
                TestTagGroup.tagGp_idList = [restext['data'][i]['id'] for i in range(count) if restext['data'][i]['label'].find('標籤群組') != -1 ]
                print(self.__class__.tagGp_idList)
        else:
            restext = json.loads(res.text)
            pprint(restext)
            assert res.status_code == 401

    edit_tagGroup_data=[
    #                    scenario,                   token,                   nonce,tag_gp_index,          label,   group_type,  expected
       (      'backend_edit_full',         'backend_token',         'backend_nonce',           0, '修改第三組標籤群組',  'custom',        2),
       ( 'controller_edit_gpType', 'liveController1_token', 'liveController1_nonce',           1,              None,    'user',        2),
       (  'controller_edit_label', 'liveController1_token', 'liveController1_nonce',           2, '修改第一組標籤群組',      None,        2),
       (            'auth error' ,             'err_token',             'err_nonce',           0,   '錯誤驗證標籤群組',    'user',        4),
    ]
    @pytest.mark.parametrize("scenario, token, nonce, index, label, group_type, expected", edit_tagGroup_data)
    def test_edit_tagGroup(self, scenario, token, nonce, index, label, group_type, expected):
        tag_group_id = TestTagGroup.tagGp_idList[index]
        header = self.tagGP.set_header(token, nonce)
        res = self.tagGP.edit_tagGroup(tag_group_id, label, group_type, header)
        assert res.status_code // 100 == expected
        if expected == 2:
            restext = json.loads(res.text)
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
            sql_str = 'select label, group_type from tag_group where id={}'.format(tag_group_id)
            [(result_label, result_group_type)] = dbConnect.dbQuery(TestTagGroup.test_parameter['db'], sql_str, 'shocklee')
            if scenario == 'backend_edit_full':
                assert result_label == '修改第三組標籤群組'
                assert result_group_type == 'custom'
            elif scenario == 'controller_edit_gpType':
                #因為第二組標籤群組的label沒修改，所以還是 '第二組標籤群組'
                assert result_label == '第二組標籤群組'
                assert result_group_type == 'user'
            else:
                #因為第一組標籤群組的 group_type 沒修改，所以還是 'user'
                assert result_label == '修改第一組標籤群組'
                assert result_group_type == 'user'
        else:
            assert res.status_code == 401


    delete_tagGroup=[
        #                        scenario,                   token,                   nonce,       tag_index,   expected
        (                 'backend query',         'backend_token',         'backend_nonce',               0,       2),
        (         'liveController1_query', 'liveController1_token', 'liveController1_nonce',               1,       2),
        (                 'backend query',         'backend_token',         'backend_nonce',               2,       2),
        (         'TagGroup_Id_Not_Found',            'user_token',            'user_nonce',               0,       4),
        (                    'Auth Error',             'err_token',             'err_nonce',               0,       4),
    ]

    #PATCH 後台刪除群組
    @pytest.mark.parametrize("scenario, token, nonce, tag_index, expected", delete_tagGroup)
    def test_delete_tag(self, scenario, token, nonce, tag_index, expected):
        tag_group_id = TestTagGroup.tagGp_idList[tag_index]
        if expected == 2 :
            #先使用後台權限新增兩個tag 並新增至目前的 tagGroup
            header = self.tagGP.set_header('backend_token',  'backend_nonce')
            tagNameA = "TestTagA_" + str(tag_group_id)
            tagNameB = "TestTagB_" + str(tag_group_id)
            tag = Tag()
            tag.prefix = TestTagGroup.tagGP.prefix
            tag.create_tag(tagNameA, "#FFFFFF", "user", [tag_group_id], header)
            tag.create_tag(tagNameB, "#FFFFFF", "user", [tag_group_id], header)
            #產生 tab settings 關係
            tab = TabSetting()
            tab.prefix = TestTagGroup.tagGP.prefix
            tplate_name = "tmplt"+ str(tag_group_id)
            tabPara =  ( {"groupId":  tag_group_id,"order": 1,"template": tplate_name} , {"groupId": tag_group_id,"order": 2,"template": tplate_name})
            tab.create_tab(header, tabPara)
        ###
        header = self.tagGP.set_header(token, nonce)
        if scenario == 'TagGroup_Id_Not_Found':
            tag_group_id == 9999999
        res = self.tagGP.delete_tagGroup(tag_group_id, header)
        assert res.status_code // 100 == expected
        restext = json.loads(res.text)
        if expected == 2:
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
            #檢查 tag 的關係解除了沒
            sql_str = "select count(*) from tag_group \
                    right join tag_association on tag_group.id=tag_association.group_id \
                    where tag_association.group_id={}".format(tag_group_id)
            [(result_count),] = dbConnect.dbQuery(TestTagGroup.test_parameter['db'], sql_str, 'shocklee')
            assert result_count == 0
            #檢查 tab settings 的關係解除了沒
            sql_str = "select tag_group_id from tab_setting where template = '{}' limit 2".format(tplate_name)
            [(result1, result2),] = dbConnect.dbQuery(TestTagGroup.test_parameter['db'], sql_str, 'shocklee')
            assert result1 == None and result2 == None
        else:
            print(restext)
            if scenario == 'Auth Error':
                assert res.status_code == 401
            elif scenario == 'Tag_Id_Not_Found':
                assert res.status_code == 400