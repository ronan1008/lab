import logging
import time
import asyncio
import timeit
import random
import dbConnect
import traceback
import json
import pytz
from datetime import datetime, timedelta
from pprint import pprint, pformat
from webSocket_room import LiveRoomMaster, LiveRoomClient

console_handler = logging.StreamHandler()
console_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s','%H:%M:%S')
console_handler.setFormatter(console_format)
# console_handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

class LiveRoomMasterCheckRobot(LiveRoomMaster):
    async def listen_to_check_robot(self):
        print(f"\n {self.loginId} listening...")
        chatbot_result = dbConnect.dbQuery(self.domain, 'Select id from chatbot where advanced = 0', 'shocklee')
        advChatbot_result = dbConnect.dbQuery(self.domain, 'Select id from chatbot where advanced = 1', 'shocklee')
        rush_result = dbConnect.dbQuery(self.domain, 'select target_user_id, quantity from chatbot_target_user where delete_at is Null', 'shocklee')
        rush_id_list = [ rushid[0] for rushid in rush_result ]

        chatbot_list = [ i[0] for i in chatbot_result]
        advChatbot_list = [ i[0] for i in advChatbot_result]
        last_sendTime = 0
        chatBot_count = 0
        total_count = 0
        advchatBot_count = 0
        lastChatbot_count = 0
        round_count = 0
        round_gift_count = 0
        while True:
            if self.socket_close:
                break
            js = {'event': None}
            await asyncio.sleep(3)
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
                    if js['event'] == 'room_in_bcst':
                            data = payload['data']
                            sendTime = payload['sendTime']
                            if data['fromUser']['id'] in advChatbot_list:
                                logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {js['event']} | from : {data['fromUser']['name']} | {sendTime} | advanced chatbot")
                                logger.info(f"{self.loginId} | room_in_bcst interval : {(sendTime - last_sendTime) / 1000} ")
                                last_sendTime = sendTime
                                chatBot_count += 1
                                advchatBot_count += 1
                                total_count += 1
                                logger.info(f"{self.loginId} | chatBot_count : {chatBot_count} ")

                            elif data['fromUser']['id'] in chatbot_list:
                                logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {js['event']} | from : {data['fromUser']['name']} | {sendTime} | chatbot")
                                logger.info(f"{self.loginId} | room_in_bcst interval : {(sendTime - last_sendTime) / 1000} ")
                                last_sendTime = sendTime
                                chatBot_count += 1
                                total_count += 1
                                logger.info(f"{self.loginId} | chatBot_count : {chatBot_count} ")

                            elif data['fromUser']['id'] == self.identity :
                                # logger.info(f"\n{pformat(js)}\n")
                                last_sendTime = sendTime
                                logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {js['event']} | from : {data['fromUser']['name']} | {sendTime} | self ")
                            else:
                                total_count += 1
                                logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {js['event']} | from : {data['fromUser']['name']} | {sendTime} | normal user")
                    elif js['event'] == 'gift_bcst':
                        data = payload['data']
                        logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {js['event']} | from : {data['fromUser']['name']} {data['gift']['name']}")
                        round_gift_count += 1
                    elif js['event'] == 'room_left_bcst':
                        data = payload['data']
                        utcnow = datetime.now(pytz.timezone('UTC'))
                        sendTime = int(utcnow.timestamp() * 1000)
                        total_count -= 1
                        if data['userId'] in advChatbot_list:
                            logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {js['event']} | from : {data['userId']} | {sendTime} | advanced chatbot")
                            logger.info(f"{self.loginId} | room_in_bcst interval : {(sendTime - last_sendTime) / 1000} ")
                            advchatBot_count -= 1
                            chatBot_count -= 1
                            logger.info(f"{self.loginId} | chatBot_count : {chatBot_count} ")
                        elif data['userId'] in chatbot_list:
                            logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {js['event']} | from : {data['userId']} | {sendTime} | chatbot")
                            logger.info(f"{self.loginId} | room_in_bcst interval : {(sendTime - last_sendTime) / 1000} ")
                            chatBot_count -= 1
                            logger.info(f"{self.loginId} | chatBot_count : {chatBot_count} ")
                        else:
                            logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {js['event']} | from : {data['userId']} | {sendTime} | normal user")
                            logger.info(f"{self.loginId} | chatBot_count : {chatBot_count} ")
                    else:
                        logger.info(f"{self.loginId} | recv <- {self.roomType}:{self.roomId} | {self.subVersion}  | {js['event']} ")

                if chatBot_count < lastChatbot_count :
                    print(f'..............[{self.roomId} : {self.loginId} : {round_count} 解散階段]..............')
                elif lastChatbot_count == 0 and chatBot_count > lastChatbot_count :
                    round_gift_count = 0
                    round_count += 1
                    print(f'..............[{self.roomId} : {self.loginId} : {round_count} 集合階段]..............')



                if lastChatbot_count != chatBot_count :
                    if self.identity in rush_id_list:
                        print(f'--------[{self.roomId} : {self.loginId}] [I am rush master]--------')
                    else:
                        print(f'--------[{self.roomId} : {self.loginId}] [I am normal master]--------')
                    lastChatbot_count = chatBot_count

                print(f"[{self.roomId} : {self.loginId} :  {round_count}]")
                print(f" total count : {total_count}")
                print(f" total chatBot count : {lastChatbot_count}")
                print(f" advchatBot count : {advchatBot_count}")
                print(f" gift count : {round_gift_count}")


                # else:
                #     print('--------[debug]--------')
                #     print(f"[round {round_count}]")
                #     print(f" total_count : {total_count}")
                #     lastChatbot_count = chatBot_count
                #     print(f" chatBot_count : {lastChatbot_count}")
                #     print(f" advchatBot_count : {advchatBot_count}")
                #     print(f" gift_count : {round_gift_count}")







