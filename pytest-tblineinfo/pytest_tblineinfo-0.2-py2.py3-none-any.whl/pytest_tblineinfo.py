
import py
import pytest
from _pytest.terminal import TerminalReporter

class NodeTerminalReporter(TerminalReporter):
    def __init__(self, reporter):
        TerminalReporter.__init__(self, reporter.config)

    def summary_failures(self):
        if self.config.option.tbstyle != "no":
            reports = self.getreports('failed')
            if not reports:
                return
            self.write_sep("=", "FAILURES")
            for rep in reports:
                if self.config.option.tbstyle == "line":
                    line = "%s %s" % (rep.nodeid, self._getcrashline(rep))
                    self.write_line(line)
                else:
                    msg = self._getfailureheadline(rep)
                    self.write_sep("_", msg)
                    self._outrep_summary(rep)

@pytest.mark.trylast
def pytest_configure(config):
    if True:
        # Get the standard terminal reporter plugin and replace it with our
        standard_reporter = config.pluginmanager.getplugin('terminalreporter')
        node_reporter = NodeTerminalReporter(standard_reporter)
        config.pluginmanager.unregister(standard_reporter)
        config.pluginmanager.register(node_reporter, 'terminalreporter')
