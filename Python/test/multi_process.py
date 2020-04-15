from multiprocessing import Process
from os import getpid
from random import randint
from time import time, sleep

def download_task(filename):
    print('啟動下載行程，行程號[ %d ].' % getpid())
    print('開始下載 %s...' % filename)
    time_to_download = randint(5, 10)
    sleep(time_to_download)
    print('%s 下載完成! 耗費了 %d 秒' % (filename, time_to_download))

def main():
    start = time()
    # 利用 Process 類別創建了行程物件
    # 透過 target 參數傳入一個函數來表示進程啟動後要執行的程式碼
    # 後面的 args 代表傳遞給函數的參數
    # Process 物件的 start 方法 (method) 用來啟動行程 (process)
    # 而 join 方法 (method) 表示等待行程 (process) 執行結束。
    p1 = Process (target = download_task, args = ('Python.pdf', ))

    p1.start()
    p2 = Process (target = download_task, args = ('Hot.avi', ))
    p2.start()
    p1.join()
    p2.join()
    # procs = 5
    # jobs = []
    # for i in range(0, 15):

    #     process =Process (target = download_task, args = ('Python.pdf', ))
    #     jobs.append(process)

    # for j in jobs:
    #     j.start()
    # for i in jobs:
    #     j.join()
    end = time()
    print('總共耗費了 %.2f 秒.' % (end - start))

if __name__ == '__main__':
    main()