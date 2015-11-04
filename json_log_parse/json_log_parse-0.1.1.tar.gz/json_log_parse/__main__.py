"""
@package {name: "json_log_parse"}
@module-attributes
@author {name: "Craig Simons", email: "craigsimons@sfu.ca"}
@copyright {entity: "Craig Simons", year: "2015"}
@license {name: "MIT", url: "https://opensource.org/licenses/MIT"}

I like to look at log files. I like data JSON formatted, because I don't know what I'm going to do with it next. I'm not good with RegEx. That's where this script comes in.

# Usage

## Piping StdIn
Data cen be piped directed from standard input. All that is required is the columns you wish to see.

Example:
```bash
echo '{"name": "column name", "message": "This is a potentially long message that might have to be wrapped!"}' | python ~/apps/json_log_parse.py -c name,message
```
Should output
```bash
column name           This is a potentially long     
                      message that might have to be  
                      wrapped! 
```

"""

import sys
import json
import argparse
import select
from argparse import RawTextHelpFormatter
import re
import os
import subprocess
import select
import time
import platform
from Column import Column

# Command line arguments
# @var {dataType: "dict()"}
args = {}

# A list of dictionaries with individual column defaults. This allows the user to specify a custom config for one/more columns that differ from the global config.
# Format of dict needs to be:
# ```python
# {
#	"minSize": integer,
#	"maxSize": integer,
#	"justify": string	
# }
# ```
# @var {dataType: "list(dict())"}
columnConfig = []

def getArgs():
	"""
	Gets command line arguments and switches.
	@return {dataType: "dict()", comment: "Command Line arguments."}
	"""

	desc = 	"##########################################\n"
	desc += "#              json_log_parse            #\n"
	desc += "##########################################\n"
	desc += "\n\n"
	desc += "This script attempts to decode a JSON formatted log file and nicely output the format to the screen. This is useful for search/parsing JSON formatted logs that would otherwise be a mess of markup. \n\n"
	desc += ""
	parser = argparse.ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
	parser.add_argument("-o", "--offset", help="The offset to start looking at a log line. Usually not required as script will look for first instance of '{' and read to the end of the line. (default: %(default)s)\n\n", required=False, default=0, type=int)
	parser.add_argument("-c", "--columns", help="Comma separated list of columns to output. \n\n", required=True, default="")
	parser.add_argument("-d", "--delimiter", help="Specifies the string that will separated the columns in the output. (default: \"%(default)s\") \n\n", required=False, default="  ")
	parser.add_argument("-f", "--file", help="Process an entire file instead of piping to it. Use in conjunction with '--tail' to provide pseudo 'tail -f' functionality. \n\n", required=False, default="")
	parser.add_argument("-t", "--tail", help="Provide tail-like functionality. Used in conjunction with the 'file' argument. (default: %(default)s)\n\n", required=False, action="store_true", default=False)
	parser.add_argument("-j", "--justify", help="Default text justification. (default: %(default)s)\n\n", required=False, default="left")
	parser.add_argument("-m", "--maxwidth", help="Maximum size of column. If the data contained in the column exceeds this value it will be wrapped. (default: %(default)s)\n\n", required=False, default=30, type=int)
	parser.add_argument("-n", "--minwidth", help="Minimum size of column. The column size will expand to the maximum. Useful for small columns that never come close to max. (default: %(default)s)\n\n", required=False, default=20, type=int)
	result = parser.parse_args()

	return result

def getColumnConfig(): 
	"""
	Returns a configuration that should be stored in {@link #columnConfig}.

	Dict format:
	```python
	{
	  "name": string,
	"minSize": integer,
	"maxSize": integer,
	"justify": string	
	}
	```
	@param {dataType: "list(string)"}
	@return {list(dict())}
	"""

	global args

	r = re.compile(r'(?:[^,(]|\([^)]*\))+')
	columns = r.findall(args.columns)	
	columnList = []
	minWidth = args.minwidth
	maxWidth = args.maxwidth
	justify = args.justify

	for column in columns:
		items = column.split("(")
		if len(items) > 1:
			config = items[1].replace(")","").split(",")
			minWidth = int(config[0].strip())

			if len(config) > 1:
				maxWidth = int(config[1].strip())

			if len(config) > 2:
				justify = config[2].strip()

		# check thar min is less/= max
		if minWidth > maxWidth:
			print "Error: column \"" + items[0] + "\" was specified with a minimum greater than the maximum"
			sys.exit(1)

		columnList.append({
			"name": items[0],
			"minWidth": minWidth,
			"maxWidth": maxWidth,
			"justify": justify
		})

	return columnList

