# 連線到多台主機，把所有的 log 取回，只抓取 明確有 error 的 log
import json, sys, os
from configparser import ConfigParser
import paramiko
from pathlib import Path
from pprint import pprint

def exe_remote_cmd(hostAddr, cmd, keyfile = None):
    keyfile = str(Path.home()) + '/.ssh/id_rsa' #SSH密钥
    if not Path(keyfile).is_file(): print("rsa 檔案不存在")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostAddr, username='shocklee', key_filename=keyfile)
    _, stdout, stderr = ssh.exec_command(cmd)
    stdout = (stdout.read().decode()).rstrip()
    stderr = (stderr.read().decode()).rstrip()
    ssh.close()
    return stdout

def scp_files_to_local(ip, user, remoteFiles, localtestDir):
    cmd = ''
    # os.system('cd  {localDir}; rm -rf {ip}'.format(localDir = localtestDir,ip= ip))
    os.system('cd  {localDir}; mkdir {ip}'.format(localDir = localtestDir ,ip= ip))
    for remoteFile in remoteFiles:
        print(remoteFile)
        cmd += "scp -r  {username}@{ip}:{File} {local}/{ip}/ \n".format(username = user, ip=ip, File=remoteFile, local=localtestDir)
        # cmd = ' scp -r  {remote} {local} ; \n'.format(remote=remote, local=localDir )
    print(cmd)
    res = os.system(cmd)
    if res == 0:
        print('{} : files transfer success!'.format(ip))
    else:
        print('{} : files transfer failed, please check!'.format(ip))

if len(sys.argv) == 1 or len(sys.argv) > 2:
    sys.exit("請輸入至少一個 Master LoginId: python3 {} [fileName]".format(sys.argv[0]))

elif len(sys.argv) == 2: #參數只有一個的時候
    if sys.argv[1] == 'remote':
        config = ConfigParser()
        config.read('gamePressure.ini')
        db = config.get('Enviroment', 'DB')
        prefix = config.get('Enviroment', 'DOMAIN')
        hostID_list = config.options('Host And Clent')
        hostName_list = config.options('ServerIP')
        serverIP_list =  [ config.get('ServerIP', hostName)  for hostName in hostName_list ]
        downloadsFiles = [
            '/home/shocklee/stress_test/GameStreeTest/gamehost*',
            '/home/shocklee/stress_test/GameStreeTest/*debug*.png',
            '/home/shocklee/stress_test/GameStreeTest/error*',
        ]
        os.system('cd /Users/shocklee/Downloads/gamePress; rm -rf *')
        GameResult = dict()

        for i, ip in enumerate(serverIP_list):
            if ip != '':
                picCount = exe_remote_cmd( ip,  "ls /home/shocklee/stress_test/GameStreeTest | grep 'debug' | wc -l")
                errorCount = exe_remote_cmd( ip,  "cat /home/shocklee/stress_test/GameStreeTest/error*| grep Traceback | wc -l")
                gameOKCount = exe_remote_cmd( ip,  "cat /home/shocklee/stress_test/GameStreeTest/gamehost* | grep 'OK' | wc -l")

                if gameOKCount != '0':
                    gameRound = exe_remote_cmd( ip,  "cat /home/shocklee/stress_test/GameStreeTest/gamehost* | grep 'OK' | awk '{ print $2 }'  | sed ':a;N;$!ba;s/\\n/ /g'")
                    GameResult[ip] = {'Round': gameRound, 'errorPic': picCount, 'Exception': errorCount}
                else:
                    gameRound = 0
                    GameResult[ip] = {'Round': gameRound, 'errorPic': picCount, 'Exception': errorCount}

                if errorCount != '0' or picCount != '0' or gameOKCount == '0' :
                    print("{} : picCount: {} errorCount: {} gameOKCount {}".format(ip ,picCount, errorCount, gameRound))
                    scp_files_to_local(ip, 'shocklee', downloadsFiles, '/Users/shocklee/Downloads/gamePress')
        print('machine number: '+ str(len(GameResult)))
        pprint(GameResult)
    else:
        fileName = sys.argv[1]
        with open(fileName, 'r') as gamelog:
            load_data = json.load(gamelog)

            print("[Result]")
            for ip, val in load_data.items():
                result = load_data[ip].get('result', '')
                print(ip, result)
            print('\n\n')
            print("[Error]")
            for ip, val in load_data.items():
                result = load_data[ip].get('error', 'No Error')
                print(ip, result)
            print('\n\n')
            print("[Log]")
            for ip, val in load_data.items():
                result = load_data[ip].get('error', None)
                exceptionError = (load_data[ip].get('log', '')).find('exceptionError') != -1
                if result or exceptionError:
                    result = load_data[ip].get('log', '')
                    print("---------------------" + ip + "------------------------")
                    print(result)




