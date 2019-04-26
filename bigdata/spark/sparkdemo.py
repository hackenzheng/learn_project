# pip install pyspark

import sys
import os
# import findspark
from operator import add
from pyspark import SparkContext
from pyspark import SparkConf


SPARK_MASTER = "local[*]"   # "local[*]"  "spark://localhost:7077"
SPARK_EXECUTOR_MEMORY = '1g'
SPARK_APP_NAME = 'test_connect'


# RDD的基础操作整体参考 https://blog.csdn.net/cymy001/article/details/78483723

def init_sc():
    """
    任何Spark程序都是SparkContext开始的，SparkContext的初始化需要一个SparkConf对象，SparkConf包含了Spark集群配置的各种参数(比如主节点的URL)。
    初始化后，就可以使用SparkContext对象所包含的各种方法来创建和操作RDD和共享变量。Spark shell会自动初始化一个SparkContext(在Scala和Python下可以，但不支持Java)。
    :return:
    """


    conf = SparkConf().setMaster(SPARK_MASTER).setAppName(SPARK_APP_NAME).set("spark.executor.memory", SPARK_EXECUTOR_MEMORY)
    sc = SparkContext(conf=conf)
    # sc=SparkContext.getOrCreate(conf)  # 视情况新建session或利用已有的session
    return sc


def creat_rdd_from_list():
    """
    从本地内存初始化一个rdd,list中的元素将被自动分块
    :return:
    """
    rdd = sc.parallelize([1,2,3,4,5])  # 使用sc.parallelize可以把Python list，NumPy array或者Pandas Series,Pandas DataFrame转成Spark RDD
    print(rdd)
    print('\n')
    print(rdd.getNumPartitions())  # #方法查看list被分成了几部分
    print('\n')
    print(rdd.glom().collect())    #　具体的分区情况，测试环境为4-core的CPU笔记本;Spark创建了4个executor，然后把数据分成4个块。colloect()方法很危险，数据量上BT文件读入会爆掉内存

    sentencesRDD=sc.parallelize(['Hello world','This is a Test'])
    wordsRDD=sentencesRDD.flatMap(lambda sentence: sentence.split(" "))
    print(wordsRDD.collect())
    print(wordsRDD.count())


def creat_rdd_from_file(path=os.getcwd()):
    """
    直接把文本读到RDD。文本的每一行都会被当做一个item，不过需要注意的一点是，Spark一般默认给定的路径是指向HDFS的，如果要从本地读取文件的话，需要加file://，且是绝对路径
    :param path:
    :return:
    """
    rdd=sc.textFile("file://" + path)
    print(rdd)
    print('\n')
    print(rdd.first())          # 取读入的rdd数据第一个item, 是文件的第一行


def creat_rdd_from_folder(path=os.getcwd()):
    """
    读入整个文件的文件
    :param path:
    :return:
    """
    rdd = sc.wholeTextFiles("file://" + path)
    print(rdd)
    rdd.first()   #　RDD中的每个item实际上是一个形如(文件名，文件所有内容)的元组。


def transform_example():
    """
    rdd会经过转换会得到一个新的RDD
    :return:
    """
    numbersRDD = sc.parallelize(range(1,10+1))
    print(numbersRDD.collect())
    #map()对RDD的每一个item都执行同一个操作
    squaresRDD = numbersRDD.map(lambda x: x**2)           # Square every number
    print(squaresRDD.collect())
    #filter()筛选出来满足条件的item
    filteredRDD = numbersRDD.filter(lambda x: x % 2 == 0) # Only the evens
    print(filteredRDD.collect())


def transform_union():
    """
    多个transform的串联使用
    :return:
    """

    def doubleIfOdd(x):
        if x % 2 == 1:
            return 2 * x
        else:
            return x

    numbersRDD = sc.parallelize(range(1,10+1))
    resultRDD = (numbersRDD.map(doubleIfOdd).filter(lambda x: x > 6).distinct())
    resultRDD.collect()


def transform_kv():
    """
    当item是“pair RDDs”的以元组形式组织的k-v对时有一些特殊的transform
    reduceByKey(): 对所有有着相同key的items执行reduce操作
    groupByKey(): 返回类似(key, listOfValues)元组的RDD，后面的value List 是同一个key下面的
    sortByKey(): 按照key排序
    countByKey(): 按照key去对item个数进行统计
    collectAsMap(): 和collect有些类似，但是返回的是k-v的字典

    """
    rdd=sc.parallelize(["Hello hello", "Hello New York", "York says hello"])
    #将word映射成(word,1)
    resultRDD=(rdd .flatMap(lambda sentence:sentence.split(" ")) .map(lambda word:word.lower()) .map(lambda word:(word, 1))
                      .reduceByKey(lambda x, y: x + y)) #reduceByKey对所有有着相同key的items执行reduce操作 resultRDD.collect()
    result = resultRDD.collectAsMap()  #collectAsMap类似collect,以k-v字典的形式返回
    print(result)
    resultRDD.sortByKey(ascending=True).take(2)  #sortByKey按键排序
    #取出现频次最高的2个词
    print(resultRDD
          .sortBy(lambda x: x[1], ascending=False)
          .take(2))


def transform_join():
    """
    多个RDD可以合并为一个，也可以进行join等操作
    :return:
    """
    pass


def word_count():
    """
    spark中进行word count的三种方法
    :return:
    """
    sc= SparkContext.getOrCreate()

    path = 'file:///data.txt'
    # 第一种方法
    rdd1 = sc.textFile(path)
    counts = rdd1.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add)
    print(type(counts))
    output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word, count))

    # 第二中方法
    result = rdd1.flatMap(lambda x: x.split(' ')).countByValue().items()
    print(result)

    # 第三种方法
    result = rdd1.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).countByKey().items()
    print(result)

    # findspark.init("/root/spark")  # spark二进制文件目录
    # spark = SparkSession.builder.master("spark://cloud-spark-master:7077").appName("my_first_app_name").getOrCreate()



if __name__ == "__main__":
    sc = init_sc()
    creat_rdd_from_list()
    creat_rdd_from_file(os.getcwd() + '/sparkdemo.py')




