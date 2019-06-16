"""
hive连接与读写测试，hive操作方式就是直接执行sql语句,连接的都是preto服务地址
"""

# drop table if exists user;

def sqlalchemy_test():
    from sqlalchemy.engine import create_engine
    import pandas as pd
    engine = create_engine('presto://192.168.11.127:30890/hive/default') # host是服务器ip，port是端口，hive指的是Presto的catalog， default是默认的库，可以换成其他的。
    df = pd.read_sql("select * from day_result", engine)   # 和一般pandas从数据库中读取数据无任何区别
    print(df)


def pyhive_test():
    from pyhive import presto
    # 通过presto访问hive, presto也支持rest api访问
    conn = presto.Connection(host='192.168.11.127', port=30890)
    cursor = conn.cursor()
    # sql_str = 'create table user_product(id INTEGER);'
    cursor.execute('select * from day_result')
    # cursor.execute(sql_str)

    result = cursor.fetchall()
    print(result)


if __name__ == '__main__':
    pyhive_test()
    sqlalchemy_test()