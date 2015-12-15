import re

each = re.compile('::for\s+(.*?)\s+in\s+(.*?)\s*:')
ifc = re.compile('::(?:el)?if\s+(.*?)\s*:')
include = re.compile('::include\(([^,]*),([^\)]*)\)')
w = re.compile('::with(.*?)as(.*?):')
