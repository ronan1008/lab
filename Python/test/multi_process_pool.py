import multiprocessing
import time
import requests
import json

data = {
        'a': 123,
        'b': 456
}
def post_api(seqNum, data):
    print("process: {} start".format(seqNum))

    url = "http://localhost:8000"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    time.sleep(1)
    if response.status_code == 200 :
        print("process: {} PASS".format(seqNum))
    else:
        print("process: {} FAIL".format(seqNum))
 
if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = 3)
    # item_list = ['processes1' ,'processes2' ,'processes3' ,'processes4' ,'processes5' ,]
    # count = len(item_list)
    for item in range(30):
        res = pool.apply_async(post_api, (item,data))
        #print(res.get())    
    pool.close()
    pool.join()
    print('Ending....')
