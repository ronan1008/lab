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

async def joinRoom_sendGift(sip, sport, user_header, room_id, host_id, user_id, gift, isSend, inTime):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (sip, sport)
    sock.connect(server_address)
    chatlib.chat_room_auth(sock, user_header)
    chatlib.join_room(room_id,'',sock)
    if (isSend):
        chatlib.send_gift(sock, gift ,host_id)
    asyncio.sleep(20)
    chatlib.leave_room(room_id, sock)
    # start_time = time.time()
    # is_keep = True
    # while is_keep:
    #     chatlib.keep_live(sock)
    #     end_time = time.time()
    #     if (end_time - start_time) > inTime:
    #         is_keep = False
    #         chatlib.leave_room(room_id, sock)

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
    print("roomId:{}, hostId:{}, sip:{}, sport:{}".format(room_id, host_id, sock, sip, sport))
    return  room_id, host_id, sock, sip, sport


gift = '95641eb9-301f-49ee-b9e4-71784409fb05'
header['X-Auth-Token'] = test_parameter['broadcaster_token']
header['X-Auth-Nonce'] = test_parameter['broadcaster_nonce']
user_ids = userIdList_with_header(test_parameter['prefix'], header, 'track', 150, 30)

loop = asyncio.get_event_loop()

Users_InRoom = True
gift_send_total_times = 0
if Users_InRoom :
    print('－－－－－－開始多行程－－－－－')
    for user_id in user_ids:
        is_send = False if gift_send_total_times >=10 else random.choice([True, False])
        if is_send == True : gift_send_total_times += 1
        user_header = user_ids[user_id]
        loop.run_until_complete(joinRoom_sendGift('34.80.110.80', 8090, user_header, 1014, 'd82a7ba2-5c11-4615-aba7-2a768d927165', user_id, gift, is_send, 30))
        #result = pool.apply_async( joinRoom_sendGift , ('34.80.110.80', 8090, user_header, 973, 'd82a7ba2-5c11-4615-aba7-2a768d927165', user_id, gift, is_send, 30) )

print("使用者都進去了")
print("總共送禮物: "+str(gift_send_total_times))
# pool.close()
# pool.join()



