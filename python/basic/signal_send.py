# -*- coding:utf-8 -*-
import os  
import signal  
   
#发送信号，16175是前面那个绑定信号处理函数的pid，需要自行修改  
os.kill(23326,signal.SIGTERM)  
#发送信号，16175是前面那个绑定信号处理函数的pid，需要自行修改  
os.kill(23326,signal.SIGUSR1) 
