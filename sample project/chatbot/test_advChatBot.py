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

def table_referenced_list(db, tableName, sshUser, del_list:list=[], truncate_list:list=[])-> list:
    ref_sql = '''
    select table_name from information_schema.KEY_COLUMN_USAGE where table_schema = 'live_casting' and referenced_table_name = '{}';
    '''.format(tableName)
    result = dbQuery(db, ref_sql, sshUser)
    if len(result) == 0:
        truncate_list.append(tableName)
    else:
        for row in result:
            refTable = row[0]
            if refTable not in del_list:
                del_list.insert(0, refTable)
                del_list, truncate_list = table_referenced_list(db, refTable, sshUser, del_list, truncate_list)

    for i in del_list:
        if i in truncate_list:
            del_list.remove(i)

    if tableName in del_list:
        del_list.remove(tableName)
    del_list.append(tableName)
    truncate_list = list(set(truncate_list))
    return [del_list, truncate_list]

def clear_relative_table(db, table, sshUser):
    print(f"\n Starting Clean ref table by {table}")
    del_list, truncate_list = table_referenced_list(db, table, sshUser)
    livedb = SshMySQL(db, sshUser)
    del_sql = []
    for table in truncate_list:
        del_sql.append('TRUNCATE TABLE {}'.format(table))
    for table in del_list:
        del_sql.append('DELETE FROM {}'.format(table))
        del_sql.append('ALTER TABLE {} auto_increment = 1'.format(table))

    livedb.execLists(del_sql)
    livedb.close()

def get_remain_points(host, identity_id):
    remain_points_sql = f"select remain_points from remain_points where identity_id = '{identity_id}'"
    [(remain_points,)] = dbQuery(host, remain_points_sql, 'shocklee')
    return remain_points

# api
def apiFunction(prefix, head, apiName, way, body):
    request_methods = {
        'post':requests.post,
        'put':requests.put,
        'patch':requests.patch,
        'get':requests.get,
        'delete':requests.delete}
    url = prefix + apiName
    if body:
        head['Content-Type'] = 'application/json'
        res1 = request_methods[way](url, headers=head, json=body)
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
        api_name = f"/api/v3/backend/chatbot/promotionTicket"
    print(api_name)
    pprint(body)
    res = apiFunction(prefix, header, api_name, 'put', body)
    return res

def get_chatbot_promotionTicket_insight(prefix, header, id, item, page):
    api_name = f"/api/v3/backend/chatbot/promotionTicket/{id}/insight?item={item}&page={page}"
    res = apiFunction(prefix, header, api_name, 'get', None)
    return res

# remote
def execute_remote_command(host, cmd):
    print(f"Command: {cmd}")
    keyfile = str(Path.home()) + '/.ssh/id_rsa' #SSH密钥
    if not Path(keyfile).is_file():
        print("RSA file does not exist.")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='shocklee', key_filename=keyfile)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    try:
        result = stdout.read().decode()
    except Exception as e :
        print(e)
        result = ''
    ssh.close()
    return result

def update_remote_time(host, set_time):
    time.sleep(10)
    return execute_remote_command(host, f'sudo -S date -s "{set_time}"')

def correct_remote_system_time(host):
    return execute_remote_command(host, f'sudo ntpdate time.stdtime.gov.tw')

def download_file_and_delete_from_remote(remote_host, remote_path, local_path, filename_pattern="*"):
    keyfile = str(Path.home()) + '/.ssh/id_rsa' #SSH密钥
    if not Path(keyfile).is_file():
        print("RSA file does not exist.")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_host, username='shocklee', key_filename=keyfile)
    sftp = ssh.open_sftp()
    remote_files = sftp.listdir(remote_path)
    matched_files = fnmatch.filter(remote_files, filename_pattern)
    download_file_list = []
    for file in matched_files:
        remote_file_path = os.path.join(remote_path, file)
        local_file_path = os.path.join(local_path, file)
        try:
            sftp.get(remote_file_path, local_file_path)  # Download file via SFTP
            print(f"Downloaded file: {file}")
            sftp.remove(remote_file_path)
            print(f"Remote file deleted: {file}")
            download_file_list.append(local_file_path)
        except Exception as e:
            print(e)
    sftp.close()
    ssh.close()
    return download_file_list

