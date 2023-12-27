#!/usr/bin/python
# -*- coding: utf-8 -*-
from configparser import ConfigParser
from pathlib import Path
from pprint import pprint
from datetime import datetime
import threading, queue, paramiko, sys, os, time, json
from tool import api
import re
import random
import traceback
#連線到 gamePressure.ini 裡面的多台主機 ，上傳最新檔案、殺掉殭屍進程、ping主機...等等
#所有主機測試的返回結果
remote_exec_result = dict()
def exe_remote_cmd(hostAddr, cmd, keyfile = None):
    # time.sleep(random.randint(10, 50))
    keyfile = str(Path.home()) + '/.ssh/id_rsa' #SSH密钥
    if not Path(keyfile).is_file(): print("rsa 檔案不存在")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostAddr, username='shocklee', key_filename=keyfile, timeout=10)
    _, stdout, stderr = ssh.exec_command(cmd)
    stdout = (stdout.read().decode()).rstrip()
    stderr = (stderr.read().decode()).rstrip()
    ssh.close()
    global remote_exec_result
    # stdout = stdout.replace("\n","")
    last_stdout = stdout.split("\n")
    if last_stdout[-1].find("OK") != -1 and stderr == "":
        remote_exec_result[hostAddr] = {'result': last_stdout[-1], 'log':stdout}
    elif stdout.strip() =='' and stderr.strip()== '':
        remote_exec_result[hostAddr] = {'result': 'PROCESS...'}
    else:
        remote_exec_result[hostAddr] = {'result': 'FAIL', 'log': stdout, 'error': stderr  }
        print(stderr)

def scp_files(ip, user, remoteDir, localFiles):
    cmd = ''
    remote = "{username}@{ip}:{dir}".format(username = user, ip=ip, dir=remoteDir)
    for localFile in localFiles:
        cmd += ' scp -r {local} {remote} \n'.format(local=localFile, remote=remote)
    res = os.system(cmd)
    if res == 0:
        print('{} : files transfer success!'.format(ip))
    else:
        print('{} : files transfer failed, please check!'.format(ip))

def local_cmd(cmd, q):
    res = os.popen('{}'.format( cmd))
    q.put(res.read().strip())

