import hashlib
import datetime
import requests
import json
import urllib.parse
import multiprocessing
from pprint import pprint

def generate_signKey(phone_num, timestamp, ace_sign = 'ACE_SIGN'):
    data = ace_sign + str(timestamp) + phone_num
    md5 = hashlib.md5()
    md5.update(data.encode("utf-8"))
    signKey = md5.hexdigest()
    return signKey

def ace_format_timestamp():
    timestamp = int(datetime.datetime.now().timestamp())
    format_timestamp = str('{:0<13d}'.format(timestamp))
    return format_timestamp

def post_api(api_url, data):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = urllib.parse.urlencode(data)
    response = requests.request("POST", api_url, headers=headers, data = data)
    obj = json.loads(response.text)
    return obj

def customer_account_info(base_url, uid, apikey, securityKey, phone_num):
    partial_url = '/coin/customerAccount'
    format_timestamp = ace_format_timestamp()
    signKey = generate_signKey(phone_num, format_timestamp)
    
    data = {
        'uid': uid,
        'timeStamp': format_timestamp,
        'signKey': signKey,
        'apiKey' : apiKey,
        'securityKey' : securityKey
    }

    main_url = base_url + partial_url
    obj = post_api(main_url, data)
    return obj


def get_coin_exchange_info(base_url, uid, apikey, securityKey, phone_num):
    partial_url = '/coin/coinRelations'
    format_timestamp = ace_format_timestamp()
    signKey = generate_signKey(phone_num, format_timestamp)
    
    data = {
        'uid': uid,
        'timeStamp': format_timestamp,
        'signKey': signKey,
        'apiKey' : apiKey,
        'securityKey' : securityKey
    }

    main_url = base_url + partial_url
    obj = post_api(main_url, data)
    return obj

def get_kline_info(base_url, uid, apikey, securityKey, phone_num, tradeCurrencyId, baseCurrencyId, limit):
    partial_url = '/kline/getKlineMin'
    format_timestamp = ace_format_timestamp()
    signKey = generate_signKey(phone_num, format_timestamp)

    data = {
        'uid': uid,
        'timeStamp': format_timestamp,
        'signKey': signKey,
        'apiKey' : apiKey,
        'securityKey' : securityKey,
        'tradeCurrencyId' : tradeCurrencyId,
        'baseCurrencyId' : baseCurrencyId,
        'limit' : limit,
    }
    main_url = base_url + partial_url
    obj = post_api(main_url, data)
    return obj

def new_order(base_url, uid, apiKey, securityKey, phone_num, currencyId, baseCurrencyId, buyOrSell, price, num, trade_type):
    partial_url = '/order/order'
    format_timestamp = ace_format_timestamp()
    signKey = generate_signKey(phone_num, format_timestamp)

    data = {
        'uid': uid,
        'timeStamp': format_timestamp,
        'signKey': signKey,
        'apiKey' : apiKey,
        'securityKey' : securityKey,
        'currencyId' : currencyId,
        'baseCurrencyId' : baseCurrencyId,
        'buyOrSell' : buyOrSell,
        'price' : price,
        'num' : num,
        'type' : trade_type,
        'fdPassword' : None,
    }
    main_url = base_url + partial_url
    obj = post_api(main_url, data)
    return "Create order "+obj['attachment']+" Success!!" if obj['status']== 200 else  obj['message']


def cancel_order(base_url, uid, apiKey, securityKey, orderNo):
    print("process: {} start".format(orderNo))
    partial_url = '/order/cancel'
    format_timestamp = ace_format_timestamp()
    signKey = generate_signKey(phone_num, format_timestamp)

    data = {
        'uid': uid,
        'timeStamp': format_timestamp,
        'signKey': signKey,
        'apiKey' : apiKey,
        'securityKey' : securityKey,
        'orderNo':orderNo,
    }

    main_url = base_url + partial_url
    obj = post_api(main_url, data)
    return "Cancel "+orderNo+" Success!!" if obj['status']== 200 else  obj['message']

