import json
import inspect

EVENT_CONNECT = "#connect"
EVENT_DISCONNECT = "#disconnect"
CHANNEL_DECORATOR = "#"

#
# Logging
#

class LOG_LEVELS:
    LEVEL_TRACE = 0
    LEVEL_DEBUG = 10
    LEVEL_INFO = 20
    LEVEL_WARNING = 30
    LEVEL_ERROR = 40
    LEVEL_CRITICAL = 50
    LEVEL_NONE = 100

    LEVEL_NAMES  = {
        0  : "trace",
        10 : "debug",
        20 : "info",
        30 : "warning",
        40 : "error",
        50 : "critical"
    }

class _RouteLogger:
    def __init__(self, logger):
        self.obj = logger

    def trace(self, text):      self.obj.trace(text)
    def debug(self, text):      self.obj.debug(text)
    def info(self,text):        self.obj.info(text)
    def warning(self,text):     self.obj.warning(text)
    def error(self,text):       self.obj.error(text)
    def critical(self,text):    self.obj.critical(text)

class NullLogger:
    def trace(self, text):      pass
    def debug(self, text):      pass
    def info(self,text):        pass
    def warning(self,text):     pass
    def error(self,text):       pass
    def critical(self,text):    pass

class SimpleLogger:

    def __init__(self, tag="[sig]", level= LOG_LEVELS.LEVEL_INFO):
        self.tag = tag
        self.level = level

    def do_print(self, level, text):
        # discard message
        if(level < self.level):
            return

        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)

        # do print
        level_str = LOG_LEVELS.LEVEL_NAMES.get(level,"")
        print "%s[%4.4s][%20.40s][%8.8s]-%s" % (self.tag, calframe[2][2], calframe[2][3], level_str, text)

    def trace(self, text):
        self.do_print(LOG_LEVELS.LEVEL_TRACE, text)

    def debug(self, text):
        self.do_print(LOG_LEVELS.LEVEL_DEBUG, text)

    def info(self, text):
        self.do_print(LOG_LEVELS.LEVEL_INFO, text)

    def warning(self, text):
        self.do_print(LOG_LEVELS.LEVEL_WARNING, text)

    def error(self, text):
        self.do_print(LOG_LEVELS.LEVEL_ERROR, text)

    def critical(self, text):
        self.do_print(LOG_LEVELS.LEVEL_CRITICAL, text)


logger = _RouteLogger(NullLogger())

def setup_logger(objlogger):
    global logger
    logger.obj = objlogger

def stringify_object(object):
    return "\n--begin--\n%s\n--end--\n" % (
            json.dumps(object, indent= 4, sort_keys= True)
        )

#
# TODO: listener class
#

class Listener:
    def __init__(self):
        pass

#
# EVENT class
#

def hasChannelDecorator(name):
    return True if \
            name is not None \
            and (type(name) is str or type(name) is unicode) \
            and name[0] == CHANNEL_DECORATOR \
            else False

def isBuiltinEvent(name):
    return True if \
            name is not None \
            and (type(name) is str or type(name) is unicode) \
            and (name == EVENT_CONNECT or name == EVENT_DISCONNECT) \
            else False

class Event:
    def __init__(self, objsender, name):

        # initialize
        self.listeners = []
        self.name = name
        self.objsender = objsender

        # check if it's a channel event
        ischannel = hasChannelDecorator(name)

        # if it's a channel event add it to router
        if ischannel and objsender.name is not None:
            self.channel = self.objsender.objrouter.getSender(None).getEvent(name, create= True)
        else:
            self.channel = None

        logger.trace("Event '%s' created for sender '%s" % (name, objsender.getName()))

    def getListeners(self):
        return self.listeners

    def getSender(self):
        return self.objsender

    def getName(self):
        return self.name

    def isChannel(self):
        return self.channel is not None

#
# SENDER class
#

