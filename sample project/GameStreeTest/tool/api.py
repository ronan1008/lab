#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# pylint: disable=unbalanced-tuple-unpacking
import json, sys, time, random, socket
import requests, paramiko
from pathlib import Path
from pprint import pprint
import urllib.parse as urlparse
from urllib.parse import urlencode
# from tool import chatlib, dbConnect
from . import chatlib, dbConnect
# import chatlib


def user_login(prefix, account, pwd):
    url = prefix + '/api/v2/identity/auth/login'
    body = {
        "account": account,
        "password": pwd,
        "pushToken": ''
    }
    #print(body)
    res = requests.post(url, json=body)
    #print(json.loads(res.text))
    if res.status_code // 100 == 2:
        restext = json.loads(res.text)
        return(restext)
    else:
        return(json.loads(res.text))

def get_personal_info(prefix, head):
    url = prefix + '/api/v1/personal/info'
    #print('url=%s' % url)
    res = requests.get(url, headers=head)
    if res.status_code != 200:
        json_result = ''
    else:
        json_result = json.loads(res.text)
    return(json_result)


def get_backend_user(prefix, head, id):
    url = prefix + '/api/v1/backend/user/' + id
    res = requests.get(url, headers=head)
    if res.status_code != 200:
        json_result = ''
    else:
        json_result = json.loads(res.text)
    return(json_result)


def register(prefix, account, header):
    url = prefix + '/api/v1/identity/register'
    body = {"loginId": account, 'password': '123456', 'publicSexInfo': False}
    requests.post(url, headers=header, json=body)
    #str1 = res.text
    #print(str1)
    return


def add_point(prefix, id, header):
    url = prefix + '/api/v1/identity/' + id + '/points'
    body = {'addPoints': 5000, 'ratio': 2, 'reason': 'testing'}
    requests.put(url, headers=header, json=body)
    #str1 = res.text
    return

def search_user(prefix, account, header):
    url = prefix + '/api/v1/backend/identity/search'
    #print('account = %s' % account)
    body = {"input": account, "page": 0, "size": 10, "statuses": []}
    res = requests.post(url, headers=header, json=body)
    json_result = json.loads(res.text)
    print(json_result)
    if json_result['totalCount'] > 1:
        for i in json_result['data']:
            if i['loginId'] == account:
                id = i['id']
                break
        return(id)
    else:
        return(json_result['data'][0]['id'])


def search_master(prefix, header, body, inum, pnum):
    url = prefix +  '/api/v1/identity/search/liveMaster/' + inum + '/' + pnum
    res = requests.post(url, headers=header, json=body)
    return(res)

def get_room_info(prefix, bid, header):
    room_info = {'roomId': 0, 'socketIp': '', 'socketPort': ''}
    url = prefix + '/api/v1/live/info/' + bid
    res = requests.get(url, headers=header)
    str1 = res.text
    if str1 != '':
        json_result = json.loads(str1)
        room_info['roomId'] = json_result['roomId']
        room_info['socketIp'] = json_result['socketIp']
        room_info['socketPort'] = json_result['socketPort']
    return(room_info)


def get_load_balance(prefix, header):
    url= prefix + '/api/v1/live/loadBalance/'
    #print(url)
    res = requests.get(url, headers=header)
    #print(res.status_code)
    if res.status_code != 200:
        json_result = ''
    else:
        json_result = json.loads(res.text)
    return(json_result)


def backend_user(prefix, head, body, id):
    url = prefix + '/api/v2/backend/user/' + id
    res = requests.post(url, headers=head, json=body)
    return(res)


def apiFunction(prefix, head, apiName, way, body):
    resquestDic = {
        'post':requests.post,
        'put':requests.put,
        'patch':requests.patch,
        'get':requests.get,
        'delete':requests.delete}
    url = prefix + apiName
    if body:
        head['Content-Type'] = 'application/json'
        res1 = resquestDic[way](url, headers=head, json=body)
    else:
        if head.get('Content-Type'):
            del head['Content-Type']
        res1 = resquestDic[way](url, headers=head)
    # print(head)
    # print('url = %s, method= %s'% (url, way))
    # print(body) if body else print('no body')
    # pprint('status code = %d'%res1.status_code)
    # pprint(json.loads(res1.text))
    return res1

