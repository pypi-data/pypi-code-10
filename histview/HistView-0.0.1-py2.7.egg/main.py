import sys,pickle,logging,logging.config,os,json,copy
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from autobahn.twisted.websocket import WebSocketClientProtocol, \
                                       WebSocketClientFactory
#imports for kivy app
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from twisted.internet import reactor

from twisted.python import log

import Util.Utils as UTIL
import API.HistologyAPI as API

def get_log_conf(targetdir=os.getcwd(),loglevel='WARN'):
    '''
    verbose formatter prints stacktraces
    '''
    #TODO: if targetdir dne, create the dir
    #create_dir_dne(targetdir)

    conf = {
        'version': 1,              
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'verbose':{
                'format':'%(asctime)s %(levelname)s %(name)s %(message)s [%(filename)s@%(lineno)d in %(funcName)s]'
            },
            'simple':{
                'format':'%(asctime)s: %(message)s'
            },
        },
        'handlers': {
            'error': {
                'level':'ERROR',    
                'class':'logging.handlers.TimedRotatingFileHandler',
                'formatter':'verbose',
                'filename': os.path.join(targetdir,'HistViewError.log'),
                'when':'midnight',
                'backupCount':30,
            },
            'client': {
                'level':loglevel,
                'class':'logging.handlers.TimedRotatingFileHandler',
                'formatter':'verbose',
                'filename':os.path.join(targetdir,'HistView.log'),
                'when':'midnight',
                'backupCount':30,
                'delay':True,
            }
        },
        'loggers': {
            '': {                  
                'handlers': ['error'],        
                'level': 'ERROR',  
                'propagate': True  
            },
            'HistView': {                  
                'handlers': ['client','error'],        
                'level': loglevel,  
                'propagate': False  
            },
        }
    }
    return conf

logging.config.dictConfig(get_log_conf(
                            targetdir=os.path.join(os.getcwd(),'log'),
                            loglevel=logging.WARN)
                            )

logger = logging.getLogger('HistView') 

def json_test():
    '''
    JSON test
        
    Turn reciever fan on then off

    Turn heater on then off
    '''
    f1 = copy.deepcopy({k:v for k,v in self._messages.items() if k == 'receiver_fan'})
    f2 = copy.deepcopy({k:v for k,v in self._messages.items() if k == 'receiver_fan'})
    f1['receiver_fan']['on'] = True

    h1 = copy.deepcopy({k:v for k,v in self._messages.items() if k == 'heater'})
    h2 = copy.deepcopy({k:v for k,v in self._messages.items() if k == 'heater'})
    h1['heater']['on'] = True
    h1['heater']['setpoint'] = 20.3

    ret = list(reversed([f1,f2,h1,h2]))
    return ret

def pickle_test():
    f1 = API.ReceiverFan()
    f1.on = True
    f2 = API.ReceiverFan()

    h1 = API.Heater()
    h1.on = True
    h1.setpoint = 20.3

    h2 = API.Heater()

    ret = list(reversed([f1,f2,h1,h2])) 
    return ret


class UISimService(object):
    '''
    receiver_fan bool turn on the fan on or off
    heater bool turn the heat on or off at a setpoint 0.0 to 100.0 must be > then 0 to turn on
    stilldata {} request for data update
    '''
    _messages = {'receiver_fan':{'on':False},
                'heater':{'on':False,
                          'setpoint':0.0},
                'stilldata':{}
                }


    def __init__(self,model,testlist):
        self.testlist = testlist
        self.test = []
        self.model = model

    def getNext(self):
        try:
            return self.test.pop()
        except:
            self.test = self.testlist()
            return self.test.pop()

class HistologyClientProtocol(WebSocketClientProtocol):

    #def onConnect(self, response):
    #    logger.warn("Server connected: {0}".format(response.peer))
    #    #logger.warn("Server connected: {0}".format(response.peer))
    #    self.service = self._service()
    def dumps(self,obj):
        ret = pickle.dumps(obj,protocol=2)
        logger.debug('Pickled {0}'.format(type(obj)))
        return ret

    def loads(self,msg):
        return pickle.loads(msg)

    def onOpen(self):
        logger.warn("WebSocket connection open.")
        self.factory._app.print_message('WebSocket connection open.')
        self.factory._proto = self
        self.stilldata_request()

    def send_stilldata(self,dt):
        self.send(API.StillData())

    def stilldata_request(self):
        '''Send a StillData message every 2 seconds
        '''
        logger.warn('Scheduling StillData message ever 2 seconds')
        Clock.schedule_interval(self.send_stilldata, 2)

    def send(self,msg):
        self.sendMessage(self.dumps(msg),isBinary=True)

    def onMessage(self, payload, isBinary):
        if isBinary:
            logger.debug("Binary message received: {0} bytes".format(len(payload)))
            self.handle_binary(payload)
            
        else:
            self.handle_message(payload)

    def handle_binary(self,payload):
        resp = self.loads(payload)
        self.factory._app.handle_message(resp)

    def handle_message(self,payload):
        msg = payload.decode('utf8')
        logger.warn("Text message received: {0}".format(msg))
        self.factory._app.print_message(msg)

    def onClose(self, wasClean, code, reason):
        logger.warn("WebSocket connection closed: {0}".format(reason))
        self.factory._app.print_message("WebSocket connection closed: {0}".format(reason))
        self.factory._proto = None

