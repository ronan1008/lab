#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import json
import requests
import urllib3
import utilitylib

def backend_login(prefix, account, pwd, header):
    url = prefix + '/api/v1/auth/blogin'
    body = {"loginId": account, "password": pwd}
    res = requests.post(url, json=body)
    str1 = res.text
    json_result = json.loads(str1)
    header['X-Auth-Token'] = json_result['token']
    header['X-Auth-Nonce'] = json_result['nonce']
   # print(header)
    return(header)


def user_login(prefix, account, pwd, header):
    url = prefix + '/api/v1/auth/login'
    body = {'loginId': account, 'password': pwd}
    res = requests.post(url, json=body)
    str1 = res.text
    if str1.find('token') > 0:
        json_result = json.loads(str1)
        header['X-Auth-Token'] = json_result['token']
        header['X-Auth-Nonce'] = json_result['nonce']
    else:
        print('account %s login failed' % account)
    return(header)


def register(prefix, account, header):
    url = prefix + '/api/v1/identity/register'
    body = {"loginId": account, 'password': '123456', 'publicSexInfo': False}
    requests.post(url, headers=header, json=body)
    #str1 = res.text
    #print(str1)
    return


def search_user(prefix, account, header):
    uid = ''
    url = prefix + '/api/v1/backend/identity/search'
    body = {"input": account, "page": 0, "size": 10, "statuses": []}
    res = requests.post(url, headers=header, json=body)
    str1 = res.text
    print(str1)
    json_result = json.loads(str1)
    if json_result['totalCount'] != 0:
        for i in range(json_result['totalCount']):
            if json_result['data'][i]['loginId'] == account:
                uid = json_result['data'][i]['id']
                break
    return(uid)


def change_user_mode(prefix, id, mode, header):
    url = prefix + '/api/v1/backend/user/' + id
    body = {'identityStatus': mode, 'id': id}
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


def set_tracking(prefix, header, bid):
    url = prefix + '/api/v1/track/tracking/' + bid
    body = {}
    res = requests.post(url, headers=header, json=body)
    if res.status_code == 200:
        print('tracking OK')
    return


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


def get_live_hot_list(prefix, apiname, header):
    url = prefix + '/api/v1/live/' + apiname + '/10000/0'
    res = requests.get(url, headers=header)
    if res.status_code != 200:
        result = ''
    else:
        json_result = json.loads(res.text)
        result = json_result['liveList']
    return(result)


def apply_to_master(prefix, account, ihash, header):
    print('apply to master')
    url = prefix + '/api/v1/personal/apply'
    body = {'email': 'test123@truelovelive.dev', 'imageHash': ihash, 'name': account, 'phoneNumber': '0988111111'}
    res = requests.post(url, json=body, headers=header)
    if res.status_code != 200:
        str1 = res.text
        print(str1)
    return


def image_create1(prefix, header):
    print('image_create')
    url = prefix + '/api/v1/image/create/personal'
    form_result = utilitylib.crate_form_data(['img', 'img', 'C:\\test\\image1.png', 'image/png'])
    header['Content-Type'] = ('multipart/form-data; boundary=%s' % form_result[1])
    res = requests.post(url, data=form_result[0], headers=header)
    if res.status_code != 200:
        str1 = ''
        print(res.text)
    else:
        str1 = res.text
    return(str1)

def set_bank(prefix, bid, header):
    url = prefix + '/api/v1/identity/' + bid + '/account'
    body = {'accountNo': '0', 'bankName': '0', 'branchBank': '0', 'branchNo': '0'}
    res = requests.put(url, headers=header, json=body)
    if res.status_code != 200:
        str1 = res.text
        print(str1)
    return


def change_roles(prefix, bid, header, rtype):
    url = prefix + '/api/v1/backend/identity/roles'
    body = {'identityId': bid, 'roleType': rtype}
    res = requests.put(url, headers=header, json=body)
    if res.status_code != 200:
        str1 = res.text
        print(str1)
    return


def get_load_balance(prefix, header):
    url= prefix + '/api/v1/live/loadBalance/'
    res = requests.get(url, headers=header)
    str1 = res.text
    if res.status_code != 200:
        print(str1)
        json_result = ''
    else:
        json_result = json.loads(str1)
    return(json_result)


def get_live_master_info(prefix, header, mid):
    url = prefix + '/api/v1/live/masterInfo/' + mid
    print(url)
    res = requests.get(url, headers=header)
    str1 = res.text
    if res.status_code != 200:
        print(str1)
        json_result = ''
    else:
        json_result = json.loads(str1)
    return(json_result)


def edit_personal_info(prefix, header, desc, nickname):
    url = prefix + '/api/v1/personal/info'
    body = {'age': 60, 'desc': desc, 'email': '', 'imageHash': '', 'newPassword': '123456', 'nickname': nickname, 'sex': 0}
    res = requests.post(url, headers=header, json=body)
    str1 = res.text
    if res.status_code != 200:
        print(str1)
    return()

