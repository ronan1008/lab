#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import multiprocessing
import apilib

#env = 'http://35.236.145.25:8080' #testing
env = 'http://104.199.175.123:80'  #Stage
header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}


def job(n, header1):
    str1 = 'master'
    idlist = []
    for i in range(10):
        k = str(n * 10 + i + 1)
        if (len(k)) == 1:
            account = str1 + '00' + k
        elif (len(k)) == 2:
            account = str1 + '0' + k
        #elif (len(k)) == 3:
        #    account = str1 + '0' + k
        else:
            account = str1 + k
        #account = 'lisa668'
        apilib.register(env, account, header1)
        uid = apilib.search_user(env, account, header1)
        apilib.change_user_mode(env, uid, -2, header1)
        apilib.change_user_mode(env, uid, 1, header1)
        apilib.set_bank(env, uid, header1)
        idlist.append(uid)
    # 1:admin;4:直撥主;5:一般用戶
    apilib.change_roles(env, idlist, header1, 4)
    return


if __name__ == '__main__':
    header1 = apilib.backend_login(env, 'tl-lisa', '12345678', header)
    numList = []
    for i in range(1):
        p = multiprocessing.Process(target=job, args=(i, header1,))
        numList.append(p)
    try:
        for p in numList:
            p.start()
    except Exception as e:
        print(e)
    finally:
        for p in numList:
            p.join()
        print('Process end.')
