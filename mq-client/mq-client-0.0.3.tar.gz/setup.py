from setuptools import setup


setup(
    name='mq-client',
    version='0.0.3',
    url='https://github.com/deginner/mq-client',
    py_modules=['mq_client', 'mq_listener', 'mq_publisher'],
    author='deginner',
    author_email='support@deginner.com',
    description='A simple pika client implementation based on the examples.',
    install_requires=['amqp', 'pika', 'tornado'],
    entry_points = """
    [console_scripts]
    mqlisten = mq_listener:run
    mqpublish = mq_publisher:run
    """
)
