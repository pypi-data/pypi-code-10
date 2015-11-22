import re, sys

# String utils

def camelcase(name):
	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
	return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def sanitize_key(key, prefix = ''):
	if key is None:
		key = ''
	if prefix is '':
		key = key.split('_')[-1]
	else:
		key = key.replace(prefix, '')
	return key.lower()

def colorize(text, color = 'white'):
	color = 'black red green yellow magenta cyan white'.split(' ').index(color)

	# Based on Python cookbook, #475186
	if not hasattr(sys.stdout, "isatty"):
		return text
	if not sys.stdout.isatty():
		return text # auto color only on TTYs
	try:
		import curses
		curses.setupterm()
		if curses.tigetnum("colors") > 2:
			return "\x1b[1;%dm" % (30+color) + text + "\x1b[0m"
		else:
			return text
	except:
		return text