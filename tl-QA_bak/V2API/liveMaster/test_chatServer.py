#這個檔案為個人測試使用，與票無關
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

import asyncio

header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
giftType = ['95641eb9-301f-49ee-b9e4-71784409fb05', 'abc6985b-ac7d-4758-8e32-cde8c223b67f', '4700b45c-dc93-4807-a91f-b4c717e66f06']
env = 'QA2'
test_parameter = {}
initdata.set_test_data(env, test_parameter)

#account_prefix = track , account_suffix = 150 , usersNum = 10 -> track0150 - track0160



def userIdList_with_header(prefix, header, account_prefix, account_suffix, users_count):
    login_ids = [ "track{0:04d}".format(i) for i in range(account_suffix, account_suffix + users_count) ]
    users_list = dict()
    for login_id in login_ids:
        result = api.user_login(prefix, login_id, '123456')
        id = api.search_user(prefix, login_id, header)
        users_list[id] = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': result['data']['token'], 'X-Auth-Nonce': result['data']['nonce']}
    return users_list

def joinRoom_sendGift(sip, sport, user_header, room_id, host_id, user_id, gift, isSend, inTime):
    time.sleep(random.randint(1,20))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (sip, sport)
    sock.connect(server_address)
    chatlib.chat_room_auth(sock, user_header)
    chatlib.join_room(room_id,'',sock)
    if (isSend):
        time.sleep(random.randint(1, 10))
        chatlib.send_gift(sock, gift ,host_id)
    start_time = time.time()
    is_keep = True
    while is_keep:
        chatlib.keep_live(sock)
        time.sleep(10)
        end_time = time.time()
        if (end_time - start_time) > inTime:
            is_keep = False
            chatlib.leave_room(room_id, sock)

def open_ZegoRoom(prefix, header, title, description):
    result = api.get_personal_info(test_parameter['prefix'], header)
    host_id = result['id']
    room_id, streamId = api.open_zegoRoom(prefix, header, title, description)
    sockinfo = api.get_load_balance(prefix, header)
    sip, sport = sockinfo['socketIp'], int(sockinfo['socketPort'])
    server_address = (sip, sport)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    chatlib.chat_room_auth(sock, header)
    chatlib.enterZego(sock, room_id)
    print("roomId:{}, hostId:{}, sip:{}, sport:{}".format(room_id, host_id, sip, sport))
    return  room_id, host_id, sock, sip, sport

loop = asyncio.get_event_loop()

gift = '95641eb9-301f-49ee-b9e4-71784409fb05'

header['X-Auth-Token'] = test_parameter['broadcaster_token']
header['X-Auth-Nonce'] = test_parameter['broadcaster_nonce']
room_id, host_id, sock, sip, sport = open_ZegoRoom(test_parameter['prefix'], header, '測試直播', '每天都好快樂')

header['X-Auth-Token'] = test_parameter['broadcaster_token']
header['X-Auth-Nonce'] = test_parameter['broadcaster_nonce']
user_ids = userIdList_with_header(test_parameter['prefix'], header, 'track', 150, 10)

broadcaster_InRoom = True
Users_InRoom = True
start_time = time.time()
gift_points = 0
userCount_in_room = 0
userCount_out_room = 0
test = 0
while broadcaster_InRoom:
    receive_data = sock.recv(4096).decode('utf-8', errors='ignore')
    print(receive_data)
    strList = receive_data.split('\n')
    for i in strList:
        if len(i)  > 0:
            check1 = json.loads(i)
            if check1['event'] == 'GIFT':
                gift_points += check1['data']['point']
                print(('禮物累積收到{} points').format(gift_points))
            elif check1['event'] == 'ROOM_JOIN':
                userCount_in_room += 1
                print(('累積看到{}人進房間').format(userCount_in_room))
            elif check1['event'] == 'ROOM_LEAVE':
                userCount_out_room += 1
                print(('累積看到{}人出去房間').format(userCount_out_room))

    # if Users_InRoom :
    #     print('－－－－－－開始多行程－－－－－')
    #     pool = multiprocessing.Pool(processes = 10)
    #     for user_id in user_ids:
    #         is_send = random.choice([True, False])
    #         user_header = user_ids[user_id]
    #         result = pool.apply_async( joinRoom_sendGift , (sip, sport, user_header, room_id, host_id, user_id, gift, is_send, 15) )
    #     print("使用者都進去了")
    #     Users_InRoom = False

    chatlib.keep_live(sock)
    end_time = time.time()
    if (end_time - start_time) > 10000:
        broadcaster_InRoom = False
        chatlib.leave_room(room_id, sock)

# pool.close()
# pool.join()



