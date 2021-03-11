# milestone29:[需求] Mobile註冊-簡訊發送驗證碼及密碼格式驗證 POST /v2/identity/register/mobile/send #1892
# milestone29:[需求] Mobile註冊-安全碼驗證 POST /v2/identity/register/mobile/activate #1893
# pylint: disable=unbalanced-tuple-unpacking
import json
import pytest
import time
from assistence import api
from assistence import initdata
from assistence import dbConnect
from pprint import pprint
env = 'QA2'
test_parameter = {}
header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
initdata.set_test_data(env, test_parameter)
Ok = []
def get_activate_code_in_identity_mobile_register_history(tmpToken):
    query_sql = "select activate_code from identity_mobile_register_history where token='{}'".format(tmpToken)
    [(activate_code,)]=dbConnect.dbQuery(test_parameter['db'], query_sql, 'shocklee')
    return activate_code

def set_phoneNumber_exists_in_identity(countryCode, mobile):
    update_sql = ["update identity set phone_country_code = '{}' and phone_number = '{}' where login_id = 'shoc3fsdfdf'".format(countryCode, mobile)]
    dbConnect.dbSetting(test_parameter['db'], update_sql, 'shocklee')

    api_name = '/api/v2/identity/register/mobile/send'
    body = {
        "countryCode" : countryCode, "mobile" : mobile, "loginId" : 'testAcc111', "password" : '323qerqw' }
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    restext = json.loads(res.text)
    tmpToken = restext['data']['tmpToken']
    activate_code = get_activate_code_in_identity_mobile_register_history(tmpToken)

    api_name = '/api/v2/identity/register/mobile/activate'
    body = {
        "tmpToken" : tmpToken,
        "activateCode" : activate_code,
    }
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)

def set_loginId_exists_in_identity(login_id):
    update_sql = ["update identity set login_id = '{}' where phone_number = '4343423'".format(login_id)]
    dbConnect.dbSetting(test_parameter['db'], update_sql, 'shocklee')

def set_ActCode_Expire_in_identity_mobile_register_history(tmpToken):
    time.sleep(2)
    update_sql = ["update identity_mobile_register_history set expires_in=1 where token ='{}'".format(tmpToken)]
    dbConnect.dbSetting(test_parameter['db'], update_sql, 'shocklee')

def set_Mobile_Sent_Reach_Limit(countryCode, mobile):
    api_name = '/api/v2/identity/register/mobile/send'
    body = {
        "countryCode" : countryCode,
        "mobile" : mobile,
        "loginId" : 'shock4324223423',
        "password" : 'pwd21322'
    }
    send = True
    while send :
        res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
        if res.status_code // 100 == 4:
            send = False

def delete_identity_by_mobile(countryCode, mobile):
    sqlList = []
    sqlList.append("delete from remain_points where identity_id in ( select id from identity where phone_country_code='{}' and phone_number = '{}')".format(countryCode, mobile))
    sqlList.append("delete from identity_role where identity_id in( select id from identity where phone_country_code='{}' and phone_number = '{}')".format(countryCode, mobile))
    sqlList.append("delete from user_settings where identity_id in( select id from identity where phone_country_code='{}' and phone_number = '{}')".format(countryCode, mobile))
    sqlList.append("delete from identity where phone_country_code='{}' and phone_number = '{}'".format(countryCode, mobile))
    dbConnect.dbSetting(test_parameter['db'], sqlList, 'shocklee')

def delete_identity_by_id(identity_id):
    sqlList = []
    sqlList.append("delete from remain_points where identity_id in ( select id from identity where login_id='{}')".format(identity_id))
    sqlList.append("delete from identity_role where identity_id in ( select id from identity where login_id='{}')".format(identity_id))
    sqlList.append("delete from user_settings where identity_id in ( select id from identity where login_id='{}')".format(identity_id))
    sqlList.append("delete from identity where login_id='{}'".format(identity_id))
    dbConnect.dbSetting(test_parameter['db'], sqlList, 'shocklee')
def setup_module():
    #先把記錄全部清除
    clear_sql = ["delete from identity_mobile_register_history"]
    dbConnect.dbSetting(test_parameter['db'], clear_sql, 'shocklee')

    #先把有這支手機 937855506 記錄給清除
    update_sql = ["update identity set phone_number=NULL where phone_number = '937855506'"]
    dbConnect.dbSetting(test_parameter['db'], update_sql, 'shocklee')

