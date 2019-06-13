## mongodb
mongodb不能支持事务，不能自动回滚，需要自己实现回滚逻辑，也不支持多表查询.
nosql放弃了关系数据库的两大重要基础: 以关系代数为基础的结构化查询语言和事物一致性保证(ACID),nosql相比于关系型数据库,方便扩展列, 
关系型数据库为了保证关系运算(通过sql)的正确性, 在设计数据库表结构的时候,就需要指定表的schema即字段名称及属性,并需要遵循特定的设计范式. 

mongodb副本集：
（1）三个节点，若两个节点挂掉，第三个节点只能读不能写，若配置的时候就只有一个节点，配置为副本集，读写都是可以的。或一开始3个节点，然后主动remove两个，剩下的一个也是读写都可以。
（2）主节点上的用户和密码也会同步到其他节点上去，不用在从节点上创建用户密码，若创建也是可以的。
（3）从单机升级为副本集，修改配置文件重启下就ok，再从副本集切回单机，将配置文件修改再重启即可，若再切回副本集出现一直是other状态，则reconfig一下。

mongodb聚合查询：

    $match是匹配条件， _id之后的是用于区分的， $addToSet/$min/$max/$sum是聚合函数。group之前的match，是对源数据进行查询，group之后的match是对group之后的数据进行筛选。 
    db.AttackAction.aggregate([ {$match:{'src_ip': '183.39.156.231'}},
                                    {$group:
                                        {_id: {'src_ip': '$src_ip', 'type_name': '$type_name'}, 
                                        'ip': {$addToSet: '$ip'},
                                        'net_action': {$addToSet: '$net_action'},
                                        'risk_level': {$min: '$risk_level'},
                                        'start_time': {$min: '$record_time'},
                                        'end_time': {$max: '$record_time'},
                                         cnt: {$sum: 1},
                                         }
                                    } ,
                                    { $sort:{'cnt':-1}}
                                    ])
 
    可以在group的基础上再group一次，可以叠加的，$addToSet去重，$push不去重; $project是对最终的结果重新进行选择或者对字段进行重命名
    db.AttackAction.aggregate([{$match:{'record_time': {$gte: 0, $lt: 1497088856}}},
                                    {$group: {_id: {'src_ip': '$src_ip', 'type_name': '$type_name'}, 
                                        'ip': {$addToSet: '$ip'},
                                        'net_action': {$addToSet: '$net_action'},
                                        'risk_level': {$min: '$risk_level'},
                                        'start_time': {$min: '$record_time'},
                                        'end_time': {$max: '$record_time'},
                                        cnt: {$sum: 1}
                                    }},
                                    {$group: {_id: {'src_ip': '$_id.src_ip'},
                                        'detail': {
                                            $push : {
                                                'ip': '$ip', 
                                   'start_time': {$min: '$start_time'},
                                        'end_time': {$max: '$end_time'},
                                        total: {$sum: '$cnt'}
                                    }},
                                    {$sort: {'type_list.risk_level': 1, 'total': -1}}
                        $project:{
                                'net_action': '$net_action',
                                                'risk_level': '$risk_level', 
                             'type_list': {
    
                                                     $push: {
    
                                                    'type_name': '$_id.type_name',
    
                                                    'type_cnt': '$cnt'
    
                                                  }
                                            }]
                                        },
 



## mongodb部署

物理机部署
    
    官方下载地址 https://www.mongodb.com/download-center/community
    下载Ubuntu版本deb包安装之后只会有服务端，没有客户端
    
    下载二进制版本， 版本号对应修改
    curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.10.tgz
    tar -zxvf mongodb-linux-x86_64-4.0.10.tgz
    mv mongodb-linux-x86_64-4.0.10 /usr/local/mongodb
    
    mongod --dbpath=/data/db  # 启动服务并指定数据存储路径， 要后台启动就加&, 本身没有后台启动的选项
    mongo   # 在服务器本机会直接登录
    mongod --shutdown --dbpath /data/db   # 停止服务

登录认证：

    MongoDB 默认安装完成以后，只允许本地连接，同时不需要使用任何账号密码就可以直接连接MongoDB，这样就容易被黑
    
    创建管理员用户
    use admin
    db.createUser({user:"admin",pwd:"admin",roles:["root"]})  # 用户的权限是跟库绑定的
    
    ./mongod --auth  --bind_ip_all # 启用认证,允许远程登录
    
    ./mongo 进入到交互模式， 是启动客户端之后再认证而不想MySQL等要先输入密码认证再进入交互模式
    use admin   # 一定要用admin数据库才能认证， 直接db.auth会报错
    db.auth("admin", "password") 认证登录
    

## 常用命令
 
    show dbs; 查看数据库
    db.dropDatabase(); 删除当前数据库
    use yourdb;  切换或创建数据库
    show users;   查看用户
    show roles;   查看角色
    
    use admin; db.system.users.find()  # 显示当前系统用户
    
    use newdb;  创建数据库
    db.createCollection('newcollection')  创建新的表
    show collections  显示所有的表
    
    db.test.find()  # 查询所有数据
    db.test.find().count()  计数
    
    # 在3.0.0 版本前创建索引方法为ensureIndex()，之后的版本使用了createIndex()，ensureIndex()还能用，但只是createIndex() 的别名。
    db.collection.createIndex(keys, options)  
    db.collection.createIndex({open: 1, close: 1}, {background: true})　　# 在后台创建索引,索引的升序主要是跟排序或范围查询的时候有关
    
    
## 性能测试 YCSB
没有自带的benchmark测试工具，可以写脚本自行测试，另外有YCSB。 YCSB是雅虎开源的一款通用的NoSQL性能测试工具.

使用：
    
    下载ycsb并解压
    curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.5.0/ycsb-0.5.0.tar.gz
    tar xfvz ycsb-0.5.0.tar.gz
    cd ycsb-0.5.     # bin目录下有yscb执行文件，是个Python脚本； workloads目录下有各种workload的模板，可以基于workload模板进行个性化修改
    
    ycsb测试的时候分为load和transaction两阶段， load用于构造测试数据。 对于不同的db都有一些选项，比如mongo就有mongodb 和 mongodb-async，默认是同步模式。
    测试mongo的时候在配置文件中配置mongo
    
    mongodb.url=mongodb://admin:admin192.168.137.10:34001/ycsb?  # mongodb对应的uri等
    mongodb.database=ycsb # 对应的db
    mongodb.writeConcern=normal # 写级别
    
    ./bin/ycsb load mongodb-async -s -P workloads/workloada > outputLoad.txt  # 使用异步模式加载数据, -P 指定workload文件，-s把状态输出到stderr中
    ./bin/ycsb run mongodb-async -s -P workloads/workloada > outputRun.txt    # 使用异步模式执行测试
    
    如果要自定义表和字段，需要修改jar包源码，不能通过配置实现