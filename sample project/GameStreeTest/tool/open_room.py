import json, requests, pytest, time, multiprocessing, sys, socket, random, threading, psutil, traceback, argparse
import urllib.parse as urlparse
from urllib.parse import urlencode
from pprint import pprint
from datetime import datetime
from configparser import ConfigParser
import api, chatlib

EXE_TIME = 30000



def user_joinRoom_playGame(sip, sport, user_header, room_id, host_id, user_id, inTime):
    try:
        time.sleep(random.randint(1,30))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(60)
        server_address = (sip, sport)
        sock.connect(server_address)
        chatlib.chat_room_auth(sock, user_header)
        chatlib.join_room(room_id,'',sock)
        print("使用者: {} 進去房間 {} 了!".format(user_id, room_id))
        game_url = api.get_v2game_url(2, user_header['X-Auth-Token'], user_header['X-Auth-Nonce'], room_id)
        print( 'cleint'+ game_url)
        start_time = time.time()
        while True:
            time.sleep(30)
            print('Client {} 還活著'.format(user_id))
            chatlib.keep_ping(sock)
            end_time = time.time()
            if (end_time - start_time) > inTime :
                chatlib.leave_room(room_id, sock)
                print("時間到了，使用者離開房間")
                break
        return
    except Exception as e:
        print(e)
        time.sleep(5)
        traceback.print_exc()
        print('{} 重新進入聊天室'.format(user_id))
        return user_joinRoom_playGame(sip, sport, user_header, room_id, host_id, user_id, inTime)


def broadcaster_open_ZegoRoom_UserPlayIn(prefix, header, title, description, track_ids:dict):
    room_id, livemaster_id, sock, sip, sport = api.open_enter_ZegoRoom(prefix, header, title, description)
    guest_list = [guest_id for guest_id in track_ids ]
    print('這是房間 : ' + str(room_id) + '，等等會有 : ' + str(len(guest_list)) + ' 位使用者進入')
    start_time = time.time()

    game_url = api.get_v2game_url(1, header['X-Auth-Token'], header['X-Auth-Nonce'], room_id)
    print( 'Host: '+ game_url)
    try:
        guest_enter_room = True
        msg_untreated = ''
        while True:
            msg_part = sock.recv(1024).decode('unicode_escape', errors='ignore')
            msg_all = msg_untreated + msg_part
            msg_list = msg_all.split('\n')
            msg_last = msg_list[-1]
            if msg_last[-2:-1] != '\n':
                msg_untreated = msg_list.pop()
            for msg in msg_list:
                if len(msg) >0 :
                    check1 = json.loads(msg)
                    # print(check1)
                    if  check1['event'] == 'ROOM_JOIN':
                        print(check1['data']['content'])
                    elif check1['event'] == 'ROOM_LEAVE':
                        print(check1['data']['content'])
                    elif check1['event'] == 'GAME_MESSAGE':
                        GUESS_NUM = check1['data']['answer']
                        print(check1['data'])
                    elif check1['event'] == 'GAME_OVER':
                        GAME_OVER = True
                        print(check1)
                    elif check1['event'] == 'GAME_STARTED':
                        print(check1)

            if guest_enter_room :
                print('in')
                threads = []
                for uid in track_ids:
                    user_header = track_ids[uid]
                    client = threading.Thread(target = user_joinRoom_playGame, args = (sip, sport, user_header, room_id, livemaster_id, uid, EXE_TIME))
                    threads.append(client)
                    client.setDaemon(True)
                    client.start()
                guest_enter_room = False

            print('Host {} 還活著'.format(livemaster_id))
            chatlib.keep_ping(sock)
            time.sleep(20)

            #結束遊戲的條件
            end_time = time.time()
            if (end_time - start_time) > EXE_TIME :
                print("總共運行了: {} 秒".format(int(end_time - start_time)))
                chatlib.leave_room(room_id, sock)
    except:
        traceback.print_exc()

if __name__ == '__main__':
    prefix = 'http://testing-api.xtars.com'
    header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': 'gamehost0001', 'X-Auth-Nonce':'gamehost0001'}
    result = api.user_login(prefix, 'tl-lisa', '12345678')
    backend_token, backend_nonce  = result['data']['token'], result['data']['nonce']
    backend_header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': backend_token, 'X-Auth-Nonce': backend_nonce}
    user_loginIds=['guest1000', 'guest1001', 'guest1002', 'guest1003', 'guest1004']
    user_header_dict = api.get_multiUsers_token_nonce(prefix, backend_header, user_loginIds)

    # pprint(user_header_dict)
    broadcaster_open_ZegoRoom_UserPlayIn(prefix, header, 'test', 'just test', user_header_dict)