def run_wsTest_and_generate_new_log(cmd):
    res = execute_remote_command(host, f'. ./env/bin/activate; cd tl-QA/autoTest/wsTest;  {cmd}')
    # res = execute_remote_command(host, '. ./env/bin/activate; cd tl-QA/autoTest/wsTest;  pytest -s jason_test.py --m master01 master02 --t default.json5')
    res = execute_remote_command(host, 'cd /home/shocklee/tl-QA/autoTest/wsTest ; ls check_autobot_enter_without_normal_user*')
    ori_filename = res.strip()
    if ori_filename :
        file_part = ori_filename.split(".")[0]
        date_part = file_part.split("_")[6] + '_' + file_part.split("_")[7]
        aft_filename = f"arrange{date_part}.log"
        res = execute_remote_command(host, "cd /home/shocklee/tl-QA/autoTest/wsTest ; mv check_autobot_enter_without_normal_user*  ../check_lib/")
        res = execute_remote_command(host, f". ./env/bin/activate; cd /home/shocklee/tl-QA/autoTest/check_lib;  python data_arrange.py {ori_filename} > {aft_filename}")
    print(f"{ori_filename} -> {aft_filename}")

# other
def get_taipei_timestamp_delta(delta: dict) -> int:
    tz = pytz.timezone('Asia/Taipei')
    now_obj = datetime.now(tz)
    delta_obj = timedelta(**delta)
    target_obj = now_obj + delta_obj
    target_ts = int(target_obj.timestamp())
    return target_ts

def create_log_directory(folder_path):
    now = datetime.now()
    suffix = now.strftime("%m%d%H%M")
    folder_path += suffix
    os.mkdir(f"./{folder_path}")
    if os.path.exists(f"./{folder_path}"):
        print(f"Folder : {folder_path} created successfully!")
    return folder_path

def timestamp_of_midnight_after_day(afterDay:int):
    tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(tz)
    tomorrow_midnight = datetime(year=now.year, month=now.month, day=now.day, tzinfo=now.tzinfo) + timedelta(days=afterDay)
    ts = int(tomorrow_midnight.timestamp())
    return ts

def get_all_chatbot_tickets_time_range(startDay, endDay, startHour, endHour):
    taipei_timezone = pytz.timezone('Asia/Taipei')
    now = datetime.now(taipei_timezone)

    available_utc_day_period = []
    available_tpe_day_period = []

    for day in range(startDay, endDay):
        taipei_timezone = pytz.timezone('Asia/Taipei')
        taipei_midnight_dt = taipei_timezone.localize(datetime(year=now.year, month=now.month, day=now.day) + timedelta(days=day))
        taipei_startHour_dt = taipei_midnight_dt.replace(hour=startHour, minute=00, second=00, microsecond=00)
        taipei_endHour_dt = taipei_midnight_dt.replace(hour=endHour, minute=00, second=00, microsecond=00)
        taipei_startHour = taipei_startHour_dt.strftime('%Y%m%d %H:%M:%S')
        taipei_endHour = taipei_endHour_dt.strftime('%Y%m%d %H:%M:%S')
        available_tpe_day_period.append(f"{taipei_startHour}~{taipei_endHour}")

        utc_timezone = pytz.timezone('UTC')
        utc_startHour_dt = taipei_startHour_dt.astimezone(utc_timezone)
        utc_endHour_dt = taipei_endHour_dt.astimezone(utc_timezone)
        utc_startHour = utc_startHour_dt.strftime('%Y%m%d %H:%M:%S')
        utc_endHour = utc_endHour_dt.strftime('%Y%m%d %H:%M:%S')
        available_utc_day_period.append(f"{utc_startHour}~{utc_endHour}")

    timezone_day_period = {'utc' : available_utc_day_period, 'tpe': available_tpe_day_period}
    return timezone_day_period

