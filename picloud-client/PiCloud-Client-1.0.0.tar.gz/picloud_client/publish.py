from picloud_client.connection import connection


def publish(event, data):
    message = {
        'action': 'publish',
        'event': event,
        'data': data
    }
    connection.send(message)