def get_order_list(base_url, uid, apiKey, securityKey):
    partial_url = '/order/getOrderList'
    format_timestamp = ace_format_timestamp()
    signKey = generate_signKey(phone_num, format_timestamp)

    data = {
        'uid': uid,
        'timeStamp': format_timestamp,
        'signKey': signKey,
        'apiKey' : apiKey,
        'securityKey' : securityKey,
        # 'baseCurrencyId' : None,
        # 'tradeCurrencyId' : None,
        # 'start' : None,
        'size' : 100,
    }

    main_url = base_url + partial_url
    obj = post_api(main_url, data)
    return obj

def get_order_list_id(base_url, uid, apiKey, securityKey):
    order_list = get_order_list(base_url, uid, apiKey, securityKey)
    order_id_list = []
    order_len = len(order_list['attachment'])
    for i in range(order_len):
        order_id_list.append(order_list['attachment'][i]['orderNo'])
    return order_id_list

def cancel_all_order(base_url, uid, apiKey, securityKey):
    
    order_list_id = get_order_list_id(base_url, uid, apiKey, securityKey)
    pool = multiprocessing.Pool(processes = 10)
    for orderNo in order_list_id:
        # print(base_url, uid, apiKey, securityKey, orderNo)
        cancel_status = pool.apply_async(cancel_order, (base_url,uid,apiKey,securityKey,orderNo))
        print(cancel_status)
    pool.close()
    pool.join()
    print('Ending....')

if __name__ == '__main__':

    #base settings
    currency = { 'TWD':1, 'BTC':2, 'ETH':4, 'LTC':7, 'XRP':10, 'TRX':13, 'USDT':14, 'BNB':17, 'BTT':19, }
    buy_or_sell = { 'buy':1, 'sell':2, }
    order_type = { 'limit':1, 'market':2, }

    base_url = 'https://stage.ace.io/polarisex/open/v1'
    uid = '437'
    apiKey = "437#2020"
    securityKey = "50caded91f924ed184ce173177294b15"
    phone_num = '0886936736561'
    
    # 獲得用戶資訊
    # customer_info = customer_account_info(base_url, uid, apiKey, securityKey, phone_num)
    # pprint(customer_info)

    # 得到所有交易對資訊
    # exchange_info = get_coin_exchange_info(base_url, uid, apiKey, securityKey, phone_num)
    # pprint(exchange_info)

    # 得到特定交易對資訊
    # twd_to_btc = get_kline_info(base_url, uid, apiKey, securityKey, phone_num, 2, 1, 5)
    # pprint(twd_to_btc)
    
    # 下訂單
    # TWD_BTC_order = new_order(base_url, uid, apiKey, securityKey, phone_num, currency['BTC'], currency['TWD'], buy_or_sell['buy'], 193346.9, 0.001, order_type['limit'])
    # orderNo = TWD_BTC_order['attachment']

    pool = multiprocessing.Pool(processes = 10)
    for i in range(1000):
            #使用 TWD 買入BTC,以 現價委託 193346.9的價格買入數量 0.001 
            # TWD_BTC_order = new_order(base_url, uid, apiKey, securityKey, phone_num, currency['BTC'], currency['TWD'], buy_or_sell['buy'], 193346.9, 0.001, order_type['limit'])
            
            TWD_BTC_order = pool.apply_async(new_order, (base_url,uid,apiKey,securityKey,phone_num,currency['BTC'],currency['TWD'],buy_or_sell['buy'],193346.9,0.001,order_type['limit']))
            print(TWD_BTC_order)
            print('第{}筆'.format(i))
    pool.close()
    pool.join()
    print('Ending....')

    # for i in range(10):
    #         #使用 TWD 買入BTC,以 現價委託 193346.9的價格賣出數量 0.001 
    #         TWD_BTC_order = new_order(base_url, uid, apiKey, securityKey, phone_num, currency['BTC'], currency['TWD'], buy_or_sell['sell'], 190346.9, 0.001, order_type['limit'])
    #         print(TWD_BTC_order)
    # 訂單資訊列表
    # order_list = get_order_list(base_url, uid, apiKey, securityKey)

    # 訂單id列表
    # order_list_id = get_order_list_id(base_url, uid, apiKey, securityKey)
    # pprint(order_list_id)
        
    # 取消所有訂單
    #cancel_all_order(base_url, uid, apiKey, securityKey)
    

