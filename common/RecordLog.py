"""
------------------------------------
@Time : 2019/6/13 9:02
@Auth : linux超
@File : RecordLog.py
@IDE  : PyCharm
@Motto: Real warriors,dare to face the bleak warning,dare to face the incisive error!
------------------------------------
"""
import logging
from logging.handlers import RotatingFileHandler
from common.CreatePath import ModelsClass
from config.config import LOG_DIR


class Log(object):
    """only record log for file"""
    def __init__(self, name=__name__, path='log.log', level='DEBUG'):
        self.__name = name
        self.__path = path
        self.__level = level
        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(self.__level)

    def __ini_handler(self):
        """初始化handler"""
        file_handler = RotatingFileHandler(self.__path, maxBytes=10*1024*1024, backupCount=3, encoding='utf-8')
        return file_handler

    def __set_handler(self, file_handler, level='DEBUG'):
        """设置handler级别并添加到logger收集器"""
        file_handler.setLevel(level)
        self.__logger.addHandler(file_handler)

    @staticmethod
    def __set_formatter(file_handler):
        """设置日志输出格式"""
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]'
                                      '-%(levelname)s-[日志信息]: %(message)s',
                                      datefmt='%a, %d %b %Y %H:%M:%S')
        file_handler.setFormatter(formatter)

    @staticmethod
    def __close_handler(file_handler):
        """关闭handler"""
        file_handler.close()

    @property
    def logger(self):
        """构造收集器，返回logger"""
        file_handler = self.__ini_handler()
        self.__set_handler(file_handler)
        self.__set_formatter(file_handler)
        self.__close_handler(file_handler)
        return self.__logger


log_name = ModelsClass.file_name('log')
log = Log(__name__, LOG_DIR + '/' + log_name)
logger = log.logger

if __name__ == '__main__':
    log = Log(__name__, 'file.log')
    logger = log.logger
    logger.debug('I am a debug message')
    logger.info('I am a info message')
    logger.warning('I am a warning message')
    logger.error('I am a error message')
    logger.critical('I am a critical message')
