# coding: utf-8
import happybase


class Hbase(object):
    """
     :param str name:table name
     :param str row: the row key
     :param list_or_tuple columns: list of columns (optional)
    """

    def __init__(self,host=THRIFT_SERVER_IP,port=THRIFT_SERVER_PORT,timeout = 60*1000):
        port=int(port)
        self.conn = happybase.Connection(host, port=port, autoconnect=False,timeout=timeout)
        self.conn.open()

    def disable(self, table_name,*args):
        if self.conn.is_table_enabled(table_name):
            self.conn.disable_table(table_name)

    def enable(self, table_name,*args):
        if not self.conn.is_table_enabled(table_name):
            self.conn.enable_table(table_name)

    def list_tables(self,*args):
        tabels = self.conn.tables()
        return tabels

    def table(self, table_name,*args):
        table = self.conn.table(table_name)
        return table

    def create(self, table_name, kw,*args):
        """
        :param name: str
        :param kw: dict
        exp:
            kw = {"":dict()}
        :return: None
        """
        families = {}
        if (type(kw) == dict):
            families = kw
        if (type(kw) == list):
            for item in kw:
                families[item] = dict()
        try:
            self.conn.create_table(table_name, families)
        except Exception as e:
            print(e)

    def drop(self, table_name,*args):
        self.conn.disable_table(table_name)
        self.conn.delete_table(table_name)

    def delete(self, table_name, row,*args):
        table = self.table(table_name)
        table.delete(row)


    def delete_column(self, table_name, row, columns,*args):
        self.table(table_name).delete(row, columns=columns)


    def cell(self, table_name, row, column,*args):
        """
        :return: list
        """
        return self.table(table_name).cells(row, column)

    def families(self, table_name,*args):
        """
        :return: dict
        """
        return self.conn.table(table_name).families()

    # data是字典类型
    def put(self, table_name, row, data,*args):
        self.table(table_name).put(row, data)

    def get(self, table_name, row,*args):
        """
        :return: dict
        """
        return self.table(table_name).row(row)

    def get_column(self, table_name, row, columns,*args):
        """

        :return: dict
        """
        return self.table(table_name).row(row, columns)

    def scan(self, table_name,begin=None,end=None,*args):
        if not begin:
            nu = self.conn.table(table_name).scan()
        elif not end:
            nu = self.conn.table(table_name).scan(row_start=begin)
        else:
            nu = self.conn.table(table_name).scan(row_start=begin,row_stop=end)

        datasets = {}
        for row in nu:
            datasets[row[0].decode('utf-8')]=row[1]
        return datasets



    def incr(self, table_name, row, column,*args):
        self.table(table_name).counter_inc(row, column=column)

    def dec(self, table_name, row, column,*args):
        self.table(table_name).counter_dec(row, column=column)

    # 将key和value可能是bytes类型的转化为str
    def to_dict(self,data):
        if data:
            if type(data)==dict:
                back = {}
                for key in data:
                    if type(key)==bytes:
                        newkey=key.decode('utf-8')
                    else:
                        newkey=key

                    if type(data[key])==bytes:
                        newvalue = data[key].decode('utf-8')
                    else:
                        newvalue=data[key]
                    if type(data[key])==dict or type(data[key])==list:
                        newvalue=self.to_dict(data[key])
                    if newkey and newvalue:
                        back[newkey]=newvalue
                return back
            if type(data)==list:
                back = []
                for key in data:
                    if type(key)==bytes:
                        newkey=key.decode('utf-8')
                    else:
                        newkey=key
                    if newkey:
                        back.append(newkey)
                return back
        return None


    def close(self):
        self.conn.close()



if __name__ == "__main__":
    #client = Hbase(host="192.168.11.127", port=30036) #Hbase(host="39.108.150.8")
    client = Hbase(host="192.168.2.161", port=9090)  # Hbase(host="39.108.150.8")
    print(client)
    print(client.list_tables())
    col_family = {"im": {}}
    table_name = "face_image"
    #client.create(table_name, col_family)
    '''
    print(client.get(table_name, "9967e72f40a5d98c2f7de6be8dcb0910") == {})
    '''
    #print(client.get(table_name, "31b2d26abf7b21797871d5b232c91b5d"))
    data = client.get(table_name, "c825dfd261007dd19ab92071e2a87cdc").get(b"im::image_data")
    #print(client.drop("face_image"))

    #print(client.list_tables())
    #print(client.scan(b"face_image"))
    print(len(client.scan("face_image")))