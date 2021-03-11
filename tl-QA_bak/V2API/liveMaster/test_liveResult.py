# pylint: disable=unbalanced-tuple-unpacking
import json
import requests
import pytest
import socket
import time
import multiprocessing
import random
import sys
import traceback
from assistence import sundry
from assistence import api
from assistence import initdata
from assistence import dbConnect
from assistence import chatlib
from pprint import pprint

header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
env = 'QA2'
test_parameter = {}
initdata.set_test_data(env, test_parameter)
header['X-Auth-Token'] = test_parameter['backend_token']
header['X-Auth-Nonce'] = test_parameter['backend_nonce']
track_ids = sundry.idList_with_header(test_parameter['prefix'], header, 'track', 160, 3)
gift = '95641eb9-301f-49ee-b9e4-71784409fb05'
room_id =''
livemaster_id = ''
def setup_module():
    header['X-Auth-Token'] = test_parameter['broadcaster_token']
    header['X-Auth-Nonce'] = test_parameter['broadcaster_nonce']
    global room_id, livemaster_id
    room_id, livemaster_id, sock, sip, sport = sundry.open_enter_ZegoRoom(test_parameter['prefix'], header, "測試直播", "每一天都開心")
    #init
    host_InRoom, users_InRoom = True, True
    gift_count, gift_points  = 0, 0
    userCount_RoomIn, userCount_RoomOut = 0, 0

    start_time = time.time()
    while host_InRoom:
        receive_data = sock.recv(4096).decode('utf-8', errors='ignore')
        strList = receive_data.split('\n')
        for i in strList:
            if len(i)  > 0:
                check1 = json.loads(i)
                if check1['event'] == 'GIFT':
                    gift_points += check1['data']['point']
                    # print(('禮物累積收到{} points').format(gift_points))
                elif check1['event'] == 'ROOM_JOIN':
                    userCount_RoomIn += 1
                    # print(('累積看到{}人進房間').format(userCount_RoomIn))
                elif check1['event'] == 'ROOM_LEAVE':
                    userCount_RoomOut += 1
                    # print(('累積看到{}人出去房間').format(userCount_RoomOut))

        if users_InRoom :
            print('－－－－－－開始多行程－－－－－')
            pool = multiprocessing.Pool(processes = 5)
            for uid in track_ids:
                is_send = random.choice([True, False])
                if is_send == True : gift_count += 1
                user_header = track_ids[uid]
                result = pool.apply_async( sundry.joinRoom_sendGift  , (sip, sport, user_header, room_id, livemaster_id, uid, gift, is_send, 30) )
            print("預計收到禮物{}次".format(gift_count))
            users_InRoom = False

        chatlib.keep_live(sock)
        end_time = time.time()
        if (end_time - start_time) > 60:
            host_InRoom = False
            chatlib.leave_room(room_id, sock)

    pool.close()
    pool.join()

#scenario, token, nonce, st_time, end_time, item, page, expect
testData = [
    #           scenario,                token,                nonce,   expect
    (   'boradcast_10User',  'broadcaster_token',  'broadcaster_nonce',   2),
    (         'Auth Error',          'err_token',          'err_nonce',   4),
    (  'Forbidden To Auth',         'user_token',         'user_nonce',   4),
    (     'Room Not Found',  'broadcaster_token',  'broadcaster_nonce',   4),
]

@pytest.mark.parametrize("scenario, token, nonce,  expect", testData)
def test_transaction_list(scenario, token, nonce,  expect):
    global room_id, livemaster_id
    sqlStr = "select total_count From live_room where id={}".format(room_id)
    [(total_count,)] = dbConnect.dbQuery(test_parameter['db'], sqlStr, 'shocklee')
    sqlStr = "select max(data_date) from live_master_date_points where live_master_id='{}'".format(livemaster_id)
    [(max_date,)] = dbConnect.dbQuery(test_parameter['db'], sqlStr, 'shocklee')
    if max_date :
        sqlStr = "select points from live_master_date_points where live_master_id='{}' and data_date ='{}'".format(livemaster_id, max_date)
        [(points,)] = dbConnect.dbQuery(test_parameter['db'], sqlStr, 'shocklee')
    else :
        points = 0
    Hot_ecpected =  (total_count + 1) * 1331 + int(points)
    header['X-Auth-Token'] = test_parameter[token]
    header['X-Auth-Nonce'] = test_parameter[nonce]
    if scenario == 'Room Not Found':
        room_id = 999999
    api_name = "/api/v2/liveMaster/liveResult/" + str(room_id)
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'get', None)
    if expect == 2:
        restext = json.loads(res.text)
        print(restext)
        assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
        assert restext['data']['hot'] == Hot_ecpected
        assert restext['data']['points'] == points
        assert restext['data']['time'] != None
    else:
        if scenario == 'Auth Error':
            assert res.status_code == 401
        elif scenario == 'Forbidden To Auth':
            assert res.status_code == 403
        elif scenario == 'Room Not Found':
            assert res.status_code == 404