def getMaxRowCount(columns):
	"""
	Determines the maximum number of rows within a list of {@link #Column Column objects}.
	@param {name: "columns", dataType: "list(Column)"}
	@return {dataType: "integer"}
	"""
	maxRows = 0
	for column in columns:
		if column.rowCount > maxRows:
			maxRows = column.rowCount
	return maxRows

def main():
	""" 
	The main part of the program.
	@return {dataType: "None"}
	"""

	# Global variables
	global args, columnConfig

	# get command line arguments
	args = getArgs()

	# get the column config
	columnConfig = getColumnConfig()

	if args.file and args.tail:
		printFromPolledFile()
	elif args.file:
		printFromFile()
	else:
		printFromStdIn()

def printFromPolledFile():
	"""
	Registers a subprocess to tail, so we can monitor file changes. Then we output when it changes, thus emulating a "tail -f".
	@return {dataType: "None"}
	"""
	# exit if we are on windows because it doesn't understand pipes.
	if platform.system() == "Windows":
		print "Error: Tailing isn't compatible on Windows... sorry."
		sys.exit(1)

	f = subprocess.Popen(['tail', '-F', args.file], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	p = select.poll()
	p.register(f.stdout)

	# loop endlessly with a poller. Only exit when requested by user
	try:
		while True:
			if p.poll(1):
				for line in iter(f.stdout.readline, b''):
					# decode the JSON and parse into column objects
					columns = parseLine(line)

					# get the number of rows this line will have
					rowCount = getMaxRowCount(columns)

					# print a line for each row
					for i in range(rowCount):
						output = ""
						for column in columns:
							output += (column.formattedRows[i] if i < column.rowCount else "".ljust(column.actualWidth)) + args.delimiter
						print output
	except KeyboardInterrupt:
		sys.exit(0)

def printFromFile():
	"""
	If the file arugment is specified, we'll read from a file instead of defaulting to stdin.
	@return {dataType: "None"}
	"""
	global args, columnConfig

	# ensure the path actually exisits
	if not os.path.isfile(args.file):
		print "Error: The file path specified is invalid (" + args.file + ")"
		sys.exit(1)

	with open(args.file) as f:
		for line in f:
			# decode the JSON and parse into column objects
			columns = parseLine(line)

			# get the number of rows this line will have
			rowCount = getMaxRowCount(columns)

			# print a line for each row
			for i in range(rowCount):
				output = ""
				for column in columns:
					output += (column.formattedRows[i] if i < column.rowCount else "".ljust(column.actualWidth)) + args.delimiter
				print output			

def printFromStdIn():
	"""
	Looks at stdin for line data. This is useful for file 'cat', 'head' or 'tail' operations or anything that comes from std input
	@return {dataType: "None"}
	"""
	global args, columnConfig

	for line in sys.stdin:
		# decode the JSON and parse into column objects
		columns = parseLine(line)

		# get the number of rows this line will have
		rowCount = getMaxRowCount(columns)

		# print a line for each row
		for i in range(rowCount):
			output = ""
			for column in columns:
				output += (column.formattedRows[i] if i < column.rowCount else "".ljust(column.actualWidth)) + args.delimiter
			print output

def parseLine(line):
	"""
	Reads a line and attempts a JSON decode. This function automatically looks for the first instance of an opening bracket '{', 
	and continues until the end of the line. The parsing will respect a given offset, but perhaps that's a bit redundant.
	@param {name: "line", dataType: "string", comment: "Line of input."}
	@return 
	"""
	global args, columnConfig

	try:
		result = json.loads(line[line[args.offset:].index('{'):].encode('utf-8'))
	except ValueError:
		return []
	except UnicodeEncodeError:
		return []

	# You didn't specify any columns
	if not args.columns:
		return "No specified columns to print.\n"

	columnList = []
	for column in columnConfig:
		columnList.append(Column(
			column["name"], 
			result[column["name"]].encode('utf-8') if column["name"] in result else "",
			justify = column["justify"],
			minWidth = column["minWidth"],
			maxWidth = column["maxWidth"]
		))

	return columnList

if __name__ == "__main__":
	main()
