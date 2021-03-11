#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import multiprocessing
import chatlib
import apilib
import time
import socket
import traceback
import random


test_env = 'http://35.236.145.25:8080'
stage_env = 'http://104.199.175.123:80'
head = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}


def job(user, env):
    try:
        head1 = apilib.user_login(env, user, '123456', head)
        print(1)
        sockinfo = apilib.get_load_balance(env, head1)
        print(sockinfo)
        sip = sockinfo['socketIp']
        sport = int(sockinfo['socketPort'])
        print('server ip: %s; server port: %d' % (sip, sport))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (sip, sport)
        sock.connect(server_address)
        print('connect success')
        chatlib.chat_room_auth(sock, head1)
        print('auth success')
        rid = chatlib.new_room(sock)
        print('rid = %d' %rid)
        start_time = time.time()
        is_keep = True
        while is_keep:
            time.sleep(20)
            end_time = time.time()
            if (end_time - start_time) > 4500:
                is_keep = False
                chatlib.leave_room(rid, sock)
            chatlib.keep_live(sock)
        return
    except Exception as e:
        print(e)


if __name__ == '__main__':
    str1 = 'broadcaster'
    numList = []
    for i in range(10):
        k = str(i + 1)
        if (len(k)) == 1:
            account = str1 + '00' + k
        elif (len(k)) == 2:
            account = str1 + '0' + k
        else:
            account = str1 + k
        p = multiprocessing.Process(target=job, args=(account, stage_env,))
        numList.append(p)
    try:
        for p in numList:
            p.start()
    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        for p in numList:
            p.join()
        print('Process end.')