class Sender:
    def __init__(self, objrouter, name):
        
        self.events = {}
        self.name = name
        self.objrouter = objrouter
        self.connected_sender = False

        # classes
        self.class_event  = objrouter.class_event
        self.class_signal = objrouter.class_signal

        # add broadcaster event
        self.events[None] = self.class_event(self, None)
        
        # add default events, if sender is not special broadcaster
        if name is not None:
            self.events[EVENT_CONNECT   ] = self.class_event(self, EVENT_CONNECT   )
            self.events[EVENT_DISCONNECT] = self.class_event(self, EVENT_DISCONNECT)

        # request handler
        self.requests = None
        
        logger.trace("Sender '%s' created" % (name))
    
    def setRequests(self, requests):
        self.requests = requests

    def isConnected(self):
        return self.connected_sender

    def getRouter(self):
        return self.objrouter

    def getName(self):
        return self.name

    def getEvents(self):
        return self.events

    def request(self, method, params= None):

        logger.debug("[SENDER] Sender '%s' request '%s'" % (self.name, method))

        # check method
        if method is None:
            logger.error("[SENDER] Request for sender '%s' with undefined method" % (self.name))
            raise ValueError("method undefined")

        # check request handler
        if self.requests is None:
            logger.error("[SENDER] Sender '%s' doesn't support requests" % (self.name))
            raise LookupError("requests not supported")

        # search method or invoke default handler
        handler = self.requests.get(method, None)
        if handler is None:

            # search default handler
            handler = self.requests.get(None, None)
            if handler is None:
                logger.error("[SENDER] Sender '%s' request handler for '%s' not found (no default handler)" % (self.name, method))
                raise LookupError("method %s not found" % (method))

            try: 
                response = handler(method, params)
                return response # reply
            except Exception as e:
                logger.error("[SENDER] Sender '%s' request '%s' failed in default handler (%s)" % (self.name, method, e))
                raise e

        # execute handler
        try:
            response = handler(params)
            return response # reply
        except Exception as e:
            logger.error("[SENDER] Sender '%s' request '%s' failed (%s)" % (self.name, method, e))
            raise e

        # should not reach
        return None

    def getEvent(self, event, create= False):
    
        # lookup
        objevent = self.events.get(event)
        
        # create if it doesn't exist
        if objevent is None:
            if create == True:

                # instantiate new event
                objevent = self.class_event(self, event)
                self.events[event] = objevent
                return objevent

        return objevent

    def addListener(self, listener, event= None):
      
        #
        # subscribe to an unconnected sender or
        # subscribe to broadcast sender for channel events
        # that must be created automatically
        #
        if self.isConnected() == False or self.name is None:
            objevent = self.getEvent(event, create= True)
            objevent.listeners.append(listener)
            return True

        # search event, and register listener
        objevent = self.events.get(event)
        if objevent is None:
            return False

        objevent.listeners.append(listener)
        return True

    def removeListener(self, listener, event= None):
      
        # search event, and remove listener
        objevent = self.events.get(event)
        if objevent is None:
            return False

    	# search listener in list, and fail if not found
    	if listener not in objevent.listeners:
    	  return False

        objevent.listeners.remove(listener)
        
        # self-destroy if no more listeners, and sender is disconnected
        # todo: optimize countListeners()
        if self.connected_sender == False and self.countListeners() == 0:
            del self.objrouter.senders[self.name]
        return True

    def getSignal(self, event):

        # get main event
        objevent = self.getEvent(event)
        if objevent is None: 
            return None

        # get broad events
        broad_events = [
                # router broadcast event
                self.objrouter.senders[None].events[None],

                # sender broadcast event
                self.events[None] ]

        # append channel event
        if objevent.channel is not None:
            broad_events.append(objevent.channel)

        return self.class_signal(objevent, broad_events)

    def countListeners(self):
        cnt = 0
        for eventname, objevent in self.events.iteritems():
            cnt += len(objevent.listeners)
        return cnt

    def hasListeners(self):
        for eventname, objevent in self.events.iteritems():
            if len(objevent.listeners) > 0:
                return True
        return False

    def remove(self):
        return self.objrouter.removeSender(self)

    #
    # private methods
    #

    # uppon sender registration connect selected events
    # and detach previous registrations to unsupported events
    def _connectEvents(self, events):
        
        # detach unknown events
        detach_events = [event
            for event in self.events
            if  event is not None and
                event != EVENT_CONNECT and
                event != EVENT_DISCONNECT and
                event not in events]

        for event in detach_events:
            logger.warning("detaching event %s from %s" % (event, self.name))
            del self.events[event]

        # connect events
        for event in events:
            self.getEvent(event, create= True)

    def _connect(self):
        if self.connected_sender: return

        # promote what sender supports (exclued broadcast event)
        data = {
            "events"   : 
                [e for e in self.events.iterkeys() if e is not None],
            "requests" : 
                None if self.requests is None else
                    [r for r in self.requests.iterkeys()],                
        }

        self.connected_sender = True
        self.getSignal(EVENT_CONNECT).trigger(data)

    def _disconnect(self):
        if not self.connected_sender: return

        # promote what sender supported (exclued broadcast event)
        data = {
            "events"   : 
                [e for e in self.events.iterkeys() if e is not None],
            "requests" : 
                None if self.requests is None else
                    [r for r in self.requests.iterkeys()],                
        }

        self.connected_sender = False
        self.setRequests(None)
        self.getSignal(EVENT_DISCONNECT).trigger(data)
 
