# -*- coding: utf-8 -*-

import requests
from clint import arguments
from clint.textui import colored, puts
from collections import deque
import subprocess
import sys
import os
import json


def get_dependencies(package):
    '''Gets the dependencies for a package from the npm registry'''
    url = 'http://registry.npmjs.org/' + package
    data = requests.get(url).json()

    if data == {}:
        puts(colored.red('✗ Could not find package ' + package))
        sys.exit()
        return []

    latest_version = data['dist-tags']['latest']

    current_repo = data['versions'][latest_version]

    if 'dependencies' in current_repo.keys():
        return current_repo['dependencies'].keys()

    return []


def create_dependency_order(packages):
    '''Uses a queue to create an order so that the packages are smushed together correctly'''
    q = deque(packages)
    order = []

    while len(q) > 0:
        package = q.pop()

        if package not in order:
            order = [package] + order

            for dependency in get_dependencies(package):
                q.appendleft(dependency)

    puts(colored.green(u'✓ Created dependency order'))
    return order


def get_args():
    '''Parses the command line arguments to determine input and output'''
    if 'package.json' not in os.listdir('.'):
        puts(colored.red(u'✗ No package.json found'))
        sys.exit()

    package_file = json.load(open('package.json'))

    if 'dependencies' not in package_file.keys() or package_file['dependencies'] == {}:
        puts(colored.red(u'✗ No packages passed'))
        sys.exit()

    dependencies = package_file['dependencies']
    input_packages = dependencies.keys()
    output_file = 'd3.min.js'
    args = sys.argv

    if len(sys.argv) == 2:
        output_file = sys.argv[1]

    puts(colored.green(u'✓ Interpreted command-line arguments'))
    return input_packages, output_file


def init_download_directory():
    '''Downloads node packages if not already done'''
    # destroy_download_directory()
    subprocess.call("npm install", shell=True)


def compress(package_order, output_file):
    '''Compresses all the min js files into 1 final min js file'''
    command = 'cat '

    for package in package_order:
        base_dir = 'node_modules/' + package + '/build/'
        command = command + base_dir + package + '.min.js '

    command = command + ' | uglifyjs -c -m -o ' + output_file
    subprocess.call(command, shell=True)

    puts(colored.green(u'✓ Minified JS'))


def main():
    '''El Jefe'''
    input_packages, output_file = get_args()
    package_order = create_dependency_order(input_packages)
    init_download_directory()
    compress(package_order, output_file)


if __name__ == "__main__":
    main()
