import threading
import time
from pprint import pprint

def do1():
    print('2222..first day do...')
    time.sleep(5)
    print('2222..second day do...')


def do2():
    print('1111..fuck you')
    time.sleep(10)
    print('1111..ending fuck')


def main():
    # 創建 thread 對象
    t1 = threading.Thread(target=do1)
    t2 = threading.Thread(target=do2)
    # thread.start 之後才開始創建 線程
    t2.start()
    t1.start()
    while True:
        if len(threading.enumerate()) == 1:
            print('Only Main Thread In Process')
            break
        else:
            for t in threading.enumerate():
                print(t)
        time.sleep(3)




if __name__ == "__main__" :
    main()
