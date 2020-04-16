import hashlib
import datetime
#https://www.ace.io/polarisex/open/v1
POST /coin/customerAccount
produ_site = 'www.ace.io'
stage_site = 'stageadmin.ace.io'
https://stageadmin.ace.io/coin/customerAccount



ace_sign = 'ACE_SIGN'
timestamp = str(int(datetime.datetime.now().timestamp()))
phone_num = '886937855506'

data = ace_sign + timestamp + phone_num
print(data)
md5 = hashlib.md5()
md5.update(data.encode("utf-8"))
signKey = md5.hexdigest()
print(signKey)

