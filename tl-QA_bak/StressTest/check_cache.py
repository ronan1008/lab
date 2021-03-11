from second import apilib
import requests
import time

test_env = 'http://35.236.145.25:8080'
header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}


if __name__ == '__main__':
    prefix = '/api/v2/'
    test_api = [{'api': 'liveMaster/0cc58d56-cd7d-4400-a121-1142b08bf1a1/photoPost?item=10&page=1',
                 'sleep_time': 4, 'duration': 6},
                {'api': 'liveMaster/photoPost/430', 'sleep_time': 4, 'duration': 6},
                {'api': 'liveMaster/photoPost/403/comment?item=10&page=1', 'sleep_time': 0, 'duration': 2},
                {'api': 'liveMaster/0cc58d56-cd7d-4400-a121-1142b08bf1a1/fans?item=10&page=0',
                 'sleep_time': 0, 'duration': 2},
                {'api': 'liveMaster/d82a7ba2-5c11-4615-aba7-2a768d927165/nameCard', 'sleep_time': 0, 'duration': 2}]
    head = apilib.user_login(test_env, 'broadcaster008', '123456', header)
    for i in test_api:
        url = test_env + prefix + i['api']
        beg_time1 = int(time.time())
        res1 = requests.get(url, headers=head)
        end_time1 = int(time.time())
        time.sleep(i['sleep_time'])
        beg_time2 = int(time.time())
        res2 = requests.get(url, headers=head)
        end_time2 = int(time.time())
        if (end_time1 - beg_time1) < (end_time2 - beg_time2):
            print('%s need check cache(first:%d, second:%d)' % (i['api'], (end_time1 - beg_time1), (end_time2 - beg_time2)))
        time.sleep(i['duration'])
        beg_time3 = int(time.time())
        res3 = requests.get(url, headers=head)
        end_time3 = int(time.time())
        print('%s second query(first:%d, second:%d)' % (i['api'], (end_time1 - beg_time1), (end_time3 - beg_time3)))




