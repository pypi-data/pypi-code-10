import eventloop

def stop():
    print "stop"
    print eventloop.get_eventloop().cancel_event(5)

def func():
    print "func"
    print eventloop.get_eventloop().add_event(2, "Test", callback = func, arguments = [], stealth = False)

if __name__ == '__main__':
        eventloop.create_eventloop(True)
        eventloop.get_eventloop().add_event(1, "func", callback = func, arguments = [], stealth = False)
        eventloop.get_eventloop().add_event(8, "stop", callback = stop, arguments = [], stealth = False)
        # eventloop.get_eventloop().add_periodical_event(config.config_vmca.DEFRAGGER_FREQUENCY, -config.config_vmca.DEFRAGGER_FREQUENCY, "defrag", callback = self.defrag, arguments = [], stealth = True)
        eventloop.get_eventloop().loop()