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
 




 
