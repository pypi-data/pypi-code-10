#
# Simple API call test. This does not use tornado ioloop. It just reads in an OTP value
# and authenticates with YubiCloud
#
import os
import sys
import logging
import tornado.ioloop

sys.path.insert(0, os.pardir)

import yubistorm
import local


def create_logger(name, loglevel=local.LOGLEVEL):
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


client = yubistorm.YubiStorm(local.YUBICLOUD_CLIENT_ID, local.YUBICLOUD_SECRET_KEY, create_logger("testapp"))
# otp = input("Please insert your YubiKey and touch it...")
# print(repr(otp))
otp = 'cccccccitnbnjhkbrhfhirlenjkntrjliingtuctcgrd'


async def main():
    global client
    global io_loop
    try:
        result = await client.verify(otp)
        print(repr(result))
    finally:
        io_loop.stop()


io_loop = tornado.ioloop.IOLoop.current()
io_loop.add_callback(main)
io_loop.start()
io_loop.close()
