# milestone29:[需求] Mobile綁定-簡訊發送驗證碼 POST /v2/identity/binding/mobile/send #1894
# milestone29:[需求] Mobile綁定-安全碼驗證 POST /v2/identity/binding/mobile/activate #1895
# pylint: disable=unbalanced-tuple-unpacking
import json
import pytest
import datetime
import time
from assistence import api
from assistence import initdata
from assistence import dbConnect
from assistence import sundry
from pprint import pprint

env = 'QA2'
test_parameter = {}
header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
initdata.set_test_data(env, test_parameter)
header['X-Auth-Token'] = test_parameter['backend_token']
header['X-Auth-Nonce'] = test_parameter['backend_nonce']
#account_prefix = track , account_suffix = 150 , usersNum = 10 -> track0150 - track0159
users_id_header = sundry.idList_with_header(test_parameter['prefix'], header, 'track', 300, 20)
usersHead = [{ 'nonce': val['X-Auth-Nonce'],'token':val['X-Auth-Token']} for key, val in users_id_header.items()]
#pprint(usersHead)
Ok = []
def get_activate_code_in_identity_mobile_register_history(tmpToken):
    query_sql = "select activate_code from identity_mobile_register_history where token='{}'".format(tmpToken)
    [(activate_code,)]=dbConnect.dbQuery(test_parameter['db'], query_sql, 'shocklee')
    return activate_code

def register_mobile_in_identity(countryCode, mobile):
    now_ts = datetime.datetime.now().timestamp()
    loginId = 'a' + str(now_ts)[-4:]
    api_name = '/api/v2/identity/register/mobile/send'
    body = {
        "countryCode" : countryCode,
        "mobile" : mobile,
        "loginId" : loginId,
        "password" : 'shocktest321'
    }
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    restext = json.loads(res.text)
    tmpToken = restext['data']['tmpToken']
    activateCode = get_activate_code_in_identity_mobile_register_history(tmpToken)
    if res.status_code // 100 == 2 :
        api_name = '/api/v2/identity/register/mobile/activate'
        body = {
            "tmpToken" : tmpToken,
            "activateCode" : activateCode,
        }
        res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
        if res.status_code // 100 == 2 :
            print("新增註冊的人成功")
        else:
            print("新增註冊的人失敗")
    else:
        print("新增註冊的人失敗")

def get_activate_code_in_identity_mobile_bind_history(tmpToken):
    query_sql = "select activate_code from identity_mobile_bind_history where token='{}'".format(tmpToken)
    [(activate_code,)]=dbConnect.dbQuery(test_parameter['db'], query_sql, 'shocklee')
    return activate_code

def set_ActCode_Expire_in_identity_mobile_bind_history(tmpToken):
    time.sleep(2)
    update_sql = ["update identity_mobile_bind_history set expires_in=1 where token = '{}'".format(tmpToken)]
    dbConnect.dbSetting(test_parameter['db'], update_sql, 'shocklee')

def update_identity_by_mobile(countryCode, mobile):
    sqlList = ["UPDATE identity  SET phone_country_code = NULL, phone_number = NULL  WHERE phone_country_code='{}' and phone_number = '{}'".format(countryCode, mobile)]
    dbConnect.dbSetting(test_parameter['db'], sqlList, 'shocklee')

def set_Mobile_Sent_Reach_Limit(countryCode, mobile):
    api_name = '/api/v2/identity/binding/mobile/send'
    body = { "countryCode" : countryCode, "mobile" : mobile, }
    apiSend = True
    while apiSend :
        res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
        if res.status_code // 100 == 4:
            apiSend = False

def set_phoneNumber_exists_in_identity(countryCode, mobile):
    api_name = '/api/v2/identity/register/mobile/send'
    body = {
        "countryCode" : countryCode, "mobile" : mobile, "loginId" : 'testAcc222', "password" : '323qerqw' }
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    restext = json.loads(res.text)
    print(restext)
    tmpToken = restext['data']['tmpToken']
    activate_code = get_activate_code_in_identity_mobile_register_history(tmpToken)

    api_name = '/api/v2/identity/register/mobile/activate'
    body = {
        "tmpToken" : tmpToken,
        "activateCode" : activate_code,
    }
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)