def get_giftname_list_from_giftId_list(host, giftId_list):
    giftId_str = ', '.join(str(x) for x in giftId_list)
    sql = f'Select name from gift_v2 where id in ({giftId_str})'
    result = dbQuery(host, sql, 'shocklee')
    giftNameList = [ i[0] for i in result]
    return giftNameList

def get_advanced_chatBot_list(db):
    sql = 'SELECT id FROM chatbot Where advanced = 1'
    result = dbQuery(db, sql, 'shocklee')
    chatBot_list = []
    for i in result:
        chatBot_list.append(i[0])
    return chatBot_list

def activate_chatbot_process_on_remote_background(host, env):
    execute_remote_command(host, "cd tl-chatbot ; source ~/.zshrc;mix deps.get")
    background = threading.Timer(3, execute_remote_command, args=[host, f'cd tl-chatbot ; source ~/.zshrc; MIX_ENV={env} mix run --no-halt > chatbot.log 2>&1 &'])
    background.start()
    time.sleep(60)


def kill_chatbot_process_on_remote_background(host):
    res = execute_remote_command(host, "ps aux | grep '[m]ix run --no-halt' | awk '{print $2}'")
    print(res.strip())
    pid = res.strip()
    if pid :
        execute_remote_command(host, f"kill -9 {pid}")
    else:
        print('No chatbot process found.....')


# Settings
host = '34.81.211.190'
prefix = f'http://{host}'
restext = user_login(prefix, 'tl-lisa', '12345678')
header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': restext['data']['token'], 'X-Auth-Nonce': restext['data']['nonce']}

def setup_module():
    #'point_consumption_history'
    kill_chatbot_process_on_remote_background(host)
    correct_remote_system_time(host)
    clear_relative_table(host, 'point_consumption_history', 'shocklee')
    clear_relative_table(host, 'chatbot_promotion_ticket', 'shocklee')
    dbSetting(host, ["UPDATE live_room SET status=0 WHERE status=1"], 'shocklee' )
    dbSetting(host, ["UPDATE remain_points SET remain_points = 0 WHERE identity_id in (select id from chatbot);"], 'shocklee' )
    dbSetting(host, ["UPDATE live_room SET status=0 WHERE status=1"], 'shocklee' )
    activate_chatbot_process_on_remote_background(host, 'qa')


def teardown_module():
    correct_remote_system_time(host)
    kill_chatbot_process_on_remote_background(host)


