import os


def new():
    project_name = ''
    while not project_name:
        project_name = input('Enter name for project: ')
    os.makedirs(project_name + '/adapters')
    os.mkdir(project_name + '/plugins')
    start_file = open(project_name + '/start.py', 'w')
    start_file.write("""
import argparse
from sheldon import Sheldon

parser = argparse.ArgumentParser(description='Start bot')
parser.add_argument('--config-prefix', type=str, default='SHELDON_',
                    help='a str from which starting all config variables')
parser.add_argument('--adapter', type=str, default='console',
                    help='a str with name of adapter from adapters folder'
                         'or PyPi')
args = parser.parse_args()

bot = Sheldon({'config-prefix': args.config_prefix,
               'adapter': args.adapter})

bot.start()
    """)
    start_file.close()

