#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import logging
from typing import List

import aiohttp

from aiohttp import ClientError
from tornado.options import options


class ApiUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {"Content-Type": "application/json", "Connection": "Keep-alive"}

    async def login(self):
        body = {"loginId": self.username, "password": self.password}
        url = options.api_url + "/api/v1/auth/login"
        try:
            async with aiohttp.request(
                "POST", url, headers=self.headers, data=json.dumps(body),
            ) as resp:
                if resp.status == 200:
                    resp_body = await resp.text()
                    json_result: dict = json.loads(resp_body)
                    self.headers.update(
                        {
                            "X-Auth-Token": json_result.get("token"),
                            "X-Auth-Nonce": json_result.get("nonce"),
                        }
                    )

        except ClientError as err:
            print("account %s login failed" % self.username)
            logging.error(err, exc_info=True)

    async def get_room_info(self, live_master_id) -> dict:
        room_info = {"roomId": 0, "socketIp": "", "socketPort": ""}
        url = options.api_url + "/api/v1/live/info/{}".format(live_master_id)
        try:
            async with aiohttp.request("GET", url, headers=self.headers) as resp:
                if resp.status == 200:
                    resp_body = await resp.text()
                    if resp_body != "":
                        json_result: dict = json.loads(resp_body)
                        room_info.update(
                            {
                                "roomId": json_result.get("roomId"),
                                "socketIp": json_result.get("socketIp"),
                                "socketPort": json_result.get("socketPort"),
                            }
                        )
        except ClientError as err:
            logging.error(err, exc_info=True)
        return room_info

    async def get_live_hot_list(self) -> List[dict]:
        result = ""
        url = options.api_url + "/api/v1/live/hotList/10000/0"
        try:
            async with aiohttp.request("GET", url, headers=self.headers) as resp:
                if resp.status == 200:
                    resp_body = await resp.text()
                    json_result: dict = json.loads(resp_body)
                    result = json_result.get("liveList")
        except ClientError as err:
            logging.error(err, exc_info=True)
        return result

    async def get_load_balance(self) -> dict:
        url = options.api_url + "/api/v1/live/loadBalance"
        result = {}
        try:
            async with aiohttp.request("GET", url, headers=self.headers) as resp:
                if resp.status == 200:
                    resp_body = await resp.text()
                    result = json.loads(resp_body)
        except ClientError as err:
            logging.error(err, exc_info=True)
        return result
