import abc
import json
import asyncio
import websockets
import traceback
import logging
import requests
import api
from pprint import pprint, pformat
import time

console_handler = logging.StreamHandler()
console_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s','%H:%M:%S')
console_handler.setFormatter(console_format)
# console_handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

def web_login(prefix ,loginId, loginPass):
    url = prefix + '/api/v2/identity/auth/web/login'
    body = {
            "type": "emailAndId",
            "account":loginId,
            "password": loginPass
    }

    res = requests.post(url, json=body)
    assert res.status_code == 200
    return res.json()


class RoomUser(metaclass =abc.ABCMeta):
    def __init__(self, domain, loginId, loginPwd, webLogin = False, tokenNonce:list = None):
        print(f"\n {loginId} Connecting...")
        self.header =  {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': '', 'X-Auth-Nonce': ''}
        self.domain = domain
        self.url = f"http://{domain}"
        self.loginId = loginId
        self.subVersion = None
        self.socket_close = False

        if tokenNonce:
            token, nonce = tokenNonce
            self.token = token
            self.nonce = nonce
            self.header['X-Auth-Token'] = token
            self.header['X-Auth-Nonce'] = nonce
        else:
            if webLogin:
                self.subVersion = "WEB"
                self.login_without_tokenNonce(loginId=loginId, loginPwd=loginPwd)
            else:
                self.subVersion = "APP"
                self.login_to_set_tokenNonce(loginId=loginId, loginPwd=loginPwd)

        self.set_identityId_from_myInfo(self.url, self.header)

#login refresh token & nonce
    def login_to_set_tokenNonce(self, loginId, loginPwd):
        # logger.info(f"{self.loginId} | Loggin to get token and nonce")
        result = api.user_login(self.url, loginId, loginPwd)
        self.token = result['data']['token']
        self.nonce = result['data']['nonce']
        self.header['X-Auth-Token'] = result['data']['token']
        self.header['X-Auth-Nonce'] = result['data']['nonce']
        # logger.info(f"{self.loginId} | Get token and nonce")
        return (result['data']['token'], result['data']['nonce'])

#login without refresh token & nonce
    def login_without_tokenNonce(self, loginId, loginPwd):
        # logger.info(f"{self.loginId} | Loggin without refresh token and nonce")
        result = web_login(self.url, loginId, loginPwd)
        self.token = result['data']['token']
        self.nonce = result['data']['nonce']
        self.header['X-Auth-Token'] = result['data']['token']
        self.header['X-Auth-Nonce'] = result['data']['nonce']
        # logger.info(f"{self.loginId} | Get token and nonce")
        return (result['data']['token'], result['data']['nonce'])


    def set_identityId_from_myInfo(self, url, header):
        # logger.info(f"{self.loginId} | Get identity from myinfo")
        apiName = f"/api/v2/identity/myInfo"
        res = api.apiFunction(url, header, apiName, 'get', None)
        json = res.json()
        self.identity = json['data']['id']
        return json['data']['id']

    async def ws_connect_by_tokenNonce(self):
        if self.subVersion == 'WEB':
            ws_add = "ws://{domain}/socket/websocket?token={token}&nonce={nonce}&session=sub".format(domain=self.domain, token=self.token, nonce=self.nonce)
        else:
            ws_add = "ws://{domain}/socket/websocket?token={token}&nonce={nonce}".format(domain=self.domain, token=self.token, nonce=self.nonce)
        print(ws_add)
        self.ws = await websockets.connect(ws_add)
        logger.info(f"{self.loginId} | websockets connect success !")
        return self.ws

    def login_get_identity(self, loginId, loginPwd, webLogin):
        if webLogin:
            self.login_without_tokenNonce(loginId=loginId, loginPwd=loginPwd)
        else:
            self.login_to_set_tokenNonce(loginId=loginId, loginPwd=loginPwd)
        self.set_identityId_from_myInfo(self.url, self.header)

    async def send_event(self, event, payload={}):
        body = {
            'ref': 'ref',
            'join_ref': 'join_ref',
            'topic': f"{self.roomType}:{self.roomId}",
            'event': event,
            'payload': payload,
        }
        # logger.info(f"{self.loginId} | send -> {self.roomType}:{self.roomId} | {self.subVersion} | {body['event']}")
        logger.debug(f"\n{pformat(body)}")
        await asyncio.sleep(0.5)
        await self.ws.send(json.dumps(body))

    async def __pingServer(self):
        while True:
            if self.socket_close:
                break
            try:
                await asyncio.sleep(40)
                await self.send_event('ping')
                # res = await asyncio.wait_for(self.ws.recv(), timeout=10)
                # jsData = json.loads(res)
            except Exception as e:
                print(f'[Ping error]: {self.loginId}')
                print(f"Error: {e}")

    async def listen(self, duration):
        print(f"\n {self.loginId} listening...")
        start_time = time.time()
        while True:
            if self.socket_close:
                break
            js = {'event': None}
            await asyncio.sleep(1)
            try:
                res = await asyncio.wait_for(self.ws.recv(), timeout=5)
                js = json.loads(res)
            except asyncio.TimeoutError as err:
                pass
            except Exception as err:
                logger.debug(err)
                logger.debug(traceback.format_exc())
            finally:
                if js.get('payload'):
                    payload = js['payload']
                    if js['event'] == 'room_left_bcst':
                        data = payload['data']
                        # logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {js['event']} | from : {data['userId']}")
                    elif js['event'] == 'pong':
                        logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {js['event']} ")
                    else:
                        ...

    async def goto_room(self, roomId):
        await self.ws_connect_by_tokenNonce()
        self.roomId = roomId
        await self.send_event(event = 'phx_join', payload= {} )
        asyncio.create_task(self.__pingServer())
        await asyncio.sleep(0.5)
        return self.roomId


    # async def master_create_goto_liveroom(self, loginId, loginPwd, roomTitle, roomDesc):
    #     self.roomId, _ = api.open_zegoRoom(self.url, self.header, roomTitle, roomDesc)
    #     await self.send_event(self.roomId, event = 'phx_join', payload= {} )
    #     asyncio.create_task(self.__pingServer())
    #     return self.roomId

    async def recv_events(self, eventPattern = None, duration=5):
        print(f"\n {self.loginId} receving...")
        start_time = time.time()
        count = 0
        while True:
            jsData = {'event': None}
            try:
                res = await asyncio.wait_for(self.ws.recv(), timeout=3)
                jsData = json.loads(res)
                count += 1
                if eventPattern :
                    if jsData['event'] == eventPattern:
                        break
            except asyncio.TimeoutError as err:
                pass
            except Exception as err:
                logger.debug(err)
                logger.debug(traceback.format_exc())
            finally:
                end_time = time.time()
                exe_time = int(end_time - start_time)
                if jsData['event']:
                    logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {jsData['event']} ")
                    logger.debug(f"\n{pformat(jsData)}\n")
                if exe_time >= duration:
                    break
        return jsData

    async def leaveRoom(self):
        await self.send_event('phx_leave', None)
        await self.ws.close()

class LiveRoomMaster(RoomUser):
    def __init__(self, domain, loginId, loginPwd, roomTitle, roomDesc, webLogin=False, tokenNonce:list = None):
        super().__init__(domain, loginId, loginPwd, webLogin, tokenNonce)
        self.roomType = 'live_room'
        self.roomId, _ = api.open_zegoRoom(self.url, self.header, roomTitle, roomDesc)
        # logger.info(f"{self.loginId} | Create liveroom : {self.roomId} success !")

    async def closeRoom(self):
        await self.send_event('close_room', {"roomId": self.roomId})
        await self.ws.close()

class LiveRoomClient(RoomUser):
    def __init__(self, domain, loginId, loginPwd, webLogin=False, tokenNonce:list = None):
        super().__init__(domain, loginId, loginPwd, webLogin, tokenNonce)
        self.roomType = 'live_room'

class ObsRoomMaster(RoomUser):
    def __init__(self, domain, loginId, loginPwd, webLogin=False, tokenNonce:list = None):
        super().__init__(domain, loginId, loginPwd, webLogin, tokenNonce)
        self.roomType = 'live_room'
        self.roomId = api.broadcaster_create_OBS_room(self.url, self.header, 'obs room', 'this is test desc', [], None)
        api.broadcaster_edit_OBS_room(self.url, self.header, self.roomId, None, None, 'ON_AIR' )

    async def closeRoom(self):
        await self.ws.close()
        res = api.broadcaster_close_OBS_room(self.url, self.header, self.roomId)
        assert res.status_code == 200

class ObsRoomClient(RoomUser):
    def __init__(self, domain, loginId, loginPwd, webLogin=False, tokenNonce:list = None):
        super().__init__(domain, loginId, loginPwd, webLogin, tokenNonce)
        self.roomType = 'live_room'


class VoiceRoomMaster(RoomUser):
    def __init__(self, domain, loginId, loginPwd, webLogin=False, tokenNonce:list = None):
        super().__init__(domain, loginId, loginPwd, webLogin, tokenNonce)
        self.roomType = 'vc_room'

class VoiceRoomClient(RoomUser):
    def __init__(self, domain, loginId, loginPwd, webLogin=False, tokenNonce:list = None):
        super().__init__(domain, loginId, loginPwd, webLogin, tokenNonce)
        self.roomType = 'vc_room'

class PriVoiceMaster(RoomUser):
    def __init__(self, domain, loginId, loginPwd, webLogin=False, tokenNonce:list = None):
        super().__init__(domain, loginId, loginPwd, webLogin, tokenNonce)
        self.roomType = 'private_vc_room'

    async def leaveRoom(self):
        await self.send_event('private_vc_leave', None)
        await self.ws.close()

class PriVoiceClient(RoomUser):
    def __init__(self, domain, loginId, loginPwd, webLogin=False, tokenNonce:list = None):
        super().__init__(domain, loginId, loginPwd, webLogin, tokenNonce)
        self.roomType = 'private_vc_room'

    async def leaveRoom(self):
        await self.send_event('private_vc_leave', None)
        await self.ws.close()

if __name__ == "__main__":

    """
    privateVoiceRoom test case
    1. privateVoiceroom_send_gift
    """

    async def privateVoiceroom_send_gift():
        logger.setLevel(logging.DEBUG)
        # domain = 'testing-api.xtars.com'
        domain = '34.81.211.190'
        priVoiceRoom_id = 39
        priMaster = PriVoiceMaster(domain, 'softnextqcshock+1@gmail.com' , '12345')
        priClient = PriVoiceClient(domain, 'track0050', '123456')
        await priMaster.goto_room(priVoiceRoom_id)
        await priClient.goto_room(priVoiceRoom_id)

        await priMaster.send_event('private_vc_enter')
        await priClient.send_event('private_vc_apply')
        # await priMaster.recv_events('private_vc_apply_bcst', 2)

        await priMaster.send_event('private_vc_review', {"userId": priClient.identity, "result": 'accept'})
        await priMaster.recv_events(None, 2)
        await priClient.send_event('gift', {"giftId": '47c32c52-a413-45d9-858d-4231464c0205', "targetUserId": priMaster.identity, "count": 1})
        await priClient.recv_events(None, 2)
        await priClient.leaveRoom()
        await priMaster.leaveRoom()
    """
    obsroom test case
    1. obsroom_send_gift
    2. obsroom_app_and_web_login
    """

    async def obsroom_send_gift():
        domain = '34.81.211.190'
        obsMaster1 = ObsRoomMaster(domain, 'obsMaster01', '123456')
        await obsMaster1.goto_room(obsMaster1.roomId)
        obsClient1 = ObsRoomClient(domain, 'track0040', '123456')
        await obsClient1.goto_room(obsMaster1.roomId)

        await obsClient1.send_event('gift', {"giftId": '3239e75d-8357-446e-b19c-7d62d51249cc', "targetUserId": obsMaster1.identity, "count": 1})
        await obsClient1.recv_events(None, 2)

        await obsClient1.leaveRoom()
        await obsMaster1.closeRoom()

    async def obsroom_app_and_web_login():
        logger.setLevel(logging.INFO)
        # logger.setLevel(logging.DEBUG)

        domain = '34.81.211.190'
        # domain = 'testing-api.xtars.com'
        obsMaster = ObsRoomMaster(domain, 'obsMaster01', '123456')
        await obsMaster.goto_room(obsMaster.roomId)
        await obsMaster.recv_events(None, 2)



        obsClient1 = ObsRoomClient(domain, 'track0040', '123456')
        await obsClient1.goto_room(obsMaster.roomId)
        await obsClient1.send_event('gift', {"giftId": '3239e75d-8357-446e-b19c-7d62d51249cc', "targetUserId": obsMaster.identity, "count": 1})
        await obsClient1.recv_events(None, 2)

        # #使用 weblogin 進入 session sub
        obsMaster_web = ObsRoomClient(domain, 'obsMaster01', '123456', webLogin = True)
        await obsMaster_web.goto_room(obsMaster.roomId)
        await obsMaster_web.recv_events(None, 2)

        await obsClient1.recv_events(None, 2)
        await obsClient1.leaveRoom()

        await obsMaster.recv_events(None, 2)
        await obsMaster_web.recv_events(None, 2)
        await obsMaster.closeRoom()


    """
    other test case
    1. asyncio_return_case
    2. obsroom_app_and_web_login
    """

    async def asyncio_return_case():
        logger.setLevel(logging.DEBUG)
        domain = '34.81.211.190'
        voiceRoom_id = 5
        voiceMaster = VoiceRoomMaster(domain, 'broadcaster021', '123456')
        await voiceMaster.goto_room(voiceRoom_id)
        voiceClient = VoiceRoomClient(domain, 'track0050', '123456')
        await voiceClient.goto_room(voiceRoom_id)
        # await voiceClient.send_event(event='gift', payload={"giftId": 'abc6985b-ac7d-4758-8e32-cde8c223b67f', "targetUserId": voiceMaster.identity, "count": 1})
        await voiceClient.send_event('gift', {"giftId": '27a4be53-1431-4c16-9ddb-c374200f7012', "targetUserId": voiceMaster.identity, "count": 1})

        recv_data = await voiceClient.recv_events('gift_bcst', 2)
        return recv_data

    """
    voiceRoom test case
    1. voiceroom_send_gift
    2. voiceroom_send_randomGift
    3. voiceroom_masterKickoutClient
    4. voiceroom_send_nonZero_backpackGift
    5. voiceroom_send_zero_backpackGift
    6. privateVoiceroom_send_gift
    """
    async def voiceroom_send_gift():
        logger.setLevel(logging.DEBUG)
        domain = '34.81.211.190'
        voiceRoom_id = 5
        voiceMaster = VoiceRoomMaster(domain, 'broadcaster021', '123456')
        await voiceMaster.goto_room(voiceRoom_id)
        voiceClient = VoiceRoomClient(domain, 'track0050', '123456')
        await voiceClient.goto_room(voiceRoom_id)
        await voiceClient.send_event(event='gift', payload={"giftId": 'abc6985b-ac7d-4758-8e32-cde8c223b67f', "targetUserId": voiceMaster.identity, "count": 1})
        await voiceClient.recv_events(None, 2)

    async def voiceroom_send_randomGift():
        logger.setLevel(logging.DEBUG)
        domain = '34.81.211.190'
        # domain = 'testing-api.xtars.com'
        voiceRoom_id = 5
        voiceMaster = VoiceRoomMaster(domain, 'broadcaster021', '123456')
        await voiceMaster.goto_room(voiceRoom_id)
        voiceClient = VoiceRoomClient(domain, 'track0050', '123456')
        await voiceClient.goto_room(voiceRoom_id)
        await voiceClient.send_event('gift_random', {"giftId": 1825, "targetUserId": voiceMaster.identity})
        await voiceClient.recv_events(None, 2)
        await voiceClient.leaveRoom()
        await voiceMaster.leaveRoom()

    async def voiceroom_send_nonZero_backpackGift():
        logger.setLevel(logging.DEBUG)
        domain = '34.81.211.190'
        # domain = 'testing-api.xtars.com'
        voiceRoom_id = 5
        voiceMaster = VoiceRoomMaster(domain, 'broadcaster021', '123456')
        await voiceMaster.goto_room(voiceRoom_id)
        voiceClient = VoiceRoomClient(domain, 'track0050', '123456')
        await voiceClient.goto_room(voiceRoom_id)
        await voiceClient.send_event('gift', {"giftId": '64d5f989-ff0a-444a-919f-0ea0d027bb69', "targetUserId": voiceMaster.identity, "count": 1, "backpackId": 4675 })
        await voiceClient.recv_events(None, 2)
        await voiceClient.leaveRoom()
        await voiceMaster.leaveRoom()

    async def voiceroom_send_zero_backpackGift():
        logger.setLevel(logging.DEBUG)
        domain = '34.81.211.190'
        # domain = 'testing-api.xtars.com'
        voiceRoom_id = 5
        voiceMaster = VoiceRoomMaster(domain, 'broadcaster021', '123456')
        await voiceMaster.goto_room(voiceRoom_id)
        voiceClient = VoiceRoomClient(domain, 'track0050', '123456')
        await voiceClient.goto_room(voiceRoom_id)
        await voiceClient.send_event('gift', {"giftId": 'ae7116bb-68dd-4f5a-afc9-49865d0e4f59', "targetUserId": voiceMaster.identity, "count": 1, "backpackId": 4676 })
        await voiceClient.recv_events(None, 2)
        await voiceClient.leaveRoom()
        await voiceMaster.leaveRoom()

    async def voiceroom_masterKickoutClient():
        domain = 'testing-api.xtars.com'
        voiceRoom_id = 5
        voiceMaster = VoiceRoomMaster(domain, 'broadcaster021', '123456')
        await voiceMaster.goto_room(voiceRoom_id)
        await voiceMaster.recv_events()

        voiceClient = VoiceRoomClient(domain, 'broadcaster001', '123456')
        await voiceClient.goto_room(voiceRoom_id)
        await voiceClient.recv_events()

        #觀眾預約上麥
        await voiceClient.send_event(event='book_seat', payload={})
        await voiceClient.recv_events('seat_booked')

        #master將觀眾拉上麥位
        await voiceMaster.send_event('pickup_seat', {"targetUserId": voiceClient.identity, "seatType": "host", "seatIndex": 1})
        await voiceMaster.recv_events('seat_pickedup')

        await asyncio.sleep(10)

        # master將觀眾踢下麥位
        await voiceMaster.send_event('kickout_seat', {"targetUserId": voiceClient.identity})
        await voiceMaster.recv_events('seat_kickedout')
        await voiceClient.leaveRoom()
        await voiceMaster.leaveRoom()



    """
    liveroom test case
    1. liveroom_LoginTest
    2. liveroom_single_operation
    3. liveroom_send_gift
    4. liveroom_send_randomGift
    5. liveroom_send_nonZero_backpackGift
    6. liveroom_send_Zero_backpackGift
    7. liveroom_send_randomGift_show_liveroom_result
    """
    async def liveroom_LoginTest():
        logger.setLevel(logging.DEBUG)
        domain = 'testing-api.xtars.com'
        # domain = '34.81.211.190'
        liveMaster = LiveRoomMaster(domain, 'broadcaster005', '12345',  'testTitle', 'testRoomDESC')
        await liveMaster.goto_room(liveMaster.roomId)
        liveClient = LiveRoomClient(domain, 'track0050', '123456')
        await liveClient.goto_room(liveMaster.roomId)
        await liveClient.recv_events(None, 5)
        await liveMaster.recv_events(None, 5)
        await liveClient.leaveRoom()
        await liveMaster.closeRoom()

    async def liveroom_single_operation():
        logger.setLevel(logging.DEBUG)
        domain = 'testing-api.xtars.com'
        roomId = 67479
        liveMaster_id = 'd82a7ba2-5c11-4615-aba7-2a768d927165'
        liveClient = LiveRoomClient(domain, 'track0050', '123456')
        await liveClient.goto_room(roomId)
        await asyncio.sleep(10)
        await liveClient.recv_events(None, 5)
        print('------------------------------------------------------------')
        await liveClient.send_event('gift', {"giftId": 'bde03503-db69-47a2-b099-e64ec35addd3', "targetUserId": liveMaster_id, "count": 1})
        await asyncio.sleep(10)
        await liveClient.recv_events(None, 5)
        await liveClient.leaveRoom()

    async def liveroom_send_gift():
        domain = '34.81.211.190'
        liveMaster = LiveRoomMaster(domain, 'broadcaster005', '12345', 'testTitle', 'testRoomDESC')
        await liveMaster.goto_room(liveMaster.roomId)
        liveClient = LiveRoomClient(domain, 'track0050', '123456')
        await liveClient.goto_room(liveMaster.roomId)
        # await liveClient.send_event('gift', {"giftId": 'ff6c0059-4dc8-4831-b2be-783f29bdaed1', "targetUserId": liveMaster.identity, "count": 1, "backpackId": 4442})
        await liveClient.send_event('gift', {"giftId": '93364e78-6e3b-442d-9eca-d37d491666ef', "targetUserId": liveMaster.identity, "count": 1})
        await liveClient.recv_events(None, 2)

    async def liveroom_send_randomGift():
        logger.setLevel(logging.DEBUG)
        domain = '34.81.211.190'
        liveMaster = LiveRoomMaster(domain, 'broadcaster005', '12345', 'testTitle', 'testRoomDESC')
        await liveMaster.goto_room(liveMaster.roomId)
        liveClient = LiveRoomClient(domain, 'track0050', '123456')
        await liveClient.goto_room(liveMaster.roomId)
        # await liveClient.send_event('gift', {"giftId": 'ff6c0059-4dc8-4831-b2be-783f29bdaed1', "targetUserId": liveMaster.identity, "count": 1, "backpackId": 4442})
        await liveClient.send_event('gift_random', {"giftId": 1743, "targetUserId": liveMaster.identity})
        await liveClient.recv_events(None, 2)
        await liveClient.leaveRoom()
        await liveMaster.closeRoom()

    async def liveroom_send_nonZero_backpackGift():
        logger.setLevel(logging.DEBUG)
        # domain = 'testing-api.xtars.com'
        domain = '34.81.211.190'
        liveMaster = LiveRoomMaster(domain, 'broadcaster005', '12345', 'testTitle', 'testRoomDESC')
        await liveMaster.goto_room(liveMaster.roomId)
        liveClient = LiveRoomClient(domain, 'track0050', '123456')
        await liveClient.goto_room(liveMaster.roomId)
        # await liveClient.send_event('gift', {"giftId": 'ff6c0059-4dc8-4831-b2be-783f29bdaed1', "targetUserId": liveMaster.identity, "count": 1, "backpackId": 4442})
        await liveClient.send_event('gift', {"giftId": '41b22231-9cae-4936-b794-a092e6dcf209', "targetUserId": liveMaster.identity, "count": 2, "backpackId": 4664 })
        await liveClient.recv_events(None, 2)
        await liveClient.leaveRoom()
        await liveMaster.closeRoom()


    async def liveroom_send_zero_backpackGift():
        logger.setLevel(logging.DEBUG)
        # domain = 'testing-api.xtars.com'
        domain = '34.81.211.190'
        liveMaster = LiveRoomMaster(domain, 'broadcaster005', '12345', 'testTitle', 'testRoomDESC')
        await liveMaster.goto_room(liveMaster.roomId)
        liveClient = LiveRoomClient(domain, 'track0050', '123456')
        await liveClient.goto_room(liveMaster.roomId)
        # await liveClient.send_event('gift', {"giftId": 'ff6c0059-4dc8-4831-b2be-783f29bdaed1', "targetUserId": liveMaster.identity, "count": 1, "backpackId": 4442})
        await liveClient.send_event('gift', {"giftId": 'b49b3c18-2546-4089-b53c-a323775b0e14', "targetUserId": liveMaster.identity, "count": 2, "backpackId": 4668 })
        await liveClient.recv_events(None, 2)
        await liveClient.leaveRoom()
        await liveMaster.closeRoom()

    async def liveroom_send_randomGift_show_liveroom_result():
        logger.setLevel(logging.DEBUG)
        domain = '34.81.211.190'
        # domain = 'testing-api.xtars.com'
        liveMaster = LiveRoomMaster(domain, 'broadcaster005', '12345', 'testTitle', 'testRoomDESC')
        await liveMaster.goto_room(liveMaster.roomId)
        liveClient = LiveRoomClient(domain, 'track0050', '123456')
        await liveClient.goto_room(liveMaster.roomId)
        await liveClient.send_event('gift', {"giftId": '451f13a3-7fbf-4ce6-94e1-8f64ab087d8a', "targetUserId": liveMaster.identity, "count": 1})
        # await liveClient.send_event('gift_random', {"giftId": 1825, "targetUserId": liveMaster.identity})
        await liveClient.recv_events(None, 2)
        await asyncio.sleep(5)
        print("-------------**home**-------------")
        api_name = f"/api/v2/live/list/home"
        res = api.apiFunction(liveMaster.url, liveMaster.header, api_name, 'get', None)
        home_data = (res.json())['data']
        for i in home_data:
            if i['liveMasterId'] == liveMaster.identity:
                pprint(i)
        print("-------------**home/more**-------------")
        api_name = f"/api/v2/live/list/home/more"
        res = api.apiFunction(liveMaster.url, liveMaster.header, api_name, 'get', None)
        home_more_data = (res.json())['data']
        for i in home_more_data:
            if i['liveMasterId'] == liveMaster.identity:
                pprint(i)
        await liveMaster.closeRoom()

        print("-------------**liveResult**-------------")
        api_name = f"/api/v2/liveMaster/liveResult/{liveMaster.roomId}"
        res = api.apiFunction(liveMaster.url, liveMaster.header, api_name, 'get', None)
        pprint(res.json())


    async def liveroom_send_gift_with_tokenNonce():
        logger.setLevel(logging.DEBUG)
        domain = 'testing-api.xtars.com'
        liveMaster = LiveRoomMaster(domain, 'broadcaster005', '12345', 'testTitle', 'testRoomDESC')
        await liveMaster.goto_room(liveMaster.roomId)
        liveClient = LiveRoomClient(domain, loginId = 'track0050', loginPwd= None, webLogin= False, tokenNonce= ['04d6990036ec4b2f8697c6e69de35051', '2K8UYPTXKS'])
        await liveClient.goto_room(liveMaster.roomId)
        # await liveClient.send_event('gift', {"giftId": 'ff6c0059-4dc8-4831-b2be-783f29bdaed1', "targetUserId": liveMaster.identity, "count": 1, "backpackId": 4442})
        await liveClient.send_event('gift', {"giftId": '3239e75d-8357-446e-b19c-7d62d51249cc', "targetUserId": liveMaster.identity, "count": 1})
        await liveClient.recv_events(None, 2)
        await liveClient.leaveRoom()
        await liveMaster.closeRoom()


    async def liveroom_listen_events():
        logger.setLevel(logging.DEBUG)
        domain = 'testing-api.xtars.com'
        liveMaster = LiveRoomMaster(domain, 'broadcaster005', '12345', 'testTitle', 'testRoomDESC')
        await liveMaster.goto_room(liveMaster.roomId)
        url = wsGame.get_v2game_url(1, liveMaster.token, liveMaster.nonce , liveMaster.roomId)
        print(url)
        await liveMaster.recv_events(None, 1200)


        await liveMaster.closeRoom()


    # [ privateVoiceRoom ]

    # print(f"( privateVoiceRoom : 私聊間 贈送禮物 )")
    # asyncio.run(privateVoiceroom_send_gift())

    # [ obsroom ]

    # print(f"( obsroom : obs直播間 贈送禮物 )")
    # asyncio.run(Obsroom_send_gift())

    # print(f"( obsroom : obs直播間 app 與 web login )")
    # asyncio.run(obsroom_app_and_web_login())

    # [ other ]

    # print(f"( other : asyncio 返回值 )")
    # x = asyncio.run(asyncio_return_case())
    # print('---------------test---------------')
    # pprint(x)


    # [ Liveroom ]

    # print(f"( Liveroom : 直播間 登入)")
    # asyncio.run(liveroom_LoginTest())

    # print(f"( Liveroom : 直播間 單一登入)")
    # asyncio.run(liveroom_single_operation())

    # print(f"( Liveroom : 直播間 贈送禮物 )")
    # asyncio.run(liveroom_send_gift())

    # print(f"( Liveroom : 直播間 贈送隨機禮物 )")
    # asyncio.run(liveroom_send_randomGift())

    # print(f"( Liveroom : 直播間 贈送有價背包禮物 )")
    # asyncio.run(liveroom_send_nonZero_backpackGift())

    # print(f"( Liveroom : 直播間 贈送無價價背包禮物 )")
    # asyncio.run(liveroom_send_zero_backpackGift())

    # print(f"( Liveroom : 直播間 贈送隨機禮物，最後看所有相關點數)")
    # asyncio.run(liveroom_send_randomGift_show_liveroom_result())

    # print(f"( Liveroom : 直接使用 token nonce 登入 直播間 贈送禮物 )")
    # asyncio.run(liveroom_send_gift_with_tokenNonce())

    # print(f"( Liveroom : 紅包測試 )")
    # asyncio.run(liveroom_listen_events())

    # [ voiceroom ]

    # print(f"( voiceroom : 聲聊間 贈送禮物 )")
    # asyncio.run(voiceroom_send_gift())

    # print(f"( voiceroom : 聲聊間 贈送隨機禮物 )")
    # asyncio.run(voiceroom_send_randomGift())

    # print(f"( voiceroom : 聲聊間 贈送有價背包禮物 )")
    # asyncio.run(voiceroom_send_nonZero_backpackGift())

    # print(f"( voiceroom  聲聊間 贈送無價價背包禮物 )")
    # asyncio.run(voiceroom_send_zero_backpackGift())

    # print(f"( voiceroom : 聲聊間 聲聊主踢出客戶)")
    # asyncio.run(voice_masterKickoutClient())


# async def liveroom_master_and_multiUser_login(domain, masterAcc, masterPass, userLoginInfo:list):
#     liveMaster = LiveRoomMaster(domain, masterAcc, masterPass,  'testTitle', 'testRoomDESC')
#     await liveMaster.goto_room(liveMaster.roomId)

#     clients_socket = []
#     for liveClient in userLoginInfo:
#         liveClient = LiveRoomClient(domain, liveClient[0], liveClient[1])
#         await liveClient.goto_room(liveMaster.roomId)
#         clients_socket.append(liveClient)
#     bg_task = asyncio.create_task(liveMaster.listen(300))
#     await bg_task
#     for cli_sock in clients_socket:
#         await cli_sock.leaveRoom()

#     await liveMaster.closeRoom()

# async def multi_liveroom_with_multiUser(login_info_list):
#     tasks = []
#     for logiInfo in login_info_list:
#         masterAcc = logiInfo['master_acc']
#         masterPass = logiInfo['master_pass']
#         login_info = logiInfo['user_loginInfo']
#         task = asyncio.create_task(liveroom_master_and_multiUser_login(domain, masterAcc, masterPass, login_info))
#         tasks.append(task)
#     await asyncio.gather(*tasks, return_exceptions=True)




# login_info = [
#         {
#             'master_acc': 'broadcaster005',
#             'master_pass': '12345',
#             'user_loginInfo': [('track0050', '123456'),  ('track0040', '123456')]
#         },
#         {
#             'master_acc': 'broadcaster026',
#             'master_pass': '123456',
#             'user_loginInfo': [('track0001', '123456'),  ('track0002', '123456'),  ('track0003', '123456'),  ('track0004', '123456'),  ('track0005', '123456')]
#         },
#         {
#             'master_acc': 'broadcaster041',
#             'master_pass': '123456',
#             'user_loginInfo': [('track0006', '123456'),  ('track0007', '123456'),  ('track0009', '123456'),  ('track0010', '123456'), ('track0011', '123456')]
#         }
# ]

# logger.setLevel(logging.INFO)
# domain = 'testing-api.xtars.com'

# asyncio.run(multi_liveroom_with_multiUser(login_info))

