#!/usr/bin/env python
"""
This is a simple nginx tool.
"""
import subprocess
import re
import sys
import os
from optparse import OptionParser
import urllib2


class bcolors:

    """
    This class is to display differnet colour fonts
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    UNDERLINE = '\033[4m'


class nginxCtl:

    """
    A class for nginxCtl functionalities
    """

    def get_version(self):
        """
        Discovers installed nginx version
        """
        version = "nginx -v"
        p = subprocess.Popen(
            version, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
        output, err = p.communicate()
        return err

    def get_conf_parameters(self):
        """
        Finds nginx configuration parameters

        :returns: list of nginx configuration parameters
        """
        conf = "nginx -V 2>&1 | grep 'configure arguments:'"
        p = subprocess.Popen(
            conf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        output = re.sub('configure arguments:', '', output)
        dict = {}
        for item in output.split(" "):
            if len(item.split("=")) == 2:
                dict[item.split("=")[0]] = item.split("=")[1]
        return dict

    def get_nginx_conf(self):
        """
        :returns: nginx configuration path location
        """
        try:
            return self.get_conf_parameters()['--conf-path']
        except KeyError:
            print "nginx is not installed!!!"
            sys.exit()

    def get_nginx_bin(self):
        """
        :returns: nginx binary location
        """
        try:
            return self.get_conf_parameters()['--sbin-path']
        except:
            print "nginx is not installed!!!"
            sys.exit()

    def get_nginx_pid(self):
        """
        :returns: nginx pid location which is required by nginx services
        """

        try:
            return self.get_conf_parameters()['--pid-path']
        except:
            print "nginx is not installed!!!"
            sys.exit()

    def get_nginx_lock(self):
        """
        :returns: nginx lock file location which is required for nginx services
        """

        try:
            return self.get_conf_parameters()['--lock-path']
        except:
            print "nginx is not installed!!!"
            sys.exit()

    def start_nginx(self):
        """
        Start nginx service if pid and socket file do not exist.
        """
        nginx_conf_path = self.get_nginx_conf()
        nginx_lock_path = self.get_nginx_lock()
        if os.path.exists(nginx_lock_path):
            print "nginx is already running... Nothing to be done!"
        else:
            cmd = "nginx -c " + nginx_conf_path
            p = subprocess.Popen(cmd,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=True
                                 )
            output, err = p.communicate()
            if not err:
                file = open(nginx_lock_path, 'w')
                file.close()
                print "Starting nginx:\t\t\t\t\t    [ %sOK%s ]" % (
                    bcolors.OKGREEN,
                    bcolors.ENDC
                    )
            else:
                print err

    def stop_nginx(self):
        """
        Stop nginx service.
        """
        nginx_pid_path = self.get_nginx_pid()
        nginx_lock_path = self.get_nginx_lock()
        if os.path.exists(nginx_pid_path):
            try:
                pid_file = open(nginx_pid_path, "r")
                pid = pid_file.read().strip()
                pid_file.close()
                pid_cmd = "ps -p %s -o comm=" % pid
                p = subprocess.Popen(pid_cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=True
                                     )
                pid, err = p.communicate()
            except IOError:
                print "Cannot open nginx pid file"
            if pid:
                cmd = "nginx -s quit"
                p = subprocess.Popen(cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=True
                                     )
                output, err = p.communicate()
                if not err:
                    if os.path.exists(nginx_lock_path):
                        os.remove(nginx_lock_path)
                    print "Stoping nginx:\t\t\t\t\t    [  %sOK%s  ]" % (
                        bcolors.OKGREEN,
                        bcolors.ENDC
                        )
                else:
                    print err

    def configtest_nginx(self):
        """
        Ensure there is no syntax errors are reported.
        The 'nginx -t' command is used for this.
        """
        p = subprocess.Popen(
            "nginx -t",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
            )
        output, err = p.communicate()
        print err

    def restart_nginx(self):
        """
        Restart nginx service. Stop and Start nginx functions are used.
        """
        self.stop_nginx()
        self.start_nginx()

    def full_status(self):
        """
        Checks against /server-status for server statistics
        """
        try:
            request = urllib2.urlopen('http://localhost/server-status')
            if str(request.getcode()) == "200":
                print """
Nginx Server Status
-------------------
%s
                    """ % request.read()
            else:
                print """
Nginx Server Status
-------------------
server-status did not return a 200 response.
                    """
        except (urllib2.HTTPError, urllib2.URLError):
            print """
