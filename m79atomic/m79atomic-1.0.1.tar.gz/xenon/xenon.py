#! /usr/bin/env python
import sys
import os
from dvdtools import *
from arg_trans import Trans

invoke = True
isdvd = False
isofiles = ['']
files = []
verbose = False


class Xenon2:
    def printbanner(self):
        banner = ['__  __', '\\ \\/ /___ _ __   ___  _ __',
                  " \\  // " + '\033[31m' + "_" + '\033[36m' + " \\ '_ \\ / " + '\033[31m' + "_" + '\033[36m' + " \\| '_ \\                    \\|/",
                  " /  \\  __/ | | | " + '\033[31m' + "(_)" + '\033[36m' + " | | | |                  (" + '\033[31m' + "o o" + '\033[36m' + ")",
                  "/_/\\_\\___|_| |_|\\___/|_| |_|" + '\033[31m' + " (-> mplayer)" + '\033[36m' + " ooO--(_)--Ooo"]

        print '\033[36m'
        for l in banner:
            print l
        print '\033[0m'

    def fiio_present(self):
        p = os.popen('aplay -l|grep FiiO', "r")
        while 1:
            line = p.readline()
            print '### ', line
            if not line: break
            if 'FiiO' in line: return True
        return False

    def create_command(self, configlist, supportedlist):
        configs = configlist + sys.argv[1:]
        tr = Trans()
        tr.add('vol', '-af volume=', 1)
        tr.add('fs', '-fs')
        tr.add('mute', '-nosound')
        tr.add('shuf', '-shuffle')
        tr.add('seek', '-ss', 1)

        tr.add('from', x.add_arg_from, 1)

        tr.walk(configs)
        command = 'mplayer' + tr.command

        if len(tr.p_file_list) - len(configlist) is 0:
            print "No file to play is given. Searching... "
            command += self.getSupportedFilesInCWD(supportedlist)
        else:
            for f in tr.p_file_list:
                if self.isSupportedFile(f, self.supportedList):
                    if os.path.exists(f):
                        if f.lower().endswith(".iso"):
                            command += self.createDVDLine(f)
                            self.print_if_verbose("Adding iso -> " + command)
                        else:
                            command += ' "' + f + '"'

        return command

    def print_if_verbose(self, msg):
        global verbose
        if verbose:
            print msg

    def get_id(self, lang, aid_or_sid):
        global languageList
        for l in languageList:
            if lang in l:
                return l.split(':')[aid_or_sid]

    def get_aid(self, lang):
        return self.get_id(lang, 1)

    def get_sid(self, lang):
        return self.get_id(lang, 2)

    def set_lang(self, next, command):
        parts = next.split(':')
        if len(parts) is 1:
            lang = parts[0]
            for lang in languageList:
                if next in lang:
                    command += ' -aid ' + self.get_aid(parts[0]) + " -nosub "
                    return command
        elif len(parts) is 2:
            aid = parts[0]
            sid = parts[1]
            for lang in languageList:
                if aid in lang:
                    command += ' -aid ' + self.get_aid(parts[0]) + " "
                if sid in lang:
                    command += ' -sid ' + self.get_sid(parts[1]) + " "
            return command

    def IN(self, list1, obj):
        for l1 in list1:
            if l1 in obj:
                return True
        return False

    def createDVDLine(self, isofile):
        global isofiles, isdvd
        isdvd = True
        isofiles.append(isofile)
        return ' dvd://1 -dvd-device ' + "\"" + isofile + "\" "

    def isSupportedFile(self, string, supportedList):
        for ending in supportedList:
            if len(ending) > 0 and string.lower().endswith(ending):
                return True
        if not string.startswith('.'):
            return self.isSupportedFile('.' + string, supportedList)
        return False

    def getSupportedFilesInCWD(self, supportedList):
        currentDir = os.getcwd()
        fileList = ''
        print len(self.fromfileinlist)
        fromFileReached = not len(self.fromfileinlist) > 0
        print 'Starting file given:', not fromFileReached
        for f in sorted(os.listdir(currentDir)):
            if self.isSupportedFile(f, supportedList):
                if str(f).strip() == self.fromfileinlist:
                    fromFileReached = True
                if fromFileReached:
                    if f.endswith(".iso"):
                        fileList += self.createDVDLine(f)
                    else:
                        fileList += " \"" + f + "\" "
        return fileList

    def get_config_section(self, configs, section):
        inside = False
        parts = ''
        for c in configs:
            if section in c:
                inside = True
            elif inside:
                if c.startswith(' '):
                    parts += c.rstrip()
                else:
                    return parts

    def read_config_file(self):
        config_file_name = os.path.dirname(os.path.abspath(__file__)) + "/.xenon.conf"
        if not os.path.isfile(config_file_name):
            config_file_name = "~/.mplayer/.xenon.conf"
        if os.path.isfile(config_file_name):
            print "config file: " + config_file_name
            with open(config_file_name) as configfile:
                return configfile.readlines()
        else:
            print "no config file found"
            return sys.argv

    fromfileinlist = ''

    def add_arg_from(self, arg):
        print 'from', arg
        if self.isSupportedFile(arg, self.supportedList):
            self.fromfileinlist = str(arg).strip()
            print 'Playing list starting with file:', self.fromfileinlist
        else:
            print 'Cannot play list from', arg


x = Xenon2()

x.printbanner()
configFile = x.read_config_file()
languageList = x.get_config_section(configFile, 'supported:languages').split(' ')
configList = x.get_config_section(configFile, 'config').split(' ')
x.supportedList = x.get_config_section(configFile, 'supported:media').split(' ')
mplayer_command = x.create_command(configList, x.supportedList)

print mplayer_command
if invoke:
    os.system(mplayer_command)
else:
    print isdvd
    if isdvd:
        for isofile in isofiles:
            read_iso(isofile)
            print select_id()
            print langs
            print subs
