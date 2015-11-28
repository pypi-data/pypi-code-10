#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  BackUpa.py
#  
#  Copyright 2015 MetalUpa <headmodofv@redchan.it>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
   
import sys
import HTMLParser
import os
import urllib
import argparse
import re

#### Get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Choose input file.")
parser.add_argument("-d","--debug", action="store_true", default="False",
	help="Enable debug.")
parser.add_argument("--fancy", action="store_true", default="False",
	help="Enables prettier filenames. This is NOT for use with Windows"
	" systems as it creates invalid filenames.")
parser.add_argument("-o","--output", help="Choose output location to"
	" create folder in. If not specified, it will be created in your"
	" current directory.")
args = parser.parse_args()

inputFile=args.input

if args.debug == True:
    print "Debug on"

if args.fancy == True:
	print "Fancy filenames on. WARNING: Doesn't work with Windows!"

#### Format the output directory path
if args.output: # If you defined an output directory, process it
	outputDirectory=args.output 
	if os.path.exists(outputDirectory) == 0: # Exit if not valid directory
		print "Output directory is not valid."
		sys.exit(2)
	if outputDirectory[-1:] == "/": # Formatting for extra slash
		finalDirectory=outputDirectory+"archivebackup/"
	else:
		finalDirectory=outputDirectory+"/archivebackup/"
else: # If not, put one in the working directory
	outputDirectory=os.getcwd()
	finalDirectory=outputDirectory+"/archivebackup/"
				
if args.debug == True:
	print "Input File = {}".format(inputFile)
	print "Output Directory = {}".format(outputDirectory)    
	print "Final Directory = {}".format(finalDirectory) 

#### Create directory for files if necessary
if "archivebackup" not in os.listdir(outputDirectory):
	print "Creating folder archivebackup in {}".format(outputDirectory)
	os.mkdir(finalDirectory)
else:
	print "Adding files to archivebackup in {}".format(outputDirectory)

#### Parse links and create list of truncated links
archiveRaw=[]
archiveLinks=[]
archiveZip=[]
strippedLines=[]
for line in open(inputFile):
    if "archive.is/" or "archive.today/" in line: # Is this redundant?
		line=line.strip()
		if args.debug == True:
			strippedLines.append(line)
		for i in range(len(line)): # Find an archive.is/ or archive.today/ ...
			if line.startswith('archive.is/', i) and line[i+11:i+16].isalnum() \
				and line[i+11:i+16]!='favic': # pesky Firefox bookmark export issue
					archiveLinks.append(line[i+11:i+16]) # ... and add to list
			if line.startswith('archive.today/', i) and line[i+14:i+19].isalnum() \
				and line[i+11:i+16]!='favic': # pesky Firefox bookmark export issue
					archiveLinks.append(line[i+14:i+19])# ... and add to list

if args.debug == True:
	print "Stripped Lines = {}".format(strippedLines)
	print "Truncated Archive Links = {}".format(archiveLinks)

#### Function to grab dates and titles, used below
#### Too lazy to make a main() call so here it is in the middle of the script
def getTitle(url):
	# Download and parse the raw HTML of the page
	print "Getting info for {}...".format(url)
	response = urllib.urlopen(url)
	html=response.read()
	html=html.strip()
	##########
	# I fear this next part may break depending on the website.
	# Also this is inefficient and will kill a toaster. Need a better method ASAP.
	##########
	# It searches for specific parts that archive.is adds in the top bar.
	# These parts contain the title and archive date for tweeting purposes.
	# The "UTC" at the end of the date section makes it easy to find this section.
	# The title search has to look ahead to something specific and it may break.
	# Could be an irrational fear, though.
	##########
	for i in range(len(html)): # Date (this works just fine)
		if html.startswith('twitter:description',i): # Find section with date in HTML
			j = html.find('UTC',i+39,i+100) # Find the last characters in the string
			title=html[i+39:j+3] # Append only the date
	for i in range(len(html)): # Page title (not sure about this one)
		if html.startswith('twitter:title',i): # Find section with title in HTML
			j = html.find('meta property',i+19,i+250) # Find the _next_ string
			title+=" - "+html[i+24:j-4] # Go backwards and append only the title
	# Improve formatting (incomplete)
	title=title.replace("&#x2018;","\'") # Turn &#x2018; into '
	title=title.replace("&#x2019;","\'") # Turn &#x2019; into '
	title=title.replace("&#x2026;","...") # Turn &#x2026; into ellipsis
	# Prune other invalid chars as last resort
	if args.fancy != True: # Purge illegal characters unless fancy is enabled
		title=re.sub(r"[\/\\\:\*\?\"\<\>\|]", '_', title) # Straight-up cargo culted this
	return title

#### Format truncated links and download backups
#### BONUS: Define fewer variables and just cat things together as needed
for line in archiveLinks:
	lineURL="https://archive.is/"+line # URL to view archive
	lineZip="https://archive.is/download/"+line+".zip" # URL to download .zip
	title=getTitle(lineURL)
	if len(title) >= 250: # Max char limit is 255 for Windows
		title=title[0:249] 
	zipCheck=title+".zip"
	zipName=finalDirectory+zipCheck # May need to tweak this
	if zipCheck not in os.listdir(finalDirectory): # Don't DL if file exists
		print "Downloading {}...".format(zipCheck)
		urllib.urlretrieve(lineZip,zipName)
		#### BONUS: Progress bar for each download
	else:
		print "{} already exists. Skipping...".format(zipCheck)

#### print completion message
print "Congration, you done it."
