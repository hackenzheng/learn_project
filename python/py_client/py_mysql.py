import pymysql
import pymysql.cursors
import logging
import traceback
import time


class PyMysql:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, host, user, passwd, db, port=3306, charset="utf8"):
        try:
            self.conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset,
                                        cursorclass=pymysql.cursors.DictCursor, )
            self.cursor = self.conn.cursor()
            logging.info('connect mysql success')
        except Exception as e:
            logging.error('connect mysql database %s error! %s' % (db, e))
            return False
        return True

    def switch_cursor(self, curclass):
        if not isinstance(curclass, (pymysql.cursors.Cursor, pymysql.cursors.DictCursor,
                                     pymysql.cursors.SSCursor, pymysql.cursors.SSDictCursor)):
            logging.debug('invalid cursor class： %s' % (type(curclass), ))
            return False
        self.cursor = self.conn.cursor(cursorclass=curclass)
        return True

    def query(self, sqlcommand, args=None):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sqlcommand, args)
            result = self.cursor.fetchall()
        except Exception as e:
            logging.error("mysql query error: %s\n mysql:%s args: %s" %(e, sqlcommand, args))
            return False
        return result

    def execute(self, sqlcommand, args=None):
        try:
            self.cursor = self.conn.cursor()
            if isinstance(args, (list, tuple)) and len(args) > 0 and \
                    isinstance(args[0], (list, tuple)):
                line = self.cursor.executemany(sqlcommand, args)
            else:
                line = self.cursor.execute(sqlcommand, args)
        except Exception as e:
            # traceback.print_exc()
            logging.error("mysql execute error: %s"% e)
            return False
        return line, self.cursor

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logging.info('close mysql success')

    def insert_data(self, table_name, data_dict):
        data_values = "(" + "%s," * (len(data_dict)) + ")"
        data_values = data_values.replace(',)', ')')
        db_field = data_dict.keys()
        data_tuple = tuple(data_dict.values())
        db_field = str(tuple(db_field)).replace("'", '')
        sql = """ insert into %s %s values %s """ % (table_name, db_field, data_values)
        params = data_tuple

        self.execute(sql, params)
        self.commit()
        #self.close()

def test():
    py_sql = PyMysql()
    py_sql.connect('127.0.0.1', 'root', '123456', 'note', 3306)
    sql = 'drop table if exists user'
    py_sql.cursor.execute(sql)
    py_sql.conn.commit()

    sql = 'drop table if exists product'
    py_sql.cursor.execute(sql)
    py_sql.conn.commit()

    sql = 'drop table if exists user_product'
    py_sql.cursor.execute(sql)
    py_sql.conn.commit()

    create_table = 'create table user(id INTEGER PRIMARY KEY AUTO_INCREMENT ,username varchar(64) not null,password varchar(64) not null, phone varchar(64));'
    py_sql.cursor.execute(create_table)
    py_sql.conn.commit()

    create_table = 'create table product(id INTEGER PRIMARY KEY AUTO_INCREMENT ,type varchar(64) not null,time varchar(64) not null, userid INTEGER,' \
                   'field varchar(64) not null,title varchar(200),content varchar(500),answer varchar(200));'
    py_sql.cursor.execute(create_table)
    py_sql.conn.commit()

    create_table = 'create table user_product(id INTEGER PRIMARY KEY AUTO_INCREMENT ,userid INTEGER not null,productid INTEGER not null, type varchar(64) not null);'
    py_sql.cursor.execute(create_table)
    py_sql.conn.commit()


if __name__ == "__main__":
    py_sql = PyMysql()
    py_sql.connect('47.106.76.200', 'root', 'introcks1234', 'intellif_face', 3306)
    # sql = 'truncate table t_face_1'   # 清空数据表
    # py_sql.execute(sql)
    # py_sql.conn.commit()
    # print('delete t_face_1')
    # py_sql.close()





