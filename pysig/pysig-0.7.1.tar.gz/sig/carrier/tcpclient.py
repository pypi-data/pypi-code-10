import socket
import threading
import time
from sig import Carrier, logger, stringify_object
from sig.utils.replyqueue import * 

#
# TODO: call handle_client_connected
#

class CarrierTCPClient(Carrier):

    def __init__(self):
        Carrier.__init__(self)

        self.auto_reconnect = True

        self.server_address = None
        self.socket = None
        self.clientid = id(self) # simply choose something that will fit
        self.thread = None
        self.thread_reconnect = None

        # callbacks
        self.on_connected = None
        self.on_disconnected = None

        # send lock
        self.send_lock = threading.Lock()

        # reply queue
        self.reply_queue = ReplyQueue()
    
    def _thread_reconnect(self):

        logger.debug("[TCP_CL] Auto reconnect to %s" % (str(self.server_address)))

        while True:

            # attempt reconnect
            response = self.connect( self.server_address[0], self.server_address[1])

            # reconnected, kill reconnect thread
            if response == True:
                break

            if self.auto_reconnect == False:
                break

            # post-pone
            time.sleep(5)
        
        self.thread_reconnect = None
        logger.debug("[TCP_CL] Auto reconnect finished")

    def _start_reconnect(self):

        # start thread
        thread = threading.Thread(target=self._thread_reconnect)
        thread.daemon = True
        thread.start()

        self.thread_reconnect = thread

    def _thread_receive(self):

        logger.info("[TCP_CL] Started receive thread for %s:%s" % (self.server_address[0], self.server_address[1]))

        try:
            while True:

                # receive
                data = self.socket.recv(4096)
                if data is None or data == "":
                    logger.info("[TCP_CL]) recv returned nothing, exiting")
                    break # done

                # unpack
                message = self.unpack(data)
                if message is None:
                    continue

                logger.debug("[TCP_CL] Message received %s" % (stringify_object(message)))

                # is it a reply?
                if message.get("status") is not None:

                    # get message id
                    message_id = message.get("id")
                    if message_id is None:
                        logger.critical("[TCP_CL] Reply doesn't have any ID associated %s" % (stringify_object(message)))
                        continue

                    logger.debug("[TCP_CL] Message is a reply (id:%s)" % (message_id))

                    # notify reply
                    self.reply_queue.notify_reply(message_id, message)
                    continue

                # invoke receive handler
                reply = self.handleRX(self.clientid, message)

                logger.debug("[TCP_CL] Replying with %s" % (stringify_object(reply)))

                # pack reply
                data = self.pack(reply)
                if data is None:
                    continue

                # send
                self.socket.sendall(data)

        except Exception as e:
            logger.critical("[TCP_CL] Exception in receive thread: %s" % (e))

        logger.info("[TCP_CL] Receive thread terminated")

        # close socket
        if self.socket is not None:
            self.socket.close()

        # reset refs
        self.thread = None
        self.socket = None

        # run disconnect handler
        self.handle_client_disconnected(self.clientid)

        # initiate auto-reconnect
        if self.auto_reconnect: 
            self._start_reconnect()
        return
            
    
    #
    # Inherited methods
    #
    
    def handle_client_connected(self, clientid):
        Carrier.handle_client_connected(self, clientid)

        if self.on_connected is not None:
            try: self.on_connected()
            except Exception as e: 
                logger.critical("[TCP_CL] on_connected callback (exception: %s)" % (e))

    def handle_client_disconnected(self, clientid):
        Carrier.handle_client_disconnected(self, clientid)

        if self.on_disconnected is not None:
            try: self.on_disconnected()
            except Exception as e: 
                logger.critical("[TCP_CL] on_disconnected callback (exception: %s)" % (e))

    def handleTX(self, clientid, message):
        
        # add an ID to it
        message_id = self.reply_queue.generate_message_id()
        self.reply_queue.register_wait_reply(message_id)

        # add id to message
        message["id"] = message_id
        logger.debug("[TCP_CL] Sending message %s" % (stringify_object(message)))

        # pack
        data = self.pack(message)
        if data is None:
            self.reply_queue.unregister_wait_reply(message_id)
            return None

        # send
        self.send_lock.acquire()
        
        try: 
            self.socket.sendall(data)
        except Exception as e:
            logger.critical("[TCP_CL] Failed to send message (%s) %s" % (e, stringify_object(message)))
            
            self.reply_queue.unregister_wait_reply(message_id)
            self.send_lock.release()
            raise

        self.send_lock.release()

        # wait for reply
        reply = self.reply_queue.wait_for_reply(message_id, unregister= True)
        if reply is None:
            logger.error("[TCP_CL] Failed to receive reply '%s' for message %s" % (message_id, stringify_object(message)))
            return None
        
        logger.debug("[TCP_CL] Reply is %s" % (stringify_object(reply)))
        return reply

    #
    # Own methods
    #
    
    def connect(self, host, port):

        if self.socket is not None:
            return False # already connected

        logger.info("[TCP_CL] Connecting to %s:%s" % (host, port))

        # create socket and connect
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.socket.connect( (host, port) )
        except Exception as e:
            logger.error("[TCP_CL] Failed to connect to %s:%s (%s)" % (host, port, e))
            
            self.socket = None
            if self.auto_reconnect == True and self.thread_reconnect is None:
                self._start_reconnect()
            return False

        # start thread
        thread = threading.Thread(target=self._thread_receive)
        thread.daemon = True
        thread.start()

        self.thread = thread

        # run callback
        self.handle_client_connected(self.clientid)
        return True

    def disconnect(self):

        # disable automatic reconnect
        self.auto_reconnect = False
        thread_reconnect = self.thread_reconnect

        # close reconnect thread
        if thread_reconnect is not None:
            logger.debug("[TCP_CL] Waiting for reconnect thread")
            thread_reconnect.join()
            logger.debug("[TCP_CL] Done")

        # close receive thread
        if self.socket is not None:
            logger.debug("[TCL_CL] Waiting for receive thread")
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.thread.join()
            self.thread = None
            self.socket = None
            logger.debug("[TCP_CL] Done")

        return True

    def isConnected(self):
        return self.socket is not None