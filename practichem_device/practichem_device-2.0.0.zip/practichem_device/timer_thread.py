"""
Copyright 2015 Practichem, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from threading import Thread, Event

# Adapted from http://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds


class TimerThread(Thread):
	""" Use a thread to call a function repeatedly 	"""

	def __init__(self, callback, delayTimeInSeconds):
		Thread.__init__(self)
		self.event = Event()
		self.callback = callback
		self.delayTimeInSeconds = delayTimeInSeconds

	def run(self):
		""" Start the call loop.
		Called by Start() on the thread.
		"""
		while not self.event.wait(self.delayTimeInSeconds):
			self.callback()

	def stop(self):
		""" Stop calling the function and exit. """
		self.event.set()
