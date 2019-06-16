from pyhive import presto
import time
import random
import uuid


fat = 1  # 10000
step_num = [100*fat, 500*fat, 1000*fat, 2000*fat, 5000*fat, 10000*fat]
lable = ['car', 'money', 'food', 'book', 'movie', 'cake', 'mall']

HOST = '192.168.11.127'
PORT = 30890

# CREATE TABLE if not exists day_result(id INT PRIMARY KEY AUTO_INCREMENT, datestr STRING, region_id INT, profile_id STRING, user_capture_days INT, age INT, gender STRING, lable ARRAY<STRING>, vip INT);


def create_talbe():

    # 可以执行的 CREATE TABLE if not exists day_result(id INT, datestr STRING, region_id INT, profile_id STRING, user_capture_days INT, age INT, gender STRING, lable ARRAY<STRING>, vip INT);
    # CREATE TABLE if not exists day_result(datestr STRING, region_id INT, profile_id STRING, user_capture_days INT, age INT, gender STRING, lable ARRAY<STRING>, vip INT);
    sql_str = 'CREATE TABLE if not exists dayresult(id INT PRIMARY KEY AUTO_INCREMENT, datestr STRING, ' \
              'region_id INT, profile_id STRING, user_capture_days INT, age INT, gender STRING, lable ARRAY<STRING>, vip INT);'

    # sql_str = 'create table user_product(id INTEGER PRIMARY KEY AUTO_INCREMENT, userid INTEGER not null, productid INTEGER not null, type varchar(64) not null);'
    conn = presto.Connection(host=HOST, port=PORT)
    cursor = conn.cursor()
    ret = cursor.execute(sql_str)
    print(ret)
    ret = cursor.fetchall()
    print(ret)
    cursor.close()
    conn.close()



class Hive(object):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, host=HOST, port=PORT):
        self.conn = presto.Connection(host=host, port=port)
        self.cursor = self.conn.cursor()

    def hive_query(self, sql_str):
        if not self.cursor:
            self.connect()

        self.cursor.execute(sql_str)
        result = self.cursor.fetchall()
        # print(result)
        return result

    def hive_insert(self, sql_str):

        if not self.cursor:
            self.connect()

        self.cursor.execute(sql_str)
        result = self.cursor.fetchall()
        # print(result)

hive_obj = Hive()

def insert_test(start, end, batch_size=1):
    count = 0
    tmp = []
    total_time = 0
    for i in range(start, end):
        count += 1
        datestr = '201906{:02d}'.format(random.randint(1, 30))
        data = {
            'datestr': datestr,
            'region_id': random.randint(1,100),
            'profile_id': uuid.uuid1(),
            'user_capture_days': random.randint(1,50),
            'age': random.randint(0,90),
            'gender': random.choice(['male', 'female']),
            'lable': random.sample(lable, k=random.randint(1, 5)),
            'vip': random.randint(0, 1)
        }
        tmp.append(data)
        if count % batch_size == 0:
            s_time = time.time()
            insert_str = "insert into day_result (datestr, region_id, profile_id, user_capture_days, age, gender, vip) " \
                         "values ('{datestr}',{region_id},'{profile_id}',{user_capture_days},{age},'{gender}',{vip})".format(
                **data)
            # print(insert_str)
            hive_obj.hive_insert(insert_str)
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
            'age': random.randint(0,90),
        }
        s_time = time.time()

        query_str = "select * from day_result where datestr='{datestr}' and age={age}".format(**filter1)
        hive_obj.hive_query(query_str)
        t_elapse = time.time() - s_time
        total_time += t_elapse
    print('average query latency time is %s' % (total_time/num))

    return total_time




if __name__ == '__main__':

    last_position = 0
    # create_talbe()
    for current_position in step_num:
        time_elapse = insert_test(last_position, current_position)
        print('data insert from %s to %s time elapse is %s' % (last_position, current_position, time_elapse))

        # 读数据
        # print('start query test')
        time_elapse = query_test()
        print('data query when num from %s to %s time elapse is %s' % (last_position, current_position, time_elapse))
        print('\n')
        last_position = current_position


    # data = {
    #     'datestr': '20190606',
    #     'region_id': 1,
    #     'profile_id': 'dafdagjoasjdfald',
    #     'user_capture_days': 1,
    #     'age': 10,
    #     'gender': 'male',
    #     'lable': ['car', 'money'],
    #     'vip': 0
    # }
    # insert_str = "insert into day_result (datestr, region_id, profile_id, user_capture_days, age, gender, lable, vip) " \
    #              "values ({datestr},{region_id},{profile_id},{user_capture_days},{age},{gender},{lable},{vip})".format(**data)
    # print(insert_str)