import sys
import logging


class GensendLogger(logging.Logger):
    def __call__(self, *args, **kwargs):
        return self.debug(*args, **kwargs)


def configure_logger(name, level=logging.DEBUG):
    logging.captureWarnings(True)
    logging.setLoggerClass(GensendLogger)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(name)s.%(levelname)s: %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


log = configure_logger('gensend', logging.DEBUG)
