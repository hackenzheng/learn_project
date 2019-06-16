import datetime
import time
from py_hbase import PyHbase

columns=['device_info:location','device_info:version','device_info:time',
         'images_info:time','image_info:image_path','image_info:box','image_info:age','image_info:gender','image_info:additional',
         ]
families=['device_info','images_info']


if __name__=='__main__':
    dt = datetime.datetime.now()
    ss=str(int(1000000*time.time()))
    select_column=['images_info:age', 'images_info:gender', 'images_info:time']
    pyhbase=PyHbase()
    result = pyhbase.get_all_table()

    print(result)
    result = pyhbase.get_row_data('product','')

    pyhbase.delete_table('device')
    pyhbase.creat_table('device',families)
    for i in range(10):
        for j in range(10):
            tt=str(int(1000000*time.time()))
            data={
                'images_info:image_path':'/data/image/2018/06/12/0012356.jpg',
                'images_info:box':[20,45,67,234,0.7,2],
                'images_info:age':i*j,
                'images_info:gender':1,
                'images_info:time':tt
            }
            pyhbase.insert_row_data('device','camera_'+str(i)+"_"+tt,data)
    # 读取最近一个的信息
    data = pyhbase.get_row_columns_data('device','camera_9_'+tt,select_column)
    print('最近一次指定列的信息1:',data)
    # 读取最近一次的信息
    data = pyhbase.get_row_data('device', 'camera_9_'+tt)
    print('最近一次全部列的信息2:',data)
    # 读取一分钟前的摄像头最近一次数据

    data = pyhbase.get_row_data_ts('device','camera_9_'+tt,timestamp=1000*int(time.time()))
    print('指定时间戳前的最新一次数据:',data)

    # 获取最近的n次数据
    cells=pyhbase.client.getVer('device','camera_9_'+tt,'images_info:age',10)
    for cell in cells:
        print('最近的10次数据（注意默认版本数目）',cell.value, cell.timestamp)

    # 获取指定时间戳之前的n次数据
    cells=pyhbase.client.getVerTs('device','camera_9_'+tt,'images_info:age',1000*int(time.time()-60),10)
    for cell in cells:
        print('1分钟前的最新的10次数据（注意默认版本数目）',cell.value, cell.timestamp)

    # 获取指定设备的多列信息
    scannerId = pyhbase.client.scannerOpenWithPrefix('device','camera_1',select_column)
    while True:
        result = pyhbase.client.scannerGet(scannerId)
        if not result:
            break
        print('指定设备的全部信息',result)
    pyhbase.client.scannerClose(scannerId)

    # 获取指定设备的指定时间范围的多列数据
    begin_time= int(1000*time.mktime(time.strptime("2018-08-25 22:03", "%Y-%m-%d %H:%M")))
    end_time= int(1000*time.mktime(time.strptime("2018-08-26 22:03", "%Y-%m-%d %H:%M")))
    scannerId = pyhbase.client.scannerOpenWithStopTs('device', 'camera_1_'+str(begin_time),'camera_1_'+str(end_time),select_column, timestamp=1000*int(time.time()))
    while True:
        result = pyhbase.client.scannerGet(scannerId)
        if not result:
            break
        print('指定设备指定时间范围的信息',result)
    pyhbase.client.scannerClose(scannerId)

