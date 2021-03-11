# encoding: utf-8
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import requests
import os
import time


def send_to_slack(msg, folder, rid):
    filename = folder + str(rid) + '.err'
    writetofile = False
    print(msg)
    if os.path.isfile(filename):
        writetofile = True
    else:
        #s_url = 'https://hooks.slack.com/services/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' #test
        s_url = 'https://hooks.slack.com/services/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' #lisa
        dict_headers = {'Content-type': 'application/json'}
        dict_payload = {'text': msg, 'username': 'QABugReport', 'icon_emoji': ':bug:'}
        json_payload = json.dumps(dict_payload)
        #res = requests.post(s_url, data=json_payload, headers=dict_headers)
        if res.status_code == 200:
            writetofile = True
    if writetofile:
        fp = open(filename, 'a+')
        fp.write(msg + '\n')
        fp.close()
    return


def crate_form_data(form_info):
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    fr = open(form_info[2], 'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (form_info[0], form_info[1]))
    data.append('Content-Type: %s\r\n' % form_info[3])
    data.append(fr.read())
    data.append('--%s--\r\n' % boundary)
    print(data)
    body = ('\r\n'.join('%s' % str1 for str1 in data))
    print(body)
    fr.close()
    return(body, boundary)