# @pytest.mark.skip(reason="設定一段時間，檢查機器人是否在指定時間送禮，在不同日期，檢查機器人是否在指定時間送禮")
def test_gift_delivery_within_specified_time():
    """
    設定一段時間，檢查機器人是否在指定時間送禮，在不同日期時段，檢查機器人是否在指定時間送禮
    """
    # pre-step
    chatbotMaster_orig_remain_points = get_remain_points('34.81.211.190', 'b3441f99-4d9e-4b11-99ce-9490af627164')
    midnightDay_1 = timestamp_of_midnight_after_day(1)
    midnightDay_4 = timestamp_of_midnight_after_day(4)
    time_range_list = get_all_chatbot_tickets_time_range(startDay=1, endDay=4, startHour=18, endHour=20)
    round1_utc_start = time_range_list['utc'][0].split('~')[0]
    roundLast_utc_start = time_range_list['utc'][-1].split('~')[0]
    giftId_list = [982, 983, 984, 985]
    # 1. 先設定 chatbot 執行時間
    res = put_chatbot_promotionTicket(prefix, header,
        startTime = midnightDay_1,
        endTime = midnightDay_4,
        startHour = 1800,
        endHour = 2000,
        totalPoints = 10000,
        reference = 'https://dummyimage.com/600x400/000/fff&text=Dummy+Image',
        status = None,
        gift = giftId_list
    )
    print(res.json())
    assert res.status_code == 200
    promoTick_id = get_id_from_chatbot_promotionTicket_list(prefix, header, midnightDay_1, midnightDay_4)
    # 2. 更改遠端系統時間
    res = update_remote_time(host, round1_utc_start)
    # 3. 執行遠端特定程式 → 開房間 → 產生 log
    run_wsTest_and_generate_new_log('pytest -s jason_test.py --m master01 master02 --t default_chatbot.json5')
    # 4. 更改遠端系統時間
    res = update_remote_time(host, roundLast_utc_start)
    # 5. 執行遠端特定程式 → 開房間 → 產生 log
    run_wsTest_and_generate_new_log('pytest -s jason_test.py --m master01 --t default_chatbot.json5')



    # 7. 將所有遠端 log 檔案取回，並刪除
    dir_path = create_log_directory('wsLogs')
    download_files = download_file_and_delete_from_remote(host, '/home/shocklee/tl-QA/autoTest/check_lib', f'./{dir_path}', "*.log")
    unprocessed_files =[i for i in download_files if 'arrange' in i]
    pprint(unprocessed_files)

    # 8. 分析 local 端 log 檔案    dataParse_files = ['tmp_logs/dataParse_20230306_124829.log' , 'tmp_logs/dataParse_20230306_130526.log']
    data_list = read_multi_json_file(unprocessed_files)
    filter_data = filter_events(data_list, ['gift_bcst', 'room_in_bcst'])
    adv_chatBots =  get_advanced_chatBot_list('34.81.211.190')
    chatBot_gift_report_expect = analyze_chatBot_gift_broadcast_events(filter_data, adv_chatBots)
    chatBot_entry_gift_interval = analyze_chatBot_entry_gift_time(filter_data, adv_chatBots)
    chatBot_gift_send_records = analyze_chatBot_gift_and_sendTime(filter_data, adv_chatBots)

    pprint(chatBot_gift_report_expect)
    pprint(chatBot_entry_gift_interval)

    # 9.  a.chatbot 送禮報表分析
    # 將 chatbot 排程取消
    res = put_chatbot_promotionTicket(prefix, header,
        id = promoTick_id,
        startTime = midnightDay_1,
        endTime = midnightDay_4,
        startHour = 1800,
        endHour = 2000,
        totalPoints = 10000,
        reference = 'https://dummyimage.com/600x400/000/fff&text=Dummy+Image',
        status = 'CANCELLED',
        gift = giftId_list
    )
    time.sleep(200) # 取消之後，等待回收點數完成
    download_file_and_delete_from_remote(host, '/home/shocklee/tl-chatbot', f'./{dir_path}', "chatbot.log")
    res = get_chatbot_promotionTicket_insight(prefix, header, promoTick_id, 100, 1)
    chatbot_report = (res.json())['data'][0]["chatbot"]
    total_count = (res.json())['totalCount']
    print(res.json())
    expect_total_points = 0
    chatbot_list = [i['id'] for i in chatBot_gift_report_expect]
    for chatbot in chatbot_report:
        check.is_in(chatbot['id'], chatbot_list, f"chatbot {chatbot['id']} doesn't match {chatbot_list}")
        for expect in chatBot_gift_report_expect:
            if chatbot['id'] == expect['id']:
                check.equal(chatbot['points'], expect['points'], f"chatbot point : {chatbot['points']} doesn't match expect : {expect['points']}")
                check.equal(chatbot['giftCount'], expect['giftCount'], f"chatbot giftCount : {chatbot['giftCount']} doesn't match expect : {expect['giftCount']} ")
                expect_total_points += chatbot['points']
    check.equal(total_count, len(chatbot_list), f"chatbot count ({total_count}): total_count doesn't match expect : {len(chatbot_list)} ")
    # 9.  b.檢查每回合送禮時間是否正確，檢查 chatbot 送出禮物的類型
    #check Round
    round1_tpe_start_ts = taipei_str_to_taipei_timestamp(time_range_list['tpe'][0].split('~')[0])
    round1_tpe_end_ts = taipei_str_to_taipei_timestamp(time_range_list['tpe'][0].split('~')[1])
    roundLast_tpe_start_ts = taipei_str_to_taipei_timestamp(time_range_list['tpe'][-1].split('~')[0])
    roundLast_tpe_end_ts = taipei_str_to_taipei_timestamp(time_range_list['tpe'][-1].split('~')[1])

    giftname_list = get_giftname_list_from_giftId_list(host, giftId_list)

    find_round1_record, find_round2_record = False, False
    for record in chatBot_gift_send_records:
        if round1_tpe_start_ts <= record['sendTime'] <= round1_tpe_end_ts:
            find_round1_record = True
            check.is_in(record['giftName'], giftname_list, f"giftName {record['giftName']} is not in {giftname_list}")
        elif roundLast_tpe_start_ts <= record['sendTime'] <= roundLast_tpe_end_ts:
            find_round2_record = True
            check.is_in(record['giftName'], giftname_list, f"giftName {record['giftName']} is not in {giftname_list}")
    check.is_true(find_round1_record, 'First Record Not Found Record')
    check.is_true(find_round2_record, 'Second Record Not Found Record')

    #    c.進房與送禮時間分析 30~60s
    check_chatBot_entry_gift_interval(chatBot_entry_gift_interval, 30, 60)
    #    d.檢查chatbotMaster點數是否已經回收
    for adv_id in adv_chatBots:
        [(identityId,remainPoints)] = dbQuery(host, f"select identity_id, remain_points from remain_points where identity_id = '{adv_id}'", 'shocklee')
        check.equal(remainPoints, 0, f"{identityId} remainPoits is not 0")

    #    e.chatbotMaster remainPoints 與 chatbot 花費的點數是否合理
    chatbotMaster_now_remain_points = get_remain_points(host, 'b3441f99-4d9e-4b11-99ce-9490af627164')
    expect_remain_points = chatbotMaster_now_remain_points + expect_total_points
    check.equal(chatbotMaster_orig_remain_points, expect_remain_points, f"chatbotMaster remain_points : {chatbotMaster_orig_remain_points} does not match the expected result ({expect_remain_points}).")


