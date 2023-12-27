#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# encoding: utf-8
import json
import time
from pprint import pprint

def chat_room_auth(sock, header):
    auth = {'action': 'AUTH','data': {'token': '', 'nonce': ''}}
    auth['data']['token'] = header['X-Auth-Token']
    auth['data']['nonce'] = header['X-Auth-Nonce']
    auth_json = json.dumps(auth) + '\n' #跳脫字元由'\r\n' 改為 '\n
    sock.send(auth_json.encode('utf-8'))
    start_time = int(time.time())
    msg_untreated = ''
    auth = False
    while not auth:
        msg_part = sock.recv(1024).decode('unicode_escape', errors='ignore')
        msg_all = msg_untreated + msg_part
        msg_list = msg_all.split('\n')
        msg_last = msg_list[-1]
        if msg_last[-2:-1] != '\n':
            msg_untreated = msg_list.pop()
        for msg in msg_list:
            if len(msg) >0 :
                check1 = json.loads(msg)
                if  check1['event'] == 'AUTH':
                    print(check1['data'])
                    auth = True
                    auth_again = False
                else:
                    current_time = int(time.time())
                    if (current_time - start_time) > 10:
                        auth_again = True
                        break
    if auth_again:
        print('在驗證一次')
        sock.send(auth_json.encode('utf-8'))


def join_room(rid, fpath, sock):
    flag = False
    room = {'action': 'IN_ROOM', 'data': {'roomId': 0}}
    room['data']['roomId'] = rid
    room_json = json.dumps(room) + '\n'
    sock.send(room_json.encode('utf-8'))
    return

def leave_room(rid, sock):
    room = {'action': 'LEAVE_ROOM', 'data': {'roomId': 0}}
    room['data']['roomId'] = rid
    #pprint(room)
    room_json = json.dumps(room) + '\n'
    sock.send(room_json.encode('utf-8'))
    return

def send_message(strmsg, rid, sock):
    msg = {'action': 'MESSAGE', 'data': {'roomId': 0, 'content': ''}}
    msg['data']['roomId'] = rid
    msg['data']['content'] = strmsg
    msg_json = json.dumps(msg) + '\n'
    sock.send(msg_json.encode('utf-8'))
    return


def send_gift(sock, gift_id, broadcastid):
    gift = {'action': 'GIFT', 'data': {'giftId': '', 'userId': '', 'count': 1}}
    gift['data']['giftId'] = gift_id
    gift['data']['userId'] = broadcastid
    gift_json = json.dumps(gift) + '\n'
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
    keep_json = json.dumps(keep) + '\n'
    sock.send(keep_json.encode('utf-8'))
    receive_data = sock.recv(2048).decode('utf-8', errors='ignore')
    if receive_data.find('error') > 0:
        result = 1
    elif receive_data.find('ROOM_EXITED') > 0:
        #print('Room_Exited %s' % time.localtime())
        result = 2
    return(result, receive_data)

def keep_ping(sock):
    ping = json.dumps({'action': 'PING'}) + '\n'
    sock.send(ping.encode('utf-8'))

def new_room(sock, roomtitle):
    strList = []
    isContinue = True
    new = {'action': 'NEW_ROOM', 'data': {'title': roomtitle}}
    new_json = json.dumps(new) + '\n'
    sock.send(new_json.encode('utf-8'))
    sock.recv(2048).decode('utf-8', errors='ignore')
    while isContinue:
        check = check_event(sock)
        strList = check[1].split('\n')
        #pprint(strList)
        for i in strList:
            if len(i)  > 0:
                check1 = json.loads(i)
                #pprint(check1)
                if check1['event'] == 'ROOM_IN':
                    #pprint('ROOM_in: %s'%check1['data'])
                    roomId = check1['data']['roomId']
                    isContinue = False
    return roomId


def enterZego(sock, roomId):
    # strList = []
    # isContinue = True
    new = {'action': 'ENTER_ZEGO_ROOM', 'data': {'roomId': roomId}}
    #new_json = json.dumps(new) + '\r\n'
    new_json = json.dumps(new) + '\n'
    sock.send(new_json.encode('utf-8'))
    # sock.recv(32768).decode('utf-8', errors='ignore')
    # receive_data = ''
    # while isContinue:
    #     recvSize = 32768
    #     part = sock.recv(recvSize).decode('utf-8', errors='ignore')
    #     receive_data += part
    #     #if len(part) % 8192 != 0 :
    #     if len(part) < recvSize :
    #         strList = receive_data.split('\n')
    #         for i in strList:
    #             if len(i)  > 0:
    #                 check1 = json.loads(i)
    #                 if  check1['event'] == 'ROOM_IN':
    #                     roomId = check1['data']['roomId']
    #                     print(check1['data'])
    #                     isContinue = False
    #         receive_data = ''
    # return roomId