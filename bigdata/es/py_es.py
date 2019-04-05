# -*- coding: utf-8 -*-
import json
import os
import random
import base64
import numpy as np
import threading
import argparse


# 使用es测试向量相似度的搜索，每个向量512维，向量元素的取值在0-100，搜索算法是knn(k近邻)
# 测试数据为每个文件500个记录,每个表100个文件，也就是5万记录，60个表是300万记录


endcommond =" > /dev/null 2>&1"


class PyES(object):
    # 没有使用sdk，直接构造http请求

    def __init__(self, url):
        self.url = url +"/"

    def decode_float_list(self, base64_string):
        # 将base64字符串转化为浮点型列表
        bytes = base64.b64decode(base64_string)
        return np.frombuffer(bytes, dtype=np.dtype('>f8')).tolist()

    def encode_array(self, arr):
        # 讲浮点型列表转化为字符串
        base64_str = base64.b64encode(np.array(arr).astype(np.dtype('>f8'))).decode("utf-8")
        return base64_str

    def make_index_data(self, index, type, id):
        dict = {}
        dict["index"] = {"_index":index, "_type": type, "_id":id}
        return dict

    def make_rand_data(self, num, start, end):
        arr = []
        for i in range(num):
            arr.append(random.uniform(start, end))
        return arr

    def make_base64(self,field_name, float_arr):
        base64_data = {}
        base64_data[field_name] = self.encode_array(float_arr)
        return base64_data

    def make_base64_file(self,filenum,directory,index,type,field):
        # 生成样本json数据测试用，每个文件不能超过10m不然没法批量向es中添加。整型数据1000条7m，浮点型数据500条7m
        # 每个数据是512维向量，向量每个元素的取值是0-100之间的随机数
        if not os.path.exists(directory):
            os.makedirs(directory)

        id = 0
        for file_id in range(0,filenum):
            filepath = directory+'/data'+str(file_id)+'.json'
            file=open(filepath,mode='w')
            for i in range(500):
                file.writelines(json.dumps(self.make_index_data(index,type,id)))
                file.writelines("\n")
                file.writelines(json.dumps(self.make_base64(field,self.make_rand_data(512,0,100))))
                file.writelines("\n")
                id+=1
            file.close()
            print(filepath,'文件写入完成')

    def import_data_from_file(self, filenum, directory):
        # 将测试文件批量上传到ES
        for file_id in range(filenum):
            command_line = 'curl -H "Content-Type: application/json" -XPOST '+self.url+'_bulk?pretty --data-binary @'+directory+'/data' + str(file_id) + '.json'
            print(command_line)
            status = os.system(command_line+endcommond)
            if status == 0:
                print(file_id, '批量导入数据成功')
            else:
                print(file_id, '批量导入数据失败')

    def add_index(self, index):
        command_line = "curl -XPUT '" + self.url + index + "?pretty'"
        status = os.system(command_line+endcommond)
        if status == 0:
            print('创建index成功')
        else:
            print('创建index失败')

    def add_mapping(self, index, type, change_mapping_data):
        commanstr = "curl -XPOST '"+self.url+index+'/'+type+"/_mapping?pretty'" + " -d '" + json.dumps(change_mapping_data) + "'"+endcommond
        status = os.system(commanstr)
        if status == 0:
            print('映射成功')
        else:
            print('映射失败')

    def get_mapping(self, index):
        commanstr = "curl -XGET '" + self.url + index + "/_mapping?pretty'"
        status = os.popen(commanstr)
        result = status.read()
        status.close()
        print('映射：',result)
        return result

    def remove_index(self, index):
        status = os.system('curl -XDELETE localhost:9200/'+index+'?pretty'+endcommond)
        if status == 0:
            print('删除index成功')
        else:
            print('删除index失败')

    def get_field(self, index, type, id):
        process = os.popen('curl '+self.url+index+"/"+type+'/'+str(id)+'?pretty=true')
        output = process.read()
        process.close()
        output = json.loads(output)
        print(output)
        return output

    def add_field(self, index, type, field, value):
        pass

    def knn(self, index=None, type=None, field=None, arr=None, k=1):
        # 使用knn查询与目标向量匹配的所有向量,需要安装插件，可参考https://github.com/alexklibisz/elastik-nearest-neighbors
        query = {
            "query": {
                "function_score": {
                    "boost_mode": "replace",
                    "script_score": {
                        "script": {
                            "inline": "binary_vector_score",
                            "lang": "knn",   # 使用插件快速查询knn
                            "params": {
                                "cosine": False,  # false表示使用点乘， true表示使用余弦相似
                                "field": field,
                                "vector": arr
                            }
                        }
                    }
                }
            },
            "size": k
        }

        linuxcommand = 'curl -H "Content-Type: application/json" -XPOST ' + self.url+index+"/_search?pretty' -d '" + json.dumps(query) + endcommond
        back = os.popen(linuxcommand).read()
        # print(linuxcommand)
        # return
        back = json.loads(back)

        # print('耗费时间：', back['took'], 'ms')

        dataarr = back['hits']['hits']
        alluser=[]
        for temp in dataarr:
            user = {}
            user['id'] = temp['_id']
            user['data'] = self.decode_float_list(temp['_source'][field])
            alluser.append(user)
            # print('用户id：',user['id'],',',user['data'])
        return alluser

    def knn_local(self,alluser,user):
        # 没有用上
        alluser_mat = np.array(alluser)
        user_mat = np.array(user).repeat(-1,1)
        result = np.dot(alluser_mat,user_mat)
        maxuser = np.where(np.max())


