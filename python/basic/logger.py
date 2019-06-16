# -*- coding: utf-8 -*-

"""
 log setup, including system log and business log
"""

# logging模块使用： https://www.cnblogs.com/xielisen/p/6817807.html

import os
import time
import inspect
import logging
import stat
import logging.handlers
LOG_PATH = '/intellif/flas_log'

G_SYS_LOGGER = None
G_MSG_LOGGER = None

G_MODULE_NAME = ""
G_FUNCTION_NAME = ""


def __sys_logger():
    """
    get system logger
    :return:
    """
    global G_SYS_LOGGER, G_MODULE_NAME, G_FUNCTION_NAME

    date_now = time.strftime("%Y%m%d", time.localtime())

    base_dir = os.path.join(LOG_PATH, date_now)
    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)
        os.chmod(base_dir, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)

    log_dir = os.path.join(base_dir, G_MODULE_NAME, 'log')
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
        os.chmod(log_dir, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)

    log_file = os.path.join(log_dir, G_FUNCTION_NAME + '.log')
    if not os.path.exists(log_file):
        tmp_file = open(log_file, 'w')
        tmp_file.close()
        G_SYS_LOGGER = SystemLog(log_file)

    if G_SYS_LOGGER is None:
        G_SYS_LOGGER = SystemLog(log_file)

    return G_SYS_LOGGER


def __msg_logger():
    """
    get business logger
    :return:
    """
    global G_MSG_LOGGER, G_MODULE_NAME, G_FUNCTION_NAME

    date_now = time.strftime("%Y%m%d", time.localtime())

    base_dir = os.path.join(LOG_PATH, date_now)
    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)
        os.chmod(base_dir, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)

    log_dir = os.path.join(base_dir, G_MODULE_NAME, 'log')
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
        os.chmod(log_dir, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)

    log_file = os.path.join(log_dir, G_FUNCTION_NAME + '_message.log')
    if not os.path.exists(log_file):
        tmp_file = open(log_file, 'w')
        tmp_file.close()
        G_MSG_LOGGER = MessageLog(log_file)

    if G_MSG_LOGGER is None:
        G_MSG_LOGGER = MessageLog(log_file)

    return G_MSG_LOGGER


def init_logger(module_name, function_name):
    """
    :param module_name:
    :param function_name:  "功能非函数"
    :return:
    """
    global G_MODULE_NAME, G_FUNCTION_NAME

    if module_name and function_name:
        G_MODULE_NAME = module_name
        G_FUNCTION_NAME = function_name
        return True
    return False


def SYS_DEBUG(msg):

    __sys_logger().debug(msg)


def SYS_INFO(msg):
    __sys_logger().info(msg)


def SYS_WARN(msg):
    __sys_logger().warn(msg)


def SYS_ERROR(msg):
    __sys_logger().debug(msg)


def SYS_CRITICAL(msg):
    __sys_logger().critical(msg)


def DEBUG(msg):
    __msg_logger().debug(msg)


def INFO(msg):
    __msg_logger().info(msg)


def WARN(msg):
    __msg_logger().warn(msg)


def ERROR(msg):
    __msg_logger().error(msg)


def CRITICAL(msg):
    __msg_logger().critical(msg)


class LogBase:
    def __init__(self, logger):
        self.m_logger = logger

    def printf_now(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def log_message(self, level, message):
        global G_MODULE_NAME, G_FUNCTION_NAME
        frame, filename, lineno, functionname, code, unknowfield = inspect.stack()[
            3]
        return "%s\t%s\t%s\t%s\t%s:%s:%s\t%s" % \
               (self.printf_now(), level, G_MODULE_NAME,
                G_FUNCTION_NAME, filename, lineno, functionname, message)

    def debug(self, message):
        self.m_logger.debug(self.log_message('DEBUG', message))

    def info(self, message):
        self.m_logger.info(self.log_message('INFO', message))

    def warn(self, message):
        self.m_logger.warn(self.log_message('WARN', message))

    def error(self, message):
        self.m_logger.error(self.log_message('ERROR', message))

    def critical(self, message):
        self.m_logger.critical(self.log_message('CRITICAL', message))


class MessageLog(LogBase):
    def __init__(self, logfile):
        path = os.path.abspath(logfile)
        self._handler = logging.FileHandler(path)
        logger = logging.getLogger('msg')
        logger.addHandler(self._handler)
        logger.setLevel(logging.INFO)

        hdlr = logging.handlers.TimedRotatingFileHandler(logfile, when='H', interval=1, backupCount=48)
        hdlr.suffix = "%Y-%m-%d_%H-%M-%S.log"
        logger.addHandler(hdlr)

        LogBase.__init__(self, logger)

    def ___del__(self):
        self._handler.flush()
        self.m_logger.removeHandler(self._handler)


class SystemLog(LogBase):
    def __init__(self, logfile):
        path = os.path.abspath(logfile)
        self._handler = logging.FileHandler(path)
        logger = logging.getLogger('sys')
        logger.addHandler(self._handler)
        logger.setLevel(logging.INFO)
        LogBase.__init__(self, logger)

    def ___del__(self):
        self._handler.flush()
        self.m_logger.removeHandler(self._handler)
