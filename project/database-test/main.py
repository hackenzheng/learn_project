from py_orm_mysql import DayResult, DBSession, batch_insert, query, engine, Base
import time
import random
import uuid
import json

# drop table day_result;  # 删除数据库
# \c dbname 切换数据库
# \l 列举数据库
# \dt 列举表
# \d tablename  描述表结构

fat = 10000
step_num = [1*fat, 10*fat, 100*fat, 500*fat, 1000*fat, 2000*fat, 4000*fat, 5000*fat, 8000*fat, 10000*fat]
lable = ['car', 'money', 'food', 'book', 'movie', 'cake', 'mall']


session = DBSession()
Base.metadata.create_all(engine)

def insert_test(start, end, batch_size=100):
    count = 0
    tmp = []
    total_time = 0
    for i in range(start, end):
        count += 1
        datestr = '2019{:02d}{:02d}'.format(random.randint(1, 12), random.randint(1, 30))
        data = {
            'datestr': datestr,
            'region_id': random.randint(1,100),
            'profile_id': uuid.uuid1(),
            'user_capture_days': random.randint(1,50),
            'age': random.randint(0,90),
            'gender': random.choice(['male', 'female']),
            # 'lable': random.choice(lable),
            'lable': random.sample(lable, k=random.randint(1, 5)),
            'vip': random.randint(0, 1)
        }
        tmp.append(data)
        if count % batch_size == 0:
            s_time = time.time()
            batch_insert(session, DayResult, tmp)
            e_time = time.time()
            interval = e_time - s_time
            total_time += interval
            tmp = []
    if total_time:
        print('average insert speed is %d item/s' % ((end - start)/total_time))
    return total_time


def query_test():

    total_time = 0
    num = 10
    for item in range(num):
        filter1 = {
            'datestr': '201906{:02d}'.format(random.randint(1, 30)),
            'gender': random.choice(['male', 'female']),
            'age': random.randint(0,90),
        }
        s_time = time.time()
        flag, data = query(session, DayResult, filter1)
        t_elapse = time.time() - s_time
        total_time += t_elapse
    print(json.dumps(filter1))
    print('average query latency time is %s' % (total_time/num))

    return total_time



if __name__ == '__main__':
    print('start test, time is: %s', time.time())
    last_position = 0
    for current_position in step_num:
        # print('current record num end is %s' % current_position)
        # 写数据
        # print('start insert test')
        #s_time = time.time()
        time_elapse = insert_test(last_position, current_position)
        #time_elapse = time.time() - s_time
        print('data insert from %s to %s time elapse is %s' % (last_position, current_position, time_elapse))

        # 读数据
        # print('start query test')
        time_elapse = query_test()
        print('data query when num from %s to %s time elapse is %s' % (last_position, current_position, time_elapse))
        print('\n')
        last_position = current_position
