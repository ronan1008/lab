import random

def job():
    i = 0
    while i < 500:
        j = random.randint(1, 1000)
        print('取得random number: %d' %j)
        i = j
        print(i)

if __name__ == '__main__':
    job()