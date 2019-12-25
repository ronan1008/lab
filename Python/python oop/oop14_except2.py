
try:
    num = int(input("input a integer number: "))

    result  = 8 / num 

    print(result)
except ValueError:
    print("請輸入正確的整數")
except Exception as result:
    print("Unknow Error: %s " % result)

else:
    print("嘗試success")

finally:
    print("無論是否出現錯誤都會執行")

print("--" * 25)