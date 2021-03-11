# Milestone 24. [匯款金流正規化][New API] #1422 後台建立/編輯匯款訂單、#1355 後台批准匯款訂單、#1354 後台建立/編輯匯款訂單
# Milestone 27. [匯款金流正規化][New API] 後台取得單一匯款訂單：GET /api/v2/backend/remittance/{{remittance_id}} #1728
# Milestone 27. [匯款金流正規化][New API] 後台取得匯款訂單列表：GET /api/v2/backend/remittance/list #1727
# Milestone 28. [Bug]後台線下匯款記錄應回產品id,而非價格 #1854
# Milestone 28. [Bug] 後台建立/編輯匯款訂單：PUT /v2/backend/remittance，編輯的時候， productNo 還是原本的。 #1826
# pylint: disable=unbalanced-tuple-unpacking
import datetime
import json
import pytest
from pprint import pprint
from assistence import api
from assistence import initdata
from assistence import dbConnect

'''後台匯款'''
class Remittance:
    def __init__(self):
        env = 'QA2'
        test_parameter = {}
        initdata.set_test_data(env, test_parameter)
        self.test_parameter = test_parameter
        self.header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
        self.header['X-Auth-Token'] = test_parameter['backend_token']
        self.header['X-Auth-Nonce'] = test_parameter['backend_nonce']
        self.header['Content-Type'] = 'application/json'
        self.body =''
        self.api_name=''
        self.res = ''
    '''建立訂單'''
    def create_order(self, user_id, pro_no, note):
        self.api_name = '/api/v2/backend/remittance'
        self.body = {'consumerUserId': user_id,
                'productNo': pro_no,
                'accountNumber': 0,
                'note': note }
        self.body = {key : val for key,val in  self.body.items() if val != ''}
        self.res = api.apiFunction(self.test_parameter['prefix'], self.header, self.api_name, 'put', self.body)
        return self.res
    '''編輯訂單'''
    def edit_order(self, remitt_id, user_id, pro_no, acc_no, note):
        self.api_name = '/api/v2/backend/remittance/'+ str(remitt_id)
        self.body = {'consumerUserId': user_id,
                'productNo': pro_no,
                'accountNumber': acc_no,
                'note': note }
        self.body = {key : val for key,val in  self.body.items() if val != ''}
        self.res = api.apiFunction(self.test_parameter['prefix'], self.header, self.api_name, 'put', self.body)
        return self.res
    '''允許訂單'''
    def approve_order(self, remitt_id):
        self.api_name = '/api/v2/backend/remittance/approve'
        self.body = {'remittanceId': remitt_id,}
        self.body = {key : val for key,val in  self.body.items() if val != ''}
        self.res = api.apiFunction(self.test_parameter['prefix'], self.header, self.api_name, 'post', self.body)
        return self.res

    '''訂單內容'''
    def order_detail(self, remitt_id):
        self.api_name = '/api/v2/backend/remittance/'+ str(remitt_id)
        self.res = api.apiFunction(self.test_parameter['prefix'], self.header, self.api_name, 'get', None)
        return self.res

    '''訂單列表'''
    def order_list(self, **kwargs):
        api_base_name = '/api/v2/backend/remittance/list'
        self.api_name = api.dict_to_url_get(api_base_name, kwargs)
        self.res = api.apiFunction(self.test_parameter['prefix'], self.header, self.api_name, 'get', None)
        return self.res

    '''debug使用'''
    def debug(self):
        print('api: ' + self.test_parameter['prefix'] + self.api_name)
        print('body: ' + str(self.body) )
        print('header: ' + str(self.header))
        # restext = json.loads(self.res.text)
        # print(self.res)
        # print(restext)

