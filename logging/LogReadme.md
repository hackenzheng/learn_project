## python的log记录
使用logging模块，可以配置为只输出到终端或只输出到文件或同时输出到终端和文件

Python的日志是同步的,所以如果直接把日志写入文件,也会有文件系统I/O的开销,更快的方式是把日志记录到sys.stderr或sys.stdout,
然后用gunicorn把标准输出的日志重定向到文件.

    # 日志配置
    import logging, logging.config
    import sys
    
    LOGGING = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
            }
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }
    
    gunicorn选项: http://docs.gunicorn.org/en/stable/settings.html#capture-output


## c/c++的log记录
syslog()
