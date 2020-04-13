import requests
import json

data = {
    'a': 123,
    'b': 456
}
url = ""
headers = {'Content-Type': 'application/json'}
response = requests.post(url, headers=headers, data=json.dumps(data))
