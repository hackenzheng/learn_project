自动化测试包含接口测试,集成测试,单元测试,其中单元测试只针对主要功能模块做测试,后端框架中的接口可以不做单测而做接口测试
单元测试的主体是一个个的模块,函数, 该模块调用到的其他函数可以mock,不然跟集成测试一样了. 
测试条件: 是否需要启动http server, 是否要准备数据库? 单元测试应该是脱离这些实际环境的, 这样跑ci的时候才能通过, 依赖的环境可以mock掉
python的webtest框架可以在不启动http server的时候进行测试, webtest会模拟http server运行,若环境不满足容易出问题.
另外python flask的app自带测试, app.test_client().post('/data')即可模拟.
unittest若要按特定顺序执行,需要使用TestSuit

Python常用的单测模块是unnitest,mock数据用的包是mock
 
举例：我们有一个简单的客户端实现，用来访问一个URL，当访问正常时，需要返回状态码200，不正常时，需要返回状态码404。首先，我们的客户端代码实现如下：
 
    import requests
    def send_request(url):
        r = requests.get(url)
        return r.status_code
    def visit_ustack():
        return send_request('http://www.ustack.com') 
外部模块调用visit_ustack()来访问UnitedStack的官网。下面我们使用mock对象在单元测试中分别测试访问正常和访问不正常的情况。 

    import unittest
    import mock
    import client
    class TestClient(unittest.TestCase):
        def test_success_request(self):
            success_send = mock.Mock(return_value='200')
            client.send_request = success_send         self.assertEqual(client.visit_ustack(), '200')
        def test_fail_request(self):
            fail_send = mock.Mock(return_value='404')
            client.send_request = fail_send
            self.assertEqual(client.visit_ustack(), '404') 

找到要替换的对象：这里测试的对象是visit_ustack函数，那么我们需要替换掉send_request函数。
实例化Mock类得到一个mock对象，并且设置这个mock对象的行为。在成功测试中，设置mock对象的返回值为“200”，在失败测试中，设置mock对象返回值为"404"。
使用这个mock对象替换掉我们想替换的对象,调用client.visit_ustack()，并且期望它的返回值和我们预设的一样。 
上面这个就是使用mock对象的基本步骤。在上面的例子中我们替换了自己写的模块的对象，其实也可以替换标准库和第三方模块的对象，方法是一样的：先import进来，然后替换掉指定的对象就可以了。 

  

参考链接： 
http://www.open-open.com/lib/view/open1449026993889.html 
http://www.yunweipai.com/archives/9269.html 
https://blog.csdn.net/huilan_same/article/details/52944782
