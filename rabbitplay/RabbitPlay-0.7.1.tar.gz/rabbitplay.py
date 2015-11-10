import pika
import ssl


class RabbitConnection(object):

    _instance = None

    def __init__(self, host='localhost', port=5672, vhost=None,
                 user=None, password=None, clean_creds=None, channel_max=None,
                 frame_max=None, heartbeat_interval=None, ca_certs=None,
                 cert_reqs=ssl.CERT_NONE, certfile=None, keyfile=None,
                 ssl_enable=False, ssl_version=ssl.PROTOCOL_SSLv23,
                 connection_attempts=None, retry_delay=None, locale=None,
                 socket_timeout=None, backpressure_detection=None):
        self.host = host
        self.port = port
        self.vhost = vhost
        self.user = user
        self.password = password
        self.clean_creds = clean_creds
        self.channel_max = channel_max
        self.frame_max = frame_max
        self.heartbeat_interval = heartbeat_interval
        self.ca_certs = ca_certs
        self.cert_reqs = cert_reqs
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_enable = ssl_enable
        self.ssl_version = ssl_version
        self.connection_attempts = connection_attempts
        self.retry_delay = retry_delay
        self.locale = locale
        self.socket_timeout = socket_timeout
        self.backpressure_detection = backpressure_detection

        self._rabbit_conn = pika.BlockingConnection(self._connection_params())

    def _credentials(self):
        return None if not self.user else pika.credentials.PlainCredentials(
                username=self.user,
                password=self.password,
                erase_on_connect=self.clean_creds
            )

    def _ssl_options(self):
        return None if not self.ssl_enable else {
            "ca_certs": self.ca_certs,
            "cert_reqs": self.cert_reqs,
            "certfile": self.certfile,
            "keyfile": self.keyfile,
            "ssl_enable": self.ssl_enable,
            "ssl_version": self.ssl_version
        }

    def _connection_params(self):
        return pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.vhost,
            credentials=self._credentials(),
            channel_max=self.channel_max,
            frame_max=self.frame_max,
            heartbeat_interval=self.heartbeat_interval,
            ssl=self.ssl_enable,
            ssl_options=self._ssl_options(),
            connection_attempts=self.connection_attempts,
            retry_delay=self.retry_delay,
            locale=self.locale,
            socket_timeout=self.socket_timeout,
            backpressure_detection=self.backpressure_detection
        )

    @classmethod
    def instance(cls, **connection_params):
        if not cls._instance or not cls._instance._rabbit_conn.is_open:
            cls._instance = RabbitConnection(**connection_params)
        return cls._instance

    @property
    def connection(self):
        return self._rabbit_conn

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def close(self):
        return self._rabbit_conn.close()


class RabbitPlay(object):

    def __init__(self, connection):
        self._rabbit_conn = connection
        self._connection = self._rabbit_conn.connection
        self._rabbit_channels = {}

    def _channel(self, queue):
        channel = self._rabbit_channels.get(queue)
        if channel and channel.is_open:
            return channel
        channel = self._connection.channel()
        channel.queue_declare(
            queue=queue,
            durable=True
        )
        self._configure_channel(channel)
        self._rabbit_channels[queue] = channel
        return channel

    def _configure_channel(self, channel):
        pass


class Producer(RabbitPlay):

    def _configure_channel(self, channel):
        channel.confirm_delivery()

    def publish(self, queue, message, exchange=''):
        return self._channel(queue).basic_publish(
            exchange=exchange,
            routing_key=queue,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )


class Consumer(RabbitPlay):

    def _configure_channel(self, channel):
        channel.basic_qos(prefetch_count=1)

    def _callback_with_ack(self, callback):
        def callback_with_ack(channel, method, properties, body):
            callback(body)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        return callback_with_ack

    def subscribe(self, queue, on_message):
        self._channel(queue).basic_consume(
            self._callback_with_ack(on_message),
            queue=queue
        )
        self._channel(queue).start_consuming()
