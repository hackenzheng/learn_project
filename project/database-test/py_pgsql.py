# -*- coding: utf-8 -*-

import psycopg2
import logging
import datetime
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

host = '192.168.12.189'
port = 30333
database = 'fl'
username = 'postgres'
password = 'postgres'
cursor = None
try:
    conn = psycopg2.connect(database=database, user=username,
                            password=password, host=host, port=port)
    cursor = conn.cursor()
except:
    logging.error("Database %s connection failed" % database)
    sys.exit(1)

if cursor:

    try:
        created_time = datetime.datetime.utcnow()
        cursor.execute("insert into public.data_set_model(name, owner,created_at) values('test','zhg', '{}')".format(created_time))
        conn.commit()
        # cursor.execute("insert into public.data_set_model(name, owner, framework, path) values('train','zhg','mxnet','/datakubeflow/cifar10/data/train.rec')")
        # cursor.execute("insert into public.data_set_model(name, owner, framework, path) values('test','zhg','mxnet','/datakubeflow/cifar10/data/test.rec')")
        # conn.commit()
        #
        # cursor.execute("insert into public.model_model(name, owner, format, framework, path) values('test','zhg','python', 'mxnet','/datakubeflow/cifar10/resnet.py')")
        # conn.commit()
        conn.close()
        logging.info('insert succeed')
    except Exception as e:
        logging.error(e)
        logging.error("Insert data failed")
        import traceback
        traceback.print_exc()
else:
    logging.info("Cursor not initialized")

