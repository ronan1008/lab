def input_password():
    pwd = input("請輸入密碼 : ")

    if len(pwd) >= 8:
        return pwd
    
    print("主動拋出異常")
    ex = Exception("密碼長度不夠")
    raise ex

try:
    print(input_password())
except Exception as result:
    print(result)