#打開 zego 聊天室，有標題，簡介
def open_zegoRoom(prefix, header1, title, description):
    url = prefix + '/api/v2/liveMaster/zego/liveRoom'
    body = {
         "title": title,
         "description": description,
        }
    res = requests.post(url, headers=header1, json=body)
    result = json.loads(res.text)
    room_id, streamId = result['data']['roomId'], result['data']['streamId']
    return (room_id, streamId)

#將字典檔轉為 url parameters
#EX: url = http://35.234.1.243/api/v2/backend/remittance/list
#EX: dict_params = {'userId': '', 'statusFilter': 'unapproved', 'item': 3, 'page': ''}
#return 結果為 http://35.234.1.243/api/v2/backend/remittance/list?statusFilter=unapproved&item=3

def get_my_points(prefix, header):
    url = '/api/v2/identity/myInfo'
    res = apiFunction(prefix, header, url, 'get', None)
    restext = json.loads(res.text)
    return (restext['data']['remainPoints'], restext['data']['revenueSummary'])

def get_my_points_from_db(db, identity_id):
    sql = "SELECT remain_points.remain_points, point_revenue_summary.point FROM remain_points join point_revenue_summary ON remain_points.identity_id = point_revenue_summary.identity_id WHERE point_revenue_summary.identity_id='{}'".format(identity_id)
    [(remain_points,point_revenue)]=dbConnect.dbQuery(db, sql, 'shocklee')
    return (remain_points, point_revenue)

def open_enter_ZegoRoom(prefix, header, title, description):
    result = get_personal_info(prefix, header)
    livemaster_id = result['id']
    room_id, _ = open_zegoRoom(prefix, header, title, description)
    sockinfo = get_load_balance(prefix, header)
    sip, sport = sockinfo['socketIp'], int(sockinfo['socketPort'])
    server_address = (sip, sport)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    chatlib.chat_room_auth(sock, header)
    chatlib.enterZego(sock, room_id)
    print("roomId:{}, livemaster_id:{}, sip:{}, sport:{}".format(room_id, livemaster_id, sip, sport))
    return  room_id, livemaster_id, sock, sip, sport


def dict_to_url_get(url, dict_params: dict):
    dict_params = { key : val for key,val in dict_params.items() if val is not None}
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(dict_params)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


def check_Remote_Output(hostAddr, cmd, keyfile = './id_rsa'):
    if not Path(keyfile).is_file(): print("rsa 檔案不存在")
    print(cmd)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostAddr, username='shocklee', key_filename=keyfile)
    _, stdout, _ = ssh.exec_command(cmd)
    result = stdout.read().decode()
    ssh.close()
    return result

def get_multiUsers_token_nonce(prefix, header, loginIdList:list):
    login_list = dict()
    time.sleep(random.randint(1, 10))
    for login_id in loginIdList:
        time.sleep(random.randint(1, 3))
        # result = user_login(test_parameter['prefix'], login_id, '12345')
        # token = login_id + 'token'
        # nonce = login_id + 'nonce'
        #///
        token = login_id
        nonce = login_id
        # while True:
        #     try:
        #         id = search_user(prefix, login_id, header)
        #         if id:
        #             break
        #     except:
        #         time.sleep(random.randint(3, 10))
        # login_list[id] = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': token, 'X-Auth-Nonce': nonce}
        login_list[login_id] = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': token, 'X-Auth-Nonce': nonce}
    return login_list


def get_game_url(playerType, hostId, userId, roomId, nickname):
    url = 'https://testing-game.xtars.com/games/up/v1/?'
    dictPara = {
        'playerType': playerType,
        'hostId': hostId,
        'userId': userId,
        'roomId': roomId,
        'nickname': nickname,
        'profilePicture':'https://test'
    }
    if playerType == 2:
        dictPara['points'] = 10000000
    return dict_to_url_get(url, dictPara)


def get_v2game_url(playerType, token, nonce, roomId):
    url = 'https://testing-game.xtars.com/games/up/v1/?'
    dictPara = {
        'playerType': playerType,
        'token': token,
        'nonce': nonce,
        'roomId': roomId,
    }
    return dict_to_url_get(url, dictPara)
