"""
@package {name: "json_log_parse"}
@module-attributes
@author {name: "Craig Simons", email: "craigsimons@sfu.ca"}
@copyright {entity: "Craig Simons", year: "2015"}
@license {name: "MIT", url: "https://opensource.org/licenses/MIT"}
"""

import re
import math

class Column(object):
	"""
	@package {name: "global"}

	A non-nested JSON object can be parsed in to a list of key/value pairs, aka "Columns". This class provides the functionality to split the data into appropriate rows, according to the 
	allowable limits. As it is assumed each column is going to be printed to a screen, it will provide the padding necessary to maintain good formatting.
	"""
	# The minimum column size. Line will be padded to match this size.
	# @var {dataType: "integer"}
	minWidth = 20

	# The maximum column size. Line will be padded to match this size.
	# @var {dataType: "integer"}
	maxWidth = 30

	# The actual width of this column. This is a calculated property that is by default the minumum, but can be any number up to the maximum.
	# 
	# Calculated in {@link #padRows}.
	# @var {dataType: "integer"}
	actualWidth = 20

	# The lines of text that will be presented as rows. These are NOT padded and formatted.
	# @var {dataType: "list(string)"}
	rows = []

	# The number of rows. This is property calculated by {@link #formatRows}.
	# @var {dataType: "integer"}
	rowCount = 0

	# The row data after all formatting has taken place.
	# @var {dataType: "list(string)"}
	formattedRows = []

	# The name of the column, which may be used as the header.
	# @var {dataType: "string"}
	name = ""

	# Justification of the line text
	# @var {dataType: "string", permittedValues: ["left", "center", "right"], defaultValue: "left"}
	justify = "left"

	# The original line of text
	# @var {dataType: "string"}
	line = ""

	def __init__(self, name, line, **kwargs):
		"""
		The constructor. 
		
		Keyword arguments include:
		- {@link #minWidth}
		- {@link #maxWidth}
		- {@link #name}
		- {@link #justify}
		
		@param {name: "line", comment: "The line of text to be analyzed."}
		@param {name: "**kwargs", comment: "Keyword arguments."}
		@return {dataType: "None"}
		"""
		# init default values
		self.minWidth = kwargs.get("minWidth", 20)
		self.maxWidth = kwargs.get("maxWidth", 30)
		self.actualWidth = self.minWidth
		self.name = name
		self.justify = kwargs.get("justify", "left")
		self.line = line
		self.formattedRows = []
		self.rows = self.wrapLineIntoRows()
		self.formatRows()

	def wrapOnSpace(self, text):
		"""
		A word-wrap function that preserves existing line breaks and most spaces in the text. Expects that existing line breaks are posix newlines (\n).
		@param {name: "text", dataType: "string", comment: "The line of text that will be analyzed."}
		@return {dataType: "list(string)"}
		"""
		return reduce(lambda line, word, width=self.maxWidth: "%s%s%s" % (line, " \n"[(len(line[line.rfind("\n")+1:]) + len(word.split("\n",1)[0]) >= self.maxWidth)], word),text.split(" "))

	def wrapAlways(self, text):
		"""
		A simple word-wrap function that wraps text on exactly width characters. It doesn't split the text in words.
		@param {name: "text", dataType: "string", comment: "The line of text that will be analyzed."}
		@return {dataType: "string"}	
		"""
		return "\n".join([ text[self.maxWidth*i:self.maxWidth*(i+1)] for i in xrange(int(math.ceil(1.*len(text)/self.maxWidth))) ])

	def wrapOnSpaceStrict(self, text):
		"""
		Similar to wrapOnSpace, but enforces the width constraint: words longer than width are split.
		@param {name: "text", dataType: "string", comment: "The line of text that will be analyzed."}
		@return {dataType: "list(string)"}	
		"""
		wordRegex = re.compile(r"\S{"+str(self.maxWidth)+r",}")
		return self.wrapOnSpace(wordRegex.sub(lambda m: self.wrapAlways(m.group()),text))

	def wrapLineIntoRows(self):
		return self.wrapOnSpaceStrict(self.line).split("\n")

	def formatRows(self):
		""" 
		Determines the proper padding required for each line. By default, each row will be padded to the minumum. 
		However, if one of the rows requires additional padding, we'll ensure ALL of the rows get the same. 
		@return {dataType: list(string)}
		"""

		self.formattedRows = []
		self.rowCount = len(self.rows)

		# get the biggest row so we know how much to pad.
		# we already know the biggest row will not exceed the maximum
		for row in self.rows:
			if len(row) > self.actualWidth:
				self.actualWidth = len(row)

		# pad and justify the row to what we need.
		for row in self.rows:
			if self.justify == "right":
				row = row.rjust(self.actualWidth)
			elif self.justify == "center":
				row = row.center(self.actualWidth)
			else:
				row = row.ljust(self.actualWidth)

			self.formattedRows.append(row)

		return self.formattedRows