from typing import List

from tornado.options import parse_config_file, parse_command_line, define

define("log_level", default="ERROR", help="root log level", type=str)


define(
    "api_url", default="http://testing-api.truelovelive.com.tw", type=str,
)

define(
    "gift_ids", default=["1d1453f1-beb3-46c7-be71-40928c9d5d79"], type=List,
)
define(
    "msg_list", default=["hello", "大家好", "主播好正", "你想吃啥?", "今天心情不美麗"], type=List,
)


parse_config_file("./client.conf")
parse_command_line()
