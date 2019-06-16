# -*- coding: utf-8 -*-
# references:
# official site: http://flask-sqlalchemy.pocoo.org/2.3/
# http://docs.sqlalchemy.org/en/latest/orm/extensions/hybrid.html?highlight=hybrid

import datetime
import logging
from sqlalchemy import create_engine, String, Column, Integer, DateTime, JSON, ARRAY, BOOLEAN, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()   # 创建对象的基类
# 初始化数据库连接

# postgres和ailite两个库
engine = create_engine("postgresql://postgres:postgres@192.168.11.127:5432/ailite")  # postgresql/mysql
# engine = create_engine("mysql+pymysql://root:@192.168.11.127:4000/ailite")  # mysql, 需要pip install pymysql
# 创建DBsession类型
DBSession = sessionmaker(bind=engine)


class BaseModel(Base):
    """Base data model for all objects"""
    __abstract__ = True

    # define here __repr__ and json methods or any common method
    # that you need for all your models

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self.to_dict().items()
        })

    def json(self, include_cols=[], exclude_cols=[]):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d %H:%M:%S')
            for column, value in self.to_dict(include_cols, exclude_cols).items()
        }

    def to_dict(self, include_cols=[], exclude_cols=[]):
        if include_cols:
            ret = {}
            for c in self.__table__.columns:
                if c.name in include_cols:
                    ret[c.name] = getattr(self, c.name, None)
            return ret
        elif exclude_cols:
            ret = {}
            for c in self.__table__.columns:
                if c.name not in exclude_cols:
                    ret[c.name] = getattr(self, c.name, None)
            return ret
        else:
            return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


class DayResult(BaseModel):
    __tablename__ = 'day_result_index'
    tid = Column(Integer, primary_key=True, autoincrement=True)
    datestr = Column(DateTime, default=datetime.datetime.utcnow, index=True)  #
    region_id = Column(Integer, nullable=False)
    profile_id = Column(String(64))
    user_capture_days = Column(Integer)
    age = Column(Integer, index=True)  #
    gender = Column(String(8))
    lable = Column(ARRAY(String))
    # lable = Column(String(32))
    vip = Column(Integer)


def test():
    # 创建session对象:
    session = DBSession()
    data = {
        'datestr': '20190606',
        'region_id': 1,
        'profile_id': 'dafdagjoasjdfald',
        'user_capture_days': 1,
        'age': 10,
        'gender': 'male',
        'lable': ['car', 'money'],
        'vip': 0
    }
    # 创建新User对象:
    new_user = DayResult(**data)
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()


def query(session, table_model, kwargs={}, include_cols=[], exclude_cols=[]):
    offset = 0
    limit = 10
    try:
        # session = DBSession()
        # items = session.query(table_model).filter_by(**kwargs).order_by().offset(offset).limit(limit).all()
        items = session.query(table_model).filter_by(**kwargs).all()
        #print(items)
        logging.info(items)
        data = [it.json(include_cols=include_cols, exclude_cols=exclude_cols) for it in items]

        return True, data
    except Exception as e:
        logging.error(e)
        return False, "Query database error"


def insert(session, table_model, kwargs):
    try:
        # kwargs["updated_by"] = configs.user_id
        new_item = table_model(**kwargs)
        # session = DBSession()
        session.add(new_item)
        # session.flush()
        session.commit()
    except Exception as e:
        logging.error(e)
        return False, "Insert item error"
    return True, new_item


def batch_insert(session, table_model, batch_data):

    if not isinstance(batch_data, list):
        logging.error('not list type')
        return False

    insert_list = []
    for item in batch_data:
        new_item = table_model(**item)
        insert_list.append(new_item)
    # session = DBSession()
    session.add_all(insert_list)
    session.commit()


if __name__ == '__main__':
    # Base.metadata.create_all(engine)  # 创建表结构
    # test()
    data = {
        'datestr': '20190606',
        'region_id': 1,
        'profile_id': 'dafdagjoasjdfald',
        'user_capture_days': 1,
        'age': 10,
        'gender': 'male',
        'lable': ['car', 'money'],
        'vip': 0
    }
    insert(DayResult, data)
    query(DayResult)