async def liveroom_master_and_multiUser_login(domain, masterAcc, masterPass, userLoginInfo:list, duration):

    Queue = asyncio.Queue()
    liveMaster = LiveRoomMasterCheckRobot(domain, masterAcc, masterPass,  f'ChatBot-{masterAcc}', '測試chatbot房間，固定有10人')
    await liveMaster.goto_room(liveMaster.roomId)
    clients_socket = []
    for liveClient in userLoginInfo:
        await asyncio.sleep(random.randint(1, 10))
        liveClient = LiveRoomClient(domain, liveClient[0], liveClient[1])
        await liveClient.goto_room(liveMaster.roomId)
        clients_socket.append(liveClient)
    asyncio.create_task(liveMaster.listen_to_check_robot())
    for client in clients_socket:
        asyncio.create_task(client.listen(duration))
    await asyncio.sleep(duration)
    for client in clients_socket:
        client.socket_close = True
        await asyncio.sleep(60)
        await client.leaveRoom()
    liveMaster.socket_close = True
    await asyncio.sleep(60)
    await liveMaster.closeRoom()

async def multi_liveroom_with_multiUser(login_info_list, duration):
    tasks = []
    for logiInfo in login_info_list:
        masterAcc = logiInfo['master_acc']
        masterPass = logiInfo['master_pass']
        login_info = logiInfo['user_loginInfo']
        await asyncio.sleep(random.randint(1, 5))
        task = asyncio.create_task(liveroom_master_and_multiUser_login(domain, masterAcc, masterPass, login_info, duration))
        tasks.append(task)
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    login_info = [
            # {
            #     'master_acc': 'broadcaster026',
            #     'master_pass': '123456',
            #     'user_loginInfo': [(f"track{i:04d}", '123456') for i in range(110, 120)]
            # },
            # {
            #     'master_acc': 'broadcaster041',
            #     'master_pass': '123456',
            #     'user_loginInfo': [(f"track{i:04d}", '123456') for i in range(120, 130)]
            # },
            # {
            #     'master_acc': 'broadcaster034',
            #     'master_pass': '123456',
            #     'user_loginInfo': [(f"track{i:04d}", '123456') for i in range(130, 140)]
            # },
            # {
            #     'master_acc': 'broadcaster083',
            #     'master_pass': '123456',
            #     'user_loginInfo': [(f"track{i:04d}", '123456') for i in range(140, 150)]
            # },
            # {
            #     'master_acc': 'broadcaster005',
            #     'master_pass': '12345',
            #     'user_loginInfo': [(f"track{i:04d}", '123456') for i in range(150, 160)]
            # },


            # {
            #     'master_acc': 'broadcaster037',
            #     'master_pass': '123456',
            #     'user_loginInfo': [(f"track{i:04d}", '123456') for i in range(160, 161)]
            # },

            {
                'master_acc': 'broadcaster066',
                'master_pass': '123456',
                'user_loginInfo': [(f"track{i:04d}", '123456') for i in range(170, 171)]
            }
    ]
    logger.setLevel(logging.INFO)
    domain = 'testing-api.xtars.com'
    # domain = '34.81.211.190'
    hours = 1

    expect_exe_time = int(timedelta(hours=hours).total_seconds())
    print(expect_exe_time)
    start_time = time.time()
    asyncio.run(multi_liveroom_with_multiUser(login_info, expect_exe_time))
    end_time = time.time()
    total_exe_time = int(end_time - start_time)
    print(f"Total Execute Time : {total_exe_time} seconds")