class TestRemittance():
    back_remittance = Remittance()
    env = 'QA2'
    test_parameter = {}
    header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
    initdata.set_test_data(env, test_parameter)
    header['X-Auth-Token'] = test_parameter['backend_token']
    header['X-Auth-Nonce'] = test_parameter['backend_nonce']
    #使用 track0050 與 track0051 使用者
    user_ids = []
    user_ids.append(api.search_user(test_parameter['prefix'],"track0050",header))
    user_ids.append(api.search_user(test_parameter['prefix'],"track0051",header))

    #初始化一個成功匯款id清單
    remitt_list = []

    def setup_class(self):
        pass
    #新增訂單資料
    create_order_data = [
        #          scenario,                   token,                   nonce, user_id, pro_no, expect
        (    'live_control', 'liveController1_token', 'liveController1_nonce', user_ids[0],     41,  2),
        ('business_manager',         'backend_token',         'backend_nonce', user_ids[0],     42,  2),
        ('business_manager',         'backend_token',         'backend_nonce', user_ids[1],     44,  2),
        (            'user',            'user_token',            'user_nonce', user_ids[0],     46,  4),
        (          'master',     'broadcaster_token',     'broadcaster_nonce', user_ids[0],     47,  4),
        (    'lack of data',         'backend_token',         'backend_nonce', user_ids[0],     '',  4),
        ( 'err token nonce',             'err_token',             'err_nonce', user_ids[0],     41,  4),
    ]
    #修改清單資料
    edit_order_data = [
        #          scenario,                   token,                   nonce, remitt_index,      user_id,  pro_no, acc_no, expect
        (    'live_control', 'liveController1_token', 'liveController1_nonce',            0,  user_ids[0],      41,  55555,     2),
        ('business_manager',         'backend_token',         'backend_nonce',            1,  user_ids[0],      48,     '',     2),
        (            'user',            'user_token',            'user_nonce',            0,  user_ids[0],      49,  33333,     4),
        (          'master',     'broadcaster_token',     'broadcaster_nonce',            0,  user_ids[0],      47,  22222,     4),
        (    'lack of data',         'backend_token',         'backend_nonce',            0,  user_ids[0],      '',  11111,     4),
        ( 'err token nonce',             'err_token',             'err_nonce',            0,  user_ids[0],      41,  66666,     4),
    ]
    #允許清單資料
    approve_order_data = [
        #          scenario,                   token,                   nonce,   remitt_index,   expect
        ('business_manager',         'backend_token',         'backend_nonce',              1,       2),
        (    'live_control', 'liveController1_token', 'liveController1_nonce',              0,       4),
        (          'master',     'broadcaster_token',     'broadcaster_nonce',              0,       4),
        (    'lack of data',         'backend_token',         'backend_nonce',             '',       4),
        ( 'err token nonce',             'err_token',             'err_nonce',              0,       4),
    ]

    #詳細清單資料
    detail_order_data = [
        #          scenario,                   token,                   nonce,   remitt_index,   expect
        (    'live_control', 'liveController1_token', 'liveController1_nonce',              1,       2),
        ('business_manager',         'backend_token',         'backend_nonce',              0,       2),
        (            'user',            'user_token',            'user_nonce',              0,       4),
        (          'master',     'broadcaster_token',     'broadcaster_nonce',              1,       4),
        ( 'err token nonce',             'err_token',             'err_nonce',              1,       4),

    ]
    #清單列表資料
    order_list_data =[
        #                  scenario,                   token,                   nonce,       userId, statusFilter,  item, page, expect
        (   'search_by_id_approved',         'backend_token',         'backend_nonce',  user_ids[0],   'approved',     3,   None,      2),
        ( 'search_by_id_unapproved', 'liveController1_token', 'liveController1_nonce',  user_ids[1], 'unapproved',     3,   None,      2),
        ('search_by_all_unapproved', 'liveController2_token', 'liveController2_nonce',         None, 'unapproved',     3,   None,      2),
        (           'search_by_all',         'backend_token',         'backend_nonce',         None,         None,    10,   None,      2),
        (             'user_nodata',         'backend_token',         'backend_nonce',      'sdfsd',         None,     0,   None,      2),
        (         'err token nonce',             'err_token',             'err_nonce',           None,       None,  None,   None,      4),
    ]
    #測試建立訂單
