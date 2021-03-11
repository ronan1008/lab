# Milestone 17. 動態贈禮 - [GET] 後台讀取禮物清單 #773,動態贈禮 - [GET] 後台讀取禮物分類清單 #772,動態贈禮 - [POST] 後台新增禮物分類 #771
# Milestone 18. 動態贈禮 - 禮物分類（gift_category）需要追加軟刪除功能 #809 後台撈取禮物清單 API 更新 #811 後台撈取禮物分類列表 API 更新 #810
# Milestone 23. 動態贈禮 [Enhancement] 前後台的「讀取禮物清單」response中，為向下相容，皆需要補上 uuid #1218
import datetime
import json
import pytest
from pprint import pprint
from assistence import api
from assistence import initdata
class GiftAndCategory:
    def __init__(self):
        env = 'QA2'
        test_parameter = {}
        initdata.set_test_data(env, test_parameter)
        self.test_parameter = test_parameter
        self.header = {'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
        self.header['X-Auth-Token'] = test_parameter['backend_token']
        self.header['X-Auth-Nonce'] = test_parameter['backend_nonce']
        self.header['Content-Type'] = 'application/json'
        self.api_name=''
    '''產生禮物分類'''
    def create_category(self,gift_name ,gift_type, on_time, off_time):
        self.api_name = '/api/v2/backend/giftCategory'
        body = {'categoryName': gift_name,
                'type': gift_type,
                'startTime': on_time,
                'endTime': off_time }
        res = api.apiFunction(self.test_parameter['prefix'], self.header, self.api_name, 'post', body)
        return res
    '''秀出分類列表'''
    def show_category_list(self, status_filter = '', type_filter = ''):
        type_filter = str(type_filter)
        api_base_name = '/api/v2/backend/giftCategory/list'
        api_n =''
        if status_filter != '' and type_filter != '':
            api_n = api_base_name +'?'+ "statusFilter=" + status_filter +'&'+ "typeFilter=" + type_filter
        elif status_filter != '':
            api_n = api_base_name +'?'+ "statusFilter=" + status_filter
        elif type_filter != '':
            api_n = api_base_name +'?'+ "typeFilter=" + type_filter

        self.api_name = api_n +'&'+ "item=" + "100"

        if status_filter == '' and type_filter == '':
            self.api_name = api_base_name +'?'+ "item=" + "100"
        res = api.apiFunction(self.test_parameter['prefix'], self.header, self.api_name, 'get', None)
        return res
    '''秀出禮物列表 giftCategoryId, type_filter, status_filter, order_by'''
    def show_gift_list(self, **kwargs):
        params = { key : val for key, val in kwargs.items() if val is not None }
        api_base_name = '/api/v2/backend/gift/list'
        self.api_name = api.dict_to_url_get(api_base_name, params)
        res = api.apiFunction(self.test_parameter['prefix'], self.header, self.api_name, 'get', None)
        return res
    '''刪除指定分類'''
    def del_gift_category(self, giftCategory_id):
        self.api_name = '/api/v2/backend/giftCategory/'+ giftCategory_id
        res = api.apiFunction(self.test_parameter['prefix'], self.header, self.api_name, 'delete', None)
        return res

class TestGiftAndCategory():
    gift = GiftAndCategory()
    now_datetime = datetime.datetime.now()
    now_datetime = now_datetime - datetime.timedelta(minutes = 1)
    off_datetime = now_datetime + datetime.timedelta(hours = 3)
    on_timestamp = int(now_datetime.timestamp())
    off_timestamp = int(off_datetime.timestamp())
    gift_name = 'shock_gitCategory' + str(on_timestamp)
    #用來存放產生的分類id
    create_category_id = []
    create_category_data = [ #尚缺非後台的驗證
        #scenario, gift_name, gift_type, on_time, off_time, expect
        ('liveRoomGift', gift_name, 1, on_timestamp      , off_timestamp,       2),
        ('liveShowGift', gift_name, 2, on_timestamp      , off_timestamp,       2),
        ('oneToOneGift', gift_name, 3, on_timestamp      , off_timestamp,       2),
        ('expiredPostGift', gift_name, 4, on_timestamp-80000, off_timestamp-70000, 2),]
    show_category_list_data =  [ #尚缺非後台的驗證
        #scenario, status_filter, type_filter, expect
        ('stat_ft tp_ft',  'on',  1, 2),
        ( 'Only stat_ft', 'off', '', 2),
        (    'No Filter',    '', '', 2),
        (   'Only tp_ft',    '',  4, 2),]
    show_gift_list_data = [ #尚缺非後台的驗證
        # scenario, giftCategoryId, type_filter, status_filter, order_by, expect
        ('all_desc'   , None , None,    None,           None, 2),
        ('on_desc74'  , 74 ,  1, 'all', 'point_desc', 2),
        ('off_asc'    , None,  1,  None,  'point_asc', 2),
        ('on_asc'     , None,  1, 'all',  'point_asc', 2),]

    def setup_class(self):
        pass
    @pytest.mark.parametrize('scenario, gift_name, gift_type, on_time, off_time, expect',create_category_data)
    def test_create_category(self, scenario, gift_name, gift_type, on_time, off_time, expect):
        res = self.gift.create_category(gift_name, gift_type, on_time, off_time)
        assert res.status_code // 100 == expect
        if expect == 2:
            restext = json.loads(res.text)
            assert restext['id'] != ''
            assert restext['Status'] == 'Ok'
            self.__class__.create_category_id.append(restext['id'])

    @pytest.mark.parametrize('scenario, status_filter, type_filter, expect',show_category_list_data)
    def test_show_category_list(self, scenario, status_filter, type_filter, expect):
        res = self.gift.show_category_list(status_filter, type_filter)
        now_timestamp = self.__class__.on_timestamp
        if scenario == 'stat_ft tp_ft':
            #on(上架)：delete_at 沒有值 AND 現在時間介於 start_time & end_time 之間
            if status_filter == 'on':
                assert res.status_code // 100 == expect
                if expect == 2:
                    restext = json.loads(res.text)
                    print("===========")
                    pprint(restext['data'][0])

                    print("===========")
                    assert restext['data'][0]['deleteAt'] == None
                    if restext['data'][0]['startTime'] != None and restext['data'][0]['startTime'] != None :
                        assert restext['data'][0]['startTime'] <= now_timestamp <= restext['data'][0]['endTime']
        elif scenario == 'Only stat_ft':
            #off(下架)：delete_at 有值 OR 現在時間不在 start_time & end_time 之間
            if status_filter == 'off':
                assert res.status_code // 100 == expect
                if expect == 2:
                    restext = json.loads(res.text)
                    assert restext['data'][0]['deleteAt'] != None or restext['data'][0]['startTime'] > now_timestamp or restext['data'][0]['endTime'] < now_timestamp
        elif scenario == 'No Filter':
            #no filter  = all(全部)：delete_at 沒有值的全撈
            if status_filter == '' and type_filter == '':
                assert res.status_code // 100 == expect
                if expect == 2:
                    restext = json.loads(res.text)
                    assert restext['data'][0]['deleteAt'] == None
        elif scenario == 'Only tp_ft':
             #all(全部)：delete_at 沒有值的全撈
            if status_filter == '':
                assert res.status_code // 100 == expect
                if expect == 2:
                    restext = json.loads(res.text)
                    assert restext['data'][0]['deleteAt'] == None

    @pytest.mark.parametrize('scenario, giftCategoryId, type_filter, status_filter, order_by, expect',show_gift_list_data)
    def test_show_gift_list(self, scenario, giftCategoryId, type_filter,status_filter, order_by, expect):
        res = self.gift.show_gift_list(giftCategoryId=giftCategoryId,typeFilter=type_filter,
                                statusFilter=status_filter,orderBy=order_by,item=None,page=None)
        #all(全部)：delete_at 沒值的全撈 與 禮物點數(降冪)
        if scenario == 'all_desc':
            assert res.status_code // 100 == expect
            if expect == 2:
                restext = json.loads(res.text)
                assert restext['data'][0]['point'] >= restext['data'][1]['point']
                assert restext['data'][0]['uuid'] != None
                assert restext['data'][0]['deleteAt'] == None
        #on(上架)：delete_at 沒值 AND isActive = 1 AND 該禮物分類在活動時間內 與 禮物點數(降冪)
        elif scenario == 'on_desc74':
            assert res.status_code // 100 == expect
            if expect == 2:
                restext = json.loads(res.text)
                assert restext['data'][0]['point'] >= restext['data'][1]['point']
                assert restext['data'][-1]['categoryId'] == 74
                assert restext['data'][0]['uuid'] != None
                assert restext['data'][0]['deleteAt'] == None
                assert restext['data'][0]['isActive'] == True
        #off(下架)：delete_at 有值 OR isActive = 0 OR 該禮物分類不在活動時間內 與 禮物點數(升冪)
        elif scenario == 'off_asc':
            assert res.status_code // 100 == expect
            if expect == 2:
                restext = json.loads(res.text)
                assert restext['data'][0]['point'] <= restext['data'][1]['point']
                assert restext['data'][0]['uuid'] != None
                assert restext['data'][0]['deleteAt'] != None or restext['data'][0]['isActive'] != False
        #on(上架)：delete_at 沒值 AND isActive = 1 AND 該禮物分類在活動時間內 與 禮物點數(升冪)
        elif scenario == 'on_asc':
            assert res.status_code // 100 == expect
            if expect == 2:
                restext = json.loads(res.text)
                assert restext['data'][-2]['point'] <= restext['data'][-1]['point']
                assert restext['data'][0]['uuid'] != None

    @pytest.mark.parametrize('ids',create_category_id)
    def del_gift_category(self,ids):
        res = self.gift.del_gift_category(ids)
        assert res.status_code // 100 == 2
        res = self.gift.del_gift_category(999999)
        assert res.status_code // 100 == 4