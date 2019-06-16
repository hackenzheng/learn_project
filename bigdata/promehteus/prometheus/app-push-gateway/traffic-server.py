import logging
import time,datetime
import base64,json
import prometheus_client
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from apscheduler.schedulers.blocking import BlockingScheduler
from my_hbase import Hbase
THRIFT_SERVER_IP = '127.0.0.1'
THRIFT_SERVER_PORT = 90
GATEWAY_URL = ''


class Promethus():

    def create_screen(self,promethus_url,job_name = 'response_num',metric_name='traffic1'):
        self.job = job_name
        self.promethus_url = promethus_url
        self.registry = CollectorRegistry()   # 存放所有Metrics的容器，以Name-Metric（Key-Value）形式维护其中的Metric对象。
        self.face_total = Gauge(metric_name, 'Total response cout of diff age and gender', ['instance','deviceid','age','gender','emotions'])
        self.registry.register(self.face_total)

    def create_device(self,promethus_url,job_name = 'response_num',metric_name='traffic2'):
        self.job = job_name
        self.promethus_url = promethus_url
        self.registry = CollectorRegistry()
        self.face_total = Gauge(metric_name, 'Total response cout of diff age and gender', ['instance','deviceid','age','gender'])
        self.registry.register(self.face_total)

    def push_prometheus(self):
        try:
            prometheus_client.push_to_gateway(self.promethus_url, job=self.job, registry=self.registry, timeout=3)
            # 将所有的error码的统计结果清空
            for label_text in self.face_total._metrics:
                self.face_total._metrics[label_text].set(0)
            # 卸载所有搜集器
            # for register in list(self.registry._collector_to_names):
            #     self.registry.unregister(register)

        except Exception as e:
            logging.error('push_to_gateway error %s' %e)


hbase_ip= THRIFT_SERVER_IP
hbase_port = THRIFT_SERVER_PORT
promethus_device= Promethus()
promethus_screen= Promethus()
promethus_screen.create_screen(promethus_url=GATEWAY_URL, job_name='traffic',metric_name='traffic1')   # GATEWAY_URL   'http://39.108.28.63:9091'
promethus_device.create_device(promethus_url=GATEWAY_URL, job_name='traffic',metric_name='traffic2')
distance_second=30

devicelist=[1,2,7,8,9,10,11,12,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]


def device_hbase():
    print(datetime.datetime.now())
    for deviceid in devicelist:
        logging.info('date now is %s' % (datetime.datetime.now()))
        startrow = str('camera_' + str(deviceid) + '_' + str(int((time.time() - distance_second+0.01) * 1000000)))  # +0.01是为了避免收尾行重复取值
        endrow = str('camera_' + str(deviceid) + '_' + str(int(time.time()* 1000000)))
        conn = Hbase(hbase_ip, port=hbase_port)
        nu_generator = conn.table("device").scan(row_start=startrow,row_stop =endrow )  # 返回一个迭代器
        num = 0

        # 循环:
        while True:
            try:
                # 获得下一个值:
                row = next(nu_generator)
                time_row_key = str(row[0], encoding='utf-8')
                dict_data = row[1]  # 所有的属性值
                gender = str(dict_data[b'image_info:gender'], encoding='utf-8')
                age = str(dict_data[b'image_info:age'], encoding='utf-8')
                num += 1
                # print(gender,age,deviceid,num)

                promethus_device.face_total.labels('yinli', str(deviceid), str(age), gender).inc(1)

            except StopIteration:
                # 遇到StopIteration就退出循环
                logging.info('data finish')
                break
        # 推送数据
        logging.info('deviceid is %s , face num is %s'%(str(deviceid),str(num)))
        promethus_device.push_prometheus()
        logging.info('push device data success %s' % datetime.datetime.now())
        conn.close()


def screen_hbase():
    logging.info('date now is %s' %(datetime.datetime.now()))
    startrow = str(int((time.time()-distance_second+0.01)*10000))
    endrow = str(int(time.time() * 10000))
    conn = Hbase(hbase_ip, port=hbase_port)
    nu_generator = conn.table("face_detect").scan(row_start=startrow,row_stop =endrow)  # 返回一个迭代器
    face_byte = bytes('faces:face', encoding='utf-8')
    device_byte=bytes('device:device_id', encoding='utf-8')
    while True:
        try:
            # 获得下一个值:
            row = next(nu_generator)
            time_row_key = str(row[0], encoding='utf-8')
            dict_data = row[1]  # 所有的属性值
            faces = json.loads(str(dict_data[face_byte], encoding='utf-8'))  # list
            deviceid = str(dict_data[device_byte], encoding='utf-8')  # list
            for face in faces:
                age = face['age']
                box = face['box']  # 是个4维的列表
                gender = face['gender']  # 是个4维的列表
                emotions=0
                if(face['emotions'] and len(face['emotions'])>0):
                    emotions = face['emotions'][0]['value']
                promethus_screen.face_total.labels('yinli', str(deviceid), str(age),gender, str(emotions)).inc(1)
        except StopIteration:
            # 遇到StopIteration就退出循环
            logging.info('data finish')
            break

    # 推送数据
    promethus_screen.push_prometheus()
    print('push screen data success')
    conn.close()


if __name__ == '__main__':
    logging.info('start to read hbase and push')
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(func=screen_hbase, trigger='interval', seconds = distance_second)
    scheduler.add_job(func=device_hbase, trigger='interval', seconds=distance_second)
    scheduler.start()