#https://receive-sms-free.net/
#https://receive-sms-free.net/Free-Japan-Phone-Number/818059845961/
#https://smstools.online/receive-free-sms/australia/1504922-61451562733
@pytest.mark.parametrize("scenario, ctyCode,        mobile,               loginId,                           pwd,  expect", [
    #正向列表
    (                   'HK Tel',  '+852',    '93470406 ',            'shock4ABC',                   '1qaz2wsx',     2),
    (                   'AU Tel',   '+61',   '476857122',             'shock621',                   '1qaz2wsx',     2),
    (                   'MA Tel',  '+853',    '63036640',             'shockA2c',                   '1qaz2wsx',     2),
    (                  'USA Tel',    '+1',  '4157415569',             'shock3281',                   'aaaaaaaa',     2),
    (                   'CN Tel',   '+86', '16532655629',             'shock4435',                   '1qaz2wsx',     2),
    (                   'ID tel',   '+62', '85574670577',             'shock4735',                   '11111111',     2),
    (                 'TW Tel 1',  '+886',  '0937855506',            'shock4q735',                   '1qaz2wsx',     2),
    (                   'PH tel',   '+63',  '9262751459',             'shock4835',                   '1qaz2wsx',     2),

    (                 'TW Tel 2',  '+886',   '937855506',             'shock6132',                   '1qaz2wsx',     2),
    (                 'pwd eq 5',  '+886',   '937855506',                 'shoc3',                      'H234B',     2),
    (                'pwd eq 20',  '+886',   '937855506',             'shock2555',       '01a34567Q9012V4567U9',     2),
    (             'loginId eq 5',  '+886',   '937855506',                'shOCK',                   '1qaz2wsx',     2),
    (            'loginId eq 20',  '+886',   '937855506', 'shock012345678901233',                   '1qaz2wsx',     2),

    # # # #反向列表
    (           'Invalid Tel ctyCode1', '+123', '15747708997',             'shockABC',                   '1qaz2wsx',     4),
    (           'Invalid Tel ctyCode2', '+099', '15747748997',             'shockABC',                   '1qaz2wsx',     4),
    (         'Invalid Tel USA mobile',   '+1',  '1234345345',             'shockABC',                   '1qaz2wsx',     4),
    (          'Invalid Tel TW mobile', '+886',    '92621631',             'shockABC',                   '1qaz2wsx',     4),
    (          'Invalid Tel CN mobile',  '+86',  '0937855506',             'shockABC',                   '1qaz2wsx',     4),

    (            'Invalid Pwd Over 20', '+886',  '0937855506',             'shockABC',   '012345678901234567890400',     4),
    (            'Invalid Pwd Under 5', '+886',  '0937855506',             'shockABC',                       '123Q',     4),
    (  'Invalid Pwd SpecialCharacter1', '+886',  '0937855506',             'shockABC',                     '&123Qa',     4),
    (  'Invalid Pwd SpecialCharacter2', '+886',  '0937855506',             'shockABC',                     'a123Q^',     4),
    (   'Invalid Pwd With EmptyString', '+886',  '0937855506',             'shockABC',                      ' 123Q',     4),


    (         'Invalid LoginID Over 20', '+886',  '0937855506','Ashock012345678901234',                   '1qaz2wsx',     4),
    (         'Invalid LoginID Under 5', '+886',  '0937855506',                 'shoc',                   '1qaz2wsx',     4),
    (    'Invalid LoginId SpecialChar1', '+886',   '937855506',             'shock!BC',                   '1qaz2wsx',     4),
    (    'Invalid LoginId SpecialChar2', '+886',  '0937855506',             'shockBC&',                   '1qaz2wsx',     4),
    ('Invalid LoginId With EmptyString', '+886',   '937855506',            'shock ABC',                   '1qaz2wsx',     4),

    (       'LoginId Exist In identity', '+886',  '937855507',             'love1234',                   '1qaz2wsx',     4),
    (         'Mobile Sent Reach Limit', '+886',  '937855506',             'shockABC',                   '1qaz2wsx',     4),
    (     'Mobile Exist Is In Identity', '+886',  '988545866',             'shockABC',                   '1qaz2wsx',     4),
])

