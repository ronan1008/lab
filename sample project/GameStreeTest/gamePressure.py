import json, requests, pytest, time, multiprocessing, sys, socket, random, threading, psutil, traceback, argparse
import urllib.parse as urlparse
from urllib.parse import urlencode
from pprint import pprint
from datetime import datetime
from configparser import ConfigParser
from tool import api, chatlib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException, InvalidSessionIdException, StaleElementReferenceException

# [ini 設定]
config = ConfigParser()
config.read('gamePressure.ini')
#Settings
PLAYER = int(config.get('Game Settings', 'PLAYER'))
RANGE = int(config.get('Game Settings', 'RANGE'))
ANSWER = int(config.get('Game Settings', 'ANSWER'))
EXE_TIME = int(config.get('Game Settings', 'EXE_TIME'))
COST_FEE = int(config.get('Game Settings', 'COST_FEE'))
ROUND_BTW_TIME = int(config.get('Game Settings', 'ROUND_BTW_TIME'))
SELENIUM_LOCATION = str(config.get('Game Settings', 'SELENIUM_LOCATION'))
HOST_BS = int(config.get('Browser Debug', 'HOST_OPEN_BROWSER'))
CLIENT_BS = int(config.get('Browser Debug', 'CLIENT_OPEN_BROWSER'))
CHECK_POINT = int(config.get('Browser Debug', 'CHECK_POINT'))
LIMIT_ROUND = int(config.get('Browser Debug', 'LIMIT_ROUND'))
WS_MASTER = int(config.get('WebSocket Debug', 'WS_MASTER'))
WS_CLIENT = int(config.get('WebSocket Debug', 'WS_CLIENT'))
#enviroment
test_parameter = dict()
test_parameter['prefix'] = config.get('Enviroment', 'DOMAIN')
test_parameter['db'] = config.get('Enviroment', 'DB')

# [命令列 參數設定]
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('masterLoginIds',nargs='+', help = "請輸入符合 ini 條件的 Master LoginId", type=str)
arg_parser.add_argument("-t", "--backend_token", type=str, help="請帶入 backend_token")
arg_parser.add_argument("-n", "--backend_nonce", type=str, help="請帶入 backend_nonce")
args = arg_parser.parse_args()
masterLoginIds = args.masterLoginIds
if args.backend_nonce and args.backend_token :
    backend_header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': args.backend_token, 'X-Auth-Nonce': args.backend_nonce}
else:
    result = api.user_login(test_parameter['prefix'], 'tl-lisa', '12345678')
    backend_token, backend_nonce  = result['data']['token'], result['data']['nonce']
    backend_header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': backend_token, 'X-Auth-Nonce': backend_nonce}

#global variable
GUEST_ENTER_ROOM_COUNT = 0
GUESS_NUM = 1
GAME_ROUND = 0
HOST_OPEN_GAME = False
GUEST_JOIN_GAME = False
END_GAME = False
GAME_PLAY_LIST = []
GAME_POINTS_CHECK = []
USER_POINTS = dict()
GAME_OVER = False
ERROR_FOUND = False
REOPEN_ROOM = False
monitor_webSocket_id = ""

#遞迴每xx秒，socket ping
def ping_interval(sock, role, seconds=60):
    global END_GAME
    if not END_GAME:
        threading.Timer(seconds, ping_interval, (sock, role, seconds, )).start()
        chatlib.keep_ping(sock)
    else:
        print("[End Ping] {} ".format(role))

