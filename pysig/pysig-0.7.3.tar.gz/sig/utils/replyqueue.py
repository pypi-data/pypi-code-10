import time
import threading
from sig import logger

class ReplyQueue:

    def __init__(self):

        # message counter
        self.msg_id = 0
        self.msg_id_lock = threading.Lock()

        # send lock
        self.send_lock = threading.Lock()

        # setup reply list
        self.replies = {}

        # and the corresponding lock
        self.replies_lock = threading.Lock()

    def generate_message_id(self):
        
        # ensure atomic access to counter
        self.msg_id_lock.acquire()
        self.msg_id += 1
        mid = self.msg_id
        self.msg_id_lock.release()
        return mid

    def register_wait_reply(self, message_id):

        logger.debug("[REPLY] Registering for message id %s" % (message_id))

        # lock reply dict
        self.replies_lock.acquire()

        # add the wait tuple
        # [0] - reply lock
        # [1] - reply message
        lock = threading.Lock()
        self.replies[message_id] = [lock, None]

        # it will be unlocked when the reply is received
        lock.acquire()

        # unlock reply dict
        self.replies_lock.release()

    def unregister_wait_reply(self, message_id):

        logger.debug("[REPLY] Unregistering for message id %s" % (message_id))

        # lock reply dict
        self.replies_lock.acquire()

        if self.replies.get(message_id) is not None:
            del self.replies[message_id]

        # unlock reply dict
        self.replies_lock.release()

    def wait_for_reply(self, message_id, timeout= 10.0, unregister= False):

        logger.debug("[REPLY] Waiting reply for message id %s" % (message_id))

        # get lock object for this message id
        self.replies_lock.acquire()

        entry = self.replies.get(message_id)
        if entry is None:
            self.replies_lock.release()
            return None

        lock = entry[0]
        self.replies_lock.release()

        while timeout > 0:

            # try to acquire the lock
            if lock.acquire(False) == False:
                time.sleep(0.01)
                timeout -= 0.01
                continue

            # succees
            if unregister == True:
                self.unregister_wait_reply(message_id)

            logger.debug("[REPLY] Reply received for message id %s" % (message_id))

            # return stored data
            return entry[1]

        logger.warning("[REPLY] Reply NOT received for message id %s" % (message_id))

        # timeout
        if unregister == True:
            self.unregister_wait_reply(message_id)

        return None

    def notify_reply(self, message_id, reply):
        
        # lock reply dict
        self.replies_lock.acquire()
        entry = self.replies.get(message_id)
        self.replies_lock.release()

        # entry not found
        if entry is None:
            return False

        # store reply and notify receive thread
        entry[1] = reply
        entry[0].release()
        return True
