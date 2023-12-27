import pymysql
import os
import time
import sshtunnel
from redis import Redis
from sshtunnel import SSHTunnelForwarder, create_logger
from pprint import pprint
from pathlib import Path

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

def ssh_tunnel_server(hostAddr, user = 'shocklee'):
    ssh_host = hostAddr #'35.201.246.119'            #SSH服务器地址
    ssh_port = 22                  #SSH端口
    keyfile = str(Path.home()) + '/.ssh/id_rsa'
    if not Path(keyfile).is_file(): print("rsa 檔案不存在")
    ssh_user = user
    redis_host = '127.0.0.1'          #数据库地址
    redis_port = 6379                 #数据库端口
    server =  SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_pkey=keyfile,
            ssh_username=ssh_user,
            remote_bind_address=(redis_host, redis_port),
    )
    return server

def dbQuery(hostAddr, sqlStr, user = 'lisa'):
    ssh_host = hostAddr #'35.201.246.119'            #SSH服务器地址
    ssh_port = 22                  #SSH端口
    keyfile = str(Path.home()) + '/.ssh/id_rsa'
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

def redisQueryKeys(hostAddr, db, keyPattern, user = 'lisa')->str:
    ssh_host = hostAddr #'35.201.246.119'            #SSH服务器地址
    ssh_port = 22                  #SSH端口
    keyfile = str(Path.home()) + '/.ssh/id_rsa'
    if not Path(keyfile).is_file(): print("rsa 檔案不存在")
    ssh_user = user
    redis_host = '127.0.0.1'          #数据库地址
    redis_port = 6379                 #数据库端口
    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_pkey=keyfile,
            ssh_username=ssh_user,
            remote_bind_address=(redis_host, redis_port),
    ) as server:
        redis = Redis(host=redis_host, port=server.local_bind_port, db=db, decode_responses=True)
        try:
        #   value = redis.get(key)
            result = []
            for key in redis.scan_iter(keyPattern):
                result.append(key)
        except Exception as err:
            print( f"Error {err} from redis")
        finally:
            del redis
        return result


class SshMySQL:

    def __init__(self, ssh_host, ssh_user, ):
        self.ssh_host = ssh_host
        self.ssh_port = 22
        self.ssh_user = ssh_user
        self.key = str(Path.home()) + '/.ssh/id_rsa'
        self.db_host = '127.0.0.1'
        self.db_port = 3306
        self.db_user = 'root'
        self.db_pass = 'mysql'
        self.db_name = 'live_casting'
        self.server = self._create_ssh()
        self.server.start()
        self.mysql_local_bind_port = self.server.local_bind_port
        self.db = self._mysqConn()

    def _create_ssh(self):
        server = SSHTunnelForwarder(
                (self.ssh_host, self.ssh_port),
                ssh_pkey=self.key,
                ssh_username=self.ssh_user,
                remote_bind_address=(self.db_host, self.db_port))
        server
        return server

    def _mysqConn(self):
        db = pymysql.connect(
        host=self.db_host,
        port=self.mysql_local_bind_port,
        user=self.db_user ,
        passwd=self.db_pass,
        db=self.db_name,
        charset="utf8")
        return db

    def query(self, sqlStr):
        # db = self._mysqConn()
        db = self.db
        cursor = db.cursor()
        collect = []
        try:
            #print(sqlStr)
            cursor.execute(sqlStr)
            data = cursor.fetchall()
            for result in data:
                collect.append(result)
            #print(collect)
        except Exception as err:
            print("Error %s from exceute sql: %s" % (err, sqlStr))
        finally:
            cursor.close()
            # db.close()
        return collect

    def execLists(self, sqlList):
        # db = self._mysqConn()
        db = self.db
        cursor = db.cursor()
        try:
            for i in sqlList:
                #print(i)
                cursor.execute(i)
            db.commit()
        except Exception as err:
            print("Error %s from exceute sql: %s" % (err, i))
            db.rollback()
        finally:
            cursor.close()
            # db.close()
        return

    def close(self):
        self.db.close()
        self.server.stop()


if __name__ == '__main__':

    # usage
    # db = SshMySQL(34.81.211.190, 'shocklee')
    # db.query(single_query)
    # db.execLists(exeList)
    # db.close()

    single_query = "SELECT max(id) from live_room"
    exeList = []
    exeList.append("insert into `live_room` (`create_at`, `end_at`, `like_count`, `live_master_id`, `rtmp_url`, `status`, `title`, `total_count`, `current_count`, `total_users`, `chat_server_id`, `type`, `socket_type`) values ('2017-12-13 03:42:14','2017-12-13 03:43:00',0,'live_master_id5','rtmp://202.39.43.80/live_angel01/livetream01',0,'test live',1,0,0,NULL,'cht', 'tcp')")
    exeList.append("insert into `live_room` (`create_at`, `end_at`, `like_count`, `live_master_id`, `rtmp_url`, `status`, `title`, `total_count`, `current_count`, `total_users`, `chat_server_id`, `type`, `socket_type`) values ('2017-12-13 03:42:14','2017-12-13 03:43:00',0,'live_master_id6','rtmp://202.39.43.80/live_angel01/livetream01',0,'test live',1,0,0,NULL,'cht', 'tcp')")
    db = SshMySQL('34.81.211.190', 'shocklee')
    [(live_room_id,)] = db.query(single_query)
    # db.execLists(exeList)
    # result = db.query("SELECT id, live_master_id FROM live_room WHERE title = 'test live'")
    db.close()
    print('[query single]')
    print(live_room_id)
    # print('[exeute list]')
    # for live_room_id in result:
    #     print(live_room_id)


    # redisResult = redisQueryKeys('34.81.211.190', 0, 'tlt-*myInfo*', 'shocklee')
    # print(redisResult)
