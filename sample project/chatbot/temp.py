import paramiko
from pathlib import Path
from dbConnect import dbQuery, dbSetting,  SshMySQL


def execute_remote_command(host, cmd):
    print(f"Command: {cmd}")
    keyfile = str(Path.home()) + '/.ssh/id_rsa' #SSH密钥
    if not Path(keyfile).is_file():
        print("RSA file does not exist.")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='shocklee', key_filename=keyfile)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    try:
        result = stdout.read().decode()
    except Exception as e :
        print(e)
        result = ''
    ssh.close()
    return result

import threading
import time
def activate_chatbot_process(host, env):
    # res = execute_remote_command(host, f'cd tl-chatbot ; source ~/.zshrc; MIX_ENV={env} mix run --no-halt > chatbot.log 2>&1 &')
    background = threading.Timer(3, execute_remote_command, args=[host, f'cd tl-chatbot ; source ~/.zshrc; MIX_ENV={env} mix run --no-halt > chatbot.log 2>&1 &'])
    return background

def kill_chatbot_process(host):
    res = execute_remote_command(host, "ps aux | grep '[m]ix run --no-halt' | awk '{print $2}'")
    print(res.strip())
    pid = res.strip()
    if pid :
        execute_remote_command(host, f"kill -9 {pid}")
    else:
        print('No chatbot process found.....')

def table_referenced_list(db, tableName, sshUser, del_list:list=[], truncate_list:list=[])-> list:
    ref_sql = '''
    select table_name from information_schema.KEY_COLUMN_USAGE where table_schema = 'live_casting' and referenced_table_name = '{}';
    '''.format(tableName)
    result = dbQuery(db, ref_sql, sshUser)
    if len(result) == 0:
        truncate_list.append(tableName)
    else:
        for row in result:
            refTable = row[0]
            if refTable not in del_list:
                del_list.insert(0, refTable)
                del_list, truncate_list = table_referenced_list(db, refTable, sshUser, del_list, truncate_list)

    for i in del_list:
        if i in truncate_list:
            del_list.remove(i)

    if tableName in del_list:
        del_list.remove(tableName)
    del_list.append(tableName)
    truncate_list = list(set(truncate_list))
    return [del_list, truncate_list]

def clear_relative_table(db, table, sshUser):
    print(f"\n Starting Clean ref table by {table}")
    del_list, truncate_list = table_referenced_list(db, table, sshUser)
    livedb = SshMySQL(db, sshUser)
    del_sql = []
    for table in truncate_list:
        del_sql.append('TRUNCATE TABLE {}'.format(table))
    for table in del_list:
        del_sql.append('DELETE FROM {}'.format(table))
        del_sql.append('ALTER TABLE {} auto_increment = 1'.format(table))

    livedb.execLists(del_sql)
    livedb.close()

if __name__ == "__main__":
    host = '34.81.211.190'
    clear_relative_table(host, 'chatbot_promotion_ticket', 'shocklee')

