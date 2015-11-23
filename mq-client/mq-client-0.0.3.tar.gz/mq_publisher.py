import argparse
import pika
from mq_client import AsyncMQPublisher
import logging

logging.basicConfig(filename='command.log',
                    filemode='a',
                    level=logging.DEBUG)

logger = logging.getLogger('mq_command')

def client_pub(args):
    def producer(publisher):
        logger.info("publishing %s" % args.message)
        publisher.publish(args.message)
        publisher._connection.close()
        try:
            publisher.stop()
        except Exception as e:
            pass

    publisher = AsyncMQPublisher(args.url,
                                 producer=producer,
                                 exchange=args.exchange,
                                 queue=args.queue,
                                 routing_key=args.routing_key,
                                 logger=logger)
    publisher.run()


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('message', help='the message to publish')
    parser.add_argument('--url', default="amqp://guest:guest@localhost:5672/%2F")
    parser.add_argument('--exchange', default="test_exchange")
    parser.add_argument('--exchange_type', default="direct")
    parser.add_argument('--queue', default="test_queue")
    parser.add_argument('--routing_key', default="")
    args = parser.parse_args()

    client_pub(args)


if __name__ == "__main__":
    run()

