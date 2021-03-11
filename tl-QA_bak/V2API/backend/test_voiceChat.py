# Milestone 28. [VoiceChat 聲聊] 後台建立聲聊房：POST /v2/backend/voiceChat #1716
# Milestone 28. [VoiceChat 聲聊] 後台編輯聲聊房：PATCH /v2/backend/voiceChat/{{voice_chat_id}} #1718
# pylint: disable=unbalanced-tuple-unpacking
import json
import requests
import pytest
import datetime
from assistence import api
from assistence import initdata
from assistence import dbConnect
from pprint import pprint

class VoiceChat:
    def __init__(self):
        self.test_parameter = {}
        self.prefix = ''

    def set_header(self, token, nonce):
        self.header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
        self.header['Content-Type'] = 'application/json'
        self.header['X-Auth-Token'] = self.test_parameter[token]
        self.header['X-Auth-Nonce'] = self.test_parameter[nonce]
        return self.header

    # [( "voiceChat_1_1","voiceChat_1_2","voiceChat_1_13" ) , ( "voiceChat_1_1","voiceChat_1_2","voiceChat_1_13" )]
    def create_voiceChat(self, header, typeId, masterId, title, description, password, streamId:list):
        api_name = "/api/v2/backend/voiceChat"
        body = {'typeId': typeId,
                'masterId': masterId,
                'title': title,
                'description': description,
                'password':  password,
                'streamId': [s for s in streamId] if streamId else None
        }
        body = {key : val for key, val in  body.items() if val != None }
        res = api.apiFunction(self.prefix, header, api_name, 'post', body)
        return res

    def update_voiceChat(self, header, voice_chat_id, typeId, masterId, title, description, password, streamId:list):
        api_name = "/api/v2/backend/voiceChat/" + str(voice_chat_id)
        body = {'typeId': typeId,
                'masterId': masterId,
                'title': title,
                'description': description,
                'password':  password,
                'streamId': [s for s in streamId] if streamId else None
        }
        body = {key : val for key, val in  body.items() if val != None }
        res = api.apiFunction(self.prefix, header, api_name, 'patch', body)
        return res