class DistClientFactory(WebSocketClientFactory):
    protocol = HistologyClientProtocol
    _msg_protocols = ['dist_pickle']

    def __init__(self, url, app):
        WebSocketClientFactory.__init__(self, url,protocols=self._msg_protocols)
        # While the Kivy app needs a reference to the factory,
        # the factory needs a reference to the Kivy app.
        self._app = app
        # Not sure why/whether _proto is needed?
        self._proto = None
        self.dataservice = self._app.dataservice
        logger.warn('Factory created {0}'.format(url))

def setup_model():
    ret = None
    return ret

class UITestApp(App):
    model = None
    dataservice = None
    pottemp_str = 'Pot Temp: {0}'
    headtemp_str = 'Head Temp: {0}'
    headtemp2_str = 'Head Temp2: {0}'

    def build(self):
        self.model = setup_model()
        self.dataservice = UISimService(self.model,pickle_test)
        root = self.setup_gui()
        self.connect_to_server()
        return root

    def setup_gui(self):
        """
        Create a vertical oriented boxlayout that contains two widgets:
        1) a label in which we show text sent/received
        2) a textinput where you can enter text
           to the server.
        """

        self.label = Label(text='Connecting...\n')
        self.PotTemp = Label(text=self.pottemp_str.format(0.0))
        self.HeadTemp = Label(text=self.headtemp_str.format(0.0))
        self.HeadTemp2 = Label(text=self.headtemp2_str.format(0.0))
        # Just 1 line of text; use 10% of the parent's height.
        #self.textbox = TextInput(size_hint_y=.1, multiline=False)
        # When the 'Enter' key is pressed, call the method send_message
        # that is defined below.
        
        #self.textbox.bind(on_text_validate=self.send_message)

        def callback(instance):
            try:
                msg = self.dataservice.getNext()
            except Exception as e:
                #logger.debug('No more messages. closing')
                #self.dropConnection()
                return
            logger.debug('Service provided msg {0}'.format(msg))
            self.send_message(msg)

        def stilldata_cb(instance):
            msg = API.StillData()
            logger.debug('Sending {0}'.format(msg))
            self.send_message(msg)

        self.tstBtn = Button(text='Send Test Message')
        self.tstBtn.bind(on_press=callback)

        self.getDataBtn = Button(text='Refresh Still')
        self.getDataBtn.bind(on_press=stilldata_cb)

        # Create the root widget ...
        self.layout = BoxLayout(orientation='vertical')
        # and add the two child widgets.
        
        self.layout.add_widget(self.PotTemp)
        self.layout.add_widget(self.HeadTemp)
        self.layout.add_widget(self.HeadTemp2)
        self.layout.add_widget(self.tstBtn)
        self.layout.add_widget(self.getDataBtn)
        self.layout.add_widget(self.label)
        return self.layout

    def connect_to_server(self):
        """
        Connect to the echoing websocket server.
        """
        # The Kivy app needs a reference to the factory object.
        self._factory = DistClientFactory("ws://localhost:9000", self)
        reactor.connectTCP('127.0.0.1', 9000, self._factory)

    def send_message(self, msg):
        """
        Send the text entered that was entered in the texbox widget.
        """
        proto = self._factory._proto
        if msg and proto:
            proto.send(msg)

            #self.print_message('Sent to server: {0}'.format(type(msg)))
            #self.textbox.text = ""

    def print_message(self, msg):
        self.label.text += msg + '\n'

    def handle_message(self,msg):
        logger.debug('App.handle_message from server {0}.handler {1}'.format(type(msg),msg.handler))
        if msg.handler == 'ReceiverFan':
            on = 'OFF'
            if msg.on:
                on = 'ON'
            
            self.label.text = 'ReceiverFan is {0}'.format(on)

        elif msg.handler == 'Heater':
            on = 'OFF'
            if msg.on:
                on = 'ON'
            
            self.label.text = 'Heater is {0}'.format(on)
            
        elif msg.handler == 'StillData':
            logger.debug('{0} PotTemp {1} HeadTemp {2}'.format(msg.handler,msg.PotTemp,msg.HeadTemp))
            self.PotTemp.text = self.pottemp_str.format(msg.PotTemp)
            self.HeadTemp.text = self.headtemp_str.format(msg.HeadTemp)
            self.HeadTemp2.text = self.headtemp2_str.format(msg.HeadTemp2)

        else:
            logger.error('App.handle_message from server {0}.handler {1} not supported.'.format(type(msg),msg.handler))


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    logger.error('Main')
    logger.warn('Main')
    logger.warn('Main')

    UITestApp().run()