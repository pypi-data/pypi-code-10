
from ..cat263 import Components, MDRd, NkRd
from ...results import Results


class Amazius(Results):
	code = 'SIA 263:13'
	selection = ['nrd', 'vrd', 'mrdy', 'mrdz', 'mdrd', 'nkrd_y', 'nkrd_z']

	def __init__(self, entries):

		self.cat = Components(entries)
		self.cross_section_class = entries['cross_section_class']
		self.ned = entries['ned']
		self.ved = entries['ved']
		self.myed = entries['medy']
		self.mzed = entries['medz']
		self.entries = entries

	def add_sel(self, sel):
		if sel not in self.selection:
			self.selection.append(sel)
		

	def compute(self):
		mdrd = MDRd(self.entries)
		mdrd.mdrd()
		nkrd = NkRd(self.entries)
		nkrd.nkrd_y()
		nkrd.nkrd_z()
		
		if self.cross_section_class == '1 + 2':
			self.class_1()

		return  self.get_results()

	def class_1(self):
		self.cat.nrd()
		self.cat.myrd()
		self.cat.mzrd()
		self.cat.vrd()

		if self.ved > 0:
			self.cat.mvrd(self.ved)
			self.add_sel('mvrd')
						
		if self.ned > 0 and self.myed > 0:
			self.cat.f49(self.ned, self.mzed, 'y')
			self.add_sel('f49_y')
		
		if self.ned > 0 and self.mzed > 0:
			self.cat.f49(self.ned, self.mzed, 'z')
			self.add_sel('f49_z')

		if self.ned > 0 and self.myed > 0 and self.mzed > 0:
			self.cat.f44(self.ned, self.myed, self.mzed)
			self.add_sel('f44')

			self.cat.f48(self.ned, self.myed, self.mzed)
			self.add_sel('f48')

			self.cat.f50(self.ned, self.myed, self.mzed)
			self.add_sel('f50')
		
		if self.ned > 0:
			self.cat.mynrd(self.ned)
			self.add_sel('mynrd')

			self.cat.mznrd(self.ned)
			self.add_sel('mznrd')

	def vrd(self):
		pass



 
