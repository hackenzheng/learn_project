测试4000万-1亿数据量pg,mongodb,tidb,hive的插入查询性能

测试过程中碰到的问题
    
    目的是造1亿条数据，索引字段是age和datestr，不小心datestr只限制在一个月内，导致每天的数据量特别大，建了索引之后查询反而更慢了。
    explain会发现走的是bitmap scan.
    
    即使建了索引，如果索引字段的某个值对应有很多数据，查询会很耗时。 比如当获取的数据分布很大(比如70%以上)时，
    用index scan 已经没有意义了，因为数据太多了，走索引再走表的代价已经超过了单纯走表的代价了。这里的分布考虑两点，
    一个是本身的数据量，如果是百万级即使只有3%也会慢；另外就是占比，如果超过50%比全量扫描的代价也差不多，因为走索引要回表。
    如果通过limit限制查询数量会加快。
    
    但如果用到了排序，即使用了limit,查询也会耗时, 所以测试应用用深分页查询。
    select * from day_result where datestr='20190605' offset 100000 limit 10;  # 立即出结果
    select * from day_result where datestr='20190605' order by age offset 100000 limit 10; #需要等几秒

    查询的时候mongodb比较耗内存，pgsql比较耗cpu.

