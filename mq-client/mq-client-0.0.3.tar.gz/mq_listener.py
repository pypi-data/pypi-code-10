import argparse
import pika
from mq_client import AsyncMQConsumer

import logging

logging.basicConfig(filename='listener.log',
                    filemode='a',
                    level=logging.DEBUG)

logger = logging.getLogger('mq_listener')


def on_message(channel, method, header, body):
    global terminate
    # Acknowledge message receipt
    channel.basic_ack(method.delivery_tag)
    print body
    logger.info(body)


def listen_and_echo(args):
    consumer = AsyncMQConsumer(args.url,
                               on_message=on_message,
                               queue=args.queue,
                               routing_key=args.routing_key,
                               logger=logger)

    consumer.run()


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default="amqp://guest:guest@localhost:5672/%2F")
    parser.add_argument('--exchange', default="test_exchange")
    parser.add_argument('--exchange_type', default="direct")
    parser.add_argument('--queue', default="test_queue")
    parser.add_argument('--routing_key', default="mq.text")
    args = parser.parse_args()

    listen_and_echo(args)


if __name__ == "__main__":
    run()

