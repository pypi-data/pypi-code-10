import ConfigParser
import os
from htpclauncher import  DEFAULT_LOG_FILE
from htpclauncher.command import Command

class Config:
  def __init__(self):
    self.commands = {}
    self.launch = None
    self.logPath = os.path.expanduser(os.path.join('~', '.%s' % DEFAULT_LOG_FILE))

  def load(self, fp):
    config = ConfigParser.RawConfigParser()
    config.readfp(fp)

    for keyName in config.sections():
      if keyName == 'startup':
        self._loadStartupOptions(config)
        continue
      elif keyName == 'log':
        self._loadLogOptions(config)
        continue
      self.commands[keyName] = self._loadCommand(config, keyName)

  def getCommand(self, keyName):
    return self.commands.get(keyName)

  def getLaunchCommand(self):
   return self.launch

  def getLogPath(self):
    return self.logPath

  def _loadStartupOptions(self, config):
    if config.has_option('startup', 'launch'):
      self.launch = config.get('startup', 'launch')

  def _loadLogOptions(self, config):
    if config.has_option('log', 'path'):
      self.logPath = config.get('log', 'path')

  def _loadCommand(self, config, keyName):
    command = Command(config.get(keyName, 'process'))
    if config.has_option(keyName, 'search'):
      command.search = config.get(keyName, 'search')
    if config.has_option(keyName, 'needsKill'):
      command.needsKill = config.getboolean(keyName, 'needsKill')
    return command

