# -*- coding: UTF-8 -*-
# encoding: utf-8
#mileston25 #1465 POST  /v2/liveMaster/zego/liveRoom  #1466 PATCH /v2/liveMaster/zego/liveRoom  #1467 SOCKET IN_ROOM
import json
import requests
import pytest
import socket
from assistence import api
from assistence import initdata
from assistence import dbConnect
from assistence import chatlib
from pprint import pprint

class openRoom:
    def __init__(self):
        env = 'QA2'
        test_parameter = {}
        initdata.set_test_data(env, test_parameter)
        self.test_parameter = test_parameter
        self.header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
        self.header['X-Auth-Token'] = test_parameter['broadcaster_token']
        self.header['X-Auth-Nonce'] = test_parameter['broadcaster_nonce']
        self.header['Content-Type'] = 'application/json'
        self.api_name=''
        self.zegoInfo = []
        self.room_id = ''
        self.sock_status = ''
        self.output = ''

    '''開啟 zego room'''
    def open_zego(self, title, description):
        self.api_name = "/api/v2/liveMaster/zego/liveRoom"
        body = {
         "title": title,
         "description": description,
        }
        res = api.apiFunction(self.test_parameter['prefix'], self.header, self.api_name, 'post', body)
        return res

    '''得到 socket'''
    def get_sock_connect(self):
        sockinfo = api.get_load_balance(self.test_parameter['prefix'], self.header)
        sip = sockinfo['socketIp']
        sport = int(sockinfo['socketPort'])
        self.sock_status = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (sip, sport)
        self.sock_status.connect(server_address)
        return self.sock_status

    '''驗證'''
    def chat_room_auth(self, sock):
        chatlib.chat_room_auth(sock, self.header)

    '''進入 zego 聊天室'''
    def enter_zego(self, sock, roomId):
        strList = []
        isContinue = True
        new = {'action': 'ENTER_ZEGO_ROOM', 'data': {'roomId': roomId}}
        new_json = json.dumps(new) + '\n'
        sock.send(new_json.encode('utf-8'))
        sock.recv(2048).decode('utf-8', errors='ignore')
        while isContinue:
            check = chatlib.check_event(sock)
            strList = check[1].split('\n')
            #pprint(strList)
            for i in strList:
                if len(i)  > 0:
                    check1 = json.loads(i)
                    pprint(check1)
                    if check1['event'] == 'ROOM_IN':
                        #pprint('ROOM_in: %s'%check1['data'])
                        self.output = check1['data']
                        roomId = check1['data']['roomId']
                        isContinue = False
        return roomId
    '''更新聊天室簡介'''
    def update_room_desc(self, roomId, descriptions):
        self.api_name = "/api/v2/liveMaster/zego/liveRoom/" + str(roomId)
        body = {
         "description": descriptions,
        }
        res = api.apiFunction(self.test_parameter['prefix'], self.header, self.api_name, 'patch', body)
        return res

    '''離開聊天室'''
    def leave_room(self, roomId, sock):
        chatlib.leave_room(roomId, sock)

