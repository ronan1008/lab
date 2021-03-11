import random
import threading
import time

import socketio


def sio_client():
    sio = socketio.Client()
    server_address = 'http://localhost:8091'
    room_ids = list(range(1, 51))

    def join_room(room_id):
        print('加入房間:' + str(room_id))
        sio.emit('join', data={'room': str(room_id)})

    def sent_to_room(num, room_id):
        if num == 0:
            msg = '哈囉,大家好'
        else:
            msg = '間隔' + str(num) + '秒再次發送詢息'
        print(msg)
        sio.emit('my_room_event', data={'data': msg, 'room': str(room_id)})

    def send_gift(room_id):
        msg = '送禮'
        sio.emit('my_room_event', data={'data': msg, 'room': str(room_id)})

    @sio.event
    def connect():
        print('connected to server')

    def my_background_task(is_stay=True, is_gift=True):
        sleep_time_1 = 0
        sleep_time = random.randint(120, 1200)
        sleep_time_1 = sleep_time_1 + sleep_time
        for i in range(sleep_time):
            if (i % 5) == 0:
                pass
            if is_stay:
                sio.sleep(1)
            else:
                break
        if is_stay:
            if is_gift:
                send_gift(room_id)
                is_gift = False
            else:
                sent_to_room(sleep_time_1, room_id)
                is_gift = True

    sio.connect(server_address)
    room_id = random.choice(room_ids)
    join_room(room_id)
    is_first_login = True
    if is_first_login:
        sent_to_room(0, room_id)
    sio.start_background_task(my_background_task)


if __name__ == '__main__':
    numList = []

    for i in range(0, 1):
        sio_client()
