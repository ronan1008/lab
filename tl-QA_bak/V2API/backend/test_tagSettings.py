#Milestone28.[首頁改版] 後台新增標籤 (Tag)：POST /v2/backend/tag #1759
#Milestone28.[首頁改版] 後台編輯標籤 (Tag)：PATCH /v2/backend/tag/{{tag_id}} #1760
#Milestone28.[首頁改版] 後台撈取標籤列表 (Tag)：GET /v2/backend/tag/list #1761
#Milestone29.[首頁改版] 後台刪除標籤 (Tag)：DELETE /v2/backend/tag/{{tag_id}} #1908
import json
import requests
import pytest
from assistence import api
from assistence import initdata
from assistence import dbConnect
from pprint import pprint
# pylint: disable=unbalanced-tuple-unpacking
class Tag():

    def __init__(self):
        self.test_parameter = {}
        self.prefix = ''

    def set_header(self, token, nonce):
        header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
        header['Content-Type'] = 'application/json'
        header['X-Auth-Token'] = self.test_parameter[token]
        header['X-Auth-Nonce'] = self.test_parameter[nonce]
        return header

    #POST 後台新增標籤
    def create_tag(self, label, color ,tag_type, groupId:list, header):
        api_name = "/api/v2/backend/tag"
        body = {'label': label,
                'color': color,
                'type': tag_type,
                'groupId': groupId
        }
        body = {key : val for key,val in  body.items() if val is not None}
        res = api.apiFunction(self.prefix, header, api_name, 'post',body)
        return res

    #GET 後台撈取標籤列表 groupFilter typeFilter item page
    def read_tag_list(self, header, **kwargs):
        api_name = "/api/v2/backend/tag/list"
        api_name = api.dict_to_url_get(api_name, kwargs)
        res = api.apiFunction(self.prefix, header, api_name, 'get', None)
        return res

    #PATCH 後台編輯標籤
    def update_tag(self, tag_id, label, color ,tag_type, groupId:list, header):
        api_name = "/api/v2/backend/tag/" + str(tag_id)
        body = {'label': label,
                'color': color,
                'type': tag_type,
                'groupId': groupId
        }
        body = {key : val for key,val in  body.items() if val != '' and val is not None}
        res = api.apiFunction(self.prefix, header, api_name, 'patch', body)
        return res

    #PATCH 後台刪除標籤
    def delete_tag(self, tag_id, header):
        api_name = "/api/v2/backend/tag/" + str(tag_id)
        res = api.apiFunction(self.prefix, header, api_name, 'delete', None)
        return res

class TestTag():
    env = 'QA2'
    test_parameter = {}
    initdata.set_test_data(env, test_parameter)
    tag = Tag()
    tag.test_parameter = test_parameter
    tag.prefix = test_parameter['prefix']
    tag_id_list = []
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    create_tag_data=[
        #                scenario,                   token,                   nonce,             label,          color, tag_type, groupId, expected
        (      'backend_all_1gId',         'backend_token',         'backend_nonce',    '測試二次元標籤',      '#C9C9C9',   'user',       [1],    2),
        (      'backend_all_4gId',         'backend_token',         'backend_nonce',      '測試狀元標籤',      '#A8A8A8',   'user',        [],    2),
        ( 'controller_no_groupId', 'liveController1_token', 'liveController1_nonce',      '測試新秀標籤',      '#D9D9D9', 'custom',      None,    2),
        ( 'backend_empty_groupId',         'backend_token',         'backend_nonce',      '測試女神標籤',      '#FFFFFF',   'user', [1,2,3,4],    2),
        (      'Lack Of Tag Type',         'backend_token',         'backend_nonce',      '缺乏type標籤',      '#E9E9E9',     None,      [1],    4),
        (         'Lack Of Label',         'backend_token',         'backend_nonce',              None,      '#E9E9E9',      None,      [1],    4),
        (       'Group Not Found',         'backend_token',         'backend_nonce',      '錯誤群組標籤',      '#E9E9E9',   'user', [1,9999],    4),
        (            'Auth Error',             'err_token',             'err_nonce',      '權限錯誤標籤',      '#E9E9E9',   'user',      [],    4),
    ]
