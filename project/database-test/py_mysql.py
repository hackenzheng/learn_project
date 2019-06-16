#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数据库链接操作
"""

import MySQLdb
import MySQLdb.cursors
import logging as log


class PyMysql:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self, host, user, passwd, db, port, charset="utf8"):
        """
        建立一个新连接，指定host、用户名、密码、默认数据库,端口
        """
        try:
            self.conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset,
                                        cursorclass=MySQLdb.cursors.DictCursor, )
        except Exception as e:
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
            """
            作用：使用游标（cursor）的execute 执行query
            参数：sqltext： 表示sql语句
                 args： sqltext的参数
            返回：元组（影响行数（int），游标（Cursor））
            """
            try:
                self.cur = self.conn.cursor()
                if isinstance(args, (list, tuple)) and len(args) > 0 and \
                        isinstance(args[0], (list, tuple)):
                    line = self.cur.executemany(sqltext, args)
                else:
                    line = self.cur.execute(sqltext, args)
            except Exception as e:
                log.error("mysql query error: %s", e)
                return False
            return line, self.cur

    def commit(self):
        """提交数据
        """
        self.conn.commit()

    def rollback(self):
        """数据回滚
        """
        self.conn.rollback()

    def close(self):
        """
        关闭当前连接
        """
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
