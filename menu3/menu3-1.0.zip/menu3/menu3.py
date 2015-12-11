#
# Menu3 - (C) 2015 Patrick Lambert - Provided under the MIT License - https://github.com/dendory/menu3
#
import os
class Menu:
	NORMAL = "\033[0m"
	YELLOW = "\033[93m"
	RED = "\033[91m"
	BLUE = "\033[94m"
	GREEN = "\033[92m"
	BOLD = "\033[1m"
	UNDERLINE = "\033[4m"
	ALLOW_QUIT = True

	def warn(self, text): # Print a warning message
		if self._windows():
			print("* " + text)
		else:
			print(self.BOLD + "* " + text + self.NORMAL)

	def fail(self, text): # Print a fail message
		if self._windows():
			print("* " + text)
		else:
			print(self.RED + "* " + text + self.NORMAL)

	def info(self, text): # Print an info message
		if self._windows():
			print("* " + text)
		else:
			print(self.BLUE + "* " + text + self.NORMAL)

	def success(self, text): # Print a success message
		if self._windows():
			print("* " + text)
		else:
			print(self.GREEN + "* " + text + self.NORMAL)

	def bold(self, text): # Print bold text
		if self._windows():
			return text
		else:
			return self.BOLD + text + self.NORMAL

	def underline(self, text): # Print an underline text
		if self._windows():
			return text
		else:
			return self.UNDERLINE + text + self.NORMAL

	def menu(self, title, choices, prompt = ""): # Print a menu and return the selected choice
		if prompt == "":
			prompt = "Your choice, 'q' to quit:" if self.ALLOW_QUIT else "Your choice:"
		num = "a"
		while not self._is_int(num) or int(num) < 0 or int(num) > len(choices):
			i = 1
			print()
			print(self.underline(title))
			for choice in choices:
				print(self.bold("[" + str(i) + "]") + "\t" + choice)
				i += 1
			num = str(input(self.bold(prompt + " ")))
			if self.ALLOW_QUIT and num.lower() == "q":
				quit()
		return int(num)

	def config_menu(self, title, config, prompt = "", return_choice = "Return"): # Print a configuration menu with default values, returning the modified dict
		while True:
			choices = []
			for k in config.keys():
				choices.append(k + ": " + self.underline(str(config[k])))
			choices.append(return_choice)
			a = self. menu(title, choices, prompt)
			if a == len(choices):
				return config
			(key, oldvalue) = choices[a-1].split(': ', 1)
			b = input(self.bold(key + " [" + oldvalue + "]: "))
			if b != "":
				if self._is_int(b):
					config[key] = int(b)
				else:
					config[key] = str(b)

	def _windows(self): # Colors are not available on Windows
		if os.name == "nt":
			return True
		return False

	def _is_int(self, text): # Check if a variable is an int
		try:
			int(text)
			return True
		except ValueError:
			return False

	def __init__(self, ALLOW_QUIT = True):
		self.ALLOW_QUIT = ALLOW_QUIT
		pass