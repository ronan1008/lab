import json
import requests
import pytest
import base64
import re
import time
from datetime import datetime, timedelta
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.parse import unquote
from assistence import api, initdata, dbConnect, sundry

env = 'test'
test_parameter = {}
initdata.set_test_data(env, test_parameter)
header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
header['Content-Type'] = 'application/json'

def myInfo_remainPoints(prefix, header):
    url = '/api/v2/identity/myInfo'
    res = api.apiFunction(prefix, header, url, 'get', None)
    restext = json.loads(res.text)
    return restext['data']['remainPoints']

def myInfo_identityId(prefix, header):
    url = '/api/v2/identity/myInfo'
    res = api.apiFunction(prefix, header, url, 'get', None)
    restext = json.loads(res.text)
    return restext['data']['id']

def esgame_generate_purchase(prefix, header, prodcutId, returnUrl):
    api_name = '/api/v3/transaction/esgame/generate-purchase'
    body = {
        "productId" : prodcutId,
        "returnUrl": returnUrl
    }
    print(body)
    res = api.apiFunction(prefix, header, api_name, 'post', body)
    return res


def esgame_callback(prefix, base64_data):
    api_name = '/api/v3/transaction/esgame/callback'
    body = {
        "data" : base64_data
    }
    res = api.apiFunction(prefix, header, api_name, 'post', body)
    return res

def decode_base64(data):
    url_decod_data = unquote(data)
    b64_decod_data = base64.b64decode(url_decod_data)
    jsData = json.loads(b64_decod_data)
    return jsData

#經過五次的post
def esgame_User_Agent(base64_data):
    url = 'https://pay.esgame.vn/purchase/3rd/generate-purchase'
    session = requests.Session()
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    r1 = session.post( url, headers=header, data={"data":base64_data}, cookies=None )
    html1 = r1.text
    soup = BeautifulSoup(html1, 'html.parser')
    esgame_vn_v1_url = soup.find(id='pay_form').get('action')
    esgame_vn_v1_data = soup.find('input',{'name':'data'}).get('value')

    r2 = session.post( esgame_vn_v1_url, headers=header, data={"data": esgame_vn_v1_data})
    html2 = r2.text
    soup = BeautifulSoup(html2, 'html.parser')
    esgame_vn_esg_order_url = soup.find(id='form1').get('action')
    esgame_vn_esg_order_data = soup.find('input',{'name':'data'}).get('value')

    r3 = session.post( esgame_vn_esg_order_url, headers=header, data={"data": esgame_vn_esg_order_data})
    html3 = r3.text
    soup = BeautifulSoup(html3, 'html.parser')
    script_tags = soup.findAll('script')
    last_tag = str(script_tags[-1])
    data = re.search(r'"data":"(.+)","COID"', last_tag)
    script_b64_data = data.group(1)

    payment_data = {
        "SPAID" : "COPGAT01",
        "data": script_b64_data,
        "Serial": "CA00000000",
        "PinCode": "1111111111"
    }

    r4 = session.post(esgame_vn_esg_order_url, headers=header, data=payment_data, allow_redirects=True)
    html4 = r4.text
    soup = BeautifulSoup(html4, 'html.parser')
    post_return_url = soup.find(id='form1').get('action')
    post_return_url_data = soup.find('input',{'name':'data'}).get('value')

    r5 = session.post( post_return_url, headers=header, data={"data": post_return_url_data})

    return r5, post_return_url_data



esgame = [
        #scenario,        token,          nonce,                           prodcutId,                                    returnUrl, expected
    (    'esgame', 'user_token',   'user_nonce',         'vn.esgame.lh3d_e_lb_00010',   'https://testshockleeapi.free.beeceptor.com/my/api/path',  2),
    (   'esgame1', 'user_token',   'user_nonce',  'xtars.web.esgame.gate.points.166',   'https://testshockleeapi.free.beeceptor.com/my/api/path',  2),

]

@pytest.mark.parametrize("scenario, token, nonce, prodcutId, returnUrl, expected", esgame)
def test_mypay_issueInvoice(scenario,  token, nonce, prodcutId, returnUrl, expected):
    header['X-Auth-Token'] = test_parameter[token]
    header['X-Auth-Nonce'] = test_parameter[nonce]
    identity_id =  myInfo_identityId(test_parameter['prefix'], header)
    init_remainPoints = myInfo_remainPoints(test_parameter['prefix'], header)
    res = esgame_generate_purchase(test_parameter['prefix'], header, prodcutId, returnUrl)
    assert res.status_code // 100 == expected
    if expected == 2:
        base64_data = (res.json())['data']['auth']
        print(base64_data)
        de_post_data =  decode_base64(base64_data)
        pprint(de_post_data)
        res, post_return_url_data = esgame_User_Agent(base64_data)
        print(res.url)
        pprint( decode_base64(post_return_url_data))
        assert res.url == returnUrl

        time.sleep(10)
        purchase_sql = '''
        SELECT
            purchase_order.id,
            product_info.price,
            product_info.points
        FROM
            purchase_order
            JOIN product_info ON product_info.id = purchase_order.product_info_id
        WHERE
            purchase_order.purchase_type = 'esgame'
            AND purchase_order.status = 1
        ORDER BY id DESC
        LIMIT 1
        '''
        [(purchase_order_id, product_price, product_points)] = dbConnect.dbQuery(test_parameter['db'], purchase_sql, 'shocklee')


        order_esgame_sql = f'''
        SELECT
            amount, user_acctid, product_id, request_base64
        FROM
            order_esgame_detail
        WHERE
            order_esgame_detail.purchase_order_id = {purchase_order_id}
        '''
        [(amount, user_acctid, product_id, request_base64 )] = dbConnect.dbQuery(test_parameter['db'], order_esgame_sql, 'shocklee')
        print(purchase_order_id)
        print(amount)
        print(user_acctid)
        print(product_id)
        print(request_base64)
        pprint(decode_base64(request_base64))
        final_remainPoints = myInfo_remainPoints(test_parameter['prefix'], header)
        assert product_id == prodcutId
        assert amount == product_price
        assert user_acctid == identity_id
        print(init_remainPoints)
        print(final_remainPoints)
        assert final_remainPoints - product_points == init_remainPoints

