#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import config_define
from tornado.options import options
import aio_chatlib

import logging
import random
import socket
import time

from tornado import ioloop, gen

import aio_apilib

logging.root.setLevel(options.log_level)


async def job(user_account):
    try:
        api_user = aio_apilib.ApiUser(user_account, "123456")
        await api_user.login()
        sock_info = await api_user.get_load_balance()
        print(sock_info)
        ip = sock_info.get("socketIp")
        port = int(sock_info.get("socketPort"))
        print("server ip: %s; server port: %d" % (ip, port))
        chat_user = aio_chatlib.ChatUser()
        await chat_user.connect(ip, port)
        await chat_user.auth(api_user.headers)
        await chat_user.new_room("測試開播{}".format(user_account))
        await gen.sleep(5)
        print("room_id = {}".format(chat_user.room_id))
        await gen.sleep(4500)
        await chat_user.leave_room()
    except Exception as e:
        print(e)


async def robot_task():
    act = "master"
    for i in range(0, 100):
        k = str(i + 1)
        if (len(k)) == 1:
            account = act + "000" + k
        elif (len(k)) == 2:
            account = act + "00" + k
        elif (len(k)) == 3:
            account = act + "0" + k
        else:
            account = act + k
        ioloop.IOLoop.current().spawn_callback(job, account)
        await gen.sleep(0.5)


if __name__ == "__main__":

    ioloop.IOLoop.current().spawn_callback(robot_task)
    ioloop.IOLoop.current().start()