#    @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.parametrize("scenario, token, nonce, label, color ,tag_type, groupId, expected", create_tag_data)
    def test_create_tag(self, scenario, token, nonce, label, color ,tag_type, groupId:list, expected):
        header = self.tag.set_header(token, nonce)
        res = self.tag.create_tag(label, color ,tag_type, groupId, header)
        assert res.status_code // 100 == expected
        if expected == 2:
            restext = json.loads(res.text)
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
            res = self.tag.read_tag_list(header, groupFilter='', typeFilter=tag_type, item=10, page=1)
            restext = json.loads(res.text)
            assert restext['data'][0]['label'] == label
            assert restext['data'][0]['type'] == tag_type
            assert restext['data'][0]['color'] == color
            if groupId:
                assert [ restext['data'][0]['groups'][i]['id'] for i in range(len(groupId)) ] == groupId
            else:
                assert len(restext['data'][0]['groups']) == 0
            TestTag.tag_id_list.append(restext['data'][0]['id'])
        else:
            if scenario.find('Lack Of') != -1 or scenario == 'Group Not Found':
                assert res.status_code == 400
            elif scenario == 'Auth Error':
                assert res.status_code == 401

    update_tag_data=[
        #                     scenario,                   token,                   nonce, tag_index,            label,         color, tag_type, groupId, expected
        (           'backend_edit_all',         'backend_token',         'backend_nonce',         0,    '修改二次元標籤',     '#AAAAAA',   'user',      [4,5],    2),
        ('backend_edit_all_no_groupId',         'backend_token',         'backend_nonce',         1,      '修改狀元標籤',     '#AAAAAA',   'user',       None,    2),
        ('backend_edit_all_no_tagType',         'backend_token',         'backend_nonce',         2,      '修改新秀標籤',     '#AAAAAA',     None,      [2,3],    2),
        (   'controller clear groupId', 'liveController1_token', 'liveController1_nonce',         3,              None,          None, 'custom',         [],    2),
        (         'Tag Type Not Found',         'backend_token',         'backend_nonce',         0,              None,          None,  'admin',       None,   4),
        (           'Tag Id Not Found',         'backend_token',         'backend_nonce',         1,    '錯誤群組ID標籤',      '#E9E9E9',  'user',     [2,99],    4),
        (                 'Auth Error',            'err_token',              'err_nonce',         2,      '權限錯誤標籤',      '#E9E9E9',   'user',       [3],    4),
    ]
    #PATCH 後台編輯標籤
#    @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.parametrize("scenario, token, nonce, tag_index, label, color ,tag_type, groupId, expected", update_tag_data)
    def test_update_tag(self, scenario, token, nonce, tag_index, label, color ,tag_type, groupId:list, expected):
        tag_id = TestTag.tag_id_list[tag_index]
        header = self.tag.set_header(token, nonce)
        if scenario == 'Tag Id Not Found':
            tag_id=999999
        res = self.tag.update_tag(tag_id, label, color ,tag_type, groupId, header)
        assert res.status_code // 100 == expected
        if expected == 2:
            restext = json.loads(res.text)
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
            res = self.tag.read_tag_list(header, groupFilter='', typeFilter='', item=5, page=1)
            restext = json.loads(res.text)
            if scenario == 'backend_edit_all':
                assert restext['data'][3]['label'] == label
                assert restext['data'][3]['color'] == color
                assert restext['data'][3]['type'] == tag_type
                assert restext['data'][3]['groups'][0]['id'] == 4 and restext['data'][3]['groups'][1]['id'] == 5
            elif scenario == 'backend_edit_all_no_groupId':
                assert restext['data'][2]['label'] == label
                assert restext['data'][2]['color'] == color
                assert restext['data'][2]['type'] == tag_type
                assert len(restext['data'][2]['groups']) == 0  #規格上說明  當 groupId 這個 key 沒帶入 視同 把關係砍掉
            elif scenario == 'backend_edit_all_no_tagType':
                assert restext['data'][1]['label'] == label
                assert restext['data'][1]['color'] == color
                assert restext['data'][1]['type'] == 'custom'
                assert restext['data'][1]['groups'][0]['id'] == 2 and restext['data'][1]['groups'][1]['id'] == 3
                print(restext['data'][1]['groups'][0])
            elif scenario == 'controller clear groupId':
                assert restext['data'][0]['label'] == '測試女神標籤'
                assert restext['data'][0]['color'] == '#FFFFFF'
                assert restext['data'][0]['type'] == 'custom'
                assert len(restext['data'][0]['groups']) == 0 #空陣列也是 視同 把關係砍掉
        else:
            if scenario.find('Lack Of') != -1 or scenario.find('Not Found') != -1:
                assert res.status_code == 400
            elif scenario == 'Auth Error':
                assert res.status_code == 401

    read_tag_list_data=[
        #                        scenario,                   token,                   nonce,     groupFilter,        typeFilter,          item,     page,   expected
        (             'backend no filter',         'backend_token',         'backend_nonce',            None,              None,          None,     None,       2),
        (   'controller_typeFilter_2item', 'liveController1_token', 'liveController1_nonce',            None,          'custom',             2,        1,       2),
        ('backend_group&typeFilter_1item',         'backend_token',         'backend_nonce',               1,            'user',            10,     None,       2),
        (               'user Auth Error',            'user_token',            'user_nonce',               2,            'user',             1,   'user',       4),
        (                    'Auth Error',             'err_token',             'err_nonce',               1,            'user',             1,   'user',       4),
    ]
