import hashlib
import datetime
import requests
import json
import urllib.parse
from pprint import pprint

def generate_signKey(phone_num, timestamp, ace_sign = 'ACE_SIGN'):
    data = ace_sign + str(timestamp) + phone_num
    md5 = hashlib.md5()
    md5.update(data.encode("utf-8"))
    signKey = md5.hexdigest()
    return signKey

def post_api(data, api_url):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", api_url, headers=headers, data = data)
    obj = json.loads(response.text)
    pprint(obj)



if __name__ == '__main__':

    produ_site = 'https://www.ace.io/polarisex/open/v1'
    stage_site = 'https://stage.ace.io/polarisex/open/v1'
    test_site = 'http://localhost:8000'
    url_path = '/coin/customerAccount'
    url_path = '/coin/coinRelations'
    api_url = stage_site + url_path
#    api_url = test_site
    uid = '437'
    apiKey = "437#2020"
    securityKey = "50caded91f924ed184ce173177294b15"

    phone_num = '0886936736561'
    timestamp = int(datetime.datetime.now().timestamp())
    format_timestamp = str('{:0<13d}'.format(timestamp))
    signKey = generate_signKey(phone_num, format_timestamp)
    format_timestamp = urllib.parse.quote_plus(format_timestamp)

    data = {
        'uid': uid,
        'timeStamp': format_timestamp,
        'signKey': signKey,
        'apiKey' : apiKey,
        'securityKey' : securityKey
    }

    data = urllib.parse.urlencode(data)

#    data = "uid={}&timeStamp={}&signKey={}&apiKey={}&securityKey={}".format(uid, format_timestamp, signKey, apiKey, securityKey)
    post_api(data, api_url)

    print('uid', uid)
    print('timeStamp', format_timestamp)
    print('signKey', signKey)
    print('apiKey', apiKey)
    print('securityKey', securityKey)
    print(data)