def parse_webSocket_log(driver, role):
    print('Starting Record WebSocket log:' + role)
    try:
        while True:
            browser_log = driver.get_log('performance')
            for wsData in browser_log:
                log = json.loads(wsData["message"])["message"]
                if "Network.webSocketFrameReceived" in log["method"]:
                    prefix = '[websocket-recv]{}: '.format(role)
                    if log['params']['response']['payloadData']== 'pong':
                        # print(prefix + 'pong')
                        pass
                    else:
                        payloadData =  json.loads(log['params']['response']['payloadData'])
                        event= payloadData['event']
                        data = payloadData['data']
                        if event == "AUTH":
                            print(prefix + 'AUTH')
                        elif event == 'ROOM_INFO':
                            if data['status'] == 'waiting':
                                print(prefix + 'Waiting Users :' + str(len(data['gameInfo']['playerInfos'])) + '/' +  str(data['gameInfo']['totalPlayers']))
                            elif data['status'] == 'playing':
                                print(prefix + 'playing')
                            elif data['status'] == 'pending':
                                print(prefix + 'pending')
                            else:
                                print('---------0---------')
                                print(prefix + str(payloadData))
                        elif event == 'ROUND_INFO':
                            if data['guessHistory']:
                                print(prefix + 'guessHistory')
                        elif event == 'GAME_OVER':
                            print(prefix + 'GAME_OVER:winner' + str(data['winner']))
                        elif event == 'ERROR':
                            print(prefix + str(data['error']))
                        elif event == 'ROOM_CLOSE':
                            print(prefix + str(data))

                        else:
                            print('---------1---------')
                            print(prefix + str(payloadData))
                elif "Network.webSocketFrameSent" in log["method"]:
                    prefix = '[websocket-sent]{}: '.format(role)
                    if log['params']['response']['payloadData']== 'ping':
                        # print(prefix + 'ping')
                        pass
                    else:
                        payloadData =  json.loads(log['params']['response']['payloadData'])
                        if payloadData['action'] == 'nextRound':
                            print(prefix + 'nextRound')
                        elif payloadData['action'] == 'registerGameRoom':
                            print(prefix +'registerGameRoom ' + str(payloadData['data']) )
                        elif payloadData['action'] == 'joinRoom':
                            print(prefix +'joinRoom')
                        elif payloadData['action'] == 'guess':
                            print(prefix +'guess ' + str(payloadData['data']))
                        elif payloadData['action'] == 'joinGame':
                            print(prefix +'client joinGame')
                        else:
                            print('---------2---------')
                            print(prefix + str(payloadData))
                elif "Network.webSocketClosed" in log["method"]:
                    print('---------3---------')
                    prefix = '[websocket-close]{}: '.format(role)
                    print(prefix + str(payloadData))
    except InvalidSessionIdException:
        print('Stop Record WebSocket log:' + role)
    except:
        pass
        # traceback.print_exc()

def open_browser(browser_type, visual):
    mobile_emulation = {
    # "deviceMetrics": { "width": 360, "height": 800, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
    chrome_options = Options()
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'performance': 'ALL'}
    if not visual :
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=400,600")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("disable-dev-shm-usage")
    chrome_options.add_argument("disable-infobars")
    # chrome_options.add_argument("--auto-open-devtools-for-tabs")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument('--disk-cache-dir=/home/shocklee/temp')
    chrome_options.add_experimental_option("detach", False)
    # chrome_options.add_experimental_option('w3c', False)
    # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    if browser_type == 'Chrome':
        if SELENIUM_LOCATION != 'local':
            driver = webdriver.Chrome(SELENIUM_LOCATION, desired_capabilities=d, options=chrome_options)
        else:
            driver = webdriver.Chrome(desired_capabilities=d, options=chrome_options)
    elif browser_type == 'Safari':
        driver = webdriver.Safari()
    elif browser_type == 'Firefox':
        driver = webdriver.Firefox(executable_path='/Users/shocklee/Downloads/geckodriver')
    driver.implicitly_wait(30)
    return driver

