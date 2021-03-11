# milestone 30.[金流][MyCard] 交易資料查詢改寫 V2版 POST /api/v2/backend/purchaseOrder/list #2001
# milestone 30.[金流][MyCard] 取得AuthCode POST /v2/transaction/mycard/authCode #2003
# milestone 30.[金流][MyCard] 交易結果回傳 POST /v2/transaction/mycard/callback #2004
# milestone 30.[金流][MyCard] 交易結果回傳(補儲) POST /v2/transaction/mycard/result #2005
# milestone 30.[金流][MyCard] 查詢交易結果 GET /v2/transaction/mycard/tradeQuery #2006
# milestone 30.[金流][MyCard] 給MyCard查詢交易紀錄差異比對 POST /v2/transaction/mycard/diff #2007
import json
import requests
import pytest
from backend.test_tagSettings import Tag
from backend.test_tabSettings import TabSetting
from assistence import api
from assistence import initdata
from assistence import dbConnect
from pprint import pprint

class MyCard():
    def __init__(self):
        self.prefix = ''
        self.api_name = ''
        self.header = ''
        self.body = ''
    #1.引用此 class 先 set prefix ，後 set header
    '''設定header，通常帶入 test_parameter[token],test_parameter[nonce]'''
    def set_header(self, token, nonce):
        self.header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
        self.header['Content-Type'] = 'application/json'
        self.header['X-Auth-Token'] = token
        self.header['X-Auth-Nonce'] = nonce
        return self.header

    '''MyCard點數購買-取得AuthCode'''
    def trans_authCode(self, prodcutId, facReturnUrl):
        self.api_name = "/api/v2/transaction/mycard/authCode"
        self.body = {'prodcutId':prodcutId ,'facReturnUrl': facReturnUrl,}
        res = api.apiFunction(self.prefix, self.header, self.api_name, 'post', self.body)
        return res

    '''MyCard點數購買-交易結果回傳'''
    def trans_callback(self,....):
        self.api_name = "/api/v2/transaction/mycard/authCode"
        self.body = {
            'ReturnCode': "1" ,
            'ReturnMsg': '測試訊息',
            'PayResult': PayResult,
            'FacTradeSeq' : FacTradeSeq,
            'PaymentType' : 'INGAME',
            'Amount': Amount,
            'Currency' : 'TWD',
            'MyCardTradeNo' : MyCardTradeNo,
            'MyCardType' : MyCardType,
            'PromoCode' : PromoCode,
            'SerialId' : SerialId,
        }
        res = api.apiFunction(self.prefix, self.header, self.api_name, 'post', self.body)
        return res

    '''MyCard點數購買-交易結果回傳(補儲)'''
    def trans_refill(self):
        self.api_name = "/api/v2/transaction/mycard/result"
        self.body = {
            'ReturnCode': "1" ,
            'ReturnMsg': '測試訊息',
            'FacServiceId': "MyCardSDK",
            'TotalNum' : 2,
            'FacTradeSeq' : ["FacTradeSeq0001", "FacTradeSeq0002"],
        }
        res = api.apiFunction(self.prefix, self.header, self.api_name, 'post',self.body)
        return res

    '''MyCard點數購買-交易成功資料之差異比對'''
    def trans_diff(self):
        self.api_name = "/api/v2/transaction/mycard/diff"
        self.body = {
            "StartDateTime" : StartDateTime,
            "EndDateTime" : EndDateTime,
            "MyCardTradeNo" : MyCardTradeNo,
        }
        res = api.apiFunction(self.prefix, self.header, self.api_name, 'post',self.body)
        return res

    '''MyCard點數購買-查詢交易結果'''
    def trans_query(self, authCode):
        self.api_name = "/api/v2/transaction/mycard/tradeQuery?authCode=" + authCode
        res = api.apiFunction(self.prefix, self.header, self.api_name, 'get', self.body=None)
        return res

    def trans_debug(self):
        print("\n ***DEBUG*** \n  prefix:{} \n header:{} \n, api_name:{} \n, body:{} \n".format(self.prefix, self.header, self.api_name, self.body))




class TestMyCard():
    env = 'QA2'
    test_parameter = {}
    initdata.set_test_data(env, test_parameter)
    trans = MyCard()
    trans.prefix = test_parameter['prefix']
    trans_authCode = []
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass
    test_auth_code = {
        #scenario, token, nonce, prodcutId,  expected
        ('Normal_Transactions1','token','nonce','xtars.web.mycard.points.240000',2)
        ('Normal_Transactions2','token','nonce','xtars.web.mycard.points.240000',2)
        ('Normal_Transactions3','token','nonce','xtars.web.mycard.points.240000',2)
        ('Product_Id_Not_Exist','token','nonce',                              '',4)

    }

    @pytest.mark.parametrize("scenario, prodcutId,  expected", test_auth_code)
    def test_trans_authCode(self, scenario, prodcutId, expected):
        token, nonce = test_parameter[token_index] , test_parameter[nonce_index]
        self.trans.set_header(token, nonce)
        res = self.trans.trans_authCode(prodcutId, facReturnUrl="")
        restext = json.loads(res.text)
        assert res.status_code // 100 == expected
        if expected == 2:
            assert restext['Status'] == 'Ok' and restext['Message'] == 'SUCCESS'
            assert restext['authCode'] != None
            trans_authCode.append(restext['authCode'])
        else:
            assert res.status_code == 400

