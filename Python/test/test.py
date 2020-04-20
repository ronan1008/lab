import urllib.parse


data = {
        'uid': 123123,
        'timeStamp': 4121242300,
        'signKey': 'sfsdflksjdflksjdlf',
        'apiKey' : 'fsdfsdfs',
        'securityKey' : 'fsdfsdf',
}
data = urllib.parse.urlencode(data)

print(data)