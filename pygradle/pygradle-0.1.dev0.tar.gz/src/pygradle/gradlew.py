# Copyright 2015 Michal Walkowski
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Python gradle wrapper module. """

import subprocess

from types import MethodType


_BASIC_GRADLE_TASKS = ['assemble', 'build', 'buildDependents', 'buildNeeded',
                       'classes', 'compileJava', 'processResources', 'clean',
                       'jar', 'testClasses', 'compileTestJava',
                       'processTestResources', 'init', 'javadoc', 'components',
                       'dependencies', 'dependencyInsight', 'help', 'model',
                       'projects', 'properties', 'tasks', 'check', 'test']


class GradleFactory(object):
    """ Gradle Factory"""

    @staticmethod
    def create(gradle_cmd='gradle'):
        """ Creates gradle wrapper with tasks loaded from gradle script. """
        gradle = Gradle(gradle_cmd)
        result = gradle.add_tasks('task', '--all').execute()
        gradle_tasks = GradleFactory._get_gradle_tasks(result.split('\n'))

        new_gradle = Gradle(gradle_cmd)
        for new_task in set(_BASIC_GRADLE_TASKS) - set(gradle_tasks):
            setattr(new_gradle, new_task,
                    MethodType(MethodType(Gradle.execute_task, new_gradle),
                               new_task))

        return new_gradle

    @staticmethod
    def _get_gradle_tasks(lines):
        """ Returns list of tasks from given lines."""
        return list(filter(None,
                           [line.split('-')[0].strip().replace(':', '_')
                            for line in lines
                            if len(line.split('-')) > 1]))


class Gradle(object):
    """ Gradle wrapper """

    def __init__(self, gradle_cmd='gradle'):
        self._gradle_cmd = gradle_cmd
        self._tasks = []
        self._options = []
        for basic_task in _BASIC_GRADLE_TASKS:
            setattr(self, basic_task,
                    MethodType(MethodType(Gradle.execute_task, self),
                               basic_task))

    def execute_task(self, task):
        """ Executes gradle task"""
        return _call_system_command(self._create_cmd([task]))

    def versions(self):
        """ Returns versions example:
            versions['Gradle'] -> '2.8'
            versions['Groovy'] -> '2.4.4'
        """
        versions = {}
        result = self.execute_task('--version').split('\n')
        for line in result:
            tmp = line.split(':')
            if 'Gradle' in line:
                versions['Gradle'] =\
                    line.replace('Gradle', '').replace(' ', '')
            elif len(tmp) > 1:
                versions[tmp[0]] = tmp[1].replace(' ', '')
        return versions

    def execute(self):
        """ Executes all task added by add_tasks"""
        return _call_system_command(self._create_cmd(self._tasks))

    def parallel(self, max_workers=3):
        """ Add parallel and max-workers switch to gradle command """
        self.add_options('--parallel', '--max-workers=' + str(max_workers))
        return self

    def add_options(self, *args):
        """ Adds options to gradle command"""
        for arg in args:
            self._options.append(arg)
        return self

    def add_tasks(self, *args):
        """ Adds task for execution"""
        for arg in args:
            self._tasks.append(arg)
        return self

    def _create_cmd(self, args):
        """ Returns created gradle command"""
        return ' '.join([self._gradle_cmd] + self._options + args)


def _call_system_command_async(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True)


def _call_system_command(cmd):
    return _call_system_command_async(cmd).communicate()[0].decode('ascii')