def play_host_game(driver, host_game_url, player, cost, numRange, answer):
    global WS_MASTER
    print("Host Open Game : {}".format(host_game_url))
    driver.get(host_game_url)
    if WS_MASTER == 1:
        h = threading.Thread(target = parse_webSocket_log, args = (driver,'master'))
        h.start()
    # time.sleep(600)
    beg_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='UltimatePassword']")))
    beg_btn.click()

    #調整人數
    play_add_btn = driver.find_element_by_xpath("//*[@id='addPlayerBtn']")
    for _ in range(2, player):
        time.sleep(2)
        play_add_btn.click()
    #調整金額
    # fee_input = driver.find_element_by_xpath("//*[@id='fee']")
    # fee_input.clear()
    # fee_input.send_keys(cost)
    #選擇數字區間
    number_range = driver.find_element_by_xpath("//*[@id='range']")
    # number_range.clear()
    # number_range.send_keys(numRange)
    #密碼自訂
    pass_cus = driver.find_element_by_xpath("//*[@id='manualMode']")
    pass_cus.click()
    pass_cus_input = driver.find_element_by_xpath("//*[@id='answerInput']")
    # pass_cus_input.clear()
    pass_cus_input.send_keys(answer)
    #輸入獎勵
    reward_input = driver.find_element_by_xpath("//*[@id='reward']")
    reward_input.send_keys('Donate Me!')
    #開啟遊戲
    game_submit_btn = driver.find_element_by_xpath("//*[@id='submitBtn']")
    game_submit_btn.click()
    # waitingBanner = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='waitingPunishmentHostDesc']")))

#直播主，打開瀏覽器
def start_game(host_game_url, player, cost, numRange, answer):
    global GUEST_JOIN_GAME, GUESS_NUM, ANSWER, HOST_OPEN_GAME, GAME_PLAY_LIST, END_GAME, GAME_ROUND, GAME_OVER, ERROR_FOUND
    broken = False
    try:
        time.sleep(random.randint(1, 5))
        driver = open_browser('Chrome', visual=HOST_BS)
        driver_process = psutil.Process(driver.service.process.pid)
        play_host_game(driver, host_game_url, player, cost, numRange, answer)
        time.sleep(2)
        GUEST_JOIN_GAME = True
    except TimeoutException:
        if not END_GAME:
            print('Error : 直播主超過時間')
            ERROR_FOUND = True
    except WebDriverException:
        traceback.print_exc()
        print('Error : 直播主browser 可能損毀，準備重啟')
        if not END_GAME:
            ERROR_FOUND = True
            broken = True
    except:
        print('Error : 出現非預期錯誤，全部重新開始')
        traceback.print_exc()
        ERROR_FOUND = True

    errRound = 0
    while True:
        try:
            if END_GAME == True:
                if driver_process.is_running():
                    driver.quit()
                print('直播主結束遊戲，關閉瀏覽器')
                break
            #如果有人猜對了答案 div class="avatarIconOverlay"
            if GAME_OVER or ERROR_FOUND:
                if ERROR_FOUND:
                    print("Error : 發現錯誤結束該回合。")
                else:
                    GAME_ROUND += 1
                print("準備初始化遊戲。")
                # WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='avatarIconOverlay']")))
                if not broken:
                    if driver_process.is_running():
                        print('直播主關閉瀏覽器')
                        driver.quit()
                #初始化所有變數
                time.sleep(ROUND_BTW_TIME)
                ERROR_FOUND = False
                GAME_OVER = False
                GUEST_JOIN_GAME = False
                GAME_PLAY_LIST = []
                HOST_OPEN_GAME = True
                # GUESS_NUM = 0
                break
            continue_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='game-continue-actions']")))
            if continue_element:
                time.sleep(random.randint(3, 8))
                print("所有成員完成作答，點擊繼續遊戲")
                con_btn = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='continueBtn']")))
                con_btn.click()
                errRound = 0
        except:
            time.sleep(5)
            errRound += 1

            if errRound == 3:
                h = threading.Thread(target = parse_webSocket_log, args = (driver,'master'))
                h.start()

            elif errRound == 8:
                if driver_process.is_running():
                    driver.get_screenshot_as_file('host_round_debug{}.png'.format(time.strftime("%m%d%H%M%S", time.localtime(time.time()))   )   )
                    print('host_round_debug{}.png'.format(  time.strftime("%m%d%H%M%S", time.localtime(time.time()))   ))
                print('Error : 直播主，超過等待時間，先結束遊戲等待重開')
                ERROR_FOUND = True

