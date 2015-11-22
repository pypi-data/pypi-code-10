import json
from steam import vdf
from heroes import Hero
from utils import colorize
from os import path

def _file_exists(file_path):
	if not path.isfile(file_path):
		_error('File not found: %s' % (file_path))
		return False
	else:
		_success('%s found!' % file_path)
		return True

def _read_file(file_path):
	with open(file_path, 'r') as file:
		return vdf.load(file)

def _error(msg):
	_log('Error', msg, 'red')

def _info(msg):
	_log('Info', msg, 'cyan')

def _success(msg):
	_log('Ok', msg, 'green')

def _log(label, msg, color = 'white'):
	print('[%s] %s' % (colorize(label, color), msg))

def _dump(content, output_path):
	with open(output_path, 'w') as outfile:
		print('Saving file in %s' % output_path)
		json.dump(content, outfile, sort_keys = True, indent = 4)

def dump(addon_path, addon_name, output_path = 'heroes.json'):

	print('Generating JSON for mod %s at %s' % (addon_name, addon_path))
	print('Finding required files...')

	vscripts_folder = path.join(addon_path, 'game/dota_addons/%s/scripts/npc' % addon_name)
	resource_folder = path.join(addon_path, 'game/dota_addons/%s/resource' % addon_name)

	heroes_custom = path.join(vscripts_folder, 'npc_heroes_custom.txt')
	abil_custom  = path.join(vscripts_folder, 'npc_abilities_custom.txt')
	addon_english = path.join(resource_folder, 'addon_english.txt') # TODO: Add available languages

	if _file_exists(heroes_custom) and _file_exists(abil_custom) and _file_exists(addon_english):
		print('Required files has been found')
		heroes    = _read_file(heroes_custom)
		abilities = _read_file(abil_custom)
		english   = _read_file(addon_english)
		hero_dump = Hero(heroes, abilities, english, ['Village']).parse()
		_dump(hero_dump, output_path)