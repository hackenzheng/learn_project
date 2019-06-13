pycharm等注册码 ：http://idea.lanyus.com/ 

Ubuntu上pycharm专业版破解安装 https://blog.csdn.net/mzl87/article/details/79632180


python2.7显示中文

import sys reload(sys)
sys.setdefaultencoding('utf8')
result = { 'shop': b'海底捞',  'date': '2018-5-31',  'total_visit': total,  'male_num': 0,  'female_num': 0,  'vip_num': match,  'vip_distribution': { 18: 0, 19: 0, 20: 0},  'age_distribution': { 'male': '',  'female': ''}
} 
json.dumps(result, ensure_ascii=False).encode('utf-8')


python支持函数嵌套，即在函数里面在定义函数，但有多种形式，闭包是其中的特殊形式，内部函数引用了外部函数的变量，但不能修改，而外部函数将内部函数作为结果返回，
闭包的应用之一就是装饰器。


python多线程主线程结束后，会默认等待子线程结束后，主线程才退出。在C/C++中，主线程结束后，其子线程会默认被主线程kill掉。
setDaemon()则将python多线程转为C++的形式，主线程结束把所有的子线程结束掉。 join是主线程等待子线程结束掉才执行后面的，调用join会阻塞直到子线程结束。

ipython是jupyter notebook的前身.jupyter拥有 cell, markdown 整合的功能, 能同时运行代码, 而且是多组的. 同时也可以插入markdown这种多功能注释包括图片.
以%开头的叫做line magic, 这种类型的指令只能作用于一行代码，默认是可以不带百分号使用的。
以%%开头的叫做cell magic, 这种类型的指令只能作用于代码块。
在ipython中可以很方便的使用linux命令，只需要在命令前加上一个！就可以了

动态从全路径导入py:
import importlib.util
module_spec = importlib.util.spec_from_file_location('resnet-py', '/mnt/cephfs/training_platform/gfs/fl/models/2018092611410469f2fab3/resnet-py.py')

import arctern_pb2时出现TypeError: __new__() got an unexpected keyword argument 'serialized_options'错误， 需要protoc的版本比python 的protobuf版本高


Python的第三方库中，除了源码和二进制exe之外，.whl文件和.egg文件也是两种常用的文件类型。 whl和egg参考 https://blog.csdn.net/mighty13/article/details/77945613?locationNum=7&fps=1  
包管理介绍：https://blog.zengrong.net/post/2169.html  
确定当前系统的Python包安装路径：  python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"


http的长连接和websocke的长连接:
长连接和短连接是应用层的,tcp连接本身是没有长短之分.只有http等应用层建立的连接才有长短之分.
HTTP1.1通过使用keep-alive进行长连接，它有一个保持时间，可以在不同的服务器软件（如nginx）中设定这个时间, 默认进行持久连接。在一次长连接中可以完成多个 HTTP 请求，但是每个请求仍然要单独发 header. 且是半双工的, 只能是客户端主动向浏览器端发送请求. 短连接就是发送完一直请求之后tcp就断了,要发送下一个请求就要建立新的连接.
websocket的长连接，是一个真的全双工。长连接第一次tcp链路建立之后，后续数据可以双方都进行发送，不需要发送请求头.
http1.1的长连接支持重叠,即支持客户端不用等待上一次请求结果返回就发送下一个请求,但同时发送到的请求数有限,不同浏览器不一样,服务端必须按接收到的请求顺序响应.

WebSocket一种在单个 TCP 连接上进行全双工通讯的协议。 WebSocket 是独立的、创建在 TCP 上的协议，
和 HTTP 的唯一关联是使用 HTTP 协议的101状态码进行协议切换，使用的 TCP 端口是80，可以用于绕过大多数防火墙的限制。
WebSocket 使得客户端和服务器之间的数据交换变得更加简单，允许服务端直接向客户端推送数据而不需要客户端进行请求，
在 WebSocket API 中，浏览器和服务器只需要完成一次握手，两者之间就直接可以创建持久性的连接，并允许数据进行双向传送。