#使用者，打開瀏覽器
def join_game(game_url, identity_id, user_header=None):
    print("{} 參加遊戲，打開瀏覽器 : {}".format(identity_id, game_url))
    global GUESS_NUM, ANSWER, END_GAME, GAME_OVER, ERROR_FOUND, monitor_webSocket_id, WS_CLIENT
    time.sleep(random.uniform(1, 5))
    broken = False
    try:
        driver = open_browser('Chrome', visual=CLIENT_BS)
        if identity_id == monitor_webSocket_id and WS_CLIENT == 1:
            c = threading.Thread(target = parse_webSocket_log, args = (driver,'client {}'.format(identity_id)))
            c.start()
        driver.get(game_url)
        driver_process = psutil.Process(driver.service.process.pid)
        # 開始頁面，按下
        join_btn = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='joinBtn']")))
        join_btn.click()
    except TimeoutException:
        if not END_GAME:
            print('Error : 使用者 {} TimeoutException'.format(identity_id))
            ERROR_FOUND = True
    except WebDriverException:
        if not END_GAME:
            print('Error : 使用者 {} WebDriver 可能 Fail'.format(identity_id))
            ERROR_FOUND = True
            broken = True
    except:
        print('Error : 出現非預期錯誤')
        traceback.print_exc()
        ERROR_FOUND = True

    # 參加遊戲之後，檢查點數有無被扣除
    if CHECK_POINT == 1:
        remainPoints, revenueSummary = api.get_my_points_from_db(test_parameter['db'], identity_id)
        orig_remainPoints, orig_revenueSummary = USER_POINTS[identity_id]
        if (orig_remainPoints - remainPoints) == COST_FEE and (orig_revenueSummary == revenueSummary):
            print('\033[32m {} 第 {} 回合 點數沒問題 \033[0m'.format(identity_id, GAME_ROUND))
            GAME_POINTS_CHECK.append(True)
        else:
            print('\033[93m {} 第 {} 回合 點數有問題，請檢查 \033[0m'.format(identity_id, GAME_ROUND))
            print('{identity_id} 原本的 剩餘點數:{rpts} , 業績點數:{rvpts}'.format(identity_id=identity_id, rpts = orig_remainPoints, rvpts= orig_revenueSummary))
            print('{identity_id} 現在的 剩餘點數:{rpts} , 業績點數:{rvpts}'.format(identity_id=identity_id, rpts = remainPoints, rvpts= revenueSummary))
            GAME_POINTS_CHECK.append(False)
    errRound = 0
    while True:
        try:
            if END_GAME == True:
                if driver:
                    driver.quit()
                print('使用者結束遊戲，關閉瀏覽器')
                break
            if GAME_OVER or ERROR_FOUND:
                if not broken:
                    if driver_process.is_running():
                        driver.quit()
                        print('使用者關閉瀏覽器')
                break
            #如果出現 請作答 的頁面，就填入數字
            passInput_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@inputmode='numeric']")))
            if passInput_element:
                time.sleep(random.randint(3, 6))
                minN, maxN = passInput_element.get_attribute("placeholder").split('-')
                randNum = random.randint(int(minN), int(maxN))
                print("玩家 {} 在 {} {} 之間，輸入了數字 : {}".format(identity_id, minN, maxN, randNum))
                passInput_element.send_keys(randNum)
                driver.find_element_by_xpath("//button[@id='submitBtn']").click()
                time.sleep(5)
                errRound = 0
                GUESS_NUM = randNum
        except:
            time.sleep(5)
            errRound += 1
            if errRound == 4:
                c = threading.Thread(target = parse_webSocket_log, args = (driver,'client {}'.format(identity_id)))
                c.start()
            elif errRound == 6:
                error_time = time.strftime("%m%d%H%M%S", time.localtime(time.time()))
                driver.get_screenshot_as_file('user_round_debug{}.png'.format(error_time))
                print('user_round_debug{}.png'.format(error_time))
                print('Error : 使用者 {} 看見白畫面超過 20 回合等待，先結束遊戲等待重開'.format(identity_id))
                ERROR_FOUND = True

