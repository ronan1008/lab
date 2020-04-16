import requests
import json

emailOrPhone=""
authType=
source=2
codeid='0000'
pwd=""
validate=""

data = {
    'a': 123,
    'b': 456
}
url = "https://stageadmin.ace.io/user/loginGAFirst"


headers = {'Content-Type': 'application/json'}
response = requests.post(url, headers=headers, data=json.dumps(data))




loginService.getUserLoginGAFirst(
                    nECaptchaValidate,
                    captchaId,
                    codeid,
                    emailOrPhone,
                    pwd,
                    source,
                    vercode
                )