import threading
END_GAME = False
COUNT = 0

def ping_every_seconds(sock, seconds=60):
    global COUNT, END_GAME
    print(COUNT, END_GAME)

    if COUNT >= 2:
        END_GAME = True
        print('in')

    if not END_GAME:
        threading.Timer(seconds, ping_every_seconds, (sock, seconds)).start()
        print("ping alive")
        COUNT += 1

sock = ''
ping_every_seconds(sock,30)