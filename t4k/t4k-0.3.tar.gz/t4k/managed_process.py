#!/usr/bin/env python

import psutil
from multiprocessing import Process, Pipe

DONE = True
NOT_DONE = False

class ManagedProcess(object):
	'''
	Runs a target function in a subprocess and monitors it.
	The subprocess must call back through a pipe periodically.  If the
	manager doesn't hear from the subprocess after a specified time delay,
	it assumes the subprocess is hung, and so kills the process, and 
	then restarts it by calling the target function again.  
	
	When the target function completes successfully, it should call back
	to the manager and signal that it is done.
	'''

	def __init__(self, target, args=(), kwargs={}, call_delay=60):

		# Register args
		self.target = target
		self.args = args
		self.kwargs = kwargs
		self.call_delay = call_delay


	def _start_managed_process(self):

		# Make a pipe for communication with the subprocess
		self.connection, child_connection = Pipe()
		self.kwargs['pipe'] = child_connection

		# Call target as a separate process
		self.managed_process = Process(
			target=self.target,
			args=self.args,
			kwargs=self.kwargs
		)
		self.managed_process.start()


	def start(self):
		'''
		call <func> inside a subprocess, passing it <args> and <kwargs>.  
		Expect that subprocess to communicate via a pipe every 
		<call_delay> seconds.  If no call back is received after 
		<call_delay> seconds, kill the subprocess, and restart it
		by calling func again with the original arguments.

		The target function must have an argument called pipe, which
		will be passed one end of a multiprocessing.Pipe().  It doesn't
		matter where that argument occurs in the function signature,
		but any arguments after 'pipe' should be filled using <kwargs>.
		'''

		# Start the subprocess
		self._start_managed_process()

		# Monitor it.  Restart if it crashes or hangs.
		status = NOT_DONE
		while status == NOT_DONE:

			# Listen for a call from the subprocess
			responding = self.connection.poll(self.call_delay)

			# If no call was received after call_delay, restart the process
			if not responding:
				print 'Manager: the process is not responding.'

				# If the process is alive, assume it is hung, kill it.
				if self.managed_process.is_alive():
					print (
						'Manager: but it is still alive.  Killing it...'
					)
					kill_proc_tree(self.managed_process.pid)

				# Restart the process
				print 'Manager: respawning process...'
				self._start_managed_process()

			# Update the status based on the subprocess' call
			else:
				status = self.connection.recv()

		print 'Manager: process finished!'


def kill_proc_tree(pid):    
	'''
	Kill the process having id <pid> and kill all of it's children.
	'''

	# get the process
	parent = psutil.Process(pid)

	# get the children recursively
	children = parent.children(recursive=True)

	# kill all children
	for child in children:
		child.kill()
	psutil.wait_procs(children, timeout=5)

	# now kill the parent
	parent.kill()
	parent.wait(5)