@pytest.mark.skip(reason="設定一段時間，檢查機器人是否再在指定時間送禮，超過時間之後，會將點數回收。")
def test_chatbotMaster_overTime_remainPoints_takeBack():
    # pre-step
    chatbotMaster_orig_remain_points = get_remain_points(host, 'b3441f99-4d9e-4b11-99ce-9490af627164')
    midnightDay_1 = timestamp_of_midnight_after_day(1)
    midnightDay_4 = timestamp_of_midnight_after_day(4)
    time_range_list = get_all_chatbot_tickets_time_range(startDay=1, endDay=4, startHour=18, endHour=20)
    round1_utc_start = time_range_list['utc'][0].split('~')[0]
    roundLast_utc_start = time_range_list['utc'][-1].split('~')[0]
    roundLast_utc_end = time_range_list['utc'][-1].split('~')[1]

    giftId_list = [982, 983, 984]
    # 1. 先設定 chatbot 執行時間
    res = put_chatbot_promotionTicket(prefix, header,
        startTime = midnightDay_1,
        endTime = midnightDay_4,
        startHour = 1800,
        endHour = 2000,
        totalPoints = 10000,
        reference = 'https://dummyimage.com/600x400/000/fff&text=Dummy+Image',
        status = None,
        gift = giftId_list
    )
    print(res.json())
    assert res.status_code == 200
    promoTick_id = get_id_from_chatbot_promotionTicket_list(prefix, header, midnightDay_1, midnightDay_4)
    # 2. 更改遠端系統時間
    res = update_remote_time(host, round1_utc_start)
    # 3. 執行遠端特定程式 → 開房間 → 產生 log
    run_wsTest_and_generate_new_log('pytest -s jason_test.py --m master01 master02 --t default_chatbot.json5')
    # 4. 更改遠端系統時間至準備過期時間
    res = update_remote_time(host, timestamp_to_utc_str(midnightDay_4))
    time.sleep(200)
    # 5. 將所有遠端 log 檔案取回，並刪除
    dir_path = create_log_directory('wsLogs')
    download_files = download_file_and_delete_from_remote(host, '/home/shocklee/tl-QA/autoTest/check_lib', f'./{dir_path}', "*.log")
    download_file_and_delete_from_remote(host, '/home/shocklee/tl-chatbot', f'./{dir_path}', "chatbot.log")
    unprocessed_files =[i for i in download_files if 'arrange' in i]
    pprint(unprocessed_files)

    # 6. 分析 local 端 log 檔案    dataParse_files = ['tmp_logs/dataParse_20230306_124829.log' , 'tmp_logs/dataParse_20230306_130526.log']
    data_list = read_multi_json_file(unprocessed_files)
    filter_data = filter_events(data_list, ['gift_bcst', 'room_in_bcst'])
    adv_chatBots =  get_advanced_chatBot_list('34.81.211.190')
    chatBot_gift_report_expect = analyze_chatBot_gift_broadcast_events(filter_data, adv_chatBots)
    chatBot_entry_gift_interval = analyze_chatBot_entry_gift_time(filter_data, adv_chatBots)
    chatBot_gift_send_records = analyze_chatBot_gift_and_sendTime(filter_data, adv_chatBots)

    pprint(chatBot_gift_report_expect)
    pprint(chatBot_entry_gift_interval)

    # 7.  a.chatbot 送禮報表分析

    res = get_chatbot_promotionTicket_insight(prefix, header, promoTick_id, 100, 1)
    chatbot_report = (res.json())['data'][0]["chatbot"]
    total_count = (res.json())['totalCount']
    expect_total_points = 0
    chatbot_list = [i['id'] for i in chatBot_gift_report_expect]
    result = dbQuery(host, 'select id from chatbot where advanced = 1', 'shocklee')
    chatbot_list = [ i[0] for i in result]
    for chatbot in chatbot_report:
        check.is_in(chatbot['id'], chatbot_list, f"chatbot {chatbot['id']} doesn't match {chatbot_list}")
        for expect in chatBot_gift_report_expect:
            if chatbot['id'] == expect['id']:
                check.equal(chatbot['points'], expect['points'], f"chatbot point : {chatbot['points']} doesn't match expect : {expect['points']}")
                check.equal(chatbot['giftCount'], expect['giftCount'], f"chatbot giftCount : {chatbot['giftCount']} doesn't match expect : {expect['giftCount']} ")
                expect_total_points += chatbot['points']
    check.equal(total_count, len(chatbot_list), f"chatbot count ({total_count}): total_count doesn't match expect : {len(chatbot_list)} ")

    #   b.檢查每回合送禮時間是否正確，檢查 chatbot 送出禮物的類型
    #check Round
    round1_tpe_start_ts = taipei_str_to_taipei_timestamp(time_range_list['tpe'][0].split('~')[0])
    round1_tpe_end_ts = taipei_str_to_taipei_timestamp(time_range_list['tpe'][0].split('~')[1])

    giftname_list = get_giftname_list_from_giftId_list(host, giftId_list)

    find_round1_record = False
    for record in chatBot_gift_send_records:
        if round1_tpe_start_ts <= record['sendTime'] <= round1_tpe_end_ts:
            find_round1_record = True
            check.is_in(record['giftName'], giftname_list, f"giftName {record['giftName']} is not in {giftname_list}")
    check.is_true(find_round1_record, 'First Record Not Found Record')
    #    c.進房與送禮時間分析 30~60s
    check_chatBot_entry_gift_interval(chatBot_entry_gift_interval, 30, 60)

    #    d.檢查chatbotMaster點數是否已經回收
    for adv_id in adv_chatBots:
        [(identityId, remainPoints)] = dbQuery(host, f"select identity_id, remain_points from remain_points where identity_id = '{adv_id}'", 'shocklee')
        check.equal(remainPoints, 0, f"{identityId} remainPoits is not 0")

    #    e.chatbotMaster remainPoints 與 chatbot 花費的點數是否合理
    chatbotMaster_now_remain_points = get_remain_points(host, 'b3441f99-4d9e-4b11-99ce-9490af627164')
    expect_remain_points = chatbotMaster_now_remain_points + expect_total_points
    check.equal(chatbotMaster_orig_remain_points, expect_remain_points, f"chatbotMaster remain_points : {chatbotMaster_orig_remain_points} does not match the expected result ({expect_remain_points}).")





