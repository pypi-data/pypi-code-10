__author__ = 'meatpuppet'

import logging
from logging.handlers import RotatingFileHandler
import os

formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def log(bot, msg):
    if not os.path.exists(bot.settings['muc_logging']):
        os.makedirs(bot.settings['muc_logging'])
    room = msg.get('from').bare
    logger = logging.getLogger(room)
    filehandler = RotatingFileHandler(os.path.join(bot.settings['muc_logging'], room + '.log'))
    filehandler.setFormatter(formatter)

    logger.addHandler(filehandler)
    logger.info('%s: %s' % (msg['mucnick'], msg['body']))