def broadcaster_open_ZegoRoom_UserPlayIn(prefix, header, title, description, track_ids:dict):
    room_id, livemaster_id, sock, sip, sport = api.open_enter_ZegoRoom(prefix, header, title, description)
    ping_interval(sock, role = livemaster_id, seconds=60)
    guest_list = [guest_id for guest_id in track_ids ]
    pprint(guest_list)
    print('這是房間 : ' + str(room_id) + '，等等會有 : ' + str(len(guest_list)) + ' 位使用者進入')
    # game_url = api.get_game_url(1, livemaster_id, livemaster_id, room_id, 'babyDoll')
    game_url = api.get_v2game_url(1, header['X-Auth-Token'], header['X-Auth-Nonce'], room_id)
    start_time = time.time()
    global HOST_OPEN_GAME, ANSWER, RANGE, EXE_TIME, GUEST_ENTER_ROOM_COUNT, GAME_ROUND, END_GAME, COST_FEE, PLAYER, GUESS_NUM, GAME_OVER, GUEST_JOIN_GAME, ERROR_FOUND, REOPEN_ROOM
    try:
        guest_enter_room = True
        wait_user_round = 0
        msg_untreated = ''
        while True:
            msg_part = sock.recv(8192).decode('unicode_escape', errors='ignore')
            msg_all = msg_untreated + msg_part
            msg_list = msg_all.split('\n')
            msg_last = msg_list[-1]
            if msg_last[-2:-1] != '\n':
                msg_untreated = msg_list.pop()
            for msg in msg_list:
                if len(msg) >0 :
                    check1 = json.loads(msg)
                    print('直播主 sock Event : ')
                    if  check1['event'] == 'ROOM_JOIN':
                        try:
                            print(check1['data']['content'])
                        except:
                            pass
                        GUEST_ENTER_ROOM_COUNT += 1
                        if GUEST_ENTER_ROOM_COUNT == PLAYER :
                            HOST_OPEN_GAME = True
                    elif check1['event'] == 'ROOM_LEAVE':
                        GUEST_ENTER_ROOM_COUNT -= 1
                        print(check1['data']['content'])
                    elif check1['event'] == 'GAME_MESSAGE':
                        GUESS_NUM = check1['data']['answer']
                        print(check1['data'])
                    elif check1['event'] == 'GAME_OVER':
                        GAME_OVER = True
                        print(check1)
                    elif check1['event'] == 'GAME_STARTED':
                        print(check1)
                        # GUEST_JOIN_GAME = True
                    else:
                        print(check1)
            #Game V2
            if  GUESS_NUM == ANSWER:
                time.sleep(10)
                GAME_OVER = True
                GUESS_NUM = 0

            if guest_enter_room :
                threads = []
                for uid in track_ids:
                    user_header = track_ids[uid]
                    client = threading.Thread(target = user_joinRoom_playGame, args = (sip, sport, user_header, room_id, livemaster_id, uid, EXE_TIME))
                    threads.append(client)
                    client.setDaemon(True)
                    client.start()
                guest_enter_room = False

            #當人員湊齊了，就開始遊戲
            if HOST_OPEN_GAME :
                print("-----------------------------------------")
                print("直播主開始第 {} 回遊戲".format(GAME_ROUND))
                time.sleep(5)
                gameRoom = threading.Thread(target = start_game, args = (game_url, PLAYER, COST_FEE, RANGE, ANSWER))
                gameRoom.setDaemon(True)
                gameRoom.start()
                HOST_OPEN_GAME = False

            # time.sleep(20)
            # chatlib.keep_ping(sock)

            #結束遊戲的條件
            end_time = time.time()
            if (end_time - start_time) > EXE_TIME or GAME_ROUND >= LIMIT_ROUND:
                print("總共運行了: {} 秒".format(int(end_time - start_time)))
                END_GAME = True
                for client in threads:
                    client.join()