#
# SIGNAL class
#

class Signal:
    def __init__(self, objevent, broad_events):

        # store broad events
        self.broad_events = broad_events

        # prepare event information
        objsender = objevent.getSender()
        self.event_info = {
                "sender" : objsender.getName(),
                "event"  : objevent.getName()
            }

        # back reference
        self.objsender = objsender
        self.objevent  = objevent

    def trigger(self, data):

        # run broad events
        for event in self.broad_events:
            for listener in event.listeners:
                listener(self.event_info, data)

        # run event
        for listener in self.objevent.listeners:
            listener(self.event_info, data)

#
# ROUTER class
#

class Router:
    def __init__(self, 
            class_sender = Sender,
            class_signal = Signal,
            class_event  = Event ):

        self.senders = {}

        # classes
        self.class_sender = class_sender
        self.class_event  = class_event
        self.class_signal = class_signal

        # add broadcaster grup
        broadsender = class_sender(self, None)
        broadsender.connected_sender = True
        self.senders[None] = broadsender
    
    def __repr__(self):
        
        #
        # in case some derived class registers
        # listeners of theirselfes, like ClientRouter does
        # the router object will try to make a string
        # representation of itself, recursively
        #
        if getattr(self, "_printing", False): 
            return "myself"

        ret = ""
        self._printing = True

        # senders
        for sendername, objsender in self.senders.iteritems():
            if sendername is None: sendername = "*"
            ret += "[%s] (%s)\n" % (sendername, objsender.isConnected())

            # events
            for eventname, objevent in objsender.events.iteritems():
                if eventname is None: eventname = "*"
                
                ret += "-|  %s\n" % eventname
                # listeners
                for listener in objevent.listeners:
                    ret += "-|--> %s\n" % str(listener)
        
        self._printing = False

        return ret
    
    def addListener(self, listener, sender= None, event= None):

        # find sender and add listener
        objsender = self.getSender(sender, create= True)
        return objsender.addListener(listener, event)

    def removeListener(self, listener, sender=None, event=None):

        # find sender and remove listener
        objsender = self.getSender(sender)
        if objsender is None:
            return False

        return objsender.removeListener(listener, event)

    def addSender(self, sender, events, requests= None):

        # validate input
        if sender is None:
            raise ValueError("no given sender name")

        if events is None and requests is None:
            raise ValueError("no events or requests registered for sender %s" % (sender))

        # create sender
        objsender = self.getSender(sender, create=True)

        if objsender.isConnected() == True:
            raise NameError("sender %s is already connected" % (sender))

        # you can pass a single event
        if type(events) is not list:
            events = [events]

        # setup request handler
        objsender.setRequests(requests)

        # attach given events to the sender
        objsender._connectEvents(events)

        # trigger connect
        objsender._connect()
        return objsender

    def getSender(self, sender, create=False):

        # get or create sender
        objsender = self.senders.get(sender)
        if objsender is None:
            if create:
                objsender = self.class_sender(self, sender)
                self.senders[sender] = objsender
            else:
                return None

        return objsender

    def removeSender(self, sender):

        # don't allow removing broadcast sender
        if sender is None:
            raise ValueError("cannot remove broadcast sender")

        # parameter is sender object
        if isinstance(sender, Sender):

            # wrong router
            if sender.objrouter != self:
                return False

            objsender = sender
            sender    = objsender.getName()
        else:
        # parameter is sender identifier
            objsender = self.getSender(sender)
            if objsender is None:
                return False

        if objsender.isConnected() == False:
            return False # already disconnected

        # trigger disconnect
        objsender._disconnect()

        # destroy sender only if it has no listeners
        try:
            if not objsender.hasListeners():
                del self.senders[sender]
        except Exception as e:
            logger.critical("[R] failed to remove sender %s" % (sender))
            raise

        return True

    def request(self, sender, method, params= None):

        # lookup sender
        objsender = self.getSender(sender)
        if objsender is None or objsender.isConnected() == False:
            raise NameError("Sender %s is not connected" % (objsender.getName()))

        # invoke
        return objsender.request(method, params= params)

