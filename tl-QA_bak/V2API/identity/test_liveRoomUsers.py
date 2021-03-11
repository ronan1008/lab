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

#如果沒有 remain point 把使用者預設加入為 0
def add_default_remain_points(db_env, id):
    sqlStr = "select count(*) from remain_points where identity_id='{}'".format(id)
    db_result = dbConnect.dbQuery(db_env, sqlStr, 'shocklee')
    if (db_result[0][0] == 0):
        sqlStr = ["INSERT INTO remain_points VALUES (0,'{}', 2.00)".format(id)]
        dbConnect.dbSetting(db_env, sqlStr, 'shocklee')
#        print('this {} added default remain points success'.format(id))
    return
#產生 trackxxxx - track xxxx 並加入點數
def generate_users_then_add_points(start, value):
    account_list =[ "track{0:04d}".format(i) for i in range(start, start + value) ]
    users = {}
    for account in account_list:
        result = api.user_login(test_parameter['prefix'], account, '123456')
        header['X-Auth-Token'] = test_parameter['backend_token']
        header['X-Auth-Nonce'] = test_parameter['backend_nonce']
        print('prepare ' + account + ' data')
        id = api.search_user(test_parameter['prefix'], account, header)
        #add_default_remain_points(test_parameter['db'], id)
        #api.add_point(test_parameter['prefix'], id, header)
        users[id] = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': result['data']['token'], 'X-Auth-Nonce': result['data']['nonce']}
    return users

def user_go_room_then_send_gift(sip, sport, user_header, room_id, host_id, user_id, gift, isSend):
    time.sleep(random.randint(2, 10))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (sip, sport)
    sock.connect(server_address)
    chatlib.chat_room_auth(sock, user_header)
    chatlib.join_room(room_id,'',sock)
#    print("使用者{}進房了".format(user_id))
    if (isSend):
        time.sleep(random.randint(2, 10))
        chatlib.send_gift(sock, gift ,host_id)
    start_time = time.time()
    is_keep = True
    while is_keep:
        chatlib.keep_live(sock)
        time.sleep(10)
        end_time = time.time()
        if (end_time - start_time) > 60:
            is_keep = False
            chatlib.leave_room(room_id, sock)
#    print("{} 使用者 送了 {} {} 次".format(user_id, gift, times))
def get_room_users_list(prefix, room_id, header):
    api_name = '/api/v2/identity/roomUsers/liveRoom/' + str(room_id)
    header['Content-Type'] = 'application/json'
    res = api.apiFunction(test_parameter['prefix'], header, api_name , 'get', None)
    return res

header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
giftType = ['95641eb9-301f-49ee-b9e4-71784409fb05', 'abc6985b-ac7d-4758-8e32-cde8c223b67f', '4700b45c-dc93-4807-a91f-b4c717e66f06']
env = 'QA2'
send_gifts_success = 0
test_parameter = {}
initdata.set_test_data(env, test_parameter)
testChat = {
    (          'Users equal 50',     'broadcaster005',                 'track0151', 50 ,50 ,2),
    (   'Users greater than 50',     'broadcaster006',                 'track0152', 53 ,50 ,2),
    (              'auth error',     'broadcaster005',                       'error', 5 ,5 ,4),
    (           'wrong room id',     'broadcaster005',                 'track0152',  5 , 5 ,4),
}
@pytest.mark.parametrize("scenario, broadcasterAcc, account, usersNum, expectUserNum, expect", testChat)
def testChatUsers(scenario, broadcasterAcc, account, usersNum, expectUserNum, expect):
    try:
        result = api.user_login(test_parameter['prefix'], broadcasterAcc, '123456')
        header['X-Auth-Token'] = result['data']['token']
        header['X-Auth-Nonce'] = result['data']['nonce']
        result = api.get_personal_info(test_parameter['prefix'], header)
        sockinfo = api.get_load_balance(test_parameter['prefix'], header)
        host_id = result['id']
        sip = sockinfo['socketIp']
        sport = int(sockinfo['socketPort'])
        print('server ip: %s; server port: %d' % (sip, sport))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (sip, sport)
        sock.connect(server_address)
        print('connect success')
        chatlib.chat_room_auth(sock, header)
        print('auth success')
        room_id = chatlib.new_room(sock,'testing room')
        print('rid = %d' %room_id)
        #產生 使用者 id track015x 如果沒有 remain_points 就加入，並儲值
        users = generate_users_then_add_points(150,usersNum)
        gift_send_total_times = 0
        gift_rece_total_times = 0
        isContinue = True
        multi_process = True
        while isContinue:
            receive_data = sock.recv(2048).decode('utf-8', errors='ignore')
            #print(receive_data+"$$$$$$$\n")
            strList = receive_data.split('\n')
            for i in strList:
                if len(i)  > 0:
                    check1 = json.loads(i)
                    if check1['event'] == 'GIFT':
                        #pprint(check1['data']['content'])
                        gift_rece_total_times += 1
                        print("收到禮物{}次".format(gift_rece_total_times))
                        #送禮次數達到預期之後就發 api 是否如預期
                        if (gift_rece_total_times == gift_send_total_times):
                            if scenario == 'wrong room id':
                                room_id = 'fsdf'
                            if scenario == 'auth error':
                                header['X-Auth-Token'] = test_parameter['err_token']
                                header['X-Auth-Nonce'] = test_parameter['err_nonce']
                            else:
                                result = api.user_login(test_parameter['prefix'], account, '123456')
                                header['X-Auth-Token'] = result['data']['token']
                                header['X-Auth-Nonce'] = result['data']['nonce']
                            res = get_room_users_list(test_parameter['prefix'], room_id, header)
                            assert res.status_code // 100 == expect
                            if expect == 2:
                                restext = json.loads(res.text)
                                user_room_num = len(restext['data'])
                                expectUserNum = 50 if (usersNum >= 50) else usersNum
                                assert user_room_num == expectUserNum
                                pprint(restext)
                                assert restext['data'][0]['points'] >= restext['data'][1]['points']
                                isContinue = False
                            elif expect == 4:
                                if scenario == 'auth error':
                                    assert res.status_code == 401
                                isContinue = False
            if multi_process :
                print('－－－－－－開始多行程－－－－－')
                pool = multiprocessing.Pool(processes = usersNum)
                for user in users:
                    gift = giftType[random.randint(0, 2)]
                    isSend = 0 if gift_send_total_times >=15 else random.randint(0, 1)
                    #isSend=random.randint(0, 1)
                    gift_send_total_times += isSend
                    header1 = users[user]
                    result = pool.apply_async(user_go_room_then_send_gift, (sip, sport, header1, room_id, host_id, user, gift, isSend))
                    multi_process = False
                print('一共有幾次' + str(gift_send_total_times))
        pool.close()
        pool.join()
        print('－－－－－－結束多行程－－－－－')
        return
    except Exception:
        print("\n\n\n")
        print(receive_data)
        print("\n\n\n")
        print(traceback.format_exc())
        sys.exit(1)