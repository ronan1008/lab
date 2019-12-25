def demo1():
    return int(input("input a integer number :　"))


def demo2():
    return demo1()


try:
    print(demo2())
except Exception as result:
    print("未知錯誤 %s" % result) 





