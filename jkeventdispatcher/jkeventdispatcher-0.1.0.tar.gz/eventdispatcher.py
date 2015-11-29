class EventDispatcher():
    def __init__(self):
        self.__listeners = {}

    def addListener(self, eventName, listener, method):
        if not self.hasListener(eventName=eventName):
            self.__listeners[eventName] = []

        self.__listeners[eventName].append({
            'listener': listener,
            'method': method    
        })

    def hasListener(self, eventName):
        if self.__listeners.has_key(eventName):
            return True

        return False

    def dispatch(self, eventName, event):
        listeners = self.__getListenersByEventName(eventName)

        for item in listeners:
            listener = item['listener']
            method = item['method']
            
            callableFuntion = getattr(listener, method)
            callableFuntion(event)

    def __getListenersByEventName(self, eventName):
        if not self.hasListener(eventName=eventName):
            return []

        return self.__listeners[eventName]

    def getListeners(self):
        return self.__listeners

    def register(self, key, instance):
        self.__container[key] = instance;

    def get(self, key):
        obj = self.__container[key]

        if (hasattr(obj, '__call__')):
            obj = obj(self)

        return obj 