#    @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.parametrize("scenario, token, nonce, groupFilter, typeFilter, item, page, expected", read_tag_list_data)
    def test_read_tag_list(self, scenario, token, nonce, groupFilter, typeFilter, item, page, expected):
        header = self.tag.set_header(token, nonce)
        res = self.tag.read_tag_list(header, groupFilter=groupFilter, typeFilter=typeFilter, item=item, page=page)
        assert res.status_code // 100 == expected
        if expected == 2:
            restext = json.loads(res.text)
            #pprint(restext)
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS' and restext['totalCount'] != None
            assert all([ x in restext['data'][0] for x in ['id', 'label', 'color', 'type', 'groups']]) == True
            if restext['data'][0]['groups']:
                assert all([ x in restext['data'][0]['groups'][0] for x in ['id', 'label', 'type']]) == True
            if scenario == 'backend no filter':
                sql = "select count(*) from tag"
                [(db_count,)] = dbConnect.dbQuery(TestTag.test_parameter['db'], sql , 'shocklee')
            elif scenario == 'controller_typeFilter_2item':
                sql ="select count(*) from tag where tag_type='{}'".format(typeFilter)
                [(db_count,)] = dbConnect.dbQuery(TestTag.test_parameter['db'], sql , 'shocklee')
                assert len(restext['data']) <= item
                assert all( [ restext['data'][i]['type'] == typeFilter for i in range(len(restext['data'])) ]) == True
            elif scenario == 'backend_group&typeFilter_1item':
                sql ="select count(*) from tag where tag_type='{}'  and id in ( select tag_id from tag_association where group_id={})".format(typeFilter, groupFilter)
                [(db_count,)] = dbConnect.dbQuery(TestTag.test_parameter['db'], sql , 'shocklee')
                assert all( [ restext['data'][i]['type'] == typeFilter for i in range(len(restext['data'])) ]) == True
                assert all( [ restext['data'][i]['groups'][0]['id'] == groupFilter for i in range(len(restext['data'])) ]) == True

            assert db_count == restext['totalCount']

        else:
            if scenario == 'Auth Error':
                assert res.status_code == 401

    delete_tag=[
        #                        scenario,                   token,                   nonce,       tag_index,   expected
        (                 'backend query',         'backend_token',         'backend_nonce',               0,       2),
        (         'liveController1_query', 'liveController1_token', 'liveController1_nonce',               1,       2),
        (                 'backend query',         'backend_token',         'backend_nonce',               2,       2),
        (              'Tag_Id_Not_Found',            'user_token',            'user_nonce',               0,       4),
        (                    'Auth Error',             'err_token',             'err_nonce',               0,       4),
    ]

    #PATCH 後台刪除標籤
    @pytest.mark.parametrize("scenario, token, nonce, tag_index, expected", delete_tag)
    def test_delete_tag(self, scenario, token, nonce, tag_index, expected):
        header = self.tag.set_header(token, nonce)
        tag_id = TestTag.tag_id_list[tag_index]
        #刪除該 tag id 指定給 identity 的所有相關聯。
        #為了測試插入一個sql，新增 identity 與 tag 的關係，等待之後刪除，關係應該被解開
        sql = ["Insert into identity_tag_association (identity_id, tag_id) Values ('83d5543d-586c-4824-8a0e-5b52d57e1f39', {})".format(tag_id)]
        dbConnect.dbSetting(TestTag.test_parameter['db'], sql, 'shocklee')
        if scenario == 'Tag_Id_Not_Found':
            tag_id == 9999999
        res = self.tag.delete_tag(tag_id, header)
        assert res.status_code // 100 == expected
        restext = json.loads(res.text)
        if expected == 2:
            #斷開其 id 在 tag_association table 中所有與其相關的 tag Group之關聯
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
            sql = "select count(*) from tag left join tag_association on tag.id = tag_association.tag_id where tag.id ={}".format(tag_id)
            [(tag_tagourp_assoc,)] = dbConnect.dbQuery(TestTag.test_parameter['db'], sql , 'shocklee')
            assert tag_tagourp_assoc == 0
            #刪除該 tag id 指定給 identity 的所有相關聯。也就是希望原本有貼上這標籤的直播主，通通刪掉這層標籤
            sql = "select count(*) from identity_tag_association left join tag on identity_tag_association.tag_id = tag.id where tag.id={}".format(tag_id)
            [(identity_tag_assoc,)] = dbConnect.dbQuery(TestTag.test_parameter['db'], sql , 'shocklee')
            assert identity_tag_assoc == 0
        else:
            print(restext)
            if scenario == 'Auth Error':
                assert res.status_code == 401
            elif scenario == 'Tag_Id_Not_Found':
                assert res.status_code == 400