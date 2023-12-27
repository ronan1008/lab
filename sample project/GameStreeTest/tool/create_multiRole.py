# pylint: disable=unbalanced-tuple-unpacking
# 建立多個 users
import json
import pytest
import time
import sys
from pprint import pprint
# import dbConnect
# import api
from . import dbConnect
from . import api
# import api

def get_activate_code(db, registerMethod, tmpToken):
    if registerMethod == 'Mail':
        query_sql = "select activate_code from identity_email_register_history where token='{}'".format(tmpToken)
    elif registerMethod == 'Mobile':
        query_sql = "select activate_code from identity_mobile_register_history where token='{}'".format(tmpToken)
    else:
        return False

    [(activate_code,)]= dbConnect.dbQuery(db, query_sql, 'shocklee')
    return str(activate_code)
def mobile_register_active(db, cty_code, mobile_num, loginId, password):
    #註冊mobile
    api_name = '/api/v2/identity/register/mobile/send'
    body = {
        "countryCode" : cty_code,
        "mobile" : mobile_num,
        "loginId" : loginId,
        "password" : password
    }
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    restext = json.loads(res.text)

    print(restext)
    assert res.status_code == 200
    tmpToken = restext['data']['tmpToken']


    #啟用mobile
    activate_code = get_activate_code(db, 'Mobile', tmpToken)
    api_name = '/api/v2/identity/register/mobile/activate'
    body = {
        "tmpToken" : tmpToken,
        "activateCode" : activate_code,
    }
    res = api.apiFunction(test_parameter['prefix'], header, api_name, 'post', body)
    print(res)


def changeRole(prefix, token, nonce, idList, roleType):
    #5:一般用戶；4:直播主
    header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
    header['X-Auth-Token'] = token
    header['X-Auth-Nonce'] = nonce
    url = '/api/v2/backend/user/role'
    body = {'ids': idList, 'role': roleType}
    res = api.apiFunction(prefix, header, url, 'patch', body)
    return(res)

def get_id_by_loginId(prefix, token, nonce, account):
    header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': token, 'X-Auth-Nonce': nonce}
    id = api.search_user(prefix, account, header)
    return id


if __name__ == '__main__':

    env = 'QA2'
    test_parameter=dict()

    if env == 'QA':
        test_parameter['prefix'] = 'http://35.234.17.150'
        test_parameter['db'] = '35.234.17.150'
    elif env == 'test':
        test_parameter['prefix'] = 'http://testing-api.xtars.com'
        test_parameter['db'] = 'testing-api.truelovelive.com.tw'
    elif env == 'QA2':
        test_parameter['prefix'] = 'http://34.80.110.80'
        test_parameter['db'] = '34.80.110.80'
    # server = dbConnect2.createSSH(test_parameter['db'])
    # server.start()


    acc_prefix = 'voiceMaster'
    tel_prefix = '99887'

    regAccList = [  ("{}{:0>4d}".format(acc_prefix,i) , "{}{:0>4d}".format(tel_prefix, i)  ) for i in range(1, 5)]
    pprint(regAccList)
    # sys.exit('test, remove this line to execute')
    change_id_list=[]
    #regitster and active
    # result = api.user_login(test_parameter['prefix'], 'tl-lisa', '1234567')
    result = api.user_login(test_parameter['prefix'], 'tl-lisa', '123456')

    header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
    test_parameter['backend_token'] = result['data']['token']
    test_parameter['backend_nonce'] = result['data']['nonce']

    for regAcc, mobile in regAccList :
        regLoginId =  '886' + mobile
        mobile_register_active(test_parameter['db'], '+886', mobile, regAcc, '123456')
        identity = get_id_by_loginId(test_parameter['prefix'], test_parameter['backend_token'], test_parameter['backend_nonce'], regLoginId)
        change_id_list.append(identity)

    #change role
    res = changeRole(test_parameter['prefix'], test_parameter['backend_token'], test_parameter['backend_nonce'], change_id_list, 4)
    # res = changeRole(test_parameter['prefix'], test_parameter['backend_token'], test_parameter['backend_nonce'], change_id_list, 14)
    print()
    assert res.status_code == 200
    # server.stop()

# UPDATE identity SET login_id = CONCAT_WS('', 'gamehost', SUBSTR(login_id, 9, 4)) WHERE login_id LIKE '886991650%'