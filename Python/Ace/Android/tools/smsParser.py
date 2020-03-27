from pyquery import PyQuery as pq
import requests
import pprint
from IPython.core.display import display, HTML
headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
r = requests.get('https://smsreceivefree.com/info/18192724632/',headers=headers)
print(r.status_code)
doc = pq(r.text)
td = doc("td")
smsList=[]
smsStr=''
for n , item in enumerate(td.items()):
    newStr = item.text().replace(',', '')
    #newStr = item.text()
    if n % 3 != 2:
        smsStr += newStr+','
    else:
        smsStr += newStr
        smsList.append(smsStr)
        smsStr=''
for i in smsList:
    print(i+'\n')
#pprint.pprint(smsList)
