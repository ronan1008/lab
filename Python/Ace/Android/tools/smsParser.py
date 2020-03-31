from pyquery import PyQuery as pq
import requests , pprint , re
import pprint
headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
r = requests.get('https://smsreceivefree.com/info/18192724632/',headers=headers)
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

def find_verifi_code(items):
    match = re.search(r"Verification code: (\d+)", items)
    if match :
        verificationCode = match.group(1)
        return verificationCode
    else:
        return False

def get_verification_code(pattern):
    for i in smsList:
        iList = i.split(',')
        if iList[1].find('seconds') != -1 and iList[2].find(pattern) != -1 :
            return    find_verifi_code(iList[2])
            
        elif iList[1].find('minutes') != -1 and iList[2].find(pattern) != -1 :
            return    find_verifi_code(iList[2])
          
        else:
            pass


#print(get_verification_code('[ACE]'))

#14249001XXX	20 seconds ago	[ACE]Verification code: 306692, Available for 10 minutes. Please check that you are visiting "ace.io", and do not share the code with anyone !


