import json
import os.path

from pkg_resources import resource_string

cache = {}

def get_from_cache(key, language):
	return cache[language]['lang']['Tokens'].get(key)

def translate(key, language = 'English'):
	if language in cache:
		return get_from_cache(key, language)
	else:
		config = resource_string(__name__, 'locales/dota_%s.json' % language.lower())
		cache[language] = json.loads(config)
		return get_from_cache(key, language)

# Alias for translate
def t(key, language = 'English'):
	return translate(key, language)