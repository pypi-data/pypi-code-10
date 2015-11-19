#!/usr/bin/env python
import os
import subprocess
from string import Template
from .command import Command


def _connection_string(dbms, connection, user, password):
    if dbms.lower() == 'oracle':
        return user + '/' + password + '@' + connection


def _sql_script(file_path):
    file = open(file_path, 'r')
    script = file.read()
    script += '\nshow error'
    return script


class RunSqlScript(Command):

    def _add_arguments(self, parser):
        parser.add_argument(
            '-s', '--dbms',
            type=str,
            required=True,
            help='oracle or mssql')

        parser.add_argument(
            '-d', '--directory',
            type=str,
            required=True,
            help='Directory containing script')

        parser.add_argument(
            '-f', '--file',
            type=str,
            required=True,
            help='Script file name')

        parser.add_argument(
            '-c', '--connection',
            type=str,
            required=True,
            help='db connection string')

        parser.add_argument(
            '-u', '--user',
            type=str,
            required=True,
            help='Database user')

        parser.add_argument(
            '-p', '--password',
            type=str,
            required=True,
            help='Password')

    def _runScript(self, file_path, dbms, connection):
        script = _sql_script(file_path)

        os.chdir(os.path.dirname(file_path))

        if dbms.lower() == 'oracle':
            process = subprocess.Popen(
                ['sqlplus', '-S', '-L', connection],
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE)
            process.stdin.write(script.encode('utf-8'))
            process.stdin.close()
            process.wait()

    def _execute(self):
        file_path = os.path.join(self.args.directory, self.args.file)

        message = Template(
            'Matador: Executing ${file} against ${connection} \n')
        substitutions = {
            'file': os.path.basename(file_path),
            'connection': self.args.connection
        }
        self._logger.info(message.substitute(substitutions))

        connection_string = _connection_string(
            self.args.dbms,
            self.args.connection, self.args.user, self.args.password)
        self._runScript(file_path, self.args.dbms, connection_string)
