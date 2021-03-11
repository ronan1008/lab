import json
import logging
from datetime import datetime


class Event:
    event: str
    data: dict
    sendTime: int

    def __init__(
        self,
        event: str,
        data: dict = None,
        sendTime=int(datetime.utcnow().timestamp() * 1000),
    ):
        self.event = event
        self.data = data if data else {}
        self.sendTime = sendTime

    def __str__(self):
        return "Response: \n" + json.dumps(self.__dict__)


class Action:
    action: str
    data: dict

    def __init__(self, action: str, data: dict = None):
        self.action = action
        self.data = data if data else {}

    def to_bytes(self):
        logging.debug(self.action)
        logging.debug(self.data)
        return bytes(json.dumps(self.__dict__), encoding="utf-8") + b"\n"
