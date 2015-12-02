import requests, threading

class Sender(object):
    '''Responsible ONLY for sending messages on an anonymous port'''

    # Try to send over socket
    def send(self, message, target_location):
        '''
        Send a POST message to target_location. if you want encryption, you want
        to send it before this step!
        '''
        # Gather the target's location and port
        location, port = target_location.split(':')
        args = (message, location, port, )

        # Spin up a thread for the POST to occur
        sender_thread = threading.Thread(target=self.post, args=args)
        sender_thread.daemon = True
        sender_thread.start()

    def post(self, message, location, port):
        '''
        Actually send an encoded json message to the location and port
        '''
        try:
            headers = {'Accept': 'application/json',\
                        'Content-Type': 'application/json',\
                        "Connection": "close"}
            with requests.Session() as s:
                payload = {"message" : message}
                url = 'http://{0}:{1}'.format(location, port)
                r = requests.post(url, json=payload, headers=headers, timeout=1)

        except Exception as msg:
            print("ERROR @{0}: {1}".format(location, msg))