def knn(data_list, i):
    alluser = es.knn(index_src+str(i), type_src+str(i), field_src+str(i), data_list, 1)
    print(alluser)


table_filenum = 100  # 一个表的文件数目,一个文件500条
tablenum = 180       # 使用180个表格存储。每个表5万，共900万记录
index_src = 'user'
type_src = 'icon'
field_src = 'column'
es = PyES('127.0.0.1:9200')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='es do something')
    parser.add_argument('--makefile', default=False, action='store_true', help='make file to insert database')
    parser.add_argument('--delindex', default=False, action='store_true', help='delete index')
    parser.add_argument('--importfile', default=False, action='store_true', help='import file to database')
    parser.add_argument('--tablenum', default=10, help='table num')
    parser.add_argument('--es', default=False, action='store_true', help='whether search')
    args = vars(parser.parse_args())

    if args['makefile']:   # 如果命令中要产生文件
        for i in range(tablenum):
            es.make_base64_file(table_filenum,'data/data'+str(i),index_src+str(i),type_src+str(i),field_src+str(i))

    if args['delindex']:  # 如果命令中要删除index
        es.remove_index('*')
        for i in range(tablenum):
            index=index_src+str(i)
            type=type_src+str(i)
            field=field_src+str(i)
            change_mapping_data = {
                type: {
                    "properties": {
                        field: {
                            "type": "binary",
                            "doc_values": True
                        }
                    }
                }
            }

            es.add_index(index)
            es.add_mapping(index, type, change_mapping_data)
            es.get_mapping(index)

    if args['importfile']:
        print('start to import')
        # curl localhost:9200/_cat/indices?v
        for i in range(0, 1):  # int(args['tablenum'])
            es.import_data_from_file(table_filenum, 'data/data' + str(i))

    # es.get_field(index_src + str(0), type_src + str(0), id=502)  # 根据id查询field的值

    if args['es']:
        # 构造测试向量查询
        data_list = es.make_rand_data(512, 0, 100)
        tablenum = int(args['tablenum'])
        for i in range(tablenum):
            group = tablenum/60   # 每次只能同时查询300万记录,耗时1.5s
            t = threading.Thread(target=knn, args=(data_list, i))
            t.start()