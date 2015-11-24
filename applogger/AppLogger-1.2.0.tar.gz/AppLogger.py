#!/usr/bin/python
"""
    description: Applogger for logging errors to file/console
    author : Ashwani Singh
    created on : 20 Oct, 2015
"""

import logging
import os.path
from datetime import date


class SingleLevelFilter(logging.Filter):
    def __init__(self, pass_level, reject):
        self.pass_level = pass_level
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return record.levelno == self.pass_level
        else:
            return record.levelno != self.pass_level


class AppLogger:
    app_logger = ''

    @staticmethod
    def __init__(config):
        today_date_str = str(date.today())
        app_root_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
        logger_folder = config['log_folder']
        logger_dir_path = app_root_path + '/' + logger_folder + '/' + today_date_str

        # checking for logger folder
        if not os.path.exists(logger_dir_path):
            os.makedirs(logger_dir_path)

        AppLogger.logger_dir_path = logger_dir_path

        # logging format
        AppLogger.logging_format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s\n\r"

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to info
        """handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)"""

        AppLogger.app_logger = logger
        AppLogger.register_handler()

    @staticmethod
    def register_handler():
        AppLogger.add_debug_handler()
        AppLogger.add_info_handler()

    @staticmethod
    def add_info_handler():

        today_date_str = str(date.today())

        # info logger file name
        log_file_name_info = "info_"+today_date_str+".log"

        # create info file handler and set level to info
        info_fh = logging.FileHandler(os.path.join(AppLogger.logger_dir_path, log_file_name_info), "a")
        info_fh.setLevel(logging.INFO)
        formatter = logging.Formatter(AppLogger.logging_format)
        info_fh.setFormatter(formatter)
        # added filter for logging only INFO messages
        info_filter = SingleLevelFilter(logging.INFO, True)
        info_fh.addFilter(info_filter)
        AppLogger.app_logger.addHandler(info_fh)

    @staticmethod
    def add_debug_handler():

        today_date_str = str(date.today())

        # error logger file name
        log_file_name_debug = "all_"+today_date_str+".log"

        # create info file handler and set level to info
        debug_fh = logging.FileHandler(os.path.join(AppLogger.logger_dir_path, log_file_name_debug), "a")
        debug_fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(AppLogger.logging_format)
        debug_fh.setFormatter(formatter)
        # added filter for not logging INFO messages
        info_filter = SingleLevelFilter(logging.INFO, False)
        debug_fh.addFilter(info_filter)
        AppLogger.app_logger.addHandler(debug_fh)

    @staticmethod
    def info(msg):
        logging.info(msg)

    @staticmethod
    def warning(msg):
        logging.warning(msg)

    @staticmethod
    def error(msg):
        logging.error(msg)

    @staticmethod
    def critical(msg):
        logging.critical(msg)

    @staticmethod
    def exception(msg):
        logging.exception(msg)

    @staticmethod
    def debug(msg):
        # if AppLogger.app_logger.isEnabledFor(logging.DEBUG):
        logging.debug(msg)

    @staticmethod
    def start(msg):
        logging.info('-------------------------------------')
        logging.info(msg)
        logging.info('-------------------------------------')

    @staticmethod
    def end(msg):
        logging.info('-------------------------------------')
        logging.info(msg)
        logging.info('-------------------------------------')