@pytest.mark.skip(reason="設定一段時間，檢查機器人是否再在指定時間送禮，更改時段與禮物，檢查機器人是否再在更改時段送禮，並且是更改後的禮物")
def test_change_delivery_time_and_gift():
  # pre-step
    chatbotMaster_orig_remain_points = get_remain_points('34.81.211.190', 'b3441f99-4d9e-4b11-99ce-9490af627164')
    midnightDay_1 = timestamp_of_midnight_after_day(1)
    midnightDay_4 = timestamp_of_midnight_after_day(4)
    time_range_list = get_all_chatbot_tickets_time_range(startDay=1, endDay=4, startHour=18, endHour=20)
    round1_utc_start = time_range_list['utc'][0].split('~')[0]
    roundLast_utc_start = time_range_list['utc'][-1].split('~')[0]
    round1_tpe_start_ts = taipei_str_to_taipei_timestamp(time_range_list['tpe'][0].split('~')[0])
    round1_tpe_end_ts = taipei_str_to_taipei_timestamp(time_range_list['tpe'][0].split('~')[1])
    giftId_list = [982, 983, 984, 985]
    giftname_list1 = get_giftname_list_from_giftId_list(host, giftId_list)

    # 1. 先設定 chatbot 執行時間
    res = put_chatbot_promotionTicket(prefix, header,
        startTime = midnightDay_1,
        endTime = midnightDay_4,
        startHour = 1800,
        endHour = 2000,
        totalPoints = 10000,
        reference = 'https://dummyimage.com/600x400/000/fff&text=Dummy+Image',
        status = None,
        gift = giftId_list
    )
    print(res.json())
    assert res.status_code == 200
    promoTick_id = get_id_from_chatbot_promotionTicket_list(prefix, header, midnightDay_1, midnightDay_4)
    # 2. 更改遠端系統時間
    res = update_remote_time(host, round1_utc_start)
    # 3. 執行遠端特定程式 → 開房間 → 產生 log
    run_wsTest_and_generate_new_log('pytest -s jason_test.py --m master01 master02 --t default_chatbot.json5')
    # 4. 更改時段與禮物 → 開房間 → 產生 log
    time_range_list = get_all_chatbot_tickets_time_range(startDay=1, endDay=4, startHour=22, endHour=23)
    roundLast_utc_start = time_range_list['utc'][-1].split('~')[0]
    roundLast_tpe_start_ts = taipei_str_to_taipei_timestamp(time_range_list['tpe'][-1].split('~')[0])
    roundLast_tpe_end_ts = taipei_str_to_taipei_timestamp(time_range_list['tpe'][-1].split('~')[1])
    giftId_list = [718, 719]
    res = put_chatbot_promotionTicket(prefix, header,
        id = promoTick_id,
        startTime = midnightDay_1,
        endTime = midnightDay_4,
        startHour = 2200,
        endHour = 2300,
        totalPoints = 10000,
        reference = 'https://dummyimage.com/600x400/000/fff&text=Dummy+Image',
        status = None,
        gift = giftId_list
    )
    print(res.json())
    assert res.status_code == 200

    # 5. 更改遠端系統時間
    res = update_remote_time(host, roundLast_utc_start)
    # 6. 執行遠端特定程式 → 開房間 → 產生 log
    run_wsTest_and_generate_new_log('pytest -s jason_test.py --m master01 --t default_chatbot.json5')

    # 7. 將所有遠端 log 檔案取回，並刪除
    dir_path = create_log_directory('wsLogs')
    download_files = download_file_and_delete_from_remote(host, '/home/shocklee/tl-QA/autoTest/check_lib', f'./{dir_path}', "*.log")
    unprocessed_files =[i for i in download_files if 'arrange' in i]
    pprint(unprocessed_files)

    # 8. 分析 local 端 log 檔案    dataParse_files = ['tmp_logs/dataParse_20230306_124829.log' , 'tmp_logs/dataParse_20230306_130526.log']
    data_list = read_multi_json_file(unprocessed_files)
    filter_data = filter_events(data_list, ['gift_bcst', 'room_in_bcst'])
    adv_chatBots =  get_advanced_chatBot_list('34.81.211.190')
    chatBot_gift_report_expect = analyze_chatBot_gift_broadcast_events(filter_data, adv_chatBots)
    chatBot_entry_gift_interval = analyze_chatBot_entry_gift_time(filter_data, adv_chatBots)
    chatBot_gift_send_records = analyze_chatBot_gift_and_sendTime(filter_data, adv_chatBots)

    pprint(chatBot_gift_report_expect)
    pprint(chatBot_entry_gift_interval)

    # 9.  a.chatbot 送禮報表分析
    # 將 chatbot 排程取消
    res = put_chatbot_promotionTicket(prefix, header,
        id = promoTick_id,
        startTime = midnightDay_1,
        endTime = midnightDay_4,
        startHour = 1800,
        endHour = 2000,
        totalPoints = 10000,
        reference = 'https://dummyimage.com/600x400/000/fff&text=Dummy+Image',
        status = 'CANCELLED',
        gift = giftId_list
    )
    time.sleep(200) # 取消之後，等待回收點數完成
    download_file_and_delete_from_remote(host, '/home/shocklee/tl-chatbot', f'./{dir_path}', "chatbot.log")
    res = get_chatbot_promotionTicket_insight(prefix, header, promoTick_id, 100, 1)
    chatbot_report = (res.json())['data'][0]["chatbot"]
    total_count = (res.json())['totalCount']
    print(res.json())
    expect_total_points = 0
    result = dbQuery(host, 'select id from chatbot where advanced = 1', 'shocklee')
    chatbot_list = [ i[0] for i in result]
    for chatbot in chatbot_report:
        check.is_in(chatbot['id'], chatbot_list, f"chatbot {chatbot['id']} doesn't match {chatbot_list}")
        for expect in chatBot_gift_report_expect:
            if chatbot['id'] == expect['id']:
                check.equal(chatbot['points'], expect['points'], f"chatbot point : {chatbot['points']} doesn't match expect : {expect['points']}")
                check.equal(chatbot['giftCount'], expect['giftCount'], f"chatbot giftCount : {chatbot['giftCount']} doesn't match expect : {expect['giftCount']} ")
                expect_total_points += chatbot['points']
    check.equal(total_count, len(chatbot_list), f"chatbot count ({total_count}): total_count doesn't match expect : {len(chatbot_list)} ")
    # 9.  b.檢查每回合送禮時間是否正確，檢查 chatbot 送出禮物的類型
    #check Round
    giftname_list2 = get_giftname_list_from_giftId_list(host, giftId_list)
    find_round1_record, find_round2_record = False, False
    for record in chatBot_gift_send_records:
        if round1_tpe_start_ts <= record['sendTime'] <= round1_tpe_end_ts:
            find_round1_record = True
            check.is_in(record['giftName'], giftname_list1, f"giftName {record['giftName']} is not in {giftname_list1}")
        elif roundLast_tpe_start_ts <= record['sendTime'] <= roundLast_tpe_end_ts:
            find_round2_record = True
            check.is_in(record['giftName'], giftname_list2, f"giftName {record['giftName']} is not in {giftname_list2}")
    check.is_true(find_round1_record, 'First Record Not Found Record')
    check.is_true(find_round2_record, 'Second Record Not Found Record')

    #    c.進房與送禮時間分析 30~60s
    check_chatBot_entry_gift_interval(chatBot_entry_gift_interval, 30, 60)
    #    d.檢查chatbotMaster點數是否已經回收
    for adv_id in adv_chatBots:
        [(identityId,remainPoints)] = dbQuery(host, f"select identity_id, remain_points from remain_points where identity_id = '{adv_id}'", 'shocklee')
        check.equal(remainPoints, 0, f"{identityId} remainPoits is not 0")

    #    e.chatbotMaster remainPoints 與 chatbot 花費的點數是否合理
    chatbotMaster_now_remain_points = get_remain_points(host, 'b3441f99-4d9e-4b11-99ce-9490af627164')
    expect_remain_points = chatbotMaster_now_remain_points + expect_total_points
    check.equal(chatbotMaster_orig_remain_points, expect_remain_points, f"chatbotMaster remain_points : {chatbotMaster_orig_remain_points} does not match the expected result ({expect_remain_points}).")