http短连接，一次请求一次响应就结束; http长连接，多个请求多个响应，只能client端主动请求；websocket是client和server都能主动发，不限次数；
rpc远程调用，client端调用一次响应一次，grpc就是基于http2.0实现的，只需要一次握手，然后保持连接。


使用http必须得知道IP,端口,一些列的请求头信息.http接口是在接口不多、系统与系统交互较少的情况下，解决信息孤岛初期常使用的一种通信手段；优点就是简单、直接、开发方便。
如果是一个大型的网站，内部子系统较多、接口非常多的情况下，RPC框架的好处就显示出来了，首先（基于TCP协议的情况下）就是长连接，不必每次通信都要像http 一样去3次握手什么的，减少了网络开销；其次就是RPC框架一般都有注册中心，有丰富的监控管理；发布、下线接口、动态扩展等，对调用方来说是无感知、统 一化的操作。
rpc即可以用tcp实现也可以用http实现,grpc内容交换格式采用protobuf,传输协议采用http2,性能比http1.1好很多.http2有服务推送,即服务端主动向客户端发送,从而实现全双工.
使用http而不是tcp实现有可以复用http的功能,也方便测试等.
rpc框架和微服务框架没有必然的关系,但微服务框架一般是用rpc而不是http也就实现了RPC,微服务框架还需要实现服务注册与发现.grpc提供了数据传递的功能，但要把他微服务化还要支持服务发现和负载平衡


WSGI定义了 web服务器和 web应用之间的接口规范。只要 web服务器和web应用都遵守WSGI协议，那么 web服务器和 web应用就可以随意的组合。
flask不仅实现了wsgi application还实现了wsgi server,但是单进程，性能不够，生产环境用gunicorn,而应用程序可以不变,方便的提升性能. uWSGI和Gunicorn都是实现了
WSGI server协议的服务器，Django，Flask是实现了WSGI application协议的web框架，可以根据项目实际情况搭配使用. https://www.jianshu.com/p/d6961f713e46


Flask通过render_template()函数来实现模板的渲染。默认支持的模板是jinja2, jinja2是一种模板格式,还有其他的格式.
不同的格式渲染的方式是不一样的,python模块jinja2是渲染jinja2格式的引擎. render_template()只能渲染jinja2格式的模板.
查看Flask源码可以看到Flask是依赖jinja2模板和Werkzeug.
flask目录下templates是模板,需要渲染,static是存储一些静态资源,比如图片,是能够直接访问的,而templates目录下的是不能直接访问.
flask中视图函数(view function)返回的响应可以是包含HTML 的简单字符串,也可以是复杂的表单
在flask前后端不分离的编程中,为了方便实现模块化编程,使用blueprint,它可以有独立的templates、static等.
使用方式是先定义,然后注册,从而将一个独立的模块添加到应用中.  所以blueprint是flask中组织view函数或者说组织各种静态资源的一种方式


threadlocal是解决多线程情况下变量访问的问题，如果一个线程里面有多个函数要使用到同一变量，用参数传递的方式太繁琐，
使用threadlocal，就可以即作为全局变量，每个函数都可以直接访问，不同线程之间也不会冲突

面向对象编程的特征之一就是封装， 封装的目的是避免参数直接对外暴露，而是通过接口，通过接口访问或者修改可以限制行为，做参数校验
一个下划线是可以直接访问的，两根下划线不能直接访问
记住只有双下划线开头而且后缀没有双下划线是不可以直接访问的，其他都是可以的，但是单下划线虽然可以访问，但意思是不要直接访问
父类也叫为超类(super)，所以子类中初始化父类时用的是super
type和isinstance的区别，在基本类型的使用没有问题，但是对有继承关系的父子类就有区别，type得到的就是一个类型，而isinstance是会灵活判断的

