import json, glob
from steam import vdf
from heroes import Hero
from utils import colorize
from os import path
from os import makedirs

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
		_info('Saving file in %s' % output_path)
		json.dump(content, outfile, sort_keys = True, indent = 4)

def _language_files(addon_path, addon_name):
	resource_folder = path.join(addon_path, 'game/dota_addons/%s/resource' % addon_name) + '/addon_'
	return glob.glob(resource_folder + '*.txt')

def _language_name_from_file(addon_path, addon_name, file_name):
	resource_folder = path.join(addon_path, 'game/dota_addons/%s/resource' % addon_name) + '/addon_'
	return file_name.replace(resource_folder, '').replace('.txt','')

def dump(addon_path, addon_name, output_directory, language = None, include = []):

	print('Generating JSON for mod %s at %s' % (addon_name, addon_path))
	print('Finding required files...')

	vscripts_folder = path.join(addon_path, 'game/dota_addons/%s/scripts/npc' % addon_name)
	resource_folder = path.join(addon_path, 'game/dota_addons/%s/resource' % addon_name)

	heroes_custom = path.join(vscripts_folder, 'npc_heroes_custom.txt')
	abil_custom  = path.join(vscripts_folder, 'npc_abilities_custom.txt')

	# TODO: take into account language parameter
	if _file_exists(heroes_custom) and _file_exists(abil_custom):

		if language is None:
			languages = _language_files(addon_path, addon_name)
		else:
			languages = [path.join(addon_path, 'game/dota_addons/%s/resource/addon_%s.txt' % (addon_name, language.lower()))]

		if not path.exists(output_directory):
			_info('Creating output directory: %s' % output_directory)
			makedirs(output_directory)

		for addon_language in languages:
			if _file_exists(addon_language):
				print('Required files has been found')
				heroes    = _read_file(heroes_custom)
				abilities = _read_file(abil_custom)
				english   = _read_file(addon_language)
				hero_dump = Hero(heroes, abilities, english, include).parse()
				_dump(hero_dump, path.join(output_directory, _language_name_from_file(addon_path, addon_name, addon_language)) + '.json')

def possible_languages(addon_path, addon_name):
	resource_folder = path.join(addon_path, 'game/dota_addons/%s/resource' % addon_name) + '/addon_'
	files = _language_files(addon_path, addon_name)
	languages = map(lambda x: x.replace(resource_folder, '').replace('.txt',''), files)
	return languages