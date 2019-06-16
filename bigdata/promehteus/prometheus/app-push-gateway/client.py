# coding=utf-8

import time,json
import requests
import time,datetime,random

if __name__ == "__main__":
    url = "http://127.0.0.1:8000/metrics"
    print(datetime.datetime.now())
    print('==============')
    for i in range(1):

        data = {
                'metrics':{
                    'request_total': {
                        'labels': ['method', 'client_ip'],
                        'describe': 'test',
                        'exist_not_update_type': 'clear',
                        'exist_update_type': 'add',
                        'not_exist_update_type': "update",
                        'pull_finish_deal_type': "clear",
                        'data': [
                            [['get', '192.168.11.127'], random.randint(1, 12)],
                            [['post', '192.168.11.11'], random.randint(1, 12)],
                            [['get', '192.168.11.23'], random.randint(1, 12)]
                        ]
                    }
            }

        }
        begin_time = time.time()
        r = requests.post(url, json=data)
        result = json.loads(r.text)
        print(result)
        end_time = time.time()
        print(end_time-begin_time)
    print('=============')