#
# The Carrier class is responsible for defining a common API
# for transporting messages to and from a client to and from a
# certain server or node.
#
# The Carrier class also implements a packing/unpacking method
# that can be overrided (if desired) by the class that implements
# the transport. The default implementation uses JSON encoding.
#

class Carrier:

    def __init__(self):
        self.callback_rx = None
        self.methods = None
        self.callback_client_connected = None
        self.callback_client_disconnected = None
        self.callback_all_clients_disconnected = None

    def unpack(self, data):
        try:
            obj = json.loads(data)
            return obj
        except Exception as e:
            logger.critical("Unpack failed: %s" % (e))
        return None

    def pack(self, message):
        try:
            content = json.dumps(message)
            return content
        except Exception as e: 
            logger.critical("Pack failed: %s" % (e))
        return None
 
    #
    # Handles the messages received.
    #
    # The 'data' parameter holds the unpacked message and the
    # result of the function must holds the response that must be
    # sent back.
    #
    # Therefore the class that implements the transport is required
    # to handle unpacking data received and also packing the reply.
    #
    # if the response is 'None', nothing is sent back to the client.
    #

    def handleRX(self, clientid, data):
        if self.callback_rx:
            self.callback_rx(clientid, data)

        if self.methods is not None:
            return self.handleRPC(clientid, data)

        return None

    def handleRPC(self, clientid, data):
 
        reply = None

        # extract message id
        # Note: the id field is kept for tracking replies;
        #       it is returned in the reply message, in the
        #       exact form that was sent in the original
        #       message by the client or server.
        message_id = data.get("id")
        
        # extract method
        method = data.get("method")
        if method is None:
            logger.critical("[CARRIER] No method defined in RPC message %s" % (stringify_object(data)))
            reply = { "id" : message_id, "status" : -3 }
            return reply
        
        # extract params and prepare reply
        params = data.get("params")

        logger.debug("[CARRIER] Method invoked %s" % (method))

        # methods expect a valid dictionary for params,
        # even if empty
        if params is None: params = {}

        # extract method from list
        fnmethod = self.methods.get(method)

        # method not found
        if fnmethod is None:
            logger.critical("[CARRIER] No method '%s' found for RPC message %s" % (method, stringify_object(data)))
            reply = { "id" : message_id, "status" : -1 }
            return reply

        # run handler and pack response
        try:
            response = fnmethod(clientid, params)
            reply = {
                    "id"       : message_id,
                    "status"   : 0,
                    "response" : response
                }

        except Exception as e:
            logger.critical("[CARRIER] Failed running method '%s' defined in RPC message %s\nException: %s" % (
                method, 
                stringify_object(data),
                e ))

            reply = { "id" : message_id, "status" : -2, "exception" : str(e) }
            #raise

        return reply

    # 
    # Handle sending the messages.
    #
    # The 'data' parameter hold the unpacked message and the response
    # represents the unpacked reply that must be sent back.
    #
    def handleTX(self, clientid, data):
        pass

    #
    # Handlers that are run when a client is connected/disconnected
    #

    def handle_client_connected(self, clientid):
        if self.callback_client_connected:
            self.callback_client_connected(clientid)

    def handle_client_disconnected(self, clientid):
        if self.callback_client_disconnected:
            self.callback_client_disconnected(clientid)

    #
    # all clients disconnected handler, is run only in case of a server
    #

    def handle_all_clients_diconnected(self):
        if self.callback_all_clients_disconnected:
            self.callback_all_clients_disconnected()