#    @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.parametrize('scenario, token, nonce, user_id, pro_no,  expect',create_order_data)
    def test_create_order(self, scenario, token, nonce, user_id, pro_no,  expect):
        self.back_remittance.header['X-Auth-Token'] = self.__class__.test_parameter[token]
        self.back_remittance.header['X-Auth-Nonce'] = self.__class__.test_parameter[nonce]
        note = str(datetime.datetime.now().timestamp())
        res = self.back_remittance.create_order(user_id, pro_no, note)
        assert res.status_code // 100 == expect
        if expect == 2:
            #訂單建立成功，需 insert一筆資料進 remittance & purchase_order 這兩張 table。
            sqlStr = "Select remittance.id, purchase_order.purchase_type from remittance join purchase_order on remittance.order_id = purchase_order.id where note='{}'".format(note)
            db_result = dbConnect.dbQuery(self.__class__.test_parameter['db'], sqlStr , 'shocklee')
            assert db_result != []
            remittance_id = db_result[0][0]
            purchase_type = db_result[0][1]
            assert purchase_type == 'remittance'
            self.__class__.remitt_list.append(remittance_id)
        elif expect == 4:
            if scenario == 'lack of data':
                assert res.status_code == 400
            elif scenario == 'err token nonce':
                assert res.status_code == 401
            else:
                assert res.status_code == 403

    #測試修改訂單
#    @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.parametrize('scenario, token, nonce, remitt_index, user_id, pro_no, acc_no, expect',edit_order_data)
    def test_edit_order(self, scenario, token, nonce, remitt_index, user_id, pro_no, acc_no, expect):
        self.back_remittance.header['X-Auth-Token'] = self.__class__.test_parameter[token]
        self.back_remittance.header['X-Auth-Nonce'] = self.__class__.test_parameter[nonce]
        note = str(datetime.datetime.now().timestamp())+'change'
        remitt_id = self.__class__.remitt_list[remitt_index]
        res = self.back_remittance.edit_order(remitt_id, user_id, pro_no, acc_no, note)
        assert res.status_code // 100 == expect
        #restext = json.loads(res.text)
        if expect == 2:
            #訂單建立成功，確認修改至 remittance & purchase_order 這兩張 table。
            sqlStr = "Select note, product_info_id from remittance join purchase_order on remittance.order_id = purchase_order.id where note='{}'".format(note)
            [(result_note,result_pro_no)] = dbConnect.dbQuery(self.__class__.test_parameter['db'], sqlStr, 'shocklee')
            assert result_note == note
            assert result_pro_no == pro_no
        elif expect == 4:
            if scenario == 'lack of data':
                assert res.status_code == 400
            elif scenario == 'err token nonce':
                assert res.status_code == 401
            else:
                assert res.status_code == 403
    #確認批准訂單
#    @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.parametrize('scenario, token, nonce, remitt_index, expect',approve_order_data)
    def test_approve_order(self, scenario, token, nonce, remitt_index, expect):
        self.back_remittance.header['X-Auth-Token'] = self.__class__.test_parameter[token]
        self.back_remittance.header['X-Auth-Nonce'] = self.__class__.test_parameter[nonce]
        remitt_id = '' if remitt_index == '' else self.__class__.remitt_list[remitt_index]
        res = self.back_remittance.approve_order(remitt_id)
#        self.back_remittance.debug()
        restext = json.loads(res.text)
        assert res.status_code // 100 == expect
        if expect == 2:
            #檢查DB : 需 insert一筆資料進 remain_point_history 並且更新 remain_point & remittance & purchase_order 這幾張 table。
            sqlStr = "SELECT po.id, po.product_info_id FROM purchase_order AS po \
                        INNER JOIN remittance AS r ON po.id  = r.order_id \
                        INNER JOIN remain_points_history AS rph ON po.id = rph.purchase_order_id \
                        INNER JOIN identity AS i ON i.id = rph.identity_id \
                        INNER JOIN remain_points AS rp ON i.id = rp.identity_id \
                        WHERE r.id ='{}'".format(remitt_id)
            db_result = dbConnect.dbQuery(self.__class__.test_parameter['db'], sqlStr, 'shocklee')
            purchase_order_id = db_result[0][0]
            assert db_result != []
            #此時不可對訂單內容進行編輯，除了備註以外，批准的瞬間就會以當下的設定內容進行加點處理，這段由前端處理，API不處理這段
            #使用者在 Client端 App中， 「我的 > 我的點數 > 儲值紀錄」 中，應可看見匯款儲值紀錄。
            api_name = '/api/v2/identity/transactionList'
            header = self.header
            header['X-Auth-Token'] = self.test_parameter['user_token']
            header['X-Auth-Nonce'] = self.test_parameter['user_nonce']
            res = api.apiFunction(self.test_parameter['prefix'], header, api_name , 'get', None)
            restext = json.loads(res.text)
            assert res.status_code // 100 == expect
            assert restext['data'][0]['orderId'] == purchase_order_id
            assert restext['data'][0]['purchaseType'] == 'remittance'
        elif expect == 4:
            if scenario == 'lack of data':
                assert res.status_code == 400
            elif scenario == 'err token nonce':
                assert res.status_code == 401
            else:
                assert res.status_code == 403
    #詳細清單資料
