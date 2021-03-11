#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import json
import requests
import multiprocessing
import time

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


def get_personal_info(prefix, header):
    url = prefix + '/api/v1/personal/info'
    res = requests.get(url, headers=header)
    return(res)


def search_user(prefix, account, header):
    uid = ''
    url = prefix + '/api/v1/backend/identity/search'
    body = {"input": account, "page": 0, "size": 10, "statuses": []}
    res = requests.post(url, headers=header, json=body)
    str1 = res.text
    json_result = json.loads(str1)
    if json_result['totalCount'] != 0:
        for i in range(json_result['totalCount']):
            if json_result['data'][i]['loginId'] == account:
                uid = json_result['data'][i]['id']
    return(uid)


def change_user_mode(prefix, id, mode, header):
    #V1
    #url = prefix + '/api/v1/backend/user/' + id
    #body = {'identityStatus': mode, 'id': id}
    #V2
    url = prefix + '/api/v2/backend/user/' + id
    body = {'identityStatus': mode}
    requests.post(url, headers=header, json=body)
    return


def job1(test_account , env):
    reproduce = 0
    head = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
    head1 = user_login(env, test_account, '123456', head)
    print(head1)
    while 1:
        result = get_personal_info(env, head1)
        if result.status_code == 401:
            print('get personal info = %d' % result.status_code)
            break
        reproduce += 1
    return()


def job2(test_account , env):
    time.sleep(15)
    head = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
    head1 = user_login(env, 'tl-lisa', '12345678', head)
    uid = search_user(env, test_account, head1)
    change_user_mode(env, uid, -2, head1)
    time.sleep(1)
    change_user_mode(env, uid, 1, head1)
    return()


if __name__ == '__main__':
    test_count = 1
    test_account = 'qatest123'
    #env = 'http://35.236.145.25:8080' #test
    env = 'http://104.199.175.123:80' #stage
    while 1:
        print('第%d次測試開始' % test_count)
        numList = []
        numList.append(multiprocessing.Process(target=job1, args=(test_account, env, )))
        numList.append(multiprocessing.Process(target=job2, args=(test_account, env, )))
        try:
            for p in numList:
                p.start()
        finally:
            for p in numList:
                p.join()
            test_count += 1
            if test_count > 30:
                break
    print('測試結束')
