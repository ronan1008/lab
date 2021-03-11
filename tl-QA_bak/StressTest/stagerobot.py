#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from second import chatlib
from second import apilib
from second import utilitylib
import threading
import time
import random
import socket
import traceback




fpath = '/home/lisa/robot/'
#fpath = 'C:\QATest\second'


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
        stay_time = random.randint(10, 60)
        while is_stay:
            current_time = int(time.time())
            if ((current_time - start_time) % 20) == 0:
                keep_flag = chatlib.keep_live(sock)
                if keep_flag[0] == 2:
                    print('Room Exit')
                    break
                elif keep_flag[0] == 3:
                    utilitylib.send_to_slack(keep_flag[1], fpath, live_info['RoomId'])
                    break
            if (current_time - start_time) > stay_time:
                #print('leave room - %d' % live_info['RoomId'])
                chatlib.leave_room(live_info['RoomId'], sock)
                chatlib.check_event(sock)
                is_stay = False
    except socket.timeout as err:
        msg = 'room id: ' + str(live_info['RoomId']) + ' timeout'
        utilitylib.send_to_slack(msg, fpath, live_info['RoomId'])
    except socket.error as err:
        msg = 'room id: ' + str(live_info['RoomId']) + ' error msg ' + str(err)
        utilitylib.send_to_slack(msg, fpath, live_info['RoomId'])
    except Exception as err:
        msg = 'room id: ' + str(live_info['RoomId']) + ' error msg ' + str(err)
        utilitylib.send_to_slack(msg, fpath, live_info['RoomId'])
    finally:
        sock.close()
    return


def getlist(env, head1):
    need_check_list = []
    blist = ['newList', 'hotList']
    for kind in blist:
        live_list = apilib.get_live_hot_list(env, kind, head1)
        #print(len(live_list))
        for i in live_list:
            master_info = {'MasterId': '', 'RoomId': 0, 'ServerIp': '', 'Port': 0}
            if i['roomStatus'] == 1:
                room_info = apilib.get_room_info(env, i['liveMasterId'], head1)
                master_info['ServerIp'] = room_info['socketIp']
                master_info['Port'] = int(room_info['socketPort'])
                master_info['MasterId'] = i['liveMasterId']
                master_info['RoomId'] = int(i['roomId'])
                need_check_list.append(master_info)
            else:
                #print('跳出迴圈')
                break
    return(need_check_list)


def job(user_acc, process_num, broadcastlist):
    env = test_env
    try:
        head1 = apilib.user_login(env, user_acc, '123456', head)
        if len(broadcastlist) is 0:
            need_check_list = getlist(env, head1)
        else:
            need_check_list = broadcastlist
        if len(need_check_list) == 0:
            raise AttributeError
        else:
            start_time = time.time()
            while 1:
                for i in range(len(need_check_list)):
                    chatroom(need_check_list[i], head1)
                current_time = time.time()
                if (current_time - start_time) > 300:
                    break
        return
    except AttributeError:
        utilitylib.send_to_slack('目前沒有開播', fpath, 0)
    return


if __name__ == '__main__':
    act = 'track'
    numList = []
    broadcastlist = ['0cc58d56-cd7d-4400-a121-1142b08bf1a1']
    for i in range(10):
        k = str(i + 1)
        if (len(k)) == 1:
            account = act + '000' + k
        elif (len(k)) == 2:
            account = act + '00' + k
        elif (len(k)) == 3:
            account = act + '0' + k
        else:
            account = act + k
        p = threading.Thread(target=job, args=(account, i, broadcastlist,))
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