Nginx Server Status
-------------------
Attempt to query /server-status returned an error
                """

    def status_nginx(self):
        """
        Report nginx status based on pid and socket files.
        """
        nginx_pid_path = self.get_nginx_pid()
        nginx_lock_path = self.get_nginx_lock()
        if os.path.exists(nginx_pid_path):
            try:
                pid_file = open(nginx_pid_path, "r")
                pid = pid_file.read().strip()
                pid_file.close()
                cmd = "ps -p %s -o comm=" % pid
                p = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True)
                output, err = p.communicate()
                if output:
                    print "nginx (pid %s) is running ..." % pid
            except IOError:
                print "Cannot open nginx pid file"
        elif (os.path.exists(nginx_lock_path) and not
                os.path.exists(nginx_pid_path)):
            print "nginx pid file exists"
        else:
            print "nginx is stopped"

    def get_vhosts(self):
        """
        Discover a list of configured vhosts by parsing nginx configuration
        files and print those vhosts on commanline.
        This function parses nginx default configuration file,
        /etc/nginx/nginx.conf, and looks for keyword Include.
        It parse all files and folders referenced by Include directrive.
        """
        nginx_conf_path = self.get_nginx_conf()  # path of main nginx file
        fo = open(nginx_conf_path, "r")
        file = fo.read()
        vhost_files = []
        # Get a list of files/folders refernced with 'include' directive on
        # main nginx config
        for line in file.split("\n"):
            line = line.strip()
            if not line.startswith("#"):
                #if "include" in line:	
                if re.search(r"\binclude\b",line):
                    line.split()
                    vhost_files.append(line.split()[1])
        fo.close()
        mydict = {}

        for v in vhost_files:
            # find how a folder is specified on nginx config.
            if "/*" in v:
                dir = v.split("/*", 1)[0]
                ext = v.split("/*", 1)[1].strip(";")  # find the extension.
                for f in os.listdir(dir):
                    if f.endswith(ext) or "*" in ext or not ext:
                        file = v.split("/*", 1)[0] + "/" + f
                        num = 0
                        domain = ""
                        port = ""
                        for l in open(file, "r"):
                            li = l.strip()
                            num = num + 1
                            if not li.startswith("#"):
                                if re.search('server_name', li):
                                    li = li.split(";", 1)[0]
                                    li = li.strip(";")
                                    if li.split()[1] == "_":
                                        domain = "default_server_name"
                                    else:
                                        domain = li.split()[1]
                                    domain_num = num
                                    alias = li.split()[2:]
                                if re.search('listen', li):
                                    li = li.strip()
                                    li = li.strip(";")
                                    port = li.split()[1]
                                if domain and port:
                                    info = (domain_num, file, alias)
                                    mydict[(domain, port)] = info
                                    domain = ""
                                    port = ""

            else:
                num = 0
                domain = ""
                port = ""
                v = v.strip(";")
                if not re.search('/',v):
                    v = "/etc/nginx/" + v
                for l in open(v, "r"):
                    li = l.strip()
                    num = num + 1
                    if not li.startswith("#"):
                        if re.search('server_name', li):
                            li = li.strip(";")
                            if li.split()[1] == "_":
                                domain = "default_server_name"
                            else:
                                domain = li.split()[1]
                            domain_num = num
                            alias = li.split()[2:]
                        if re.search('listen', li):
                            li = li.strip()
                            port = li.split()[1]
                        if domain and port:
                            info = (domain_num, file, alias)
                            mydict[(domain, port)] = info
                            domain = ""
                            port = ""

        print "%snginx vhost configuration:%s" % (
            bcolors.BOLD,
            bcolors.ENDC
            )
        for key, value in mydict.iteritems():
            if re.search(':', key[1]):
                ip = key[1].split(":")[0]
                port = key[1].split(":")[1]
            else:
                ip = "*"
                port = key[1]

            print "%s:%s is a Virtualhost" % (
                ip,
                port
                )
            print "\tport %s %s %s %s (%s:%s)" % (
                port,
                bcolors.OKGREEN,
                key[0],
                bcolors.ENDC,
                value[1],
                str(value[0])
                )
            for i in value[2]:
                print "\t\talias  %s %s %s" % (
                    bcolors.CYAN,
                    i,
                    bcolors.ENDC
                    )
            print "\n"

        self.configtest_nginx()


def main():
    n = nginxCtl()

    def usage():
        print ("Usage: %s [option]" % sys.argv[0])
        print ("Example: %s -v" % sys.argv[0])
        print "\n"
        print "Available options:"
        print "\t-S list nginx vhosts"
        print "\t-t configuration test"
        print "\t-k start|stop|status|restart|fullstatus"
        print "\t-v version"
        print "\t-h help"

    def version():
        print "version 1.0"

    commandsDict = {"-S": n.get_vhosts,
                    "-t": n.configtest_nginx,
                    "-k": n.restart_nginx,
                    "-v": version,
                    "-h": usage}
    subcommandsDict = {"start": n.start_nginx,
                       "stop": n.stop_nginx,
                       "restart": n.restart_nginx,
                       "status": n.status_nginx,
                       "fullstatus": n.full_status}
    allCommandsDict = {"-S": n.get_vhosts,
                       "-t": n.configtest_nginx,
                       "-k": usage,
                       "-v": version,
                       "-h": usage,
                       "start": n.start_nginx,
                       "stop": n.stop_nginx,
                       "restart": n.restart_nginx,
                       "status": n.status_nginx,
                       "fullstatus": n.full_status}
    commandline_args = sys.argv[1:]
    if len(commandline_args) == 1:
        for argument in commandline_args:
            if argument in allCommandsDict:
                allCommandsDict[argument]()
            else:
                usage()
    elif len(commandline_args) == 2:
        if sys.argv[1] == "-k":
            flag = sys.argv[2:]
            for f in flag:
                if f in subcommandsDict:
                    subcommandsDict[f]()
        else:
            usage()
    else:
        usage()
if __name__ == "__main__":
    main()
