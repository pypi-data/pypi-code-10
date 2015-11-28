import logging
import datetime as dt


# http://stackoverflow.com/questions/15727420/using-python-logging-in-multiple-modules
class MyFormatter(logging.Formatter):
    converter = dt.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s


# http://stackoverflow.com/questions/7621897/python-logging-module-globally
def setup_custom_logger(name, filename=None):
    formatter = MyFormatter(fmt='[%(asctime)s][%(module)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S.%f%z')
    # formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    if filename:
        handler = logging.FileHandler(filename)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
