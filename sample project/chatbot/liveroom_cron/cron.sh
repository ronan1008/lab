#!/bin/bash
PATH=/home/shocklee/.asdf/shims:/home/shocklee/.asdf/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
source /home/shocklee/env/bin/activate
TIMESTAMP=`date "+%Y%m%d%H%M%S"`
python /home/shocklee/data_test/liveroom_cron/multi_liveroom.py > "${TIMESTAMP}_ws.log" 2>&1 
