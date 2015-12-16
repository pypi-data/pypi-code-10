class Leet:

	def __init__(self, text):
		self.text = text

	def translate(self):
		phrase = {
		"cker": "xxor",
		"ckers": "xxorz",
		}

		chars = {
		"a": "@",
		"e": "3",
		"i": "!",
		"o": "0",
		#"u": u'+03BC',
		"s": "5",
		}

		for p in phrase:
			self.text = self.text.replace(p, phrase.get(p))

		for c in chars:
			self.text = self.text.replace(c, chars.get(c))

		return self.text