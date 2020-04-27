import hashlib
import datetime
import requests
import json
import urllib.parse
import multiprocessing
from pprint import pprint

class Ace:
    '''Initial Settings'''
    def __init__(self, uid, apiKey, securityKey, phone_num):

        self.base_url = 'https://stage.ace.io/polarisex/open/v1'
        self.uid = '437'
        self.apiKey = "437#2020"
        self.securityKey = "50caded91f924ed184ce173177294b15"
        self.phone_num = '0886936736561'
        self.ace_sign = 'ACE_SIGN'
        self.timestamp = self._ace_format_timestamp()
        self.signKey = self._generate_signKey()
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.data = None
        #dictionary
        self.currency = { 'TWD':1, 'BTC':2, 'ETH':4, 'LTC':7, 'XRP':10, 'TRX':13, 'USDT':14, 'BNB':17, 'BTT':19, }
        self.buy_or_sell = { 'buy':1, 'sell':2, }
        self.order_type = { 'limit':1, 'market':2, }

    '''timestamp trans to ace format'''
    def _ace_format_timestamp(self):
        timestamp = int(datetime.datetime.now().timestamp())
        format_timestamp = str('{:0<13d}'.format(timestamp))
        return format_timestamp
    '''generate signkey'''
    def _generate_signKey(self):
        data = self.ace_sign + str(self.timestamp) + self.phone_num
        md5 = hashlib.md5()
        md5.update(data.encode("utf-8"))
        signKey = md5.hexdigest()
        return signKey
    '''post api'''
    def _post_api(self, data, partial_url):
        api_url = self.base_url + partial_url
        headers = self.headers
        data = urllib.parse.urlencode(data)
        response = requests.request("POST", api_url, headers=headers, data = data)
        obj = json.loads(response.text)
        return obj

    '''show customer information'''
    def customer_account_info(self):
        partial_url = '/coin/customerAccount'

        self.data = {
            'uid': self.uid,
            'timeStamp': self.timestamp,
            'signKey': self.signKey,
            'apiKey' : self.apiKey,
            'securityKey' : self.securityKey
        }

        obj = self._post_api(self.data, partial_url)
        return obj

    def get_coin_exchange_info(self):
        partial_url = '/coin/coinRelations'

        self.data = {
            'uid': self.uid,
            'timeStamp': self.timestamp,
            'signKey': self.signKey,
            'apiKey' : self.apiKey,
            'securityKey' : self.securityKey
        }
        obj = self._post_api(self.data, partial_url)
        return obj

    def get_kline_info(self,tradeCurrencyId, baseCurrencyId, limit):
        partial_url = '/kline/getKlineMin'
        self.data = {
            'uid': self.uid,
            'timeStamp': self.timestamp,
            'signKey': self.signKey,
            'apiKey' : self.apiKey,
            'securityKey' : self.securityKey,
            'tradeCurrencyId' : tradeCurrencyId,
            'baseCurrencyId' : baseCurrencyId,
            'limit' : limit,
        }
        obj = self._post_api(self.data, partial_url)
        return obj


    def new_order(self, currencyId, baseCurrencyId, buyOrSell, price, num, trade_type):
        partial_url = '/order/order'
        self.data = {
            'uid': self.uid,
            'timeStamp': self.timestamp,
            'signKey': self.signKey,
            'apiKey' : self.apiKey,
            'securityKey' : self.securityKey,
            'currencyId' : self.currency[currencyId],
            'baseCurrencyId' : self.currency[baseCurrencyId],
            'buyOrSell' : self.buy_or_sell[buyOrSell],
            'price' : price,
            'num' : num,
            'type' : self.order_type[trade_type],
            'fdPassword' : None,
        }
        obj = self._post_api(self.data, partial_url)
        return "Create order "+obj['attachment']+" Success!!" if obj['status']== 200 else  obj['message']


    def cancel_order(self, orderNo):
        #print("process: {} start".format(orderNo))
        partial_url = '/order/cancel'
        self.data = {
            'uid': self.uid,
            'timeStamp': self.timestamp,
            'signKey': self.signKey,
            'apiKey' : self.apiKey,
            'securityKey' : self.securityKey,
            'orderNo': orderNo,
        }

        obj = self._post_api(self.data, partial_url)
        return "Cancel "+orderNo+" Success!!" if obj['status']== 200 else  obj['message']



    def get_order_list(self):
        partial_url = '/order/getOrderList'
        self.data = {
            'uid': self.uid,
            'timeStamp': self.timestamp,
            'signKey': self.signKey,
            'apiKey' : self.apiKey,
            'securityKey' : self.securityKey,
            # 'baseCurrencyId' : None,
            # 'tradeCurrencyId' : None,
            # 'start' : None,
            'size' : 100,
        }
        obj = self._post_api(self.data, partial_url)
        return obj

    def show_order_status(self, orderId):
        partial_url = '/order/showOrderStatus'
        self.data = {
            'uid': self.uid,
            'timeStamp': self.timestamp,
            'signKey': self.signKey,
            'apiKey' : self.apiKey,
            'securityKey' : self.securityKey,
            'orderId' : orderId,
        }
        obj = self._post_api(self.data, partial_url)
        return obj

    def show_order_history(self, orderId):
        partial_url = '/order/showOrderHistory'
        self.data = {
            'uid': self.uid,
            'timeStamp': self.timestamp,
            'signKey': self.signKey,
            'apiKey' : self.apiKey,
            'securityKey' : self.securityKey,
            'orderId' : orderId,
        }
        obj = self._post_api(self.data, partial_url)
        return obj



    def get_order_list_id(self):
        order_list = self.get_order_list()
        order_id_list = []
        order_len = len(order_list['attachment'])
        for i in range(order_len):
            order_id_list.append(order_list['attachment'][i]['orderNo'])
        return order_id_list


    def cancel_all_order(self):
        order_list_id = self.get_order_list_id()

        if len(order_list_id) == 0:
            return "Cancel all order finished"
        else:
            pool = multiprocessing.Pool(processes = 5)
            for orderNo in order_list_id:
                pool.apply_async(self.cancel_order, (orderNo,))
            pool.close()
            pool.join()
            print('Contiune Deleting....')
            return self.cancel_all_order()

    def batch_new_order(self, currencyId, baseCurrencyId, buyOrSell, price, num, trade_type, batchNum):
        start_time = datetime.datetime.now()
        pool = multiprocessing.Pool(processes = 5)
        for i in range(batchNum):
            #使用 TWD 買入BTC,以 現價委託 193346.9的價格買入數量 0.001
            pool.apply_async(self.new_order, (currencyId, baseCurrencyId, buyOrSell, price, num, trade_type))
        pool.close()
        pool.join()
        end_time = datetime.datetime.now()

        total_time = end_time - start_time
        total_time = total_time.seconds
        return '一共產生{}筆訂單,花了{:.2f}秒'.format(batchNum, total_time)

if __name__ == '__main__':
    #uid, apiKey, securityKey, phone_num
    member_a = Ace(437, "437#2020", "50caded91f924ed184ce173177294b15", '0886936736561')
    account_info = member_a.customer_account_info()
    pprint(account_info)
    pprint(member_a.data)

    #使用 TWD 買入BTC,以 現價委託 193346.9的價格買入數量 0.001
    #order_status = member_a.new_order('BTC', 'TWD', 'buy', "193346.9" , "0.001", 'limit')

    #使用 mutli-process 大量產生 1000 筆: TWD 買入BTC,以 現價委託 193346.9的價格買入數量 0.001
    #order_status = member_a.batch_new_order('BTC', 'TWD', 'buy', "193346.9" , "0.001", 'limit', 5000)
    #print(order_status)

    #得到所有訂單的id
    #id_list = member_a.get_order_list_id()
    #print(id_list)


    #刪除所有訂單
    #cancel_status = member_a.cancel_all_order()
    #print(cancel_status)


    #查看該筆訂單歷史紀錄
    #order_status = member_a.show_order_history('15875352484822652103401100243963')
    #pprint(order_status)