self参数只是个占位符，是类实例自身，__new函数创建一个对象，那么自然有返回，返回的是object.new, 是类的静态方法
调用的时候不用传递，所以可以访问类实例的方法， 而classmethod的是类的方法，cls占位符，可以访问类的变量， 那么类的方法和实例的方法
staticmethod外面直接调用，但不能访问内部变量， 而classmethod也能直接调用，而且还能访问内部变量。并且staticmethod用法和classmethod在继承的时候有点区别
staticmethod是调普通函数一样外部通过类而不实例调用，但不能访问类对象或实例内部的属性，方便组织代码； classmethod外部直接调用，而且可以访问内部属性，类的方法则只能通过实例来调用，能够访问内的属性



gevent基于libev和grelent两个包，gevent也包含socket等包，都是用的grelent,标准的socket则是非异步的。
monkey patch的目的是模块用到的其他的标准模块包也弄成异步模式。


线程运行的过程中可以调度到不同的核上, 1个死循环,c++上是会把cpu跑满,python也可以,但python多线程运行也只能跑满1个核,因为GIL的作用
多进程多线程的模式可以提高多任务处理的效率. 单进程单线程的模式也能处理多任务,即事件驱动模型.Nginx就是支持异步IO的Web服务器，它在单核CPU上采用单进程模型就可以高效地支持多任务. 对应到Python语言，单线程的异步编程模型称为协程，有了协程的支持，就可以基于事件驱动编写高效的多任务程序.
 
python socket测试,服务端如果使用多线程,能够同时服务多个client. 服务端使用单线程模式,则只能服务完一个才能服务完第二个.但是后面的连接能够建立,只是不会响应,
建立的连接应该是在连接队列里.
直接用socket编程完成网页的请求的过程:先建立连接,然后发送GET命令即可,所以http建立在tcp之上.
 
协程: 函数间的调用,除非中断,不然是不会顺序执行直到返回.  协程看上去也是子程序，但执行过程中，在协程内部可中断，然后转而执行别的协程，在适当的时候再返回来接着执行。
去执行其他的协程并不是函数调用,因为并没有显式的发起调用.
优势就是协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。
第二大优势就是不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。
Python对协程的支持是通过generator实现的。
 
yield是一个表达式, 只能用在函数里面,用于生成迭代器,有两种写法:
1. yield 2   #调用next会返回2
2. m = yield 2  #返回值2会赋值给m,并且参数2可以通过send替换

协程是coroutine,很多语言里面实现了协程,用于高并发的场景,提高效率. python里边是async关键字定义一个协程对象,
另外asyncio是异步io库,也可以定义协程对象.协程不能直接运行，需要将协程加入到事件循环loop中. 协程里面yield用于有io请求时进行中断,跳转到其他协程继续执行.await也可以针对耗时的操作进行挂起，就像生成器里的yield一样，函数让出控制权。如果只有一个协程,让出控制权也没有意义.
比如以前做的多线程进行DNS切换,可以提高效率,用一个线程开多个协程同样可以实现.
很多时候，我们的事件循环用于注册协程，而有的协程需要动态的添加到事件循环中。一个简单的方式就是使用多线程。当前线程创建一个事件循环，然后在新建一个线程，在新线程中启动事件循环。

定义协程:@asyncio.coroutine和async
io请求时让出控制权:yield from和await


python多线程程序 第一个ctrl+c不会中断,第二个才会, 作为子线程运行时不受键盘中断信号影响
多个子线程,若其中一个子线程因为代码抛异常没有处理,则该线程会退出(可以通过手动raise异常测试), 不影响其他的线程及主进程.  但任何一个线程挂掉都可能直接造成整个进程崩溃，比如子线程的栈溢出,因为所有线程共享进程的内存.
因为主线程和子线程分别使用各自的栈，主线程并不能截获子线程调用过程中的异常.在子线程异常退出后，主线程执行了后续代码（此时主线程不知道子线程的退出状态）
由于子线程运行结束后，其内存并没有被回收，因此可以继续使用该实例获得其成员变量。基于这一点，我们可以通过添加模拟线程退出信息的成员变量来记录子线程退出状态。
在主线程中获得子线程的异常信息，从而为debug提供了依据.

