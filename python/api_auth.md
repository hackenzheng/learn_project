http请求头中Authorization字段是用于认证的, 若是基本认证, 该字段的值是把用户密码进行base64加密,安全性很低,生产环境很少使用. 
一般是通过post传送用户密码.  OAuth（开放授权）是一个开放的授权标准，允许用户让第三方应用访问该用户在某一web服务上存储的私密的资源，
而无需将用户名和密码提供给第三方应用。过程是先请求认证,认证后获得token,再用token去访问资源.
 

 
restful api本身是没有状态的, 也不会记录登录状态. 可以通过cookie和session记录. 
 
访问需要认证的api验证方式: 
 
(1)用户名密码: 每次访问都需要用户名密码, 比较繁琐,且效率低. 不通过表单传送, 因为api本身的认证,不是登录界面. 那么用户密码通过HTTP BASIC Authentication, 用户密码通过base64编码后放在authentiate字段.
(2)token的方式: 第一次客户端与服务器交换过认证信息后得到一个认证token，后面的请求就使用这个token进行请求.Token通常会给一个过期的时间，
当超过这个时间后，就会变成无效，需要产生一个新的token。这样就算token泄漏了，危害也只是在有效的时间内。Token机制在服务端不需要存储任何信息，因为Token自身包含了所有用户的信息及过期时间，
客户端只会拿着token给到不同的服务端，每个服务事先约定好加密秘钥，用同一个秘钥加解密。
(3)cookie和session,用于浏览器, 因为浏览器请求才会自动带上cookie,其他比如python脚本, curl命令都需要手动设置才能有cookie. 
其中session又分为客户端和服务端, 客户端指所有的session内容都编码作为cookie,  服务端则是只把session id放到cookie传递. 
 
第一种和第二种在flask使用Flask-HTTPAuth,第三种方式使用flask_login

 
http协议是无状态的， 浏览器和web服务器之间可以通过cookie来身份识别。 桌面应用程序(比如新浪桌面客户端， skydrive客户端)跟Web服务器之间是如何身份识别呢




跨域:
浏览器为了安全考虑有一个同源策略的限制, 同源的意思是协议,域名(含子域名)和端口都要一样.
  
在浏览器上当前访问的网站向另一个网站发送ajax请求获取数据的过程就是跨域请求, 前后端分离的开发模式就会产生跨域请求, 
往往端口会不一样.但这种情况并非是不安全的,所以需要解决跨域资源共享的问题.    
  
而form请求等请求整个网页的方式是不会出现跨域的,    因为原页面用 form 提交到另一个域名之后，原页面的脚本无法获取新页面中的内容。 

所以浏览器认为这是安全的。而 AJAX 是可以读取响应内容的，因此浏览器不能允许你这样做。如果你细心的话你会发现，其实请求已经发送出去了，你只是拿不到响应而已。

所以浏览器这个策略的本质是，一个域名的 JS ，在未经允许的情况下，不得读取另一个域名的内容。但浏览器并不阻止你向另一个域名发送请


jwt json web token， 就是json格式的token认证方式， 分为3部分内容，是个json格式，然后再通过secret加密， 加密的过程就是签发，
用户和密码登录时服务端进行签发， 后面每次请求都带上这个token，不用session认证， 解决了单点登录， 以及分布式场景下的认证问题
jwt的传输方式多样，可以是url参数，可以是post,也可以是http头部

session就是会话， 会话需要一个唯一的id， 这个id生成之后有两种方式传递，放请求参数里面或用cookie，显然cookie更方便。
浏览器一次打开多个网站，每个网站都有cookie，那么就需要区分cookie所属的网站即cookie的域，浏览器发送http请求时会自动携带与该域匹配的cookie，而不是所有cookie。 
单点登录就是在一个多系统用用群中登录一个系统，便可得到授权访问其他系统无需再次登录，如果这些子系统在同一个顶级域名下面，是没有问题的，但是不同域名，技术也不一样，就会出现问题。 单点登录就有单点注销，
session通常是存储在服务器的内存，只能限定于这一台服务器，如果有多台，就有问题。session需要通过cookie传递信息，服务端在响应头设置好cookie，下次请求的时候就带上cookie。 session分为服务端和客户端两种，服务端就是session的内容存储在服务端，通过cookie传递sessionid，客户端是将所有内容加密为一个字符串，放在cookie中传输。 请求头中cookie字段支持很多对key/value内容。


用户密码的登录方式是通过表单输入，请求到服务端认证之后返回cookie，
而HTTP Basic Auth每次请求API时都提供用户的username和password，信息没有加密很容易暴露，基本不用

token认证的方式有很多，比如登录之后手动创建token如dnspod，每次就可以拿这个token去认证
也有每次登陆的时候签发token，jwt就是这种，Token信息可以放在COOKIE中，也可以放在HTTP的Authorization头中，首先在cookie中查找Token信息，如果没有找到，则在HTTP Authorization Head中查找； JWT的方式就是在authorization head中。
jwt与session的区别就是认证信息都在token字符串里面，解码之后就判断，分布式下每个服务器都能做到
 


若服务端在代码里不设置cookie,响应头是没有'set-cookie'字段.
若服务端先设置cookie,后面又不设置cookie, 浏览器发出的请求头都是带有cookie字段的
flask服务重启所有变量清空,session不可用.

session根据存储位置有client端和server端两种, client端表示所有的session数据通过key加密作为cookie,一旦可key泄露就不安全. server端则是数据存储在服务器端,可以是redis,memcached或者硬盘,然后取session_id放在cookie传送.  flask自带的cookie是client端方式,所以要设置key. flask_session和flask_kvsession是拓展.https://stackoverflow.com/questions/32084646/flask-session-extension-vs-default-session

设置session,只需要简单的设置里面的取值,比如session['username'], 可以设置多个key.
设置不会导致同一个用户同时不同地方登录出问题, 每次登录,都会生成一个新的session,有唯一的sessionid.
可以在两个浏览器里面同时登录,然后查看session的取值,是否做了区分. 