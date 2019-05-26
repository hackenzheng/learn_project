## CRLF回车换行
回车换行， 回车，换行三个本质上是一样的，都是换行，只是在Windows系统下是\r\n,在unix下\n就可以，在早期的mac系统下\r就可以。
Python中对换行做了统一的处理，定义为\n, 比如print("hello \n world ")就会输出两行。

最开始之所以换行需要回车和换行两步是从打字机开始的，打字机换行需要针头回到行首而且纸张要往下移动一行。

<CRLF是什么东西> https://blog.csdn.net/lunda5/article/details/40963045