事件（Event）：事件是异步事件通知机制的核心，比如fd事件、超时事件、信号事件、定时器事件。有时候也称事件为事件处理器（EventHandler)
事件循环（EventLoop）：等待并分发事件
高性能网络事件库:
libevent :名气最大，应用最广泛，历史悠久的跨平台事件库；
libev :较libevent而言，设计更简练，性能更好，但对Windows支持不够好；
libev试图做好一件事而已（目标是成为POSIX的事件库），这是最高效的方法。libevent则尝试给你全套解决方案（事件库，非阻塞IO库，http库，DNS客户端)
gevent最开始是用的libevent,后面改用了libev

python中的协程实现:
1. 自带的yield生成器: 使用复杂,实现过程不易于理解
2. greenlet: 对操作进行了统一,协程之间的切换使用switch即可. Greenlet没有自己的调度过程，所以一般不会直接使用
3.gevent: greenlet仍然要在切换的地方人为的指定下一个要执行的协程,使用麻烦. gevent每次遇到io等耗时等待的操作时,
会自动跳转到下一个协程继续执行. Gevent的2架马车，libevent与Greenlet。不同于Eventlet的用python实现的hub调度，Gevent通过Cython调用libev来实现一个高效的event loop调度循环。
gevent带有的数据结构有event,queue, pool, local(线程局部变量)等. Gevent为HTTP内容服务提供了两种WSGI server,gevent.wsgi.WSGIServer和gevent.pywsgi.WSGIServer.
4. Eventlet基于greenlet和select.poll,在Greenlet的基础上实现了自己的GreenThread，实际上就是greenlet类的扩展封装，而与Greenlet的不同是，Eventlet实现了自己调度器称为Hub，使用方式与gevent一致.

gevent和eventlet是亲近，唯一不同的是eventlet是自己实现的事件驱动，而gevent是使用libev
Gevnet是当前使用起来最方便的协程了，但是由于依赖于libev所以不能在pypy上跑，如果需要在pypy上使用协程，Eventlet是最好的选择。
pypy是用Python实现的python解释器,常用的是cpython.

协程无需关心共享的原因:同一时间内只有一个协程在运行，无需对共享变量加锁．
greenlet实现的协程的执行顺序执行顺序由程序来控制,存在的问题就是:如果我们想要写一个协程，那到底该如何来控制函数的执行过程了，如果协程多了，控制岂不是很复杂了
evenlet实现过程:
1.spawn函数，调用该函数，将会使用一个GreenThread来执行用户传入的函数
2.实现的hub用于调度greenthread, 因为greenlet是人为调度,现在要实现自动化调度.
 hub是一个循环,里面有self.timers 和 self.next_timers两个变量，前者是一个列表，但是在这个列表上实现了一个最小堆，用来存储将被调度运行的greenthread，后者，用来存储新加入的greenthread。

spawn是产卵的意思, 在gevent和evenlet中, spawn()干的事情就是生成一个Greenlet实例，然后将这个实例的self.switch方法注册到主循环(hub)回调中
gevent.joinall就是用来启动事件轮询并等待运行结果的。  总结:gevent.spawn创建一个新的Greenlet，并注册到hub的loop上，调用gevent.joinall或者Greenlet.join的时候开始切换到hub。


## python进程后台运行并重定向

nohup python -u test.py >> services.log 2>&1 &

-u选项非常重要, 由于python有缓冲机制，print不一定会立刻输出到文件！！！ 加了-u可以让stdout等强制无缓冲, 立刻输出到文件。 不加则要等程序运行结束才会有结果。