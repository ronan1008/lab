#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import apilib

#env = 'http://35.236.145.25:8080' #testing
env = 'http://104.199.175.123:80'  #Stage
header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}

if __name__ == '__main__':
    idlist = []
    accList = ['qa-cs', 'qa-cs1', 'qa-market', 'qa-market1', 'qa-project', 'qa-project1']
    header1 = apilib.backend_login(env, 'tl-lisa', '12345678', header)
    for i in accList:
        apilib.register(env, i, header1)
        uid = apilib.search_user(env, i, header1)
        apilib.change_user_mode(env, uid, -2, header1)
        apilib.change_user_mode(env, uid, 1, header1)
        apilib.set_bank(env, uid, header1)
        idlist.append(uid)
    # 1:admin;4:直撥主;5:一般用戶
    apilib.change_roles(env, idlist, header1, 5)