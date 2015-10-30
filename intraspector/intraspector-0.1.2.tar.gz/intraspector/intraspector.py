from functools import wraps
import inspect
import time

class Intraspector():
    def __init__(self, debug=True):
        self._trace = []
        self._debug=debug

    def record(self):
        def record_decorator(func):
            def wrapper(*args, **kwargs):
                if self._debug:
                    trace_obj = {
                        'name': func.__name__,
                        'documentation': inspect.getdoc(func),
                        'file': inspect.getfile(func),
                        'source_code': inspect.getsourcelines(func)[0],
                        'source_line': inspect.getsourcelines(func)[1],
                        'module': inspect.getmodule(func).__name__,
                        'call_timestamp': time.time()
                    }
                    self._trace.append(trace_obj)
                return func(*args, **kwargs)
            return wrapper
        return record_decorator

    def start_trace(self):
        self._trace = []

    def get_trace(self):
        return self._trace

    def get_debug_mode(self):
        return self._debug
