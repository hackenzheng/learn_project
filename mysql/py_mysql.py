#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors
import logging as log
import traceback
import time


class PyMysql:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self, host, user, passwd, db, port, charset="utf8"):
        try:
            self.conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset,
                                        cursorclass=MySQLdb.cursors.DictCursor, )
        except Exception as e:
            traceback.print_exc()
            log.error('connect mysql database %s error! %s' % (db, e))
            return False
        return True

    def switch_cursor(self, curclass):
        if not isinstance(curclass, (MySQLdb.cursors.Cursor, MySQLdb.cursors.DictCursor,
                                     MySQLdb.cursors.SSCursor, MySQLdb.cursors.SSDictCursor)):
            log.debug('invalid cursor class： %s' % (type(curclass), ))
            return False
        self.cur = self.conn.cursor(cursorclass=curclass)
        return True

    def query(self, sql, args=None):
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(sql, args)
            result = self.cur.fetchall()
        except Exception as e:
            log.error("mysql query error: %s\n mysql:%s args: %s", e, sql, args)
            return False
        return result

    def execute(self, sqltext, args=None):
        try:
            self.cur = self.conn.cursor()
            if isinstance(args, (list, tuple)) and len(args) > 0 and \
                    isinstance(args[0], (list, tuple)):
                line = self.cur.executemany(sqltext, args)
            else:
                line = self.cur.execute(sqltext, args)
        except Exception as e:
            traceback.print_exc()
            log.error("mysql execute error: %s", e)
            return False
        return line, self.cur

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def insert_data(self, table_name, data_dict):
        data_values = "(" + "%s," * (len(data_dict)) + ")"
        data_values = data_values.replace(',)', ')')
        db_field = data_dict.keys()
        data_tuple = tuple(data_dict.values())
        db_field = str(tuple(db_field)).replace("'", '')
        sql = """ insert into %s %s values %s """ % (
            table_name, db_field, data_values)
        params = data_tuple

        self.execute(sql, params)
        self.commit()
        #self.close()


if __name__ == "__main__":
    py_sql = PyMysql()
    py_sql.connect('127.0.0.1', 'root', '123456', 'Device', 3306)
    create_table = 'create table snap_info(face_id varchar(64),age int,gender tinyint, \
                     handle_time int, vip tinyint,face_group char(64),face_info char(64),\
                    save_path char(64) not null, reg_path char(64));'
    data = {
        'face_id': 'dagadsf',
        'age': 10,
        'gender': 1,
        'face_group': 'at',
        'save_path': 'sfajo',
        'handle_time': int(time.time()),
        'face_info': 'aitest',
    }
    py_sql.insert_data('snap_info', data)
    py_sql.commit()
    print 'query result'
    print py_sql.query('select * from snap_info')
