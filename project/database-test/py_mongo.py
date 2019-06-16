#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mongodb数据库操作
"""

import pymongo
import logging as log
from bson.objectid import ObjectId

HOST = '192.168.11.127'
USER = 'admin'
PASSWD = 'admin'
DB = 'ailite'   # 要先创建库，并且user要有对该库读写的权限  db.grantRolesToUser("admin", [{role:"readWrite", db:"ailite"}])
PORT = 27017    # 表不存在会自动创建


class MongoDB:
    """mongodb数据库链接
    """
    def __init__(self):
        self.conn = None
        self.db = None
        self.coll = None
        self.connect()

    def connect(self, host=HOST, user=USER, passwd=PASSWD, database=DB, port=PORT, auth_db=DB):
        """建立链接
        """
        try:
            self.conn = pymongo.MongoClient(host, port)
            # 授权认证
            db_auth = self.conn[auth_db]
            db_auth.authenticate(user, passwd)
            self.db = self.conn[database]
            print(self.db)
            print(self.conn)
        except Exception as e:
            log.error('connect mongo database %s error! %s' % (database, e))
            return False
        return True

    def close(self):
        """关闭链接
        """
        if self.conn is not None:
            self.conn.close()

    def select_coll(self, coll):
        """设置表格
        """
        self.coll = coll

    def insert_one(self, data, coll):
        """插入单条数据，(注:官方文档不赞成直接用insert)
        """
        if not isinstance(data, dict):
            return False
        try:
            self.db[coll].insert_one(data)
        except Exception as e:
            log.error('insert data error! %s' % e)
            log.error('db:%s' % self.db)
            return False
        return True

    def insert_many(self, data, coll, ordered=True):
        """更新多条数据，(注:官方文档不赞成直接用insert)
           param: coll 集合名
                  data 插入的数据
                  ordered 插入是否有序
        表不存在会自动创建
        """
        if not isinstance(data, list):
            return False
        try:
            ret = self.db[coll].insert_many(data)
        except Exception as err:
            log.error('insert many data failed, err: %s', err)
            return False
        return True

    def find_many(self, coll, filter=None, **kwargs):
        """
        查找数据,支持参数：
            sort：格式[(key, order), (...)] key: 排序key值 order:1,升序;-1 降序
            limit: int 取n个，不填默认全部
            skip: 跳过前n条，默认0
            projection： 设置需要返回的列，默认全部
            以上为常用的参数，其他的请看help(pymongo.collection)
        """

        log.debug('filter is %s !' % filter)
        log.debug('coll is %s' % coll)
        records = []
        try:
            result = self.db[coll].find(filter, **kwargs)
            if result is False:
                return False
            if not result:
                return records
            for item in result:
                records.append(item)
            return records
        except Exception as e:
            log.error('find data error from coll %s! %s' % (coll, e))
            return False

    def find_one(self, coll, filter=None):
        """查找一条数据
        """
        try:
            return self.db[coll].find_one(filter)
        except Exception as e:
            log.error('find data error from coll %s! %s' % (coll, e))
            return False

    def update_many(self, coll, filter, update, upsert=False):
        """更新数据库操作
        """
        try:
            return self.db[coll].update_many(filter, update, upsert=upsert)
        except Exception as e:
            log.error('update coll failed! filter:%s, update:%s! %s' % (filter, update, e))
            return False

    def upsert(self, coll, filter, update):
        """upsert数据库操作
        """
        try:
            return self.db[coll].update(filter, update, upsert=True)
        except Exception as e:
            log.error('update coll failed! filter:%s, update:%s! %s' % (filter, update, e))
            return False

    def aggregate(self, coll, pipeline, **kwargs):
        """归并日志
        """
        try:
            return list(self.db[coll].aggregate(pipeline, **kwargs))
        except Exception as e:
            log.error('aggregate data error from coll %s! %s' % (coll, e))
            return False

    def reomve(self, coll):
        """清空指定collection
        """
        try:
            self.db[coll].remove()
        except Exception as e:
            log.error("Clear collection %s failed!(%s)" % coll, e)
            return False
        return True

    def add_index(self, coll, field):
        # db.getCollection('tablename').getIndexes()  获取索引信息
        # 给1亿条记录的两个字段加索引，耗时2000s左右
        self.db[coll].create_index([(field, pymongo.ASCENDING)], unique=True)