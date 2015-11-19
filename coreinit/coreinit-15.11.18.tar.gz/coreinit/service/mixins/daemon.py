from threading import Thread
import signal

threads = []


def stop_daemons(signal, action):
    global threads
    for thread in threads:
        thread.cleanup()


signal.signal(signal.SIGTERM, stop_daemons)
signal.signal(signal.SIGINT, stop_daemons)


class DaemonMixin(Thread):
    i_am_running = True

    def run(self):
        pass

    def _start_daemon(self, background=False):
        global threads
        threads.append(self)
        if background:
            self.start()
        else:
            self.run()

    def cleanup(self):
        self.i_am_running = False
        super(DaemonMixin, self).cleanup()