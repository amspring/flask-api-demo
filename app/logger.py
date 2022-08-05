# -*- coding: utf-8 -*-
# Project  : db
# File     : logger.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-03-29 09:54
# Remarks  :不同级别的日志输出到不同的日志文件中
import os
import threading
import time
import logging
import inspect
from logging.handlers import TimedRotatingFileHandler

from .conf import settings


class Singleton(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        实例化调用
        Args:
            *args:
            **kwargs:
        Returns:
        """
        if not hasattr(cls, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instance


class FileLogger(metaclass=Singleton):

    def __init__(self):
        self.__loggers = {}

        # 从配置读取存放日志目录, 配置未配置的默认为 代码根目录下logs
        dir_root = settings.get("logs", "logs")

        # 创建日志目录
        if not dir_root.startswith("/"):
            basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            log_file_path = "/".join([basedir, dir_root])
        else:
            log_file_path = dir_root
        os.makedirs(log_file_path, exist_ok=True)

        # 日志目录 + 文件名称, 只列出两种文件存储
        handlers = {
            logging.INFO: os.path.join(log_file_path, 'info.log'),
            logging.ERROR: os.path.join(log_file_path, 'error.log')
        }
        for level in handlers.keys():
            _logger = logging.getLogger(str(level))
            info_handler = TimedRotatingFileHandler(filename=os.path.abspath(handlers[level]),
                                                    when="D",
                                                    backupCount=30,
                                                    encoding="utf-8")
            _logger.addHandler(info_handler)
            _logger.setLevel(level)
            self.__loggers.update({level: _logger})

    @staticmethod
    def _format_message(level, message):
        """
        日志格式展示
        Args:
            level:
            message:
        Returns:
            [时间] [日志类型] [文件路径 行数 方法] 信息
            [2022-03-30 17:17:31] [info] [/vagrant/python/v3/db/./app/repositories.py - 37 - rep_sync_user] 666666
        """
        # for s in inspect.stack():
        #     print("=======:", s)
        frame, filename, line_no, function_name, code, un_know_field = inspect.stack()[2]
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return "[%s] [%s] [%s - %s - %s] %s" % (time_now, level, filename, line_no, function_name, message)
        # return "[%s] [%s] [%s]" % (time_now, level, message)

    def info(self, message):
        """
        正常日志
        Args:
            message:
        Returns:
        """
        self.__loggers[logging.INFO].info(self._format_message("info", message))

    def error(self, message):
        """
        错误日志
        Args:
            message:
        Returns:
        """
        self.__loggers[logging.ERROR].error(self._format_message("error", message))

    def warning(self, message):
        """
        警告日志
        Args:
            message:
        Returns:
        """
        self.__loggers[logging.INFO].warning(self._format_message("warning", message))

    def debug(self, message):
        """
        调试日志
        Args:
            message:
        Returns:
        """
        self.__loggers[logging.INFO].debug(self._format_message("debug", message))

    def critical(self, message):
        """
        不可逆的错误日志
        Args:
            message:
        Returns:
        """
        self.__loggers[logging.ERROR].critical(self._format_message("critical", message))


logger = FileLogger()

__all__ = ["logger"]
