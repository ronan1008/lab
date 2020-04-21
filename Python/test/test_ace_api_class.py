import hashlib
import datetime
import requests
import json
import urllib.parse
import multiprocessing
from pprint import pprint

class Ace:

    def __init__(self):

        self.base_url = 'https://stage.ace.io/polarisex/open/v1'
        self.uid = '437'
        self.apiKey = "437#2020"
        self.securityKey = "50caded91f924ed184ce173177294b15"
        self.phone_num = '0886936736561'
        self.ace_sign = 'ACE_SIGN'
        self.timestamp = self.ace_format_timestamp()
        self.signKey = self.generate_signKey()
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        self.currency = { 'TWD':1, 'BTC':2, 'ETH':4, 'LTC':7, 'XRP':10, 'TRX':13, 'USDT':14, 'BNB':17, 'BTT':19, }
        self.buy_or_sell = { 'buy':1, 'sell':2, }
        self.order_type = { 'limit':1, 'market':2, }

    def ace_format_timestamp(self):
        timestamp = int(datetime.datetime.now().timestamp())
        format_timestamp = str('{:0<13d}'.format(timestamp))
        return format_timestamp

    def generate_signKey(self):
        data = self.ace_sign + str(self.timestamp) + self.phone_num
        md5 = hashlib.md5()
        md5.update(data.encode("utf-8"))
        signKey = md5.hexdigest()
        return signKey

    def post_api(self, data, partial_url):
        api_url = self.base_url + partial_url
        headers = self.headers
        data = urllib.parse.urlencode(data)
        response = requests.request("POST", api_url, headers=headers, data = data)
        obj = json.loads(response.text)
        return obj

    def customer_account_info(self):
        partial_url = '/coin/customerAccount'

        data = {
            'uid': self.uid,
            'timeStamp': self.timestamp,
            'signKey': self.signKey,
            'apiKey' : self.apiKey,
            'securityKey' : self.securityKey
        }

        obj = self.post_api(data, partial_url)
        return obj

    def get_coin_exchange_info(self):
        partial_url = '/coin/coinRelations'

        data = {
            'uid': self.uid,
            'timeStamp': self.timestamp,
            'signKey': self.signKey,
            'apiKey' : self.apiKey,
            'securityKey' : self.securityKey
        }
        obj = self.post_api(data, partial_url)
        return obj

    def get_kline_info(self,tradeCurrencyId, baseCurrencyId, limit):
        partial_url = '/kline/getKlineMin'
        data = {
            'uid': self.uid,
            'timeStamp': self.timestamp,
            'signKey': self.signKey,
            'apiKey' : self.apiKey,
            'securityKey' : self.securityKey,
            'tradeCurrencyId' : tradeCurrencyId,
            'baseCurrencyId' : baseCurrencyId,
            'limit' : limit,
        }
        obj = self.post_api(data, partial_url)
        return obj