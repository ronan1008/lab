import requests

url = "https://stage.ace.io/polarisex/open/v1/coin/customerAccount"

payload = 'uid=437&timeStamp=1587376807000&signKey=0fbd19ed427355b5bda40145c02b80aa&apiKey=437%232020&securityKey=50caded91f924ed184ce173177294b15'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))