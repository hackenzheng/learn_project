from py_orm_mysql import DayResult, DBSession, batch_insert, query, engine, Base
from py_mongo import MongoDB
import time
import random
import json
import uuid
import sys

lable = ['car', 'money', 'food', 'book', 'movie', 'cake', 'mall']


session = DBSession()
Base.metadata.create_all(engine)


def query_test():
    # pgsql在无索引查询的时候cpu会飙升，3个pg进程，每个会达到100%
    total_time = 0
    num = 10
    max = 0
    min = 1000
    for item in range(num):
        filter1 = {
            'datestr': '2019{:02d}{:02d}'.format(6, random.randint(1, 30)),
            'age': random.randint(0, 99),
        }
        s_time = time.time()
        print(json.dumps(filter1))
        flag, data = query(session, DayResult, filter1)
        t_elapse = time.time() - s_time
        max = max if max > t_elapse else t_elapse
        min = min if min < t_elapse else t_elapse
        total_time += t_elapse
    print('min query latency time is %s' % (min))
    print('max query latency time is %s' % (max))
    print('average query latency time is %s' % (total_time/num))

    return total_time


def mongo_query_test():
    # 1亿条数据，只要一查询内存占用就会升到46%
    # mongodb插入速度快很多
    mongo_obj = MongoDB()
    table_name = 'day_result'
    total_time = 0
    num = 20
    max = 0
    min = 1000
    tmp = {
        'skip': 10000,
        'limit': 100,
    }
    print('with skip and limit args')
    for item in range(num):
        filter1 = {
            'datestr': '2019{:02d}{:02d}'.format(6, random.randint(1, 30)),
            'age': random.randint(10, 80),
        }


        s_time = time.time()
        print(json.dumps(filter1))
        data = mongo_obj.find_many(table_name, filter1, **tmp)
        if data == False:
            print('query failed')
            sys.exit(1)
        t_elapse = time.time() - s_time
        max = max if max > t_elapse else t_elapse
        min = min if min < t_elapse else t_elapse
        total_time += t_elapse
    print('min query latency time is %s' % (min))
    print('max query latency time is %s' % (max))
    print('average query latency time is %s' % (total_time/num))

    return total_time

if __name__ == '__main__':

    # 读数据
    print('start query test')
    time_elapse = query_test()
    # time_elapse = mongo_query_test()
    print('data query elapse is %s' % ( time_elapse))
