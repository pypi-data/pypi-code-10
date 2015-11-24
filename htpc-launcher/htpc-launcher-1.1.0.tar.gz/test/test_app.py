from htpclauncher import HtpcLauncherApp, DEFAULT_CONF_FILE
from htpclauncher.config import Config
from htpclauncher.ostools import OsTools
from mock import Mock
import pytest

class TestApp(object):
  def setup_method(self, method):
    self.ostools = Mock(OsTools)
    self.config = Mock(Config)

  def testConfigIsLoadedFromHomeDirectoryIfAvailable(self):
    expected = Mock()

    self.ostools.openUserFile.return_value = expected
    self.app = HtpcLauncherApp(ostools = self.ostools, config = self.config)

    self.ostools.openUserFile.assert_called_with('.' + DEFAULT_CONF_FILE)
    self.config.load.assert_called_with(expected)

  def testConfigIsLoadedFromEtcIfHomeConfigNotAvailable(self):
    expected = Mock()

    self.ostools.openUserFile.return_value = None
    self.ostools.openSystemConfFile.return_value = expected
    self.app = HtpcLauncherApp(ostools = self.ostools, config = self.config)

    self.ostools.openUserFile.assert_called_with('.' + DEFAULT_CONF_FILE)
    self.ostools.openSystemConfFile.assert_called_with(DEFAULT_CONF_FILE)
    self.config.load.assert_called_with(expected)

  def testErrorRaisedIfNoConfigFileFound(self):
    self.ostools.openUserFile.return_value = None
    self.ostools.openSystemConfFile.return_value = None
    with pytest.raises(Exception):
      self.app = HtpcLauncherApp(ostools = self.ostools, config = self.config)

  def testLogOpenedWithOptionsGivenInConfig(self):
    expected = 'exmaple/path'
    self.config.getLogPath.return_value = expected

    HtpcLauncherApp(ostools = self.ostools, config = self.config)
    self.ostools.getRotatingLogHandler.assert_called_with(expected, backupCount = 5, maxBytes = 1024000)

