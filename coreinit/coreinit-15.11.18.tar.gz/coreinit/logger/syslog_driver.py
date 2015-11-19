from coreinit.logger.logger_base import LoggerBase
import syslog
import traceback

class Logger(LoggerBase):
    log_prefix = ''

    def configure(self, prefix='coreinit'):
        self.log_prefix = prefix

    def _format_msg(self, msg='', exception=None):
        f = traceback.extract_stack(limit=5)[-3][2]
        e = []
        a = ''

        if exception != None:
            e = traceback.format_exc().splitlines()

        if msg != '':
            a = ': '

        r = str(f + a + msg).splitlines()
        r.extend(e)
        return r

    def _syslog(self, loglevel, msg='', exception=None):
        syslog.openlog(self.log_prefix)

        for line in self._format_msg(msg, exception):
            syslog.syslog(loglevel, line)


    def debug(self, msg, exception=None):
        self._syslog(syslog.LOG_DEBUG, msg, exception)


    def info(self, msg, exception=None):
        self._syslog(syslog.LOG_INFO, msg, exception)


    def warning(self, msg, exception=None):
        self._syslog(syslog.LOG_WARN, msg, exception)


    def error(self, msg, exception=None):
        self._syslog(syslog.LOG_ERR, msg, exception)


    def crit(self, msg, exception=None):
        self._syslog(syslog.LOG_CRIT, msg, exception)