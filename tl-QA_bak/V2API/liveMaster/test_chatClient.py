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
    try:
        time.sleep(random.randint(1,4))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (sip, sport)
        sock.connect(server_address)
        chatlib.chat_room_auth(sock, user_header)
        chatlib.join_room(room_id,'',sock)
        if (isSend):
            time.sleep(random.randint(1, 20))
            chatlib.send_gift(sock, gift ,host_id)
            print('send')
        start_time = time.time()
        is_keep = True
        while is_keep:
            chatlib.keep_live(sock)
            time.sleep(10)
            end_time = time.time()
            if (end_time - start_time) > inTime:
                is_keep = False
                chatlib.leave_room(room_id, sock)
    except Exception as e:
        print(traceback.format_exc())
        print(e)

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


gift = 'b0a2945a-8d2b-4f5d-924a-7dd8d3a4be6b'
header['X-Auth-Token'] = test_parameter['backend_token']
header['X-Auth-Nonce'] = test_parameter['backend_nonce']
user_ids = userIdList_with_header('http://testing-api.truelovelive.com.tw', header, 'track', 150, 35)

Users_InRoom = True
gift_send_total_times = 0
if Users_InRoom :
    print('－－－－－－開始多行程－－－－－')
    pool = multiprocessing.Pool(processes = 35)
    for user_id in user_ids:
        is_send = False if gift_send_total_times >=10 else random.choice([True, False])
        is_send = True
        if is_send == True : gift_send_total_times += 1
        user_header = user_ids[user_id]
        result = pool.apply_async( joinRoom_sendGift , ('35.236.145.25', 8093, user_header, 28422, 'd24d896b-055f-47d9-aea2-77c7d27c8d8e', user_id, gift, is_send, 120) )

print("使用者都進去了")
print("總共送禮物: "+str(gift_send_total_times))
pool.close()
pool.join()



