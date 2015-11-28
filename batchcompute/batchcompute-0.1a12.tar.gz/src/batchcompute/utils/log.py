import logging

import constants 

def set_log_level(loglevel='WARNING'):
    if hasattr(logging, loglevel.upper()):
        level = getattr(logging, loglevel.upper())
        constants.LOG_LEVEL = level
        constants.LOG_HANDLER.setLevel(level)

        for logname, logger in constants.ALL_LOGS.items():
            logger.setLevel(level)
    else:
        # XXX a warning.warn() should be raised. 
        pass

def get_logger(logname):
    if not constants.LOG_HANDLER:
        constants.LOG_HANDLER = logging.FileHandler(constants.LOG_FILE_NAME) 
        constants.LOG_HANDLER.setLevel(constants.LOG_LEVEL)
        formatter = logging.Formatter(constants.LOG_FORMATTER)
        constants.LOG_HANDLER.setFormatter(formatter)
        root_logger = logging.getLogger("batchcompute")
        root_logger.addHandler(constants.LOG_HANDLER)

    logger = None
    if logname in constants.ALL_LOGS:
        logger = constants.ALL_LOGS[logname]
    else:
        logger = logging.getLogger(logname) 
        logger.setLevel(constants.LOG_LEVEL)
        constants.ALL_LOGS[logname] = logger
    return logger 