#
# CLIENT
#

class ClientRouter(Router):

    def __init__(self, carrier):
        Router.__init__(self)

        # register of remote  senders and listeners
        self.server_senders = []
        self.server_listeners = {}

        # register to carrier
        self.carrier = carrier
        carrier.methods = {
                "signal"  : self.handle_signal,
                "request" : self.handle_request
                }

        # connect/disconnect handlers
        carrier.callback_client_connected = \
            self.handle_client_connected
        carrier.callback_client_disconnected = \
            self.handle_client_disconnected

    def _clientSendMessage(self, message):

        # send
        try:
            reply = self.carrier.handleTX(str(id(self)), message)
        except Exception as e:
            logger.critical("[CR] Failed to send message (clientid: %s)(exception %s)" % (id(self), e))
            return None

        if reply is None:
            logger.error("[CR] No reply for message %s" % (stringify_object(message)))
            return None

        # check status
        status = reply.get("status")
        if status is None:
            logger.error("[CR] Reply has no status field %s" % (stringify_object(reply)))
            return None

        # check status code
        if status != 0:
            logger.error("[CR] Client call failed (status:%s)\nMessage:%sReply:%s" % 
                (str(status), stringify_object(message), stringify_object(reply)))
            return None

        # check response
        response = reply.get("response")
        if response is None:
            response = {}
        return response

    def handle_client_connected(self, clientid):
        logger.debug("[CR] Method: client_connected")
        
        # reset
        self.server_senders = []
        self.server_listeners = {}

    def handle_client_disconnected(self, clientid):
        logger.debug("[CR] Method: client_disconnected")

        # destroy all previously registered senders
        for objsender in self.server_senders:
            objsender.removeListener(self._signal_cbk_forward_to_server)
            objsender.remove()

        # reset
        self.server_senders = []
        self.server_listeners = {}

    def handle_signal(self, clientid, params):

        logger.debug("[CR] Method: handle_signal Clientid: %s Params: %s" % (clientid, params))

        # extract message data
        listener_id = params.get("listener_id")
        data        = params.get("data")
        info        = params.get("info")

        # check listener_id
        if listener_id is None:
            raise Exception("listener_id not given")

        # check info
        if info is None:
            raise Exception("info is not provided")

        # find listener
        listener = self.server_listeners.get(listener_id)
        if listener is None:
            raise LookupError("listener id %s not found" % (listener_id))

        # execute
        listener(info, data)
        return None

    def handle_request(self, clientid, params):

        logger.debug("[CR] Method: handle_request Clientid: %s Params: %s" % (clientid, params))

        # extract message data
        sender     = params.get("sender")
        req_method = params.get("method")
        req_params = params.get("params")

        if sender is None or req_method is None:
            raise Exception("invalid arguments: sender or method are missing")

        # find sender
        objsender = self.getSender(sender)
        if objsender is None:
            raise LookupError("sender %s not found" % (sender))

        # execute
        return objsender.request(req_method, req_params)

    #
    # Main purpose of this callback is to forward all
    # events from remote registered senders, to the connected 
    # server.
    #
    def _signal_cbk_forward_to_server(self, info, data):

        logger.debug("[CR] Forwarding signal '%s' to remote router" %(info))

        # craft message
        message = {
                "method" : "signal",
                "params" : {
                    "info" : info,
                    "data" : data }
                }

        # send it
        # TODO: log error
        self._clientSendMessage(message)

    def addRemoteSender(self, sender, events, requests= None):

        logger.debug("[CR] addRemoteSender(%s,%s)" % (sender, events))

        # prepare the list of supported requests
        if requests is not None:
            requests_list = [r for r in requests.iterkeys()]
        else:
            requests_list = None

        # do add sender
        objsender = self.addSender(sender, events, requests= requests)
        if objsender is None:
            return None

        # mark sender as being remote
        setattr(objsender, "remote", True)

        # any events from this sender will be sent to server
        objsender.addListener(self._signal_cbk_forward_to_server)

        # craft message
        message = {
                "method" : "add_sender",
                "params" : {
                    "sender" : sender,
                    "events" : events,
                    "requests" : requests_list
                    }
                }

        # send
        # TODO: check error message
        self._clientSendMessage(message)

        # register remote sender
        self.server_senders.append(objsender)
        return objsender

    def removeRemoteSender(self, sender):

        logger.debug("[CR] removeRemoteSender(%s)" % (sender))

        if isinstance(sender, Sender):
            senderobj = sender
            sender    = senderobj.getName()
        else:
            senderobj = self.getSender(sender)
            if senderobj is None:
                return False # not found

        # not a remote sender?
        if getattr(senderobj, "remote", False) == False:
            logger.error("[CR] Sender '%s' is not a remote sender" % (sender))
            return False

        # unregister listener from this sender
        senderobj.removeListener(self._signal_cbk_forward_to_server)

        # craf message
        message = {
                "method" : "remove_sender",
                "params" : {
                    "sender" : sender 
                    }
                }

        # send
        # TODO: check error message
        self._clientSendMessage(message)

        # remove sender
        senderobj.remove()

        # remove from register
        del self.server_senders[senderobj]
        return True

    def addRemoteListener(self, listener, sender, event):

        logger.debug("[CR] addRemoteListener(%s,%s,%s)" % (listener, sender, event))

        # craft message
        message = {
                "method" : "add_listener",
                "params" : {
                    "sender" : sender,
                    "event"  : event
                    }
                }

        # send
        response = self._clientSendMessage(message)
        if response is None:
            return False

        # get listener_id
        listener_id = response.get("listener_id")
        if listener_id is None:
            logger.error("[CR] Registering listener failed (sender:%s) (event:%s)" % (sender, event))
            return False

        # map listener_id to listener object
        self.server_listeners[listener_id] = listener
        return True

    def removeRemoteListener(self, listener, sender, event):

        logger.debug("[CR] removeRemoteListener(%s,%s,%s)" % (listener, sender, event))

        # lookup listener in our list
        listener_id = None
        for dict_listener_id, dict_listener in self.server_listeners.iteritems():
            if dict_listener == listener:
                listener_id = dict_listener_id
                break

        # not found
        if listener_id is None:
            return False

        # craft message
        message = {
                "method" : "remove_listener",
                "params" : {
                    "listener_id" : listener_id
                    }
                }

        # send message
        self._clientSendMessage(message)

        # remove from register
        del self.server_listeners[listener_id]
        return True

    def remoteRequest(self, sender, method, params= None):

        logger.debug("[CR] remoteRequest(%s,%s,%s)" % (sender, method, params))

        # craft message
        message = {
                "method" : "request",
                "params" : {
                    "sender" : sender,
                    "method" : method,
                    "params" : params
                    }
                }

        # send message
        response = self._clientSendMessage(message)
        return response

