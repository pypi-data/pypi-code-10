import os
import json
import fileinput

def timeSinceLastFailure(searchedTest, hist):
	# Search history for test
	time = 1
	for log in reversed(hist):
		for test in log['tests']:
			if test['path'] == searchedTest[0] + searchedTest[1] + searchedTest[2]:
				if test['result'] != 'ok':
					return time
		time += 1
	return 999999 # simulate infinity with large number

def timeSinceLastExecution(searchedTest, hist):
	# Search history for test
	time = 1
	for log in reversed(hist):
		for test in log['tests']:
			if test['path'] == searchedTest[0] + searchedTest[1] + searchedTest[2]:
				return time
		time += 1
	return 999999 # simulate infinity with large number

# Sets priority of a test
def setPriority(test, filepath, priority):
	attrExists = False
	for line in reversed(open(filepath).readlines()):
		if test + '.priority' in line:
			attrExists = True
			break
		if 'def ' + test in line:
			break
	if attrExists:
		for line in fileinput.input(filepath, inplace=True):
				if test + '.priority' in line:
					print test + '.priority=' + str(priority) + ' # prioritize\n',
				else:
					print line,
	else:
		with open(filepath, 'a') as f:
				f.write("\n" + test + ".priority = " + str(priority) + " # prioritize")

def prioritize(args):
	# Import log of previous nose execution
	if args['log']:
		# Add log to test history
		log = {'date' : '',
					'tests' : []
		}
		with open(args['log'], 'r') as f:
			date = None
			for line in f:
				if 'date' == line.rstrip('\n'):
					line = next(f)
					date = line.rstrip('\n')
					log['date'] = date
				if " ... " in line:
					linePieces = line.split(' ')
					newObject = {}
					newObject['path'] = linePieces[0]
					newObject['result'] = linePieces[2].rstrip('\n')	
					log['tests'].append(newObject)
		data = None
		with open(os.path.dirname(__file__) + '/data.json', 'r') as f:
			data = json.load(f)
		with open(os.path.dirname(__file__) + '/data.json', 'w') as f:
			data.append(log)
			json.dump(data, f)

	# Set priorities
	if not args['no_priority']:
		# Import test history
		hist = None
		with open(os.path.dirname(__file__) + '/data.json', 'r') as f:
			hist = json.load(f)
		
		# Get execution window
		execWindow = None
		if args['exec_window']:
			execWindow = args['exec_window']
		else:
			execWindow = 9 # default to 9

		# Get failure window
		failWindow = None
		if args['fail_window']:
			failWindow = args['fail_window']
		else:
			failWindow = 5 # default to 5

		# Collect old tests
		import subprocess
		import re
		p = subprocess.Popen(['nosetests', '--collect-only', '-v', '-a', 'priority'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		out, out2 = p.communicate()
		lines = out2.split('\n')
		oldTests = []
		for line in lines:
			if line[-6:-3] == '...':
				testPath = line[:-7]
				test = testPath.rpartition('.')
				oldTests.append(test)

		# Set old tests to priority={1,2}
		for test in oldTests:
			if timeSinceLastFailure(test, hist) <= failWindow:
				setPriority(test[2], test[0].replace(".", "/") + '.py', 1) # assumes filepath ends in '.py' and doesn't contain '.'
			elif timeSinceLastExecution(test, hist) > execWindow:
				setPriority(test[2], test[0].replace(".", "/") + '.py', 1) # assumes filepath ends in '.py' and doesn't contain '.'
			else:
				setPriority(test[2], test[0].replace(".", "/") + '.py', 2) # assumes filepath ends in '.py' and doesn't contain '.'

		if not args['ignore_new']:
			# Collect new tests/unprioritized tests
			p = subprocess.Popen(['nosetests', '--collect-only', '-v', '-a', '!priority'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, out2 = p.communicate()
			lines = out2.split('\n')
			newTests = []
			for line in lines:
				if line[-6:-3] == '...':
					testPath = line[:-7]
					test = testPath.rpartition('.')
					newTests.append(test)

			# Set new/unprioritized tests to priority=1
			for test in newTests:
				setPriority(test[2], test[0].replace(".", "/") + '.py', 1) # assumes filepath ends in '.py' and doesn't contain '.'
				# with open(test[0].replace('.','/') + '.py', 'a') as f:
				# 	f.write('\n' + test[2] + '.priority = 1 # prioritize')