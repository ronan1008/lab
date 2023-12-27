import json
import requests
from pprint import pprint
from . import dbConnect
import sys
# string = {'method': 'Network.webSocketFrameSent', 'params': {'requestId': '5684.20', 'response': {'mask': True, 'opcode': 1, 'payloadData': '{"action":"registerGameRoom","data":{"totalPlayers":5,"passwordToGuess":50,"fee":1000,"maxGuessNumber":99,"minGuessNumber":1,"punishmentDesc":"Donate Me!"}}'}, 'timestamp': 37902.383863}}

# print(string)
# payloadData = json.loads(string['params']['response']['payloadData'])
# print('------')
# pprint(payloadData)
# print('------')
# print('register room ' + str(payloadData['data']))
def add_point(prefix, id, header):
    url = prefix + '/api/v1/identity/' + id + '/points'
    body = {'addPoints': 3000000, 'ratio': 2, 'reason': 'game testing'}
    requests.put(url, headers=header, json=body)
    #str1 = res.text
    return

def user_login(prefix, account, pwd):
    url = prefix + '/api/v2/identity/auth/login'
    body = {
        "account": account,
        "password": pwd,
        "pushToken": ''
    }
    #print(body)
    res = requests.post(url, json=body)
    #print(json.loads(res.text))
    if res.status_code // 100 == 2:
        restext = json.loads(res.text)
        return(restext)
    else:
        return(json.loads(res.text))



prefix = 'http://testing-api.xtars.com'
result = user_login(prefix, 'tl-lisa', '12345678')
backend_token, backend_nonce  = result['data']['token'], result['data']['nonce']
back_header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': backend_token, 'X-Auth-Nonce':backend_nonce}
print(back_header)



db = 'testing-api.truelovelive.com.tw'

query_id = "SELECT `identity`.id,`identity`.login_id, remain_points.remain_points FROM `identity`  join remain_points on remain_points.identity_id = identity.id WHERE `identity`.login_id like 'guest%' and remain_points.remain_points < 2000000"
identity_data = dbConnect.dbQuery(db, query_id, user = 'shocklee')

for x in identity_data:
    identity_id =  x[0]
    login_id = x[1]
    print(identity_id, login_id)
    sys.exit('remove this line to execute')
    add_point(prefix, identity_id, back_header)
    print(login_id + ' success')
