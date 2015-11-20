#!/usr/bin/env python2.7
# convert mysql query output (in the table format) to json or yaml

import yaml, json, sys, os, argparse, logging
from os.path import expanduser
import argparse_config
import re

class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        # this is the RawTextHelpFormatter._split_lines
        if text.startswith('R|'):
            return text[2:].splitlines()  
        return argparse.HelpFormatter._split_lines(self, text, width)

#
# we expect:
# +------+-------------+-----+
# | C1   | C2          | C3  |
# +------+-------------+-----+
# |data1 | data2       | da3 |
# |dat21 | dat22       | d23 |
# +------+-------------+-----+
#
# we return:
# [ { "C1":"data1","C2":"data2","C3":"da3" },
#   { "C1":"dat21","C2":"dat22","C3":"d23" } ]
#

def f2(foo):
  retval = ''
  for char in foo:
    retval += char if not char == '\n' else ''
    if char == '\n':
        yield retval
        retval = ''
  if retval:
    yield retval

def tbltojson(td):
    i = 0
    ndr = []
    res = []
    for l in f2(td):
	if i == 0:
	    pass
        elif i == 2:
	    pass
        elif i == 1:
            logging.debug('header is %s', l)
	    hdr = re.split(r'^\| |\s* \| | \s*\|$', l)
	    hdr.pop(0)
	    hdr.pop()
	    for h in hdr:
		ndr.append(re.sub(' ', '_', h))
	    logging.debug('split is %s', hdr)
	    logging.debug('fixed is %s', ndr)
        elif l[:2] == '| ':
	    hdr = re.split(r'^\| |\s* \| | \s*\|$', l)
	    hdr.pop(0)
	    hdr.pop()
            logging.debug('data line %s', l)
	    logging.debug('columns is %s', hdr)
	    res.append(dict(zip(ndr, hdr)))
	else:
            logging.debug('last line %s', l)
	i = i + 1


    return json.dumps(res)

def run():
    loglevel = "WARNING"

    home = expanduser("~")
    prog = os.path.basename(__file__)
    cfn = home + '/' + '.' + os.path.splitext(prog)[0] + '.conf'

    p = argparse.ArgumentParser(description="table (mysql query output) to json conversion",
            formatter_class=SmartFormatter)

    # overall app related stuff
    p.add_argument('-p', '--pretty', action='store_true', dest='pretty', default=False)
    p.add_argument('-t', '--type', action='store', dest='output_type',
            default='yaml',
            choices=['json','yaml'],
            help='Output type, json or yaml' )
    # these are the command line leftovers, the file to process
    p.add_argument('file', nargs='*')

    # non application related stuff
    p.add_argument('-l', '--loglevel', action='store', dest='loglevel',
            default=loglevel,
            choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'],
            help='Log level (DEBUG,INFO,WARNING,ERROR,CRITICAL) default is: '+loglevel)
    p.add_argument('-s', '--save', action='store_true', dest='save',
            default=False, help='save select command line arguments (default is always) in "'+cfn+'" file')

    # read in defaults from ~/.PROGBASENAMENOSUFFIX
    # if the file exists
    if os.path.isfile(cfn):
        argparse_config.read_config_file(p,cfn)

    # parse arguments (after reading defaults from ~/.dot file
    args = p.parse_args()
    if args.loglevel:
        loglevel = args.loglevel

    # set our logging level (from -l INFO (or whatever))
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s', loglevel)
    logging.basicConfig(level=numeric_level)

    logging.info('Program starting :%s', prog)
    logging.debug('Arg: pretty     :%s', args.pretty)
    logging.debug('Arg: type       :%s', args.output_type)
    logging.debug('Arg: loglevel   :%s', loglevel)
    logging.debug('Arg: save       :%s', args.save)

    # save to the defaults file if a -s specified on command line
    if args.save:
        f = open(cfn, 'w')
        # remove the 'save' from the file
        f.write(re.sub('\naddminion\n', re.sub('\nsave\n','\n',argparse_config.generate_config(p, args, section='default'))))
        f.close()

    # here we go, start of program here
    s_out = { "apiVersion":"v1", "kind":"List", "items":[] }

    av = args.file
    if len(av) > 0:
        for i in range(len(av)):
            i_file = None
            if av[i] == '-':
                i_file = sys.stdin
            else:
                i_file = open(av[i])
            s_out['items'].append(yaml.load(tbltojson(i_file.read())))
    else:
        logging.debug("no arguments specified, stdin assumed")
        s_out['items'].append(yaml.load(tbltojson(sys.stdin.read())))

    # if we are only messing with a single file...
    s = s_out
    if len(av) < 2:
        s = s_out['items'][0]

    if args.output_type == 'yaml':
        print yaml.dump(s)
    elif args.output_type == 'json':
        if args.pretty:
            print json.dumps(s, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            print json.dumps(s)
    else:
        raise ValueError('Invalid output type : %s', args.output_type)

if __name__ == '__main__':
   run()