class TestOpenRoom:
    wordover200 = "使用 Apple Macbook 或 Mac 的用戶如果要使用 Windows 10 系統，那麼需要通過 Boot Camp 在 MacOS 上進行使用，用戶只需下載普通的 Windows 10 操作系統安裝包即可。 但 Apple 近日宣布推出 ARM 架構的自研處理器替代 intel 處理器，這將導致所有 Apple Mac 設備無法正常安裝 Windows 10 系統，需要 Microsoft"
    spaceDescWord200 = "   對於蘋果即將推出的iPhone 12型號，國外多個科技網站及爆料達人已經給出了完整的資訊，但尚缺官方證實，新機上市時間也眾說紛紜。不過，跨國電信公司T-Mobile在官網上率先曝光了專為iPhone 12系列打造的透明手機套，外界估計，這可能意味著新機將在9月如期亮相！T-Mobile的荷蘭官網顯示iPhone將有iPhone 12、iPhone 12 Pro、iPhone 12 Pro Max。"
    descWord200 = spaceDescWord200.strip()
    test_room_data = [
        #       scenario,                       title,             desc,   expectDesc
        (   'content is 200',             '剛好200個字',  spaceDescWord200,        descWord200),
        ( 'content over 200',                '超過200',       wordover200,                  ''),
        (    'space content',              '空白的敘述',  '    字數計算器  ',         '字數計算器'),
        (            'emoji',           'Emoji Title','😊每天都🦦好開心🥵', '😊每天都🦦好開心🥵')
    ]

    test_desc_data = [
        #           scenario,                 token,              nonce,                        desc,             expectDesc
        (         'standard',   'broadcaster_token',     'broadcaster_nonce',                   '短',                    '短'),
        ( 'content over 200',   'broadcaster_token',     'broadcaster_nonce',            wordover200,                     ''),
        (    'space content',   'broadcaster_token',     'broadcaster_nonce',            '    最後  ',                 '最後'),
        (            'emoji',   'broadcaster_token',     'broadcaster_nonce', '🍥🐚🐲笑臉迎人🧆🌯🌅', '🍥🐚🐲笑臉迎人🧆🌯🌅'),
        ( 'other livemaster',  'broadcaster1_token',     'broadcaster1_nonce',            '其他直播主',                     ''),
        (     'author error',           'err_token',             'err_nonce',              '錯誤認證',                      ''),
    ]

    def setup_class(self):
        self.chat_room = openRoom()

    def teardown_class(self):
        sock= self.chat_room.sock_status
        self.chat_room.leave_room(self.chat_room.room_id, sock)
        print("leaving...........")

    @pytest.mark.parametrize("scenario, title, desc, expectDesc", test_room_data)
    def test_open_zego_room(self, scenario, title, desc, expectDesc):
        res = self.chat_room.open_zego(title, desc)
        result = json.loads(res.text)
        if scenario == 'content over 200':
            assert res.status_code == 400
            assert result['Message'] == 'CONTENT_TOO_LONG'
        else :
            assert res.status_code == 200
            assert result['data']['roomId'] == result['data']['streamId']
            self.chat_room.room_id = result['data']['roomId']
            sock= self.chat_room.get_sock_connect()
            self.chat_room.chat_room_auth(sock)
            self.chat_room.enter_zego(sock, self.chat_room.room_id)
            assert self.chat_room.output['title'] == title
            assert self.chat_room.output['description'] == expectDesc
            pprint(self.chat_room.output)
            assert  self.chat_room.output['roomId'] == self.chat_room.output['streamId']
            #print(expectDesc)

    #@pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.parametrize("scenario, token, nonce, desc, expectDesc", test_desc_data)
    def test_update_room_desc(self, scenario, token, nonce, desc, expectDesc):
        self.chat_room.header['X-Auth-Token'] = self.chat_room.test_parameter[token]
        self.chat_room.header['X-Auth-Nonce'] = self.chat_room.test_parameter[nonce]
        strList = []
        isContinue = True
        sock = self.chat_room.sock_status
        sock.recv(2048).decode('utf-8', errors='ignore')
        res = self.chat_room.update_room_desc(self.chat_room.room_id,desc)
        result = json.loads(res.text)
        if scenario == 'content over 200' or scenario =='author error' or scenario =='other livemaster':
            assert res.status_code // 100 == 4
        else :
            assert res.status_code == 200
            assert result['Status'] == 'Ok'
            while isContinue:
                check = chatlib.check_event(sock)
                strList = check[1].split('\n')
                for i in strList:
                    if len(i)  > 0:
                        check1 = json.loads(i)
                        #pprint(check1)
                        if check1['event'] == 'ROOM_INFO_UPDATED':
                            desc = check1['data']
                            isContinue = False
            assert desc['description'] == expectDesc
