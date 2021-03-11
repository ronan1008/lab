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


async def chat_room(live_info: dict, headers: dict, job_num: int):
    while True:
        chat_user = aio_chatlib.ChatUser()
        await chat_user.connect(live_info["serverIp"], int(live_info["port"]))
        await chat_user.auth(headers)
        await chat_user.join_room(live_info.get("roomId"))
        await gen.sleep(5)
        if not chat_user.room_id:
            raise Exception("Room In Timeout")
        else:
            print("stress%d join room-%d" % (job_num, chat_user.room_id))
        await gen.sleep(random.randint(30, 1800))
        await chat_user.leave_room()


async def choice_live_master(api_user: aio_apilib.ApiUser):
    live_master_list = await api_user.get_live_hot_list()
    enable_live_master_list = [
        live_master
        for live_master in live_master_list
        if live_master.get("roomStatus") == 1
    ]
    logging.info("直播主數量{}".format(len(enable_live_master_list)))
    if len(enable_live_master_list) == 0:
        raise AttributeError
    live_master = random.choice(enable_live_master_list)
    room_info = await api_user.get_room_info(live_master.get("liveMasterId"))
    return {
        "masterId": room_info.get("liveMasterId"),
        "roomId": room_info.get("roomId"),
        "serverIp": room_info.get("socketIp"),
        "port": room_info.get("socketPort"),
    }


async def job(user_account: str, job_number: int):
    try:

        api_user = aio_apilib.ApiUser(user_account, "123456")
        await api_user.login()
        live_master_info = await choice_live_master(api_user)
        await chat_room(live_master_info, api_user.headers, job_number)

    except AttributeError as err:
        logging.error(err, exc_info=True)
    except Exception as err:
        logging.error(err, exc_info=True)


async def robot_task():
    act = "stress"
    for i in range(2000, 3000):
        k = str(i + 1)
        if (len(k)) == 1:
            account = act + "000" + k
        elif (len(k)) == 2:
            account = act + "00" + k
        elif (len(k)) == 3:
            account = act + "0" + k
        else:
            account = act + k
        ioloop.IOLoop.current().spawn_callback(job, account, i)
        await gen.sleep(0.5)


if __name__ == "__main__":
    ioloop.IOLoop.current().spawn_callback(robot_task)
    ioloop.IOLoop.current().start()