#    @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.parametrize('scenario, token, nonce, remitt_index, expect',detail_order_data)
    def test_order_detail(self, scenario, token, nonce, remitt_index, expect):
        self.back_remittance.header['X-Auth-Token'] = self.__class__.test_parameter[token]
        self.back_remittance.header['X-Auth-Nonce'] = self.__class__.test_parameter[nonce]
        remitt_id = '' if remitt_index == '' else self.__class__.remitt_list[remitt_index]
        res = self.back_remittance.order_detail(remitt_id)
        assert res.status_code // 100 == expect
        if expect == 2:
            restext = json.loads(res.text)
            pprint(restext)
            assert restext['data']['id'] == remitt_id
            assert all([ x in restext['data'] for x in ['id', 'consumer', 'productNo', 'accountNumber', 'note', 'createdAt', 'approvedAt']]) == True
            assert all([ x in restext['data']['consumer'] for x in ['id', 'nickname']]) == True
            sqlStr = "Select product_info_id from remittance join purchase_order on remittance.order_id = purchase_order.id where remittance.id='{}'".format(remitt_id)
            [(product_info_id,)] = dbConnect.dbQuery(self.__class__.test_parameter['db'], sqlStr, 'shocklee')
            assert product_info_id == restext['data']['productNo']
    #得到清單列表
    @pytest.mark.parametrize('scenario, token, nonce, userId, statusFilter, item, page, expect',order_list_data)
    def test_order_list(self, scenario, token, nonce, userId, statusFilter, item, page, expect):
        self.back_remittance.header['X-Auth-Token'] = self.__class__.test_parameter[token]
        self.back_remittance.header['X-Auth-Nonce'] = self.__class__.test_parameter[nonce]
        res = self.back_remittance.order_list(userId=userId,statusFilter=statusFilter,item=item,page=page)
        #self.back_remittance.debug()
        assert res.status_code // 100 == expect
        if expect == 2:
            restext = json.loads(res.text)
            #pprint(restext['data'])
            assert restext['totalCount'] != None
            assert len(restext['data']) <= item
            if len(restext['data']) >= 2:
                assert restext['data'][-1]['id'] < restext['data'][-2]['id']
                assert all([ x in restext['data'][0] for x in ['id', 'consumer', 'productNo', 'accountNumber', 'note', 'createdAt', 'approvedAt']]) == True
            if scenario.find("_approved") != -1:
                assert restext['data'][-1]['approvedAt'] != None
            elif scenario.find("_unapproved") != -1:
                assert restext['data'][0]['productNo'] == 44
                assert restext['data'][-1]['approvedAt'] == None
            elif scenario.find("_id") != -1:
                assert restext['data'][0]['consumer']['id'] == userId
            if scenario == 'search_by_id_unapproved':
                sqlStr ="select count(*) from purchase_order where purchase_type='remittance' and consumer_user_id='{}' and status='{}'".format(userId, 0)
                [(totalCount,)] = dbConnect.dbQuery(self.__class__.test_parameter['db'], sqlStr, 'shocklee')
                assert totalCount == restext['totalCount']
        else:
            assert res.status_code == 401