#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#import multiprocessing
import threading
import chatlib
import apilib
import time
import random
import socket
import sys
import utilitylib


test_env = 'http://35.236.145.25:8080'
stage_env = 'http://104.199.175.123:80'
head = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
gift_id = ['1d1453f1-beb3-46c7-be71-40928c9d5d79']
msg_list = ['hello', '大家好', '主播好正', '你想吃啥?', '今天心情不美麗']
fpath = '/home/lisa/robot/'
#fpath = 'C:\QATest\second'


def chatroom(live_info, head1, p_num):
    is_stay = True
    is_gift = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (live_info['ServerIp'], live_info['Port'])
    try:
        sock.connect(server_address)
        chatlib.chat_room_auth(sock, head1)
        chatlib.check_event(sock)
        if chatlib.join_room(live_info['RoomId'], fpath, sock):
            raise Exception('Room In Timeout')
        else:
            print('stress%d join room-%d' % (p_num, live_info['RoomId']))
        while is_stay:
            sleep_time = random.randint(1200, 1800)
            for i in range(sleep_time):
                if (i % 20) == 0:
                    keep_flag = chatlib.keep_live(sock)
                    if keep_flag[0] == 2:
                        is_stay = False
                        print('Room Exit')
                        chatlib.leave_room(live_info['RoomId'], sock)
                        break
                    elif keep_flag[0] == 3:
                        is_stay = False
                        utilitylib.send_to_slack(keep_flag[1], fpath, live_info['RoomId'])
                        break
                time.sleep(1)
            if is_stay:
                qq = random.randint(0, 9)
                if qq > 7:
                    if is_gift:
                        #gid = random.randint(0, len(gift_id) - 1)
                        chatlib.send_gift(sock, 0, live_info['MasterId'])
                        is_gift = False
                    else:
                        msg1 = random.randint(0, len(msg_list) - 1)
                        print(msg1)
                        chatlib.send_message(msg1, live_info['RoomId'], sock)
    except socket.timeout as err:
        msg = '(TimeOut)room id: ' + str(live_info['RoomId']) + ' timeout'
        utilitylib.send_to_slack(msg, fpath, live_info['RoomId'])
    except socket.error as err:
        msg = '(Socket error)room id: ' + str(live_info['RoomId']) + ' error msg: ' + str(err)
        if str(err).find('Errno 32') < 0:
            utilitylib.send_to_slack(msg, fpath, live_info['RoomId'])
    except Exception as err:
        print(err)
        msg = '(unknow error)room id: ' + str(live_info['RoomId']) + ' error msg: ' + str(err)
        if str(err).find('Errno 32') < 0:
            utilitylib.send_to_slack(msg, fpath, live_info['RoomId'])
    finally:
        sock.close()
    return


def getlist(env, head1):
    need_check_list = []
    blist = ['newList', 'hotList']
    for kind in blist:
        live_list = apilib.get_live_hot_list(env, kind, head1)
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
                break
    return(need_check_list)


def job(user_acc, p_num):
    env = stage_env
    try:
        head1 = apilib.user_login(env, user_acc, '123456', head)
        need_check_list = getlist(env, head1)
        if p_num == 1000:
            print("直播主數量%d" % len(need_check_list))
        if len(need_check_list) == 0:
            raise AttributeError
        i = random.randint(0, len(need_check_list) - 1)
        chatroom(need_check_list[i], head1, p_num)
        return()
    except AttributeError:
        utilitylib.send_to_slack('目前沒有開播', fpath, 0)
    except Exception as err:
        utilitylib.send_to_slack(err, fpath, 0)
    return


if __name__ == '__main__':
    act = 'stress'
    numList = []
    beg = int(sys.argv[1])
    end = int(sys.argv[2])
    for i in range(beg, end):
        k = str(i + 1)
        if (len(k)) == 1:
            account = act + '000' + k
        elif (len(k)) == 2:
            account = act + '00' + k
        elif (len(k)) == 3:
            account = act + '0' + k
        else:
            account = act + k
        p = threading.Thread(target=job, args=(account, i, ))
        numList.append(p)
    try:
        for p in numList:
            time.sleep(0.4)
            p.start()
    except Exception as err:
        print('Process abnormal: %s' % err)
    finally:
        for p in numList:
            p.join()
        print('Process end.')
