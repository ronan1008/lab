#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# encoding: utf-8
import json
import logging
import time
import socket


# import sys
# from importlib import reload

# reload(sys)
# sys.setdefaultencoding('utf-8')
from json import JSONDecodeError

from tornado import iostream, gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError

import data_type


class ChatUser:

    remain_points = 0
    roles = []
    is_master = False
    room_id: int = None
    is_stay = True
    is_gift = True

    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = iostream.IOStream(s)
        IOLoop.current().add_callback(self.handle_stream)

    async def handle_stream(self):
        try:
            while True:
                data = await self.stream.read_until(b"\n")
                data_str = str(data, encoding="utf-8").strip()
                input_data = json.loads(data_str)
                event = data_type.Event(**input_data)
                if event.event == "AUTH":
                    self.remain_points = event.data.get("remainPoints")
                    self.roles = event.data.get("roles")
                elif event.event == "ROOM_NEW":
                    self.is_master = True
                elif event.event == "ROOM_IN":
                    self.room_id = event.data.get("roomId")
                elif event.event == "ROOM_EXITED":
                    self.is_stay = False

        except StreamClosedError as err:
            logging.error("%s disconnected")
        except Exception as err:
            logging.error(err, exc_info=True)

    async def handle_ping(self):
        while True:
            await gen.sleep(30)
            ping_action = data_type.Action("PING")
            await self.stream.write(ping_action.to_bytes())

    async def connect(self, ip: str, port: int):
        await self.stream.connect((ip, port))
        IOLoop.current().add_callback(self.handle_ping)

    async def auth(self, header: dict):
        auth_action = data_type.Action(
            "AUTH",
            {"token": header.get("X-Auth-Token"), "nonce": header.get("X-Auth-Nonce")},
        )
        await self.stream.write(auth_action.to_bytes())

    async def join_room(self, room_id: int):
        join_room_action = data_type.Action("IN_ROOM", {"roomId": room_id})
        await self.stream.write(join_room_action.to_bytes())

    async def leave_room(self):
        leave_room_action = data_type.Action("LEAVE_ROOM", {"roomId": self.room_id})
        await self.stream.write(leave_room_action.to_bytes())

    async def send_message(self, message: str, room_id: int):
        send_message_action = data_type.Action(
            "MESSAGE", {"roomId": room_id, "content": message}
        )
        await self.stream.write(send_message_action.to_bytes())

    async def send_gift(self, gift_id, live_master_id):
        send_gift_acton = data_type.Action(
            "GIFT", {"giftId": gift_id, "userId": live_master_id, "count": 1}
        )
        await self.stream.write(send_gift_acton.to_bytes())

    async def ping_action(self):
        result = 0
        ping_action = data_type.Action("PING", {})
        await self.stream.write(ping_action.to_bytes())

    async def new_room(self, room_title: str):
        new_room_action = data_type.Action("NEW_ROOM", {"title": room_title})
        await self.stream.write(new_room_action.to_bytes())
