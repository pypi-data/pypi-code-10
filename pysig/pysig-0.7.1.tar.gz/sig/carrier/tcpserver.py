import threading
import time
import SocketServer
import socket

from sig import Carrier, logger, stringify_object
from sig.utils.replyqueue import *

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def setup(self):

        # current thread reference
        self.thread = threading.currentThread()

        # send lock
        self.send_lock = threading.Lock()

        # reply queue
        self.reply_queue = ReplyQueue()

        # copy carrier reference from server
        self.carrier = self.server.carrier

        # register as connection handler
        self.carrier._register_handler(id(self), self)

    def finish(self):
        # unregister as connection handler
        self.carrier._unregister_handler(id(self), self)

    # rx
    def handle_receive(self, data):
        
        # unpack
        message = self.carrier.unpack(data)
        if message is None:
            logger.critical("[TCP_SRV] Message could not be unpacked %s" % (stringify_object(data)))
            return

        logger.debug("[TCP_SRV] Received message %s" %  (stringify_object(message)))

        # is it a reply?
        # if it is, don't call handleRX, just store it
        if message.get("status") is not None:

            message_id = message.get("id")
            if message_id is None:
                logger.critical("[TCP_SRV] Reply doesn't have any ID associated %s" % (stringify_object(message)))

            logger.debug("Received reply with id: %s" % (message_id))

            # store reply
            self.reply_queue.notify_reply(message_id, message)
            return

        # invoke receive handler from Carrier
        reply = self.carrier.handleRX(id(self), message)
        if reply is None:
            logger.warning("[TCP_SRV] No reply for message")
            return # no reply

        logger.debug("[TCP_SRV] Sending back reply %s" % (stringify_object(reply)))

        # pack reply
        message = self.carrier.pack(reply)
        if message is None:
            logger.critical("[TCP_SRV] Message could not be packed %s" % (stringify_object(message)))
            return

        # send reply
        self.request.sendall(message)

    def handle(self):

        while True:
            data = self.request.recv(4096)
            if len(data) == 0: break
            try:
                self.handle_receive(data)
            except Exception as e:
                logger.critical("[TCP_SRV] Exception while handling receive %s" % (e))
                break


    # txmit
    def handleTX(self, message):

        logger.debug("[TCP_SRV] Sending message %s" % (stringify_object(message)))

        # add an ID to it
        message_id = self.reply_queue.generate_message_id()
        self.reply_queue.register_wait_reply(message_id)

        # add id to message
        message["id"] = message_id

        # pack
        data = self.carrier.pack(message)
        if data is None:
            self.reply_queue.unregister_wait_reply(message_id)
            return None

        # send
        self.send_lock.acquire()
        
        try: self.request.sendall(data)
        except:
            logger.critical("[TCP_SRV] Failed to send message %s" % (stringify_object(message)))

            self.reply_queue.unregister_wait_reply(message_id)
            self.send_lock.release()
            raise

        self.send_lock.release()

        # wait for reply
        reply = self.reply_queue.wait_for_reply(message_id, unregister= True)
        if reply is None:
            logger.error("[TCP_SRV] Failed to receive reply '%s' for message %s" % (message_id, stringify_object(message)))
            raise

        logger.debug("[TCP_SRV] Reply is %s" % stringify_object(reply))
        
        return reply


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    carrier = None

    def shutdown(self):
        # call upper class
        SocketServer.TCPServer.shutdown(self)

class CarrierTCPServer(Carrier):
    
    def __init__(self):
        Carrier.__init__(self)
        self.tcp_handlers = {}
        self.server = None
        self.server_thread = None

    def _register_handler(self, clientid, handler):
        logger.info("[TCP_SRV] Client connected (clientid: %s)(addr: %s)" % (clientid, handler.client_address))
        self.tcp_handlers[clientid] = handler

        # invoke Carrier methods
        self.handle_client_connected(clientid)

    def _unregister_handler(self, clientid, handler):
        logger.info("[TCP_SRV] Client disconnected (clientid: %s)(addr: %s)" % (clientid, handler.client_address))
        del self.tcp_handlers[clientid]

        # invoke Carrier method
        self.handle_client_disconnected(clientid)

    #
    # Inherited methods
    #

    def handleTX(self, clientid, data):

        # search handler for this clientid
        tcp_handler = self.tcp_handlers.get(clientid)
        if tcp_handler is None:
            logger.error("[TCP_SRV] Handle TX failed to find handler (clientid: %s)" % (clientid))
            return None
 
        # forward this request to handler
        return tcp_handler.handleTX(data)

    #
    # Own methods
    #

    def start(self, host, port):
        
        if self.server is not None:
            return False

        logger.info("[TCP_SRV] Starting to listen on %s:%s" % (host, port))

        # make new server
        self.server = ThreadedTCPServer( (host, port), ThreadedTCPRequestHandler)
        self.server.carrier = self # backref

        # make new thread
        self.server_thread = threading.Thread(target=self.server.serve_forever)

        # daemonize and start thread
        self.server_thread.daemon = True
        self.server_thread.start()

        return True

    def stop(self):

        if self.server is None:
            return False

        # close server socket
        self.server.shutdown()
        self.server.server_close()
        self.server = None
        self.server_thread = None

        # copy clients dictionary
        tcp_handlers = self.tcp_handlers.copy()

        # disconnect all clients
        for clientid, handler in tcp_handlers.iteritems():
            logger.info("[TCP_SRV] Diconnecting %s (clientid:%s)" % (handler.client_address, clientid))
            handler.request.shutdown(socket.SHUT_RDWR)
            handler.request.close()

        logger.info("[TCP_SRV] Waiting for clients to close")

        # wait for all threads
        for clientid, handler in tcp_handlers.iteritems():
            handler.thread.join()

        logger.info("[TCP_SRV] Stopped")
        return True
