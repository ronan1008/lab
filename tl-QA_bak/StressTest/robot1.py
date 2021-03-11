#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import chatlib
import apilib
import threading
import time
import random
import socket
import traceback

test_env = 'http://35.236.145.25:8080'
stage_env = 'http://104.199.175.123:80'
header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
header1 = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
fpath = '/Users/lisalee/Documents/QATest/second/'

def chatroom(live_info, head1):
    is_stay = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (live_info['ServerIp'], live_info['Port'])
    try:
        sock.connect(server_address)
        chatlib.chat_room_auth(sock, head1)
        chatlib.check_event(sock)
        if chatlib.join_room(live_info['RoomId'], fpath, sock):
            raise Exception('Room In Failed')
        #print('join room: %d' % live_info['RoomId'])
        start_time = int(time.time())
        stay_time = random.randint(180, 360)
        while is_stay:
            current_time = int(time.time())
            sleep_time = random.randint(15, 20)
            time.sleep(sleep_time)
            chatlib.keep_live(sock)
            chatlib.send_message('哈囉，我再說幹話', live_info['RoomId'], sock)poetry self:update
            if (current_time - start_time) > stay_time:
                #print('leave room - %d' % live_info['RoomId'])
                chatlib.leave_room(live_info['RoomId'], sock)
                chatlib.check_event(sock)
                is_stay = False
    except socket.timeout as err:
        msg = 'room id: ' + str(live_info['RoomId']) + ' timeout'
        print(msg)
    except socket.error as err:
        msg = 'room id: ' + str(live_info['RoomId']) + ' error msg ' + str(err)
        print(msg)
    except Exception as err:
        msg = 'room id: ' + str(live_info['RoomId']) + ' error msg ' + str(err)
        print(msg)
    finally:
        sock.close()
    return


def getlist(env, head1, is_need_get_list, blist):
    room_list = []
    for kind in blist:
        if is_need_get_list:
            live_list = apilib.get_live_hot_list(env, kind, head1)
        else:
            live_list = blist
        #print(len(live_list))
        for i in live_list:
            #print(i)
            master_info = {'MasterId': '', 'RoomId': 0, 'ServerIp': '', 'Port': 0}
            if is_need_get_list:
                if i['roomStatus'] == 1:
                    room_info = apilib.get_room_info(env, i['liveMasterId'], head1)
                    master_info['ServerIp'] = room_info['socketIp']
                    master_info['Port'] = int(room_info['socketPort'])
                    master_info['MasterId'] = i['liveMasterId']
                    master_info['RoomId'] = int(i['roomId'])
                    room_list.append(master_info)
                else:
                    #print('跳出迴圈')
                    break
            else:
                room_info = apilib.get_room_info(env, i, head1)
                master_info['ServerIp'] = room_info['socketIp']
                master_info['Port'] = int(room_info['socketPort'])
                master_info['MasterId'] = i
                master_info['RoomId'] = int(room_info['roomId'])
                room_list.append(master_info)
    return(room_list)


def job(user_acc, process_num, broadcastlist):
    env = test_env
    try:
        head1 = apilib.user_login(env, user_acc, '123456', header)
        Room_list = getlist(env, head1, False, broadcastlist)
        if len(Room_list) == 0:
            raise AttributeError
        else:
            start_time = time.time()
            while 1:
                for i in range(len(Room_list)):
                   # print(Room_list[i])
                    chatroom(Room_list[i], head1)
                current_time = time.time()
                if (current_time - start_time) > 300:
                    break
        return
    except AttributeError:
        print('目前沒有開播')
    return


if __name__ == '__main__':
    act = 'track'
    numList = []
    #blist = ['newList', 'hotList']
    blist = ['0cc58d56-cd7d-4400-a121-1142b08bf1a1']
    for i in range(20, 22):
        k = str(i + 1)
        if (len(k)) == 1:
            account = act + '000' + k
        elif (len(k)) == 2:
            account = act + '00' + k
        elif (len(k)) == 3:
            account = act + '0' + k
        else:
            account = act + k
        p = threading.Thread(target=job, args=(account, i, blist,))
        numList.append(p)
    try:
        for p in numList:
            p.start()
    except Exception as err:
        print('Process abnormal %s' % err)
        traceback.print_exc()
    finally:
        for p in numList:
            p.join()
        print('Process end.')