def test_register_mobile_send(scenario, ctyCode, mobile, loginId, pwd, expect):
    #先把之前註冊成功的給刪除
    delCtyCode = ctyCode  if ctyCode.find("+") != -1  else ctyCode[1:]
    delMobile = mobile[1:] if mobile.startswith("0")  else mobile
    #print(DBctyCode)
    delete_identity_by_mobile(delCtyCode, delMobile)
    delete_identity_by_id(loginId)
    if expect == 4:
        if scenario == 'LoginId Exist In identity':
            pass
            #set_loginId_exists_in_identity(loginId)
        elif scenario == 'Mobile Sent Reach Limit':
            set_Mobile_Sent_Reach_Limit(ctyCode, mobile)
        elif scenario == 'Mobile Exist Is In Identity':
            pass
            #set_phoneNumber_exists_in_identity(ctyCode, mobile)
    api_name = '/api/v2/identity/register/mobile/send'
    body = {
        "countryCode" : ctyCode,
        "mobile" : mobile,
        "loginId" : loginId,
        "password" : pwd
    }
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    restext = json.loads(res.text)
    #assert res.status_code // 100 == expect
    if expect == 2:
        assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
        assert restext['data']['tmpToken'] != None
        tmpToken = restext['data']['tmpToken']
        activate_code = get_activate_code_in_identity_mobile_register_history(tmpToken)
        Ok.append( {"loginId": loginId, "tmpToken": tmpToken, "activateCode" : activate_code ,"countryCode": ctyCode, "mobile": mobile} )
    elif expect == 4:
        assert res.status_code == 400
        if scenario.find('Invalid Tel') != -1:
            assert restext['Message'] == 'MOBILE_FORMAT_INVALID'
        elif scenario.find('Invalid Pwd') != -1:
            assert restext['Message'] == 'PASSWORD_FORMAT_INVALID'
        elif scenario.find('Mobile Exist') != -1:
            assert restext['Message'] == 'MOBILE_HAS_BEEN_BOUND'
        elif scenario.find('Reach Limit') != -1:
            assert restext['Message'] == 'WEEKLY_LIMIT_OF_MOBILECODE_SENT_REACHED'
        elif scenario.find('Invalid LoginId') != -1:
            assert restext['Message'] == 'LOGINID_FORMAT_INVALID'
        elif scenario.find('LoginId Exist') != -1:
            assert restext['Message'] == 'LOGINID_HAS_BEEN_OCCUPIED'

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.parametrize(    "scenario,    index,    expect", [
    # # #正向列表
    (                         'CN Tel',       4,         2),
    (                         'ID tel',       5,         2),
    (                       'TW Tel 1',       6,         2),

    # #反向列表
    (       'Mobile Exist In Identity',       0,         4),
    (      'LoginId Exist In identity',       1,         4),
    (           'Activate Code Expire',       2,         4),
    (            'Activate Code Error',       3,         4),
])
def test_register_mobile_activate(scenario, index, expect):
    loginId, tmpToken, activateCode, countryCode, mobile = Ok[index]['loginId'], Ok[index]['tmpToken'], Ok[index]['activateCode'], Ok[index]['countryCode'], Ok[index]['mobile']
    #如果是反向列表，先設定好環境
    if expect == 4 :
        if scenario == 'Mobile Exist In Identity':
            set_phoneNumber_exists_in_identity(countryCode, mobile)
        elif scenario == 'LoginId Exist In identity':
            set_loginId_exists_in_identity(loginId)
        elif scenario ==  'Activate Code Expire':
            set_ActCode_Expire_in_identity_mobile_register_history(tmpToken)
        elif scenario ==  'Activate Code Error':
            activateCode = '99942332'
    api_name = '/api/v2/identity/register/mobile/activate'
    body = {
        "tmpToken" : tmpToken,
        "activateCode" : activateCode,
    }
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    assert res.status_code // 100 == expect
    restext = json.loads(res.text)
    if expect == 2:
        print(restext)
        assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
        assert restext['data']['nonce'] != None and restext['data']['token'] != None and restext['data']['idToken'] != None
        nonce, token = restext['data']['nonce'], restext['data']['token']
        #確認手機是否註冊成功，拿 nonce 與 token 比對資料庫 看看是否一樣
        query_sql = "select token, nonce from identity where login_id='{}' and status='1'".format(loginId)
        [(sql_token,sql_nonce)]=dbConnect.dbQuery(test_parameter['db'], query_sql, 'shocklee')
        assert nonce == sql_nonce
        assert token == sql_token
        #確認手機是否註冊成功，檢查identity_mobile_register_history是否為1
        query_sql = "select status from identity_mobile_register_history where token='{}'".format(tmpToken)
        [(sql_status,)]= dbConnect.dbQuery(test_parameter['db'], query_sql, 'shocklee')
        assert sql_status == 1
        #把註冊成功地清除
        delCtyCode = countryCode  if countryCode.find("+") != -1  else countryCode[1:]
        delMobile = mobile[1:] if mobile.startswith("0")  else mobile
        delete_identity_by_mobile(delCtyCode, delMobile)
    elif expect == 4:
        assert res.status_code == 400
        if scenario.find('Code Expire') != -1:
            assert restext['Message'] == 'MOBILE_ACTIVATE_CODE_EXPIRED'
        elif scenario.find('Mobile Exist') != -1:
            assert restext['Message'] == 'MOBILE_HAS_BEEN_BOUND'
        elif scenario.find('LoginId Exist') != -1:
            assert restext['Message'] == 'LOGINID_HAS_BEEN_OCCUPIED'
            delete_identity_by_id('testAcc111')
        elif scenario.find('Code Error') != -1:
            assert restext['Message'] == 'MOBILE_ACTIVATE_CODE_ERROR'