class TestVoiceChat():
    env = 'QA2'
    test_parameter = {}
    initdata.set_test_data(env, test_parameter)
    vc = VoiceChat()
    vc.test_parameter = test_parameter
    vc.prefix = test_parameter['prefix']

    header = vc.set_header('backend_token', 'backend_nonce')
    broadcaster_Ids = []
    broadcaster_Ids.append( api.search_user(test_parameter['prefix'], "broadcaster005", header) )
    broadcaster_Ids.append( api.search_user(test_parameter['prefix'], "broadcaster006", header) )
    broadcaster_Ids.append( api.search_user(test_parameter['prefix'], "broadcaster007", header) )
    VC_Ids = []
    origin_pass = ''

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    streamIds = [
        ( "voiceChat_1_1", "voiceChat_1_2"),
        ( "voiceChat_2_1", "voiceChat_2_2", "voiceChat_2_3", "voiceChat_2_4"),
        ( "voiceChat_3_1", "voiceChat_3_2", "voiceChat_3_3", "voiceChat_3_4", "voiceChat_3_5" , "voiceChat_3_6" ),
    ]

    create_voiceChat_data=[
        #          scenario,                   token,                   nonce,  typeId(R),        masterId(R),   title(R),  description, password, expected, streamId
        (  'filled all args',         'backend_token',         'backend_nonce',         1, broadcaster_Ids[0], '第1間測試', '2020年第一次', '123456',       2, streamIds[2]),
        ( 'only no password',         'backend_token',         'backend_nonce',         2, broadcaster_Ids[1], '第2間測試', '2020年第二次',     None,       2, streamIds[1]),
        ('just require args',         'backend_token',         'backend_nonce',         3, broadcaster_Ids[2], '第3間測試',          None,     None,       2,        None),

        ( 'Lack Of masterId',         'backend_token',         'backend_nonce',         4,               None, '第4間聲聊', '2020年第三次', '123456',       4, streamIds[1]),
        (    'Lack Of title',         'backend_token',         'backend_nonce',         5, broadcaster_Ids[0],       None, '2020年第四次', '123456',       4, streamIds[1]),
        (       'Auth Error',             'err_token',             'err_nonce',         6, broadcaster_Ids[0], '第5間聲聊', '2020年第五次', '123456',       4, streamIds[1]),
    ]

    @pytest.mark.parametrize(      "scenario, token, nonce, typeId, masterId, title, description, password, expected, streamId", create_voiceChat_data)
    def test_create_voiceChat(self, scenario, token, nonce, typeId, masterId, title, description, password, expected, streamId):
        if title is not None:
            n_dt = datetime.datetime.now()
            title = title + str(n_dt)
        header = self.vc.set_header(token, nonce)
        res = self.vc.create_voiceChat(header, typeId, masterId, title, description, password, streamId)
        assert res.status_code // 100 == expected
        if expected == 2:
            restext = json.loads(res.text)
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
            sqlStr = "select vcr.id, vcr.description,vcr.password, vcr.title ,vcr.master_id, vct.id  \
                    from voice_chat_room as vcr \
                    join voice_chat_type as vct on vcr.type_id = vct.id \
                    where vcr.title='{}'".format(title)
            [(rid, rdes, rpass, rtitle, rmasId, rtype)] = dbConnect.dbQuery(TestVoiceChat.test_parameter['db'], sqlStr , 'shocklee')
            print((rid, rdes, rpass, rtitle, rmasId, rtype))
            sqlStr = "select voice_chat_stream.stream from voice_chat_stream \
                    join voice_chat_room on voice_chat_stream.voice_chat_room_id = voice_chat_room.id \
                    where voice_chat_room.title = '{}'".format(title)
            result = dbConnect.dbQuery(TestVoiceChat.test_parameter['db'], sqlStr , 'shocklee')
            result_stream = []
            for i in result:
                (x,) = i
                result_stream.append(x)
            result_stream = tuple(result_stream)
            assert rtype == typeId
            assert rtitle == title
            assert rmasId == masterId
            if scenario == 'filled all args':
                assert rpass != None
                assert result_stream == streamId
                assert rdes == description
                TestVoiceChat.origin_pass = rpass
            elif scenario == 'only no password':
                assert result_stream == streamId
                assert rpass == None
            TestVoiceChat.VC_Ids.append(rid)
        else:
            if scenario.find('Lack Of') != -1 :
                assert res.status_code == 400
            else:
                assert res.status_code == 401


    edit_streamIds = [
        ( "voiceChat_4_1", ),
        ( "voiceChat_5_1", "voiceChat_5_2", "voiceChat_5_3"),
        ( "voiceChat_6_1", "voiceChat_6_2", "voiceChat_6_3", "voiceChat_6_4", "voiceChat_6_5" ),
    ]

    edit_voiceChat_data=[
        #                           scenario,                   token,                   nonce,  vc_index,     typeId,           masterId,         title,   description, password, expected, streamIds
        ('change all columns no change pass',         'backend_token',         'backend_nonce',         0,          3, broadcaster_Ids[0], '編輯第1間聲聊', '編輯標題第一次',     None,       2, edit_streamIds[2]),
        (     'change all columns need pass',         'backend_token',         'backend_nonce',         1,          2, broadcaster_Ids[0], '編輯第2間聲聊', '編輯標題第二次', '123456',       2, edit_streamIds[1]),
        ('change require args still no pass',         'backend_token',         'backend_nonce',         2,          1, broadcaster_Ids[1], '編輯第3間聲聊',           None,     None,       2,              None),

        (                 'Lack Of masterId',         'backend_token',         'backend_nonce',         0,         4,                None,    '第4間聲聊',  '編輯標題第四次',     '123456',       4, edit_streamIds[1]),
        (                    'Lack Of title',         'backend_token',         'backend_nonce',         1,         5,  broadcaster_Ids[0],          None,  '編輯標題第五次',     '123456',       4, edit_streamIds[1]),
        (                       'Auth Error',             'err_token',             'err_nonce',         2,         6,  broadcaster_Ids[0],            '',  '編輯標題第六次',     '123456',       4, edit_streamIds[1]),
        (                   'Room Not Found',         'backend_token',         'backend_nonce',         0,          3, broadcaster_Ids[0], '編輯第1間聲聊2', '編輯標題第一次2',    '123456',       4, edit_streamIds[2]),
    ]

    @pytest.mark.parametrize(      "scenario, token, nonce, vc_index, typeId, masterId, title, description, password, expected, streamIds", edit_voiceChat_data)
    def test_update_voiceChat(self, scenario, token, nonce, vc_index, typeId, masterId, title, description, password, expected, streamIds):
        if title is not None:
            n_dt = datetime.datetime.now()
            title = title + str(n_dt)
        voice_chat_id = TestVoiceChat.VC_Ids[vc_index]
        if scenario == 'Room Not Found':
            voice_chat_id = 9999999
        header = self.vc.set_header(token, nonce)
        res = self.vc.update_voiceChat(header, voice_chat_id, typeId, masterId, title, description, password, streamIds)
        assert res.status_code // 100 == expected
        if expected == 2:
            restext = json.loads(res.text)
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
            sqlStr = "select vcr.id, vcr.description,vcr.password, vcr.title ,vcr.master_id, vct.id  \
                    from voice_chat_room as vcr \
                    join voice_chat_type as vct on vcr.type_id = vct.id \
                    where vcr.title='{}'".format(title)
            [(rid, rdes, rpass, rtitle, rmasId, rtype)] = dbConnect.dbQuery(TestVoiceChat.test_parameter['db'], sqlStr , 'shocklee')
            print((rid, rdes, rpass, rtitle, rmasId, rtype))
            sqlStr = "select voice_chat_stream.stream from voice_chat_stream \
                    join voice_chat_room on voice_chat_stream.voice_chat_room_id = voice_chat_room.id \
                    where voice_chat_room.title = '{}'".format(title)
            result = dbConnect.dbQuery(TestVoiceChat.test_parameter['db'], sqlStr , 'shocklee')
            result_stream = []
            for i in result:
                (x,) = i
                result_stream.append(x)
            result_stream = tuple(result_stream) if result_stream !=[] else None
            assert rdes == description
            assert rtitle == title
            assert rmasId == masterId
            assert rtype == typeId
            assert result_stream == streamIds
            if scenario == 'change all columns no change pass':
                assert rpass == TestVoiceChat.origin_pass
            elif scenario == 'change require args still no pass':
                assert rpass == None
        else:
            if scenario.find('Lack Of') != -1 :
                assert res.status_code == 400
            elif scenario == 'Room Not Found':
                assert res.status_code == 404
            else:
                assert res.status_code == 401