if __name__ == '__main__':

    index = ['uploadfiles', 'clearZombie', 'test', 'all', 'ping']
    if len(sys.argv) == 1 or sys.argv[1] not in index :
        hint = '''
請輸入至少一個 參數, EX:
python3 {filename} ping
python3 {filename} uploadfiles
python3 {filename} clearZombie
python3 {filename} test
python3 {filename} all
        '''
        hint = hint.format(filename = sys.argv[0])
        sys.exit(hint)

    config = ConfigParser()
    # config.read('gamePressure.ini')
    config.read('gamePressure.ini', encoding='utf-8')
    db = config.get('Enviroment', 'DB')
    prefix = config.get('Enviroment', 'DOMAIN')
    hostID_list = config.options('Host And Clent')
    hostName_list = config.options('ServerIP')
    serverIP_list =  [ config.get('ServerIP', hostName)  for hostName in hostName_list ]
    group = int(config.get('Enviroment', 'GROUP'))

    #backend login
    result = api.user_login(prefix, 'tl-lisa', '12345678')
    backend_token, backend_nonce  = result['data']['token'], result['data']['nonce']
    print('backend_token :' + backend_token, 'backend_nonce :'+ backend_nonce)

    uploadFiles = [
        '/Users/shocklee/Documents/TrueLove/tl-QA/GameStreeTest/tool',
        '/Users/shocklee/Documents/TrueLove/tl-QA/GameStreeTest/gamePressure.py',
        '/Users/shocklee/Documents/TrueLove/tl-QA/GameStreeTest/gamePressure.ini',
        # '/Users/shocklee/Documents/TrueLove/tl-QA/GameStreeTest/chromedriver',
    ]
    q = queue.Queue()
    start_time = int(time.time())
    if  sys.argv[1] == 'ping':
        cmds = []
        for i, ip in enumerate(serverIP_list):
            if ip != '':
                cmd = "ping -c 1 -W 2 -p 22 {}".format(ip)
                # cmd = "ls -al".format(ip)
                print(ip, cmd)
                cmd_client = threading.Thread(target = local_cmd, args = (cmd, q))
                cmds.append(cmd_client)
                cmd_client.start()
                index = i
        for cmd in cmds:
            cmd.join()
        results = []
        for _ in range(index):
            result = q.get()
            if result.find('100.0% packet loss') != -1:
                resultRow = result.split('\n')
                ipObj = re.search( r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", resultRow[3])
                ip = ipObj.group(1).strip()
                results.append(ip + ':' +resultRow[4])
                print(ip + ':' + 'Failed')
                print(ip + ':' + resultRow[4])



    if  sys.argv[1] == 'uploadfiles' or sys.argv[1] == 'all':
        try:
            for i, ip in enumerate(serverIP_list):
                if ip != '':
                    scp_files(ip, 'shocklee', remoteDir='/home/shocklee/stress_test/GameStreeTest', localFiles=uploadFiles)
        except:
            print('Error : ' + ip)
            traceback.print_exc()

    if  sys.argv[1] == 'clearZombie' or sys.argv[1] == 'all':
        try:
            cmds = []
            for i, ip in enumerate(serverIP_list):
                if ip != '':
                    cmd = "cd /home/shocklee/stress_test/GameStreeTest;"
                    cmd += "rm -f error*; rm -f *.png; rm -f gamehost*; sleep 1;"
                    cmd += "rm -rf __pycache__;rm -rf GameStreeTest; rm -f conn_server.py ;rm -f __init__.py ;rm -f api.py ; rm -f chatlib.py ; rm -f id_rsa; rm -f error*; rm -f gameResult*; sleep 1;"
                    cmd += "sleep $(shuf -i 1-60 -n 1) ;"
                    cmd += "ps aux | grep '[p]ython3 -u gamePressure.py' | awk '{ print $2 }' | xargs -r kill -9 ;  sleep 1;"
                    cmd += "ps aux | grep '[c]hrome' | awk '{ print $2 }' | xargs -r kill -9; sleep 1;"
                    cmd += "ps aux | grep '[c]hromedriver' | awk '{ print $2 }' | xargs -r kill -9;  sleep 1;"
                    # cmd += "ps aux | grep '[p]ython3' | awk '{ print $2 }' | xargs -r kill -9;  sleep 1;"
                    print(ip, cmd)
                    cmd_client = threading.Thread(target = exe_remote_cmd, args = (ip, cmd, None,))
                    cmds.append(cmd_client)
                    cmd_client.start()
            for cmd in cmds:
                cmd.join()
        except:
            print('Error : ' + ip)
            traceback.print_exc()

    exe_time = time.strftime("%m%d%H%M", time.localtime(start_time))
    print('開始執行的時間 : {}'.format(exe_time))
    if  sys.argv[1] == 'test' or sys.argv[1] == 'all':
        h_beg = 0
        cmd = ''
        threads = []
        for i, ip in enumerate(serverIP_list):
            if ip != '' :
                h_end = h_beg + group
                for masterId in hostID_list[h_beg:h_end]:
                    cmd += 'cd /home/shocklee/stress_test/GameStreeTest;'
                    cmd += 'sleep $(shuf -i 1-60 -n 1) ;nohup python3 -u gamePressure.py {} -t {} -n {}> {} 2> error_{} &\n'.format(masterId, backend_token, backend_nonce, masterId + '_' + exe_time, masterId)
                h_beg = h_end
                print(ip)
                print(cmd)
                client = threading.Thread(target = exe_remote_cmd, args = (ip, cmd, None,))
                threads.append(client)
                client.start()
                cmd = ''

        for client in threads:
            client.join()
    end_time = int(time.time())
    # fileName = 'game{}.log'.format(time.strftime("%m%d%H%M", time.localtime(end_time)))
    # with open(fileName, 'w') as gamelog:
    #     gamelog.write(json.dumps(remote_exec_result, ensure_ascii=False))

    # for remote in remote_exec_result:
    #     print(remote_exec_result[remote]['result'])

    # print("一共有 {} 執行完成".format(len(remote_exec_result)))
    print("Execution Time: {}".format(time.strftime("%m-%d %H:%M:%s", time.localtime(start_time))))
    print("Total Time: {}".format(end_time - start_time))
    print('Execution Over')

#ps aux | grep [g]amePressure | grep -v [b]ash  | awk '{print $2}' | xargs -r ps -o etime= -p