# ///////這是為了遊戲完成後，讓一個人進房間的 ROOM_IN 事件
                time.sleep(200)
                user_header =  {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': 'guest1004', 'X-Auth-Nonce': 'guest1004'}
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(30)
                server_address = (sip, sport)
                sock.connect(server_address)
                chatlib.chat_room_auth(sock, user_header)
                chatlib.join_room(room_id,'',sock)
                print("使用者: {} 進去房間 {} 了!".format('e9669001-8759-4785-b446-1e6e26158235', room_id))
                ping_interval(sock, role = 'e9669001-8759-4785-b446-1e6e26158235', seconds=60)


                while True:
                    msg_part = sock.recv(8192).decode('unicode_escape', errors='ignore')
                    msg_all = msg_untreated + msg_part
                    msg_list = msg_all.split('\n')
                    msg_last = msg_list[-1]
                    if msg_last[-2:-1] != '\n':
                        msg_untreated = msg_list.pop()
                    for msg in msg_list:
                        if len(msg) >0 :
                            check1 = json.loads(msg)
                            print('使用者 sock Event : ')
                            print(check1)

# ///////

                chatlib.leave_room(room_id, sock)

                if CHECK_POINT == 1:
                    print(GAME_POINTS_CHECK)
                    if all(GAME_POINTS_CHECK) == True:
                        print('檢查所有點數正確')
                    else:
                        print('結果有錯，請檢查')
                print("時間到了，直播主離開房間")
                break
            elif GUEST_ENTER_ROOM_COUNT < PLAYER:
                print('等待 :' + str(wait_user_round))
                wait_user_round += 1
                if wait_user_round >= 6:
                    print("直播主等不齊使用者加入聊天室，離開房間")
                    END_GAME = True
                    REOPEN_ROOM = True
                    break
                time.sleep(20)
            else:
                # print("CPU Usage : {percent}".format(percent = psutil.cpu_percent()))
                # print("目前運行了: {} 秒".format(int(end_time - start_time)))
                pass
    except:
        traceback.print_exc()

def user_joinRoom_playGame(sip, sport, user_header, room_id, host_id, user_id, inTime):
    try:
        time.sleep(random.uniform(1, 20))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
        server_address = (sip, sport)
        sock.connect(server_address)
        chatlib.chat_room_auth(sock, user_header)
        chatlib.join_room(room_id,'',sock)
        print("使用者: {} 進去房間 {} 了!".format(user_id, room_id))
        ping_interval(sock, role = user_id, seconds=60)
        game_url = api.get_v2game_url(2, user_header['X-Auth-Token'], user_header['X-Auth-Nonce'], room_id)
        start_time = time.time()
        global GUEST_JOIN_GAME, GAME_PLAY_LIST, GUEST_ENTER_ROOM_COUNT, END_GAME
        while True:
            if GUEST_JOIN_GAME and user_id not in GAME_PLAY_LIST:
                if CHECK_POINT == 1:
                    # api.check_Remote_Output(test_parameter['db'],'redis-cli flushdb')
                    # time.sleep(5)
                    # remainPoints, revenueSummary = api.get_my_points(test_parameter['prefix'], user_header)
                    remainPoints, revenueSummary = api.get_my_points_from_db(test_parameter['db'], user_id)
                    USER_POINTS[user_id] = (remainPoints, revenueSummary)
                    print('{identity_id} 剩餘點數:{rpts} , 業績點數:{rvpts} '.format(identity_id=user_id, rpts = remainPoints, rvpts= revenueSummary))
                joinGame = threading.Thread(target = join_game, args = (game_url, user_id, user_header))
                joinGame.setDaemon(True)
                joinGame.start()
                GAME_PLAY_LIST.append(user_id)
                if len(GAME_PLAY_LIST) == GUEST_ENTER_ROOM_COUNT:
                    GUEST_JOIN_GAME = False

            # time.sleep(60)
            # chatlib.keep_ping(sock)
            end_time = time.time()
            if (end_time - start_time) > inTime or GAME_ROUND >= LIMIT_ROUND:
                chatlib.leave_room(room_id, sock)
                print("時間到了，使用者離開房間")
                break
        return
    except Exception as e:
        print(e)
        time.sleep(5)
        traceback.print_exc()
        # print('{} 重新進入聊天室'.format(user_id))
        # return user_joinRoom_playGame(sip, sport, user_header, room_id, host_id, user_id, inTime)

def start_login_room_play(prefix, host_acc, user_loginIds: list):
    global monitor_webSocket_id, REOPEN_ROOM
    #broadcaster header
    # result = api.user_login(prefix, host_acc, '123456')
    # test_parameter['host_token'] = result['data']['token']
    # test_parameter['host_nonce'] = result['data']['nonce']
    # host_header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': test_parameter['host_token'], 'X-Auth-Nonce':test_parameter['host_nonce']}
    token = host_acc
    nonce = host_acc
    host_header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive', 'X-Auth-Token': token, 'X-Auth-Nonce':nonce}
    #user header
    user_header_dict = api.get_multiUsers_token_nonce(test_parameter['prefix'], backend_header, user_loginIds)
    #直播主開播，並讓使用者進入
    gameRoomTitle = host_acc + ' 小遊戲壓測房'
    # time.sleep(random.randint(1, 30))
    monitor_webSocket_id = list(user_header_dict.keys())[0]
    broadcaster_open_ZegoRoom_UserPlayIn(test_parameter['prefix'], host_header, gameRoomTitle, 'Shock 遊戲壓測試房間', user_header_dict)
    if REOPEN_ROOM == True:
        REOPEN_ROOM == False
        time.sleep(10)
        print('重開房間一次')
        broadcaster_open_ZegoRoom_UserPlayIn(test_parameter['prefix'], host_header, gameRoomTitle, 'Shock 遊戲壓測試房間', user_header_dict)

if __name__ == '__main__':

    for hostLoginID in masterLoginIds:
        if hostLoginID not in config.options('Host And Clent'):
            sys.exit("請輸入符合 ini 條件的 Master LoginId")

    if len(masterLoginIds) == 1: #參數只有一個的時候
        hostLoginID = masterLoginIds[0]
        clentLoginID_str = config.get('Host And Clent', hostLoginID)
        clentLoginID_list = clentLoginID_str.split(', ')[0:PLAYER]
        # clentLoginID_list = [ x.strip() for x in clentLoginID_list ]
        print("直播主 {} 與 {} 位使用者，準備開房間，play excited game".format(hostLoginID, len(clentLoginID_list)))
        start_login_room_play(prefix = test_parameter['prefix'], host_acc = hostLoginID, user_loginIds = clentLoginID_list)
        print('一共玩了 {} 回合'.format( GAME_ROUND + 1 ))
        print('OK {}'.format( GAME_ROUND + 1 ))
    else:
        #參數有兩個以上的時候，啟動 multi-processing or multi-thread，一組玩家分配一個cpu，這個目前有問題，因為 global variable 被互相影響，要改用 dict
        with multiprocessing.Pool(processes = len(masterLoginIds) ) as pool:
            for hostLoginID in masterLoginIds:
                clentLoginID_str = config.get('Host And Clent', hostLoginID)
                clentLoginID_list = clentLoginID_str.split(', ')[0:PLAYER]
                print("直播主 {} 與 {} 位使用者，準備開房間，play excited game".format(hostLoginID, len(clentLoginID_list)))
                result = pool.apply_async(start_login_room_play, (test_parameter['prefix'], hostLoginID, clentLoginID_list))
            pool.close()
            pool.join()
            print('一共玩了 {} 回合'.format(GAME_ROUND))
            print('OK')