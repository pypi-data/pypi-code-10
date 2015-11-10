#!/usr/bin/env python
# coding=utf-8
"""A wrapper for Paramiko that attempts to make ssh sessions easier to work with.  It also contains the
do_shell_script function for running local shell scripts!
"""
# Copyright (C) 2015 Jesse Almanrode
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import print_function
import os
import paramiko
import logging
from subprocess import Popen, PIPE, STDOUT

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'
__version__ = '1.0'


def do_shell_script(command, combine=False):
    """Run a specified command in the shell on localhost and return the output

    - **parameters** and **return types**::

        :param command: String containing the shell script to run
        :param combine: Combine stderr and stdout in output
        :return: Tuple of (command,stdout,stderr) or (command,output)
    """
    if combine:
        pipeout = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT).stdout
        stdout = pipeout.read()
        return command, stdout.strip()
    else:
        pipeout = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = pipeout.communicate()
        return command, stdout.strip(), stderr.strip()


class SSH(object):
    """SSH Session object

    - **parameters** and **return types**::

        :param fqdn: Fully qualified domain name or IP address
        :param username: SSH username
        :param password: SSH password
        :param keyfile: SSH keyfile (can be used instead of password)
        :param port: SSH port (default = 22)
        :param timeout: SSH connection timeout in seconds (default = 30)
        :return: SSH connection object
    """
    def __init__(self, fqdn, username=None, password=None, keyfile=None, port=22, timeout=30):
        self.__host__ = fqdn
        self.__username__ = username
        self.__password__ = password
        self.__keyfile__ = os.path.abspath(os.path.expanduser(keyfile))
        self.__port__ = port
        self.__timeout__ = timeout
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect()

    def ssh_command(self, command, timeout=30, combine=False):
        """Run a command over an ssh connection

        - **parameters** and **return types**::

            :param command: The command to run
            :param timeout: Timeout for the command
            :param combine: Combine stderr and stdout
            :return: Tuple of (command, stdout, stderr) or (command, output)
        """
        if combine:
            # http://stackoverflow.com/questions/3823862/paramiko-combine-stdout-and-stderr
            tran = self.connection.get_transport()
            chan = tran.open_session()
            chan.settimeout(timeout)
            chan.get_pty()
            stdout = chan.makefile()
            chan.exec_command(command)
            return command, stdout.read().strip()
        else:
            stdin, stdout, stderr = self.connection.exec_command(command, timeout=timeout)
            return command, stdout.read().strip(), stderr.read().strip()

    def close(self):
        """Closes an established ssh connection
        """
        self.connection.close()
        return None

    def is_alive(self):
        """Is an SSH connection alive
        """
        if self.connection.get_transport() is None:
            return False
        else:
            if self.connection.get_transport().is_alive():
                return True
            else:
                raise paramiko.SSHException("Unable to determine state of ssh session")

    def reconnect(self):
        """Alias to connect
        """
        self.connect()

    def connect(self):
        """Opens an SSH Connection
        """
        # http://stackoverflow.com/questions/26659772/silence-no-handlers-could-be-found-for-logger-paramiko-transport-message
        logging.basicConfig()
        if self.is_alive():
            raise paramiko.SSHException("Connection is already established")
        # Per http://stackoverflow.com/questions/19152578/no-handlers-could-be-found-for-logger-paramiko
        if self.__keyfile__ is not None:
            if self.__username__ is not None:  # Key file with a custom username!
                self.connection.connect(self.__host__, port=self.__port__, username=self.__username__,
                                        key_filename=self.__keyfile__, timeout=self.__timeout__, look_for_keys=False)
            else:
                self.connection.connect(self.__host__, port=self.__port__, key_filename=self.__keyfile__,
                                        timeout=self.__timeout__, look_for_keys=False)
        else:  # Username and password combo
            if self.__username__ is None or self.__password__ is None:
                raise paramiko.SSHException("You must enter a username and password or supply an SSH key")
            else:
                self.connection.connect(self.__host__, port=self.__port__, username=self.__username__,
                                        password=self.__password__, timeout=self.__timeout__, look_for_keys=False)
        # per https://github.com/paramiko/paramiko/issues/175
        self.connection.get_transport().window_size = 3 * 1024 * 1024
