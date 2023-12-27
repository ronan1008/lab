import pymysql
import os
import time
import sshtunnel
from sshtunnel import SSHTunnelForwarder, create_logger
from pprint import pprint
from pathlib import Path

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 10.0

def dbQuery(hostAddr, sqlStr, user = 'lisa'):
    ssh_host = hostAddr #'35.201.246.119'            #SSH服务器地址
    ssh_port = 22                  #SSH端口
    keyfile = str(Path.home()) + '/Documents/TrueLove/tl-QA/GameStreeTest/tool/id_rsa' #SSH密钥
    if not Path(keyfile).is_file(): print("rsa 檔案不存在")
    ssh_user = user
    db_host = '127.0.0.1'          #数据库地址
    db_name = 'live_casting'       #数据库名
    db_port = 3306                 #数据库端口
    db_user = 'root'               #数据库用户名
    db_passwd = 'mysql'            #数据库密码
    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_pkey=keyfile,
            ssh_username=ssh_user,
            # local_bind_address=('127.0.0.1', 8080),
            remote_bind_address=(db_host, db_port),
            # logger=create_logger(loglevel=1),
    ) as server:
        db = pymysql.connect(
            host=db_host,
            port=server.local_bind_port,
            user=db_user,
            passwd=db_passwd,
            db=db_name,
            charset="utf8")
        cursor = db.cursor()
        collect = []
        try:
            # print(sqlStr)
            cursor.execute(sqlStr)
            data = cursor.fetchall()
            for result in data:
                collect.append(result)
            #print(collect)
        except Exception as err:
            print("Error %s from exceute sql: %s" % (err, sqlStr))
        finally:
            cursor.close()
            db.close()
        return collect

def dbSetting(hostAddr, sqlStr, user = 'lisa'):
    #print('server adder=%s'%hostAddr)
    ssh_host = hostAddr #'35.201.246.119'            #SSH服务器地址
    ssh_port = 22                  #SSH端口
    keyfile = str(Path.home()) + '/.ssh/id_rsa' #SSH密钥
    if not Path(keyfile).is_file(): print("rsa 檔案不存在")
    ssh_user = user
    db_host = '127.0.0.1'          #数据库地址
    db_name = 'live_casting'       #数据库名
    db_port = 3306                 #数据库端口
    db_user = 'root'               #数据库用户名
    db_passwd = 'mysql'            #数据库密码
    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_pkey=keyfile,
            ssh_username=ssh_user,
            remote_bind_address=(db_host, db_port)
    ) as server:
        db = pymysql.connect(
            host=db_host,
            port=server.local_bind_port,
            user=db_user,
            passwd=db_passwd,
            db=db_name,
            charset="utf8")
        cursor = db.cursor()
        try:
            for i in sqlStr:
                #print(i)
                cursor.execute(i)
            db.commit()
        except Exception as err:
            print("Error %s from exceute sql: %s" % (err, i))
            db.rollback()
        finally:
            cursor.close()
            db.close()
        return