#
# SERVER
#

class ServerListener(Listener):

    def __init__(self, objrouter, clientid):
        Listener.__init__(self)
        self.objrouter = objrouter
        self.clientid  = clientid

    def _signal_cbk_forward_to_client(self, info, data):
        
        logger.info("[SL] %s called (clientid:%s) (event:%s)" % (id(self), self.clientid, info.get("event")))

        # prepare data for sending
        txmit = {
                "method" : "signal",
                "params" : {
                    "listener_id" : id(self),
                    "info" : info,
                    "data" : data 
                    }
                }

        # send
        try:
            self.objrouter.carrier.handleTX(self.clientid, txmit) 
        except Exception as e:
            logger.critical("[SL] Failed to forward signal for (clientid:%s) (event:%s)" % (self.clientid, info.get("event")))
            logger.critical("[SL] Exception: %s" % (e))
        return

class ServerRequestHandler:
    def __init__(self, objrouter, sender, clientid):
        self.objrouter = objrouter
        self.clientid = clientid
        self.sender = sender

    def generate_handler(self, method):
        return lambda params: self.default_handler(method, params)

    def default_handler(self, method, params):

        logger.debug("[SRH] Sender %s request %s invoked with params %s" % (self.sender, method, params))

        # craft message to forward to remote sender
        txmit = {
                "method" : "request",
                "params" : {
                    "sender" : self.sender,
                    "method" : method,
                    "params" : params
                    }
                }

        try:
            response = self.objrouter.carrier.handleTX(self.clientid, txmit)
            if response is None: raise Exception("invalid response from client")
            response = response.get("response", None)
            return response
        except Exception as e:
            logger.critical("[SRH] Failed to forward request for (clientid:%s) (method:%s)" % (self.clientid, method))
            logger.critical("[SRH] Exception: %s" % (e))
            raise e

        return None

