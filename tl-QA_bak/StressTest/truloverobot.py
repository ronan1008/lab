#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import multiprocessing
import chatlib
import apilib
import time
import random
import socket
import traceback
import utilitylib


test_env = 'http://35.236.145.25:8080'
stage_env = 'http://104.199.175.123:80'
fpath = '/home/lisa/robot/'
head = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}


def chatroom(live_info, head1):
    is_stay = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (live_info['ServerIp'], live_info['Port'])
    try:
        sock.connect(server_address)
        chatlib.chat_room_auth(sock, head1)
        chatlib.check_event(sock)
        if chatlib.join_room(live_info['RoomId'], sock):
            raise Exception('Room In Timeout')
        start_time = int(time.time())
        stay_time = random.randint(120, 180)
        while is_stay:
            current_time = int(time.time())
            if ((current_time - start_time) % 20) == 0:
                if chatlib.keep_live(sock):
                    is_stay = False
            if (current_time - start_time) > stay_time:
                chatlib.leave_room(live_info['RoomId'], sock)
                chatlib.check_event(sock)
                is_stay = False

    except socket.timeout as err:
        msg = 'room id: ' + str(live_info['RoomId']) + ' timeout'
        utilitylib.send_to_slack(msg, fpath, live_info['RoomId'])
    except socket.error as err:
        msg = 'room id: ' + str(live_info['RoomId']) + ' error msg ' + str(err)
        if str(err).find('Errno 32') < 0:
            utilitylib.send_to_slack(msg, fpath, live_info['RoomId'])
    except Exception as err:
        msg = 'room id: ' + str(live_info['RoomId']) + ' error msg ' + str(err)
        if str(err).find('Errno 32') < 0:
            utilitylib.send_to_slack(msg, fpath, live_info['RoomId'])
    finally:
        sock.close()
    return


def job(user_acc, process_num):
    env = stage_env
    need_check_list = []
    try:
        if process_num > 0:
            sleep_time = random.randint(5, 15)
            time.sleep(sleep_time)
        head1 = apilib.user_login(env, user_acc, '123456', head)
        live_list = apilib.get_live_hot_list(env, 'newList', head1)
        for i in live_list:
            if i['roomStatus'] == 1:
                master_info = {'MasterId': '', 'RoomId': 0, 'ServerIp': '', 'Port': 0}
                room_info = apilib.get_room_info(env, i['liveMasterId'], head1)
                master_info['ServerIp'] = room_info['socketIp']
                master_info['Port'] = int(room_info['socketPort'])
                master_info['MasterId'] = i['liveMasterId']
                master_info['RoomId'] = int(i['roomId'])
                need_check_list.append(master_info)
        if len(need_check_list) == 0:
            raise AttributeError
        else:
            for i in need_check_list:
                print(i)
                chatroom(i, head1)
        return
    except AttributeError:
        utilitylib.send_to_slack('目前沒有開播', fpath, 0)
    return


if __name__ == '__main__':
    act = 'tl-robot'
    numList = []
    robot_list = []
    for i in range(5):
        n = random.randint(0, 19)
        k = str(n + 1)
        if (len(k)) == 1:
            account = act + '0' + k
        else:
            account = act + k
        if account not in robot_list:
            robot_list.append(account)
            if len(robot_list) == 5:
                print(robot_list)
                break
    for i in range(len(robot_list)):
        account = robot_list[i]
        p = multiprocessing.Process(target=job, args=(account, i))
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
