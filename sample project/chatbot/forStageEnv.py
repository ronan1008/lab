import os
import requests
import pytz
import paramiko
import time
import fnmatch
import json
import pytest
import threading
import pytest_check as check
from pathlib import Path
from pprint import pprint
from datetime import datetime, timedelta
from dbConnect import dbQuery, dbSetting,  SshMySQL
from analysis_log import read_multi_json_file, filter_events, analyze_chatBot_gift_broadcast_events, analyze_chatBot_entry_gift_time, taipei_str_to_taipei_timestamp
from analysis_log import check_chatBot_entry_gift_interval, analyze_chatBot_gift_and_sendTime, timestamp_to_utc_str


# api
def apiFunction(prefix, head, apiName, way, body):
    request_methods = {
        'post':requests.post,
        'put':requests.put,
        'patch':requests.patch,
        'get':requests.get,
        'delete':requests.delete}
    url = prefix + apiName
    print(url)
    if body:
        head['Content-Type'] = 'application/json'
        res1 = request_methods[way](url, headers=head, json=body, allow_redirects=False)
    else:
        if head.get('Content-Type'):
            del head['Content-Type']
        res1 = request_methods[way](url, headers=head)
    return res1

def user_login(prefix, account, pwd):
    url = prefix + '/api/v2/identity/auth/login'
    body = {
        "account": account,
        "password": pwd,
        "pushToken": ''
    }
    res = requests.post(url, json=body)
    if res.status_code // 100 == 2:
        restext = json.loads(res.text)
        return(restext)
    else:
        return(json.loads(res.text))

def get_id_from_chatbot_promotionTicket_list(prefix, header, start_time, end_time):
    api_name = f"/api/v3/backend/chatbot/promotionTicket/list?item=100&page=1"
    res = apiFunction(prefix, header, api_name, 'get', None)
    proTick_list = (res.json())['data']
    for i in proTick_list:
        if i['startTime'] == start_time and i['endTime'] == end_time:
            id = i['id']
    return id

def put_chatbot_promotionTicket(prefix, header, **ticket_info):
    required_args = ['startTime', 'endTime', 'startHour',
                     'endHour', 'totalPoints', 'reference',
                     'status', 'gift']
    missing_args = [arg for arg in required_args if arg not in ticket_info]
    if missing_args:
        raise TypeError(f"Missing arguments: {', '.join(missing_args)}")
    body = {key: value for key, value in ticket_info.items() if value}
    if body.get('id'):
        api_name = f"/api/v3/backend/chatbot/promotionTicket/{body['id']}"
        del body['id']
    else :
        api_name = f"/api/v3/backend/chatbot/promotionTicket/"
    print(prefix)
    print(header)
    print(api_name)
    pprint(body)
    res = apiFunction(prefix, header, api_name, 'put', body)
    return res

def get_chatbot_promotionTicket_insight(prefix, header, id, item, page):
    api_name = f"/api/v3/backend/chatbot/promotionTicket/{id}/insight?item={item}&page={page}"
    res = apiFunction(prefix, header, api_name, 'get', None)
    return res

def add_points(prefix, header, addpoints, targetUserId):
    api_name = "/api/v2/backend/identity/points"
    body = {
    "addPoints":addpoints,
    "reason":"shock Test",
    "targetUserId":targetUserId
    }
    res = apiFunction(prefix, header, api_name, 'put', body)
    return res

if __name__ == '__main__':

# Settings
    host = "staging-api.xtars.com"
    # host = '34.81.211.190'

    prefix = f'http://{host}'
    restext = user_login(prefix, 'changjusin', '123456')
    # restext = user_login(prefix, 'tl-lisa', '12345678')

    header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': restext['data']['token'], 'X-Auth-Nonce': restext['data']['nonce']}
    # apiname = '/api/v2/identity/myInfo'
    # res = apiFunction(prefix, header, apiname, 'get', None)

    # print(res.json())


    # print('-------------------------------------------------')




    # res = add_points(prefix, header, 10000, 'fb51fd1d-838f-4cd3-bffe-4d48a569ce2a')
    # print(res)
    # pprint(res.json())

    # res = put_chatbot_promotionTicket(prefix, header,
    #     startTime = 1679374791,
    #     endTime = 1679823111,
    #     startHour = 1000,
    #     endHour = 1900,
    #     totalPoints = 10000,
    #     reference = 'https://dummyimage.com/600x400/000/fff&text=Dummy+Image',
    #     status = None,
    #     gift = [966, 705]
    # )
    # print(res.json())



    # api_name = f"/api/v2/backend/chatBotSetting"
    # res = apiFunction(prefix, header, api_name, 'get', None)
    # pprint(res.json())

    # api_name = f"/api/v3/backend/chatbot/promotionTicket/list?item=100&page=1"
    # res = apiFunction(prefix, header, api_name, 'get', None)
    # pprint(res.json())
