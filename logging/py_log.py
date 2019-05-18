# _*_ coding: utf-8 _*_
# 在程序启动的入口加载init_logger对logging进行配置，在其他py文件中使用logging打印日志即可
import logging
import logging.handlers
import os


def init_logger(parent_path='/flask_log/', sub_path='', module_name=''):
    """
    usage: output to logfile and console simultaneous
    """
    path = parent_path + sub_path
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print('please excute with root privilege, makdir error %s' % e)

    # create a logger
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    # create log file name
    if module_name == '':
        log_file = path + 'server.log'
    else:
        log_file = path + module_name + '.log'

    try:
        # define log format
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] ' +
            '%(levelname)s  %(message)s', '%Y-%m-%d %H:%M:%S')

        hdlr = logging.handlers.TimedRotatingFileHandler(log_file, when='H', interval=1, backupCount=48)
        hdlr.setLevel(logging.INFO)
        hdlr.setFormatter(formatter)
        hdlr.suffix = "%Y-%m-%d_%H-%M-%S.log"
        logger.addHandler(hdlr)

        # create a streamhandler to output to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # create a filehandler to record log to file
        # fh = logging.FileHandler(log_file)
        # fh.setLevel(logging.INFO)
        # fh.setFormatter(formatter)
        # logger.addHandler(fh)

        logger.info(logger.name)
    except Exception as e:
        logging.info(
            'please execute with root privilege, init logger error %s' % e)


def init_console_logger():
    """
    usage: only output to console
    """
    # create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create a streamhandler to output to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # define log format
    formatter = logging.Formatter(
        '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s  %(message)s',
        '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)

    # add handler
    logger.addHandler(ch)
