#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# encoding: utf-8
import json
import time
import utilitylib
#import sys
#from importlib import reload

#reload(sys)
#sys.setdefaultencoding('utf-8')


def chat_room_auth(sock, header):
    auth = {'action': 'AUTH','data': {'token': '', 'nonce': ''}}
    auth['data']['token'] = header['X-Auth-Token']
    auth['data']['nonce'] = header['X-Auth-Nonce']
    auth_json = json.dumps(auth) + '\r\n'
    sock.send(auth_json.encode('utf-8'))
    check_event(sock)
    return


def join_room(rid, fpath, sock):
    flag = False
    room = {'action': 'IN_ROOM', 'data': {'roomId': 0}}
    room['data']['roomId'] = rid
    room_json = json.dumps(room) + '\r\n'
    sock.send(room_json.encode('utf-8'))
    result_info = check_event(sock)
    if result_info[1].find('error') > 0:
        utilitylib.send_to_slack(result_info, fpath, rid)
        flag = True
    else:
        wait_flag = True
        start_time = int(time.time())
        while wait_flag:
            result_info = check_event(sock)
            if result_info[1].find('ROOM_IN'):
                wait_flag = False
            else:
                current_time = int(time.time())
                if (current_time - start_time) > 30:
                    utilitylib.send_to_slack('Join room time out', fpath, rid)
                    flag = True
                    break
    return(flag)


def leave_room(rid, sock):
    room = {'action': 'LEAVE_ROOM', 'data': {'roomId': 0}}
    room['data']['roomId'] = rid
    room_json = json.dumps(room) + '\r\n'
    sock.send(room_json.encode('utf-8'))
    return


def send_message(strmsg, rid, sock):
    msg = {'action': 'MESSAGE', 'data': {'roomId': 0, 'content': ''}}
    msg['data']['roomId'] = rid
    msg['data']['content'] = strmsg
    msg_json = json.dumps(msg) + '\r\n'
    sock.send(msg_json.encode('utf-8'))
    return


def send_gift(sock, gift_id, broadcastid):
    gift = {'action': 'GIFT', 'data': {'giftId': '', 'userId': '', 'count': 1}}
    gift['data']['giftId'] = gift_id
    gift['data']['userId'] = broadcastid
    gift_json = json.dumps(gift) + '\r\n'
    sock.send(gift_json.encode('utf-8'))
    return


def check_event(sock):
    receive_data = sock.recv(2048).decode('utf-8', errors='ignore')
    if receive_data.find('error') > 0:
        result = 3
    elif receive_data.find('ROOM_EXITED') > 0:
        result = 1
    else:
        result = 2
    return(result, receive_data)


def keep_live(sock):
    result = 0
    keep = {'action': 'PING'}
    keep_json = json.dumps(keep) + '\r\n'
    sock.send(keep_json.encode('utf-8'))
    receive_data = sock.recv(2048).decode('utf-8', errors='ignore')
    if receive_data.find('error') > 0:
        result = 1
    elif receive_data.find('ROOM_EXITED') > 0:
        print('Room_Exited %s' % time.localtime())
        result = 2
    return(result, receive_data)


def new_room(sock):
    new = {'action': 'NEW_ROOM', 'data': {'title': '水姑娘一級棒'}}
    new_json = json.dumps(new) + '\r\n'
    sock.send(new_json.encode('utf-8'))
    receive_data = sock.recv(2048).decode('utf-8', errors='ignore')
    open_success = False
    while open_success == False:
        check = check_event(sock)
        event_result = json.loads(check[1])
        if event_result['event'] == 'ROOM_NEW':
            #print('ROOM_NEW: %s' %event_result)
            rid = event_result['data']['roomId']
        elif event_result['event'] == 'ROOM_IN':
            open_success = True
            print('open room success(%s)' % rid)
    return(rid)

