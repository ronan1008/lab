import json
import pytz
import pymysql
import math
import pytest_check as check
from pprint import pprint
from datetime import datetime
from sshtunnel import SSHTunnelForwarder, create_logger
from pathlib import Path
from dbConnect import dbQuery, dbSetting
from collections import defaultdict
from argparse import ArgumentParser

class ArgumentParserError(Exception):
    pass

class ThrowingArgumentParser(ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

def process_args():
    parser = ThrowingArgumentParser(description="python3 analysis_log.py --input_file tmp_logs_202303062332/dataParse_20230306_233237.log tmp_logs_202303062332/dataParse_20230306_233325.log")
    parser.add_argument("--input_file", nargs='*')
    # parser.add_argument("-v", "--verbose", help="Show more details", action='store_true')
    return parser.parse_args()

def read_json_file(filename):
    data_str = ""
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data_str += line
        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            print(f"Invalid JSON: {data_str}")
            data = None
    return data

def filter_events(listData: list, eventList: list):
    after_filter = []
    for master in listData:
        account_dict = {"account": master["account"], "data": []}
        for i in filter(lambda x: x["event"] in eventList, master["data"]):
            account_dict["data"].append(i)
        after_filter.append(account_dict)

    return after_filter


def analyze_chatBot_gift_and_sendTime(data_list, adv_chatBots):
    records = []
    for x in data_list:
        for i in x['data']:
            if i['event'] == 'gift_bcst':
                fromUser_id = i['payload']['data']['fromUser']['id']
                targetUser_id = i['payload']['data']['targetUser']['id']
                gift_sendTime = i['payload']['sendTime'] / 1000
                sendTime_str = timestamp_to_taipei_str(gift_sendTime)
                gift_name = i['payload']['data']['gift']['name']['zh_TW']
                if adv_chatBots:
                    if fromUser_id in adv_chatBots:
                        records.append(  {'fromUser':fromUser_id,  'targetUser':targetUser_id, 'sendTime':gift_sendTime, 'sendTime_str':sendTime_str,  'giftName':gift_name } )

                else:
                    records.append(  {'fromUser':fromUser_id,  'targetUser':targetUser_id, 'sendTime':gift_sendTime, 'sendTime_str':sendTime_str,  'giftName':gift_name } )
    return records

def analyze_chatBot_gift_broadcast_events(data_list, adv_chatBots):
    records = []
    for x in data_list:
        for i in x['data']:
            if i['event'] == 'gift_bcst':
                fromUser_id = i['payload']['data']['fromUser']['id']
                gift_count = i['payload']['data']['gift']['count']
                gift_points = i['payload']['data']['gift']['totalPoints']
                gift_name = i['payload']['data']['gift']['name']['zh_TW']
                if adv_chatBots:
                    if fromUser_id in adv_chatBots:
                        # records.append(  {'fromUser':fromUser_id,  'giftcount':gift_count,  'giftPoints':gift_points, 'giftName': gift_name } )
                        records.append(  {'fromUser':fromUser_id,  'giftcount':gift_count,  'giftPoints':gift_points } )

                else:
                    # records.append(  {'fromUser':fromUser_id,  'giftcount':gift_count,  'giftPoints':gift_points, 'giftName': gift_name } )
                    records.append(  {'fromUser':fromUser_id,  'giftcount':gift_count,  'giftPoints':gift_points })

    new_dict = {}
    for record in records:
        if record['fromUser'] not in new_dict:
            # new_dict[record['fromUser']] = {'giftPoints':record['giftPoints'], 'giftcount': record['giftcount'],  'giftName': set()}
            new_dict[record['fromUser']] = {'giftPoints':record['giftPoints'], 'giftcount': record['giftcount']}

        else:
            new_dict[record['fromUser']]['giftPoints'] += record['giftPoints']
            new_dict[record['fromUser']]['giftcount'] += record['giftcount']
            # new_dict[record['fromUser']]['giftName'].add(record['giftName'])

    new_list = []
    for k, v in new_dict.items():
        # new_list.append({"id": k , "points": v['giftPoints'], "giftCount": v['giftcount'], "giftName": list(v['giftName'])})
        new_list.append({"id": k , "points": v['giftPoints'], "giftCount": v['giftcount']})

    return new_list

def read_multi_json_file(logFiles):
    data_list = []
    for logFile in logFiles:
        # print(logFile)
        data_dict = read_json_file(logFile)
        data_list += data_dict
    return data_list

def timestamp_to_taipei_datetime(timestamp):
    taipei_tz = pytz.timezone('Asia/Taipei')
    dt = datetime.fromtimestamp(timestamp)
    # print('xxxxxxx')
    # print(dt)
    # print('xxxxxxx')
    taipei_datetime = dt.astimezone(taipei_tz)
    # taipei_datetime = taipei_tz.localize(dt)
    # print('uuuuuuuuuuu')
    # print(taipei_datetime)
    # print('uuuuuuuuuuu')

    return taipei_datetime

def timestamp_to_taipei_str(timestamp):
    taipei_datetime = timestamp_to_taipei_datetime(timestamp)
    taipei_datetime_str = taipei_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return taipei_datetime_str

def timestamp_to_utc_str(timestamp):
    utc_tz = pytz.timezone('UTC')
    dt = datetime.fromtimestamp(timestamp)
    taipei_datetime = dt.astimezone(utc_tz)
    taipei_datetime_str = taipei_datetime.strftime('%Y%m%d %H:%M:%S')
    return taipei_datetime_str

def taipei_str_to_taipei_timestamp(taipei_str):
    taipei_tz = pytz.timezone('Asia/Taipei')
    if '-' in taipei_str:
        naive_datetime = datetime.strptime(taipei_str, '%Y-%m-%d %H:%M:%S')
    else:
        naive_datetime = datetime.strptime(taipei_str, '%Y%m%d %H:%M:%S')
    taipei_datetime = taipei_tz.localize(naive_datetime)
    return taipei_datetime.timestamp()
    # taipei_datetime = taipei_timestamp_to_taipei_datetime(taipei_timestamp)
    # taipei_datetime_str = taipei_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # return taipei_datetime_str


def analyze_chatBot_entry_gift_time(data_list, adv_chatBots):
    extract_dict = defaultdict(list)
    for acc in data_list:
        if 'master' in acc['account']:
            for i in acc['data']:
                event = i['event']
                fromUser_id = i['payload']['data']['fromUser']['id']
                sendTime_ts = i['payload']['sendTime']
                sendTime_str = timestamp_to_taipei_str(sendTime_ts/1000)
                key = f"{i['topic']}:{fromUser_id}"
                if adv_chatBots:
                    if fromUser_id in adv_chatBots:
                        extract_dict[key].append({
                            'event': event,
                            'fromUser': fromUser_id,
                            'sendTime': sendTime_ts,
                            'sendTime_str': sendTime_str
                        })
                else:
                    extract_dict[key].append({
                        'event': event,
                        'fromUser': fromUser_id,
                        'sendTime': sendTime_ts,
                        'sendTime_str': sendTime_str
                    })
    new_extract_dict = defaultdict(list)
    for room_idty in extract_dict:
        for i, _ in enumerate(extract_dict[room_idty]):
            if len(extract_dict[room_idty]) > 1 and i < len(extract_dict[room_idty]) -1:
                if extract_dict[room_idty][i].get('event') == 'room_in_bcst' and extract_dict[room_idty][i+1].get('event') == 'gift_bcst':
                    new_extract_dict[room_idty].extend([
                        {
                        'event': extract_dict[room_idty][i]['event'],
                        'fromUser': extract_dict[room_idty][i]['fromUser'],
                        'sendTime': extract_dict[room_idty][i]['sendTime'],
                        'sendTime_str': extract_dict[room_idty][i]['sendTime_str']
                        },
                        {
                        'event': extract_dict[room_idty][i+1]['event'],
                        'fromUser': extract_dict[room_idty][i+1]['fromUser'],
                        'sendTime': extract_dict[room_idty][i+1]['sendTime'],
                        'sendTime_str': extract_dict[room_idty][i+1]['sendTime_str']
                        },
                    ])
    new_extract_dict = dict(new_extract_dict)
    return new_extract_dict

# check function
def check_chatBot_entry_gift_interval(entry_gift_record, minSeconds, maxSeconds):
    """
    Check Function
    """
    if entry_gift_record:
        for roomIdty, records_list in entry_gift_record.items():
            for i, record in enumerate(records_list):
                if records_list[i]['event'] == 'room_in_bcst' and i < len(records_list) -1 :
                    interval = (records_list[i+1]['sendTime'] - records_list[i]['sendTime']) / 1000
                    print(records_list[i])
                    print(interval)

                check.greater_equal(math.ceil(interval), minSeconds, f'{roomIdty} : Time Interval -> {interval} less than {minSeconds}')
                check.less_equal(math.ceil(interval), maxSeconds, f'{roomIdty} : Time Interval -> {interval} greater than {maxSeconds}')


def debug(data_list, adv_chatBots):
    extract_dict = defaultdict(list)
    for acc in data_list:
        if 'master' in acc['account']:
            for i in acc['data']:
                event = i['event']
                fromUser_id = i['payload']['data']['fromUser']['id']
                sendTime_ts = i['payload']['sendTime']
                sendTime_str = timestamp_to_taipei_str(sendTime_ts/1000)
                key = f"{i['topic']}:{fromUser_id}"
                if adv_chatBots:
                    if fromUser_id in adv_chatBots:
                        extract_dict[key].append({
                            'event': event,
                            'fromUser': fromUser_id,
                            'sendTime': sendTime_ts,
                            'sendTime_str': sendTime_str
                        })
                else:
                    extract_dict[key].append({
                        'event': event,
                        'fromUser': fromUser_id,
                        'sendTime': sendTime_ts,
                        'sendTime_str': sendTime_str
                    })
    return extract_dict

if __name__ == "__main__":

    def get_advanced_chatBot_list(db):
        sql = 'SELECT id FROM chatbot Where advanced = 1'
        result = dbQuery(db, sql, 'shocklee')
        chatBot_list = []
        for i in result:
            chatBot_list.append(i[0])
        return chatBot_list
    args = process_args()
    logFiles = args.input_file
    data_list = read_multi_json_file(logFiles)
    filter_data = filter_events(data_list, [ 'gift_bcst', 'room_in_bcst'])


    adv_chatBots_example = None
    chatBot_gift_total = analyze_chatBot_gift_broadcast_events(filter_data, adv_chatBots=adv_chatBots_example)
    entry_gift_records = analyze_chatBot_entry_gift_time(filter_data, adv_chatBots=adv_chatBots_example)
    chatBot_gift_send_records = analyze_chatBot_gift_and_sendTime(filter_data, adv_chatBots=adv_chatBots_example)

    adv_chatBots =  get_advanced_chatBot_list('34.81.211.190')
    pprint(adv_chatBots)

    pprint(chatBot_gift_total)
    print('-----------------------------------')
    pprint(entry_gift_records)
    print('-----------------------------------')
    pprint(chatBot_gift_send_records)
    adv_chatBots =  get_advanced_chatBot_list('34.81.211.190')
    print('-----------------------------------')

    a = debug(filter_data, adv_chatBots=None)
    pprint(a)
    # round1_Start = '2023-03-07 07:00:00'
    # round1_End = '2023-03-07 07:59:59'
    # round1_Start_ts = taipei_str_to_taipei_timestamp(round1_Start)
    # round1_End_ts = taipei_str_to_taipei_timestamp(round1_End)

    # print(round1_Start_ts, round1_End_ts)

    # find_round1_record, find_round2_record = False, False
    # for record in chatBot_gift_send_records:
    #     if round1_Start_ts <= record['sendTime'] <= round1_End_ts:
    #         find_round1_record = True
    #         # assert record['giftName'] in ...
    #     elif round1_Start_ts <= record['sendTime'] <= round1_End_ts:
    #         find_round2_record = True
    #         # assert record['giftName'] in ...
    # assert find_round1_record == True
    # assert find_round2_record == False


    # # check_chatBot_entry_gift_interval(chatBot_gift_total, 30, 60)