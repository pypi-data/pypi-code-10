import json
import re

from math import sqrt
from nltk.corpus import cmudict
from num2words import num2words

class Readability(object):
	"""
	Calculate various readability score indexes
	"""

	# total number of sentences
	tot_sentences = 0 

	# input text stripped of all punctuation
	formatted = str()

	# list of individual words
	words = list()

	# total number of words	
	tot_words = 0

	# list of words not found in the NLTK
	not_found = list()

	# the NLTK syllable dictionary
	syl = dict()

	# total number of syllables
	tot_syl = 0

	# initialize the readability scores to 0
	flesch_kincaid = 0
	flesch_kincaid_gl = 0
	coleman_liau = 0
	smog = 0

	# empty dictionary for json result
	result = dict()

	def num_syl(self, word):
		"""
		Return the number of syllables.

		This is a helper method for the other readability score methods. 
		You can call it directly against a particular word if you would like.
		"""

		# substitute integers for the word
		# example: 10 should be "ten"
		if re.match('^[0-9]+$', word):	
			word = num2words(int(word))

		# this block protects against KeyErrors
		if word in self.syl:
			return [len(list(y for y in x if y[-1].isdigit())) for x in self.syl[word]][0]		
		else:
			if (re.match('\b', word) or word in self.not_found):
				pass
			else:
				self.not_found.append(word)
			return 0

	def flesch_kincaid_reading_ease(self):
		"""
		The Flesch-Kincaid Reading Ease test scores how difficult something is to read,
		with higher numbers being easier to read, and lower numbers being more difficult to read.

		The following is a chart showing the ranges and associated reading levels:

		+-------------+-----------------------------------------------------+
		| Score       | Notes                                               |
		+-------------+-----------------------------------------------------+
		| 90.0-100.0  | easily understood by an average 11-year-old student |
		| 60.0-70.0   | easily understood by 13- to 15-year-old students    |
		| 0.0-30.0    | best understood by university graduates             |
		+-------------+-----------------------------------------------------+

		Note that it is theoretically possible for a score to be higher than 100 or
		lower than 0.  Scores in this range do not indicate a problem with the algorithm.
		"""

		return round(206.835-(1.015*(self.tot_words/self.tot_sentences))-(84.6*(self.tot_syl/self.tot_words)),2)

	def flesch_kincaid_grade_level(self):
		"""
		The Flesch-Kincaid Grade Level score indicates the approximate grade level at which
		a passage is written.  

		When the formula results in a value greater than 10, the score can also represent the 
		number of years of formal education needed to understand the text.
		"""

		return round((0.39*(self.tot_words/self.tot_sentences))+(11.8*(self.tot_syl/self.tot_words))-15.59,2)

	def coleman_liau_score(self):
		"""
		The Coleman-Liau index indicates the approximate grade level at which a passage is written.
		"""

		num_letters = len(re.sub('\s', '', self.formatted))
		
		L = (num_letters / self.tot_words)*100
		S = (self.tot_sentences / self.tot_words)*100

		return round((0.0588*L)-(0.296*S)-15.8,2)

	def smog_grade(self):
		"""
		The SMOG grade is a measure of the number of years of education needed to understand the input text.
		"""

		# number of polysyllabic words
		num_pswords = len([x for x in self.words if self.num_syl(x) >= 3])

		a = num_pswords*(30/self.tot_sentences)

		return round(1.0430*sqrt(a)+3.1291,2)

	def main(self):
		"""
		Calculate all readability scores and populate class variables with them
		"""
		self.flesch_kincaid = self.flesch_kincaid_reading_ease()
		self.flesch_kincaid_gl = self.flesch_kincaid_grade_level()
		self.coleman_liau = self.coleman_liau_score()
		self.smog = self.smog_grade()

		self.result = json.dumps(
					  {'flesch_kincaid' : self.flesch_kincaid,
					   'flesch_kincaid_grade_level' : self.flesch_kincaid_gl,
					   'coleman_liau' : self.coleman_liau,
					   'smog' : self.smog,
					   'words_not_found' : self.not_found},
					  sort_keys=True, indent=4)

	def __init__(self, text):
		super(Readability, self).__init__()

		# make everything lowercase
		input_txt = text.lower()

		# readability formulas need the number of words, syllables, & sentences
		# treat ! and ? like periods to get the # of sentences
		sentences = re.sub('[?!]', '.', input_txt)

		self.tot_sentences = len(sentences.split('.'))
		
		# get rid of punctuation and newlines in the input text so we can get
		# an accurate list of words to be matched in the syllable dictionary
		self.formatted = re.sub('[;,:.\(\)\[\]\-?!\n]', ' ', input_txt)

		# populate the list of individual words
		self.words = self.formatted.split(' ')			

		# set how many words there are
		self.tot_words = len(self.words)

		# keep track of words not found in the NLTK corpus
		self.not_found = []		

		# setup the syllable dictionary
		self.syl = cmudict.dict()

		# set the total number of syllables
		self.tot_syl = sum([self.num_syl(x) for x in self.words if x != ''])
			
		self.main()

		
		