class ServerRouter(Router):

    server_version = "1.01"

    def __init__(self, carrier):
        Router.__init__(self)
 
        # dictionary of remote  senders and listeners
        self.client_listeners = {}
        self.client_senders = {}

        # configure data carrier
        self.carrier = carrier
        self.carrier.methods = {
                "get_version"     : self.handle_get_version,
                "list_senders"    : self.handle_list_senders,
                "add_sender"      : self.handle_add_sender,
                "remove_sender"   : self.handle_remove_sender,
                "add_listener"    : self.handle_add_listener,
                "remove_listener" : self.handle_remove_listener,
                "signal"          : self.handle_signal,
                "request"         : self.handle_request,
        }

        # connect/disconnect handlers
        self.carrier.callback_client_connected = \
                self.handle_client_connected
        self.carrier.callback_client_disconnected = \
                self.handle_client_disconnected
        self.carrier.callback_all_clients_disconnected = \
                self.handle_all_clients_diconnected

    def handle_get_version(self, clientid, params):
        return self.server_version

    def handle_list_senders(self, clientid, params):

        logger.debug("[SR] Method: list_senders Clientid: %s Params: %s" % (clientid, params))
        
        list_events = params.get("list_events",False)

        response = []
        for name,sender in self.senders.iteritems():
            
            # prepare description for sender
            entry_sender = {
                    "sender" : sender.getName(),
                    "connected" : sender.isConnected(),
                    }

            # add events to response if required
            if list_events:
                entry_events = []
                for event_name, event in sender.getEvents().iteritems():
                    entry_events.append( {"event": event_name} )
                entry_sender["events"] = entry_events

            # insert
            response.append(entry_sender)

        return response

    def handle_add_sender(self, clientid, params):

        logger.debug("[SR] Method: add_sender Clientid: %s Params: %s" % (clientid, params))
 
        sender = params.get("sender")
        events = params.get("events")
        requests_list = params.get("requests")

        #TODO: maybe it would be better to receive requests as well

        if sender is None or events is None:
            raise Exception("Invalid arguments")

        # construct default request handler
        requests = None

        if requests_list is not None:
            server_handler = ServerRequestHandler(self, sender, clientid)
            requests = {}
            for request in requests_list:
                if request is not None:
                    requests[request] = server_handler.generate_handler(request)
                else:
                    requests[None] = server_handler.default_handler


        # add to router
        objsender = self.addSender(
            sender, events, 
            requests= requests )

        # store entry of sender
        self.client_senders[clientid].append(sender)
        return None

    def handle_remove_sender(self, clientid, params):
        
        logger.debug("[SR] Method: remove_sender Clientid: %s Params: %s" % (clientid, params))

        sender = params.get("sender")

        if sender is None: 
            raise Exception("Invalid arguments")

        # remove from router
        self.removeSender(sender)

        # remove entry of sender
        self.client_senders[clientid].remove(sender)
        return None

    def find_listener(self, clientid, listenerid):
        
        listeners = self.client_listeners.get(clientid, [])
        for listener_entry in listeners:
            if listener_entry["listener_id"] == listenerid:
                return listener_entry

        return None

    def handle_add_listener(self, clientid, params):

        logger.debug("[SR] Method: add_listener Clientid: %s Params: %s" % (clientid, params))
        
        sender = params.get("sender");
        event  = params.get("event");

        objlistener = ServerListener(self, clientid)
        res = self.addListener(objlistener._signal_cbk_forward_to_client, sender, event)
        if res == False:
            raise Exception("Failed to add to router")

        # store entry of remote listener
        entry = {
                    "listener_id" : id(objlistener),
                    "listener_obj" : objlistener,
                    "sender" : sender,
                    "event"  : event
                }

        self.client_listeners[clientid].append(entry)
        return { "listener_id" : id(objlistener) }

    def handle_remove_listener(self, clientid, params):

        logger.debug("[SR] Method: remove_listener Clientid: %s Params: %s" % (clientid, params))
        
        listener_id = params.get("listener_id")

        if listener_id is None:
            raise Exception("Invalid arguments")

        entry = self.find_listener(clientid, listener_id)
        if entry is None:
            raise Exception("Listener not found")

        # remove listener from router
        res = self.removeListener( 
                entry["listener_obj"]._signal_cbk_forward_to_client,
                entry["sender"],
                entry["event"] )

        if res == False:
            raise Exception("Failed to remove from router")

        # delete entry of registered listener
        self.client_listeners[clientid].remove(entry)

        return None

    def handle_signal(self, clientid, params):
        logger.debug("[SR] Method: handle_signal Clientid: %s Params: %s" % (clientid, params))

        # extract arguments
        signal_data = params.get("data")
        signal_info = params.get("info")

        if signal_info is None:
            raise Exception("invalid arguments, missing info")

        sender = signal_info.get("sender")
        event  = signal_info.get("event")

        if sender is None:
            raise Exception("invalid arguments, missing sender")

        # lookup sender
        objsender = self.getSender(sender)
        if objsender is None:
            raise LookupError("sender %s not found" % sender)

        if objsender.isConnected() == False:
            raise Exception("sender %s not connected" % sender)

        # trigger signal
        objsender.getSignal(event).trigger(signal_data)
        return None

    def handle_request(self, clientid, params):

        logger.debug("[SR] Method: handle_request Clientid: %s Params: %s" % (clientid, params))

        sender = params.get("sender")
        method = params.get("method")
        req_params = params.get("params")

        if sender is None or method is None:
            raise Exception("invalid arguments, missing sender or method")

        # lookup sender
        response = self.request(sender, method, params= req_params)
        return response

    # 
    # these procedures will handle the following events:
    # - new client connected
    # - client disconnected
    #
    # When a client is disconnected, all senders and listeners
    # registered by the client will be automatically removed.
    #

    def handle_client_disconnected(self, clientid):

        logger.debug("[SR] Method: client_disconnected Clientid: %s" % (clientid))

        # remove senders, if any
        senders = self.client_senders.get(clientid, [])

        # remove listeners, if any
        listeners = self.client_listeners.get(clientid, [])
        for entry in listeners:
            logger.debug("[SR] -> removing listener of %s:%s (clientid: %s)" % (entry["sender"], entry["event"], clientid))
            self.removeListener(
                    entry["listener_obj"]._signal_cbk_forward_to_client,
                    entry["sender"],
                    entry["event"] )

        for sender in senders:
            logger.debug("[SR] -> removing sender %s (clientid: %s)" % (sender, clientid))
            self.removeSender(sender)

        # clear registers
        try:
            del self.client_listeners[clientid]
            del self.client_senders[clientid]
        except Exception as e:
            logger.critical("[SR] Exception while removing listener and senders (exception: %s)" % (e))
        return None

    def handle_client_connected(self, clientid):

        logger.debug("[SR] Method: client_connected Clientid: %s" % (clientid))

        self.client_listeners[clientid] = []
        self.client_senders[clientid] = []
        return None

    def handle_all_clients_diconnected(self):

        logger.debug("[SR] Method: clients_diconnected")

        for clientid, senders in self.client_senders.iteritems():
            self.handle_client_disconnected(clientid)

        # reset registers
        self.client_listeners = {}
        self.client_senders = {}