def delete_identity_by_mobile(countryCode, mobile):
    sqlList = []
    sqlList.append("delete from remain_points where identity_id in ( select id from identity where phone_country_code='{}' and phone_number = '{}')".format(countryCode, mobile))
    sqlList.append("delete from identity_role where identity_id in ( select id from identity where phone_country_code='{}' and phone_number = '{}')".format(countryCode, mobile))
    sqlList.append("delete from user_settings where identity_id in ( select id from identity where phone_country_code='{}' and phone_number = '{}')".format(countryCode, mobile))
    sqlList.append("delete from identity where phone_country_code='{}' and phone_number = '{}'".format(countryCode, mobile))
    dbConnect.dbSetting(test_parameter['db'], sqlList, 'shocklee')

def setup_module():
    clear_sql = ["delete from identity_mobile_bind_history"]
    dbConnect.dbSetting(test_parameter['db'], clear_sql, 'shocklee')

    clear_sql = ["delete from identity_mobile_register_history"]
    dbConnect.dbSetting(test_parameter['db'], clear_sql, 'shocklee')

    # #先把有這支手機 937855506 記錄給清除
    # sel_sql = "select count(*) from identity where phone_number = '937855506'"
    # [(select_count,)] = dbConnect.dbQuery(test_parameter['db'], sel_sql , 'shocklee')
    # if select_count != 0 :
    #     update_sql = ["update identity set phone_number='888888888' where phone_number = '937855506'"]
    #     dbConnect.dbSetting(test_parameter['db'], update_sql, 'shocklee')

#https://receive-sms-free.net/
#https://receive-sms-free.net/Free-Japan-Phone-Number/818059845961/
#https://smstools.online/receive-free-sms/australia/1504922-61451562733
@pytest.mark.parametrize(
                            "scenario,                  token,                 nonce, ctyCode,        mobile, expect", [
    #正向列表
    (                          'HK Tel', usersHead[0]['token'], usersHead[0]['nonce'],  '+852',    '61362620',     2),
    (                          'AU Tel', usersHead[1]['token'], usersHead[1]['nonce'],   '+61',   '451562733',     2),
    (                          'MA Tel', usersHead[2]['token'], usersHead[2]['nonce'],  '+853',    '68436392',     2),
    (                         'USA Tel', usersHead[3]['token'], usersHead[3]['nonce'],    '+1',  '2154033909',     2),
    (                          'CN Tel', usersHead[4]['token'], usersHead[4]['nonce'],   '+86', '13123046583',     2),
    (                          'ID tel', usersHead[5]['token'], usersHead[5]['nonce'],   '+62', '83175259083',     2),
    (                          'PH tel', usersHead[6]['token'], usersHead[6]['nonce'],   '+63',  '9664706988',     2),
    (                        'TW Tel 1', usersHead[7]['token'], usersHead[7]['nonce'],  '+886',  '0937855506',     2),
    (                        'TW Tel 2', usersHead[8]['token'], usersHead[8]['nonce'],  '+886',   '937855506',     2),

    # #反向列表
    (                'Invalid ctyCode1',  usersHead[11]['token'], usersHead[11]['nonce'],   '+123', '15747708997',     4),
    (                'Invalid ctyCode2',  usersHead[12]['token'], usersHead[12]['nonce'],   '+099', '15747748997',     4),
    (              'Invalid USA mobile',  usersHead[13]['token'], usersHead[13]['nonce'],     '+1',  '1234345345',     4),
    (               'Invalid TW mobile',  usersHead[14]['token'], usersHead[14]['nonce'],   '+886',    '92621631',     4),
    (               'Invalid CN mobile',  usersHead[15]['token'], usersHead[15]['nonce'],    '+86',  '0937855506',     4),
    (         'Mobile Sent Reach Limit',  usersHead[16]['token'], usersHead[16]['nonce'],   '+886',  '0937855506',     4),
    (     'Mobile Exist Is In Identity',  usersHead[17]['token'], usersHead[17]['nonce'],   '+886',  '988545866',     4),

])
def test_bind_mobile_send(scenario, token, nonce, ctyCode, mobile, expect):
    #先解除綁定
    delCtyCode = ctyCode[1:] if ctyCode.find("+") != -1  else   ctyCode
    delMobile = mobile[1:] if mobile.startswith("0")  else mobile
    print( delCtyCode, delMobile)
    update_identity_by_mobile( delCtyCode, delMobile)

    if expect == 4:
        if scenario == 'Mobile Sent Reach Limit':
            set_Mobile_Sent_Reach_Limit(ctyCode, mobile)
        # elif scenario == 'Mobile Exist Is In Identity':
        #     set_phoneNumber_exists_in_identity(ctyCode, mobile)


    header['X-Auth-Token'] = token
    header['X-Auth-Nonce'] = nonce
    api_name = '/api/v2/identity/binding/mobile/send'
    body = {
        "countryCode" : ctyCode,
        "mobile" : mobile,
    }
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    restext = json.loads(res.text)
    print(restext)
    assert res.status_code // 100 == expect
    if expect == 2:
        assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
        assert restext['data']['tmpToken'] != None
        tmpToken = restext['data']['tmpToken']
        activate_code = get_activate_code_in_identity_mobile_bind_history(tmpToken)
        Ok.append({ "token":token, "nonce": nonce, "tmpToken": tmpToken, "activateCode" : activate_code ,"countryCode": ctyCode, "mobile": mobile})
    elif expect == 4:
        assert res.status_code == 400
        if scenario.find('Invalid') != -1:
            assert restext['Message'] == 'MOBILE_FORMAT_INVALID'
        elif scenario.find('Exist') != -1:
            assert restext['Message'] == 'MOBILE_HAS_BEEN_BOUND'
        elif scenario.find('Reach Limit') != -1:
            assert restext['Message'] == 'WEEKLY_LIMIT_OF_MOBILECODE_SENT_REACHED'


@pytest.mark.parametrize(
                            "scenario,          index,        expect", [
    #正向列表
    (                         'HK Tel',             0,         2),
    (                         'AU Tel',             1,         2),
    (                         'MA Tel',             2,         2),
    (                        'USA Tel',             3,         2),
    (                         'CN Tel',             4,         2),
    (                       'TW Tel 1',             7,         2),

    #反向列表
    (       'Mobile Exist In Identity',             6,              4),
    (        'Activate Code Is Expire',             7,              4),
    (         'Activate Code Is Error',             7,              4),
    (                     'Auth Error',             7,              4),
])
def test_bind_mobile_activate(scenario, index, expect):
    token, nonce, tmpToken, activateCode, countryCode, mobile = Ok[index]['token'], Ok[index]['nonce'], Ok[index]['tmpToken'], Ok[index]['activateCode'], Ok[index]['countryCode'], Ok[index]['mobile']
    #如果是反向列表，先設定好環境
    if expect == 4 :
        if scenario == 'Mobile Exist In Identity':
            register_mobile_in_identity(countryCode, mobile)
        elif scenario ==  'Activate Code Is Expire':
            set_ActCode_Expire_in_identity_mobile_bind_history(tmpToken)
        elif scenario ==  'Activate Code Is Error':
            activateCode = "423864"
        elif scenario == 'Auth Error':
            token, nonce = 'error_token', 'error_nonce'
    #開始打API
    header['X-Auth-Token'] = token
    header['X-Auth-Nonce'] = nonce
    api_name = '/api/v2/identity/binding/mobile/activate'
    body = {
        "tmpToken": tmpToken,
        "activateCode": activateCode,
    }
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    assert res.status_code // 100 == expect
    restext = json.loads(res.text)
    if expect == 2:
        assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
        #確認手機是否綁定成功，檢查identity
        query_sql = "select phone_country_code, phone_number from identity where token='{}' and nonce='{}'".format(token, nonce)
        [(sql_country_code,sql_mobile)]=dbConnect.dbQuery(test_parameter['db'], query_sql, 'shocklee')
        assert countryCode == '+'+ sql_country_code
        mobile = mobile [1:] if mobile.startswith("0")  else mobile
        assert mobile == sql_mobile
        #確認手機是否綁定成功，檢查identity_mobile_bind_history
        query_sql = "select status from identity_mobile_bind_history where  token='{}'".format(tmpToken)
        [(sql_status,)]=dbConnect.dbQuery(test_parameter['db'], query_sql, 'shocklee')
        assert sql_status == 1

    elif expect == 4:
        assert res.status_code == 400
        if scenario == 'Mobile Exist In Identity':
            assert restext['Message'] == 'MOBILE_HAS_BEEN_BOUND'
        elif scenario ==  'Activate Code Is Expire':
            assert restext['Message'] == 'MOBILE_ACTIVATE_CODE_EXPIRED'
        elif scenario.find('Error') != -1 :
            assert restext['Message'] == 'MOBILE_ACTIVATE_CODE_ERROR'
    #最後把綁定手機清除
    update_identity_by_mobile(countryCode, mobile)