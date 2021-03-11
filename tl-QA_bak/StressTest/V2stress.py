from second import apilib
import threading
import random
import sys
import traceback
import requests

test_env = 'http://35.236.145.25:8080'
stage_env = 'http://104.199.175.123:80'
header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
header1 = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}


def analyze_api(env, api_str, acc, admin):
    master = ['beauty12', 'beauty16', 'broadcaster008', 'broadcaster011', 'broadcaster009', 'beauty20']
    if acc == '':
        i = random.randint(0, len(master) - 1)
        uid = apilib.search_user(env, master[i], admin)
        api = api_str.replace('{{MasterId}}', uid)
    else:
        uid = apilib.search_user(env, acc, admin)
        api = api_str.replace('{{uid}}', uid)
    return api


def job(user_acc, process_num, admin):
    env = test_env
    prefix = '/api/v2/'
    test_api = [{'api': 'runway/list', 'parameter': ''},
                {'api': 'tag/list', 'parameter': ''},
                {'api': 'recommend/list', 'parameter': ''},
                {'api': 'backend/achievement/list', 'parameter': ''},
                {'api': 'identity/{{uid}}/role/liveController?item=20&page=1', 'parameter': 'uid'},
                {'api': 'liveMaster/{{MasterId}}/onAirTime', 'parameter': 'MasterId'},
                {'api': 'liveMaster/{{MasterId}}/nameCard', 'parameter': 'MasterId'},
                {'api': 'liveMaster/{{MasterId}}/photoPost?item=10&page=0', 'parameter': 'MasterId'},
                {'api': 'identity/{{uid}}/achievement/effect', 'parameter': 'uid'}]

    try:
        head = apilib.user_login(env, user_acc, '123456', header)
        while 1:
            if len(test_api) == 0:
                break
            i = random.randint(0, len(test_api) - 1)
            if test_api[i]['parameter'] == '':
                url = env + prefix + test_api[i]['api']
                res = requests.get(url, headers=head)
            else:
                if test_api[i]['parameter'] == 'uid':
                    api_str = analyze_api(env, test_api[i]['api'], user_acc, admin)
                else:
                    api_str = analyze_api(env, test_api[i]['api'], '', admin)
                url = env + prefix  + api_str
                res = requests.get(url, headers=head)
            print('num=%d, test=%s, result=%d' % (process_num, url, res.status_code))
            test_api.pop(i)
    except Exception as err:
        print(err)
    finally:
        return()


if __name__ == '__main__':
    admin = apilib.user_login(test_env, 'tl-lisa', '12345678', header1)
    act = 'track'
    numList = []
 #   beg = int(sys.argv[1])
 #   end = int(sys.argv[2])
#    for i in range(beg, end):
    for i in range(4, 6):
        k = str(i + 1)
        if (len(k)) == 1:
            account = act + '000' + k
        elif (len(k)) == 2:
            account = act + '00' + k
        elif (len(k)) == 3:
            account = act + '0' + k
        else:
            account = act + k
        p = threading.Thread(target=job, args=(account, i, admin, ))
        numList.append(p)
    try:
        for p in numList:
            p.start()
    except Exception as err:
        print('Process abnormal %s' % err)
        traceback.print_exc()
    finally:
        for p in numList:
            p.join()
        print('Process end.')
