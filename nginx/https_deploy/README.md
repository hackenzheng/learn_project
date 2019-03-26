使用方式：通过python webapp.py启动服务，端口是8000,再指定配置文件启动nginx

参考：https://cloud.tencent.com/developer/article/1157556
使用nginx rewrite的功能将只提供http服务的web应用转成https
测试用只需要使用openssl命令生成私钥和公钥，但是这样的服务浏览器访问会提示不可信，
因为证书不是权威机构签发的

https的原理是使用非对称加密协商对称加密的秘钥，因为对称加密的性能高，但直接用对称
加密又不安全。需要第三方权威机构签发是防止证书被篡改。具体可以参考