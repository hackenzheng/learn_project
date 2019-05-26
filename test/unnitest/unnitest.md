## 单元测试
python的单元测试库有pytest和unitest, unitest是Python自带的，但pytest使用更简单。无论是用pytest还是unitest，
都能使用Mock构造数据以及跑代码覆盖率。 Mock测试是在测试过程中对可能不稳定、有副作用、不容易构造或者不容易获取的对象，用一个虚拟的对象来创建以便完成测试的方法。
mock库在Python3.3的时候被引入到标准库，改名为unitest.mock，也可以pip install mock， 然后直接import mock。

单测时如果环境难以准备才考虑mock,不然该依赖的还是要依赖，比如redis-py的单元测试，需要依赖服务端，服务端是比较好准备的，就不需要mock.