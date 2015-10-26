
from .params import steel_grade_dict
from .szs import Database
from .params import gamma_m1, gamma_m2, e, g
from ..results import Results
from math import pi, sqrt

code = 'SIA 262:13'




class Profile():
	code = 'SIA 262:13'
	selection = ''

	def __init__(self, entries):
		steel_grade = entries['steel_grade']
		self.shape = entries['shape']
		size = entries['size']
		
		self.gamma_m1 = gamma_m1
		self.gamma_m2 = gamma_m2

		db = Database()
		data = db.select_row_dict(self.shape, size)

		self.a = float(data['a'])
		self.av = float(data['av'])
		self.aw = float(data['aw'])
		self.iy = float(data['iy'])*1e6
		self.wely = float(data['wely'])*1e3
		self.wy = float(data['wy'])*1e3
		self.wply = float(data['wply'])*1e3
		self.iy_ = float(data['iy_'])
		self.iz = float(data['iz'])*1e6
		self.welz = float(data['welz'])*1e3
		self.wplz = float(data['wplz'])*1e3
		self.iz_ = float(data['iz_'])
		self.k = float(data['k'])*1e6
		
		self.h = float(data['h'])
		self.b = float(data['b'])
		self.tw = float(data['tw'])
		self.tf = float(data['tf'])
		self.r = float(data['r'])

		self.h1 = float(data['h1'])
		self.k_ = float(data['k_'])
		self.a_ = float(data['a_'])
		self.h2 = float(data['h2'])
		#self.w = float(data['w'])
		#self.dmax = float(data['dmax'])

		t = max(self.tf, self.tw)
		if t <= 40:
			self.fy, self.tau_y, self.fu = steel_grade_dict[steel_grade][0]
		elif t <= 100:
			self.fy, self.tau_y, self.fu = steel_grade_dict[steel_grade][1]
			
		self.profiles_I = [
			'IPE', 'PEA', 'INP', 'HEA', 'HEB', 'HEM', 'HHD', 'HL']
		self.profiles_R = ['RRK', 'RRW']



class Profile2(Profile):
	
	def __init__(self, entries):
		Profile.__init__(self, entries)

		
		steel_grade2 = entries['steel_grade2']
		self.shape2 = entries['shape2']
		size2 = entries['size2']
		
	

class Components(Profile, Results):
	code = code
	selection = ''

	def __init__(self, entries):
		Profile.__init__(self, entries)
		self.entries = entries
		if 'lk' in entries:
			self.lk = entries['lk']
		else:
			self.lk = entries['ld']

		self.ld = self.lk
		self.psi_y = entries['psi']  # !!!!!!!!!!!!!!!!!!!!
		self.psi_z = entries['psi']  #!!!!!!!!!!!!!!!!!!!!!!

	def nrd(self):
		""" (38) """
		term = self.fy*self.a/self.gamma_m1
		self.add_rslt('nrd', round(term*1e-3), 'N.Rd', 'kN', '5.1.2.1', 38)
		return term

	def myrd(self):
		""" (40) """
		term = self.fy*self.wply/self.gamma_m1
		self.add_rslt('mrdy', round(term*1e-6, 1), 'M.y.Rd', 'kNm', '5.1.3.1', 40)
		return term

	def mzrd(self):
		""" (40) """
		term = self.fy*self.wplz/self.gamma_m1
		self.add_rslt('mrdz', round(term*1e-6, 1), 'M.z.Rd', 'kNm', '5.1.3.1', 40)
		return term

	def vrd(self):
		""" (41) """
		term = self.tau_y*self.av/self.gamma_m1
		self.add_rslt('vrd', round(term*1e-3, 1), 'V.Rd', 'kN', '5.1.4.1', 41)
		return term

	def f42(self):
		"""(42)"""
		term = (self.h-self.tf)/self.tw/sqrt((4*e)/self.fy)
		self.add_rslt('f42', round(term, 3), 'f42', '5.1.4.2', 42)
		return term

	def av__(self):
		"""(42a)"""
		term = self.a-2*self.b*self.tf+(self.tw+2*self.r)*self.tf
		self.add_rslt('av', round(term, 1), 'A.v', '5.1.4.3', 43)
		return term

	def mvrd(self, ved):
		""" (43) """
		if self.shape in self.profiles_I:
			t1, t2, hw = self.tf, self.tw, self.h2
		else:
			t = self.t
			t1, t2, hw = t, 2*t, self.h-3*t

		term = self.b*t1*self.fy*(self.h-t1)/self.gamma_m1+hw**2*t2*self.fy/ \
			(4*self.gamma_m1)*(1-(ved*1e3/self.vrd())**2)
		self.add_rslt('mvrd', round(term*1e-6, 1), 'M.\u03BD.Rd', 'kNm', '5.1.5.2', 43)
		return term

	def f44(self, ned, myed, mzed):
		""" (44) """
		term = ned*1e3/self.nrd()+ myed*1e6/self.myrd()+ mzed*1e6/self.mzrd()
		self.add_rslt('f44', round(term, 3), 'f.44', '-', '5.1.6.1', 44)
		return term

	def mynrd(self, ned):
		"""(45)"""
		if self.shape in self.profiles_I:
			a = self.a__(self.b, self.tf)
		else:
			a = self.a__(self.b, self.t)
		zeta = self.zeta_(a, 'y')
		term = self.myrd()*zeta*(1-self.n(ned))
		if term >= self.myrd():
			term = self.myrd()
		self.add_rslt('mynrd', round(term*1e-6, 1), 'M.y,N,Rd', 'kNm', '5.1.6.2', 45)
		return term

	def mznrd(self, ned):
		if self.shape in self.profiles_I:
			a = self.a__(self.b, self.tf)
			zeta = self.zeta_(a, 'z')
			if self.n(ned) > a:
				""" (46) """
				term = self.mzrd()*(1-((self.n(ned)-a)/(1-a))**2)
				f = 46
			else:
				""" (47) """
				term = self.mzrd()
				f = 47
		else:
			a = self.a__(self.h, self.t)
			zeta = self.zeta_(a, 'z')
			term = term = self.mrdy()*self.zeta*(1-self.n(ned*1e3))
			if term >= self.mrdy():
				term = self.mrdy()
		self.add_rslt('mznrd', round(term*1e-6, 1), 'M.z,N,Rd', 'kNm', '5.1.6.2', f)
		return term

	def n(self, ned):
		term = ned*1e3/self.nrd()
		return term

	def a__(self, bh, t):
		term = (self.a-2*bh*t)/self.a
		return term

	def zeta_(self, a, axis):
		term = 1/(1-0.5*a)
		self.add_rslt('zeta_'+axis, round(term, 3), '\u03B6.'+axis, '-', '5.1.6.2')
		return term

	def f48(self, ned, myed, mzed):
		if self.shape in self.profiles_I:
			alpha = 2
			beta = 5*ned*1e3/self.nrd()
			if beta <= 1.1:
				beta = 1.1
		else:
			alpha = 1.66/(1-1.13*(ned*1e3/self.nrd())**2)
			beta = alpha
			if alpha >= 6.0:
				alpha = 6.0
				beta = alpha
		term = (myed*1e6/self.mynrd(ned))**alpha+(mzed*1e6/self.mznrd(ned))**beta
		self.add_rslt('f48', round(term, 3), 'f48', '-', '5.1.6.4', 48)
		return term

	def f49(self, ned, myed, axis):
		
		def zeta_(a, axis):
			term = 1/(1-0.5*a)
			if term >= 1+0.2*self.n(ned):
				term = 1+0.2*self.n(ned)
			return term

		if self.shape in self.profiles_I:
			if axis == 'y':
				a = self.a__(self.b, self.tf)
				zeta = zeta_(a, 'y')
			else:
				zeta = 1.0
		elif self.shape in self.profiles_R:
			if axis == 'y':
				a = self.a__(self.b, self.t)
				zeta = zeta_(a, 'y')
			else:
				a = self.a__(self.h, self.t)
				zeta = zeta_(a, 'z')
		else:
			zeta = 1.0
		self.add_rslt('zeta_'+axis, round(zeta, 3), '\u03B6.'+axis, '-', '5.1.6.2')

		ncr = e*getattr(self, 'i'+axis)*pi/self.lk**2
		omega = 0.6+0.4*getattr(self, 'psi_'+axis)
		if omega <= 0.4:
			omega = 0.4
		nkrd = getattr(NkRd(self.entries), 'nkrd_'+axis)()
		term = ned*1e3/nkrd + \
			   (1/(1-ned*1e3/ncr))*(omega*myed*1e6/(self.myrd()*zeta))
		self.add_rslt('f49_'+axis, round(term, 3), 'f49.'+axis, '-', '5.1.9.1', 49)
		return term

	def omega(self, psi, axis):
		term = 0.6+0.4*getattr(self, 'psi_'+axis)
		if term <= 0.4:
			term = 0.4
		self.add_rslt('omega_'+axis, round(term, 3), '\u03C9.'+axis, '-')
		return term

	def ncr(self, axis):
		term = e*getattr(self, 'i'+axis)*pi/self.lk**2
		self.add_rslt('ncr_'+axis, round(term*1e-3, 3), 'N.cr,'+axis, '-')
		return term

	def f50(self, ned, myed, mzed):
		def omega(psi, axis):
			term = 0.6+0.4*getattr(self, 'psi_'+axis)
			if term <= 0.4:
				term = 0.4
			return term
		def ncr(axis):
			term = e*getattr(self, 'i'+axis)*pi/self.lk**2
			return term

		nkrd_ = NkRd(self.entries)
		nkrd = min(nkrd_.nkrd_y(), nkrd_.nkrd_z())

		term = ned*1e3/nkrd + \
			   omega(self.psi_y, 'y')/(1-ned*1e3/ncr('y'))*myed*1e6/MDRd(self.entries).mdrd() +\
			   omega(self.psi_z, 'z')/(1-ned*1e3/ncr('z'))*mzed*1e6/self.mzrd()

		self.add_rslt('f50', round(term, 3), 'f50', '-', '5.1.10.1', 50)
		return term


class MCR(Profile, Results):
	"""SIA 263:13, Anhang B: Ideelles Kippmoment MCR 

	:param geometry: Wheter the profile ist double_symmetric or general
	:param ld: Kipplänge
	:param psi: Verhältnis des kleineren Endmoments zum grösseren

	"""
	selection = ''

	def __init__(self, entries):
		Profile.__init__(self, entries)
		if 'ld' in entries:
			self.ld = entries['ld']
		else:
			self.ld = entries['lk']
		self.psi_y = entries['psi']  # !!!!!!!!!!!!!!!!!!!!!!!

	def eta(self):
		"""B.6 Berücksichtigt Lagerung und Biegebeanspruchung"""
		term = 1.75-1.05*self.psi_y+0.3*self.psi_y**2
		if term <= -0.5:
			term = -0.5
		self.add_rslt('eta', round(term, 2), '\u03C8', '-', 'B.6', 95)
		return term

	def lk(self):
		"""B.5 Reduzierte Kipplänge"""
		term = self.ld/sqrt(self.eta())
		self.add_rslt('lk', round(term, 1), 'L.K', 'mm', 'B.5', 94)
		return term

	def i(self, geometry = 'double_symmetric'):
		"""B.5 Trägheitsradius des Druckgurtes"""

		if geometry == 'double_symmetric':
			term = sqrt((self.iz/2)/(self.b*self.tf+self.aw/6))
		else:
			hc = (self.h-self.tf)/2
			izfc = self.b**3*self.tf/12
			izwc = self.tw**3*(hc/3-self.tf/2)/12
			afc = self.b*self.tf
			awc = self.tw*(hc/3-self.tf/2)
			term = sqrt((izfc+izwc)/(afc+awc))

		term = round(term)
		self.add_rslt('id', term, 'i.D', 'mm', 'B.5', 94)
		return term

	def lambda_k(self):
		"""B.5 Schlankheit des Druckgurtes"""
		term = self.lk()/self.i()
		self.add_rslt('lambda_k', round(term), '\u03BB', '-', 'B.5', 94)
		return term

	def sigma_dw(self):
		"""B.5 Wölbanteil sigma_dw der ideellen Kippspannung"""
		# Ziffer 5.6.2.3 ist nicht berücksichtigt
		term = pi**2*e/self.lambda_k()**2
		self.add_rslt('sigma_dw', round(term, 1), '\u03A3.Dw', 'N/mm^2', 'B.5', 94)
		return term

	def c(self):
		"""B.4 Hilfswert C"""
		term = pi/(self.wely)*sqrt(g*self.k*e*self.iz)
		term = round(term*1e-3)*1e3
		self.add_rslt('c', term*1e-3, 'C', 'kN/mm', 'B.4', 93)
		return term

	def sigma_dv(self):
		"""B.4 Saint-Venantsche Anteil sigma_dv der ideellen Kippspannung"""
		# Ziffer 5.6.2.3 ist nicht berücksichtigt
		term = self.eta()*self.c()/self.ld
		self.add_rslt('sigma_dv', round(term, 1), '\u03A3.Dv', 'N/mm^2', 'B.4', 93)
		return term

	def sigma_crd(self):
		"""B.3 Ideelle Kippspannung"""
		term = sqrt(self.sigma_dv()**2+self.sigma_dw()**2)
		self.add_rslt('sigma_crd', round(term, 1), '\u03A3.cr,D', 'N/mm^2', 'B.3', 92)
		return term

	def mcr(self):
		"""B.1 Ideelles Kippmoment"""
		term = self.wely*self.sigma_crd()
		self.add_rslt('mcr', round(term, 1), 'M.cr', 'kNm', 'B.1', 91)
		return term


class MDRd(Profile, Results):
	""" SIA 213:13, 4.5.2 Kippen von Biegeträgern 

	:param production: Wheter the profile is rolled or welded
	
	"""

	def __init__(self, entries):
		Profile.__init__(self, entries)
		self.production = entries['production']
		self.sigma_crd = MCR(entries).sigma_crd()
		self.w = getattr(self, entries['w'])
		self.sub_code = entries['sub_code']
		self.entries = entries

	def alpha_d(self):
		"""4.5.2.3 Imperfektionsbeiwerte"""
		if self.production == 'rolled':
			term = 0.21
		else:
			term = 0.49
		self.add_rslt('alpha_d', term, '\u03B1.D', '-', '4.5.2.3')
		return term

	def lambda_d_(self):
		"""4.5.2.3 Kippschlankheit"""
		term = sqrt(self.fy/round(self.sigma_crd)*(round(self.w/self.wely, 2)))
		self.add_rslt('lambda_d_', round(term, 4), '\u03BB.D', '-', '4.5.2.3')
		return term
	
	def phi_d(self):
		"""4.5.2.3"""
		lambda_d_ = self.lambda_d_()
		term = 0.5*(1+self.alpha_d()*(lambda_d_-0.4)+lambda_d_**2)
		self.add_rslt('chi_d', round(term, 1), '\u03D5.D', '-', '4.5.2.3')
		return term

	def chi_d(self):
		"""4.5.2.3 Abminderungsfaktor"""
		phi_d = self.phi_d()
		term = 1/(phi_d+sqrt(phi_d**2-self.lambda_d_()**2))
		if term >= 1.0:
			term = 1.0
		self.add_rslt('chi_d', round(term, 4), '\u03C7.D', '-', '4.5.2.3', 10)
		return term

	def mdrd(self):
		"""4.5.2.2 Kippwiderstand MD,Rd """
		if self.sub_code == 'sia263':
			chi = self.chi_k()
		else:
			chi = self.chi_d()
		print('chi: {}, {}'.format(chi, self.lambda_d_()))
		term = chi*self.w*self.fy/gamma_m1
		self.add_rslt('mdrd', round(term*1e-6, 1), 'M.D.Rd', 'kNm', '4.5.2.2', 9)
		return term

	# 
	def phi_k(self):
		a = 0.21
		term = 0.5*(1+a*(self.lambda_d_()-0.2)+self.lambda_d_()**2)
		self.add_rslt('phi_k_y', round(term, 2), '\u03A6.K,y', '4.5.1.4')
		return term

	def chi_k(self):
		term = 1/(self.phi_k()+sqrt(self.phi_k()**2-self.lambda_d_()**2))
		if term >= 1.0:
			term = 1.0
		self.add_rslt('chi_k_y', round(term, 4), '\u03C8.K,y', '4.5.1.4', 8)
		return term


class NkRd(Profile, Results):
	""" SIA 263:13, 4.5.1 Knicken """
	
	def __init__(self, entries):
		Profile.__init__(self, entries)
		if 'lk' in entries:
			self.lk = entries['lk']
		else:
			self.lk = entries['ld']
		self.production = entries['production']
		
	def alpha(self, axis):
		a, b, c, d = 0.21, 0.34, 0.49, 0.76
		shapes = ['IPE', 'PEA', 'INP', 'HEA', 'HEB', 'HEM']

		if self.production == 'rolled':
			if self.shape in shapes and axis == 'y':
				if (self.h-self.tf)/self.b > 1.2 and self.tf <= 40:
					term = a
				elif self.tf <= 100:
					term = b
				else:
					term = d
				self.add_rslt('alpha_y', term, '\u03B1.y', '-', '4.5.1.4')

			elif self.shape in shapes and axis == 'z':
				if (self.h-self.tf)/self.b > 1.2 and self.tf <= 40:
					term = b
				elif self.tf <= 100:
					term = c
				else:
					term = d
				self.add_rslt('alpha_z', term, '\u03B1.z', '-', '4.5.1.4')

			elif self.shape in ['RRW']:
				term = a
				self.add_rslt('alpha', term, '\u03B1', '-', '4.5.1.4')
			else:
				pass

		else:
			pass
		self.add_rslt('alpha', term, '\u03B1', '-', '4.5.1.4')
		return term
				
	def lambda_k_y(self):
		term = self.lk/self.iy_/(pi*sqrt(e/self.fy))
		self.add_rslt('lambda_k_y', round(term, 1), '\u03BB.K,y', '4.5.1.4')
		return term

	def lambda_k_z(self):
		term = self.lk/self.iz_/(pi*sqrt(e/self.fy))
		self.add_rslt('lambda_k_z', round(term, 1), '\u03BB.K,z', '4.5.1.4')
		return term

	def phi_k_y(self):
		term = 0.5*(1+self.alpha('y')*(self.lambda_k_y()-0.2)+self.lambda_k_y()**2)
		self.add_rslt('phi_k_y', round(term, 2), '\u03A6.K,y', '4.5.1.4')
		return term

	def phi_k_z(self):
		term = 0.5*(1+self.alpha('z')*(self.lambda_k_z()-0.2)+self.lambda_k_z()**2)
		self.add_rslt('phi_k_z', round(term, 2), '\u03A6.K,z', '4.5.1.4')
		return term

	def chi_k_y(self):
		term = 1/(self.phi_k_y()+sqrt(self.phi_k_y()**2-self.lambda_k_y()**2))
		if term >= 1.0:
			term = 1.0
		self.add_rslt('chi_k_y', round(term, 4), '\u03C8.K,y', '4.5.1.4', 8)
		return term

	def chi_k_z(self):
		term = 1/(self.phi_k_z()+sqrt(self.phi_k_z()**2-self.lambda_k_z()**2))
		if term >= 1.0:
			term = 1.0
		self.add_rslt('chi_k_z', round(term, 4), '\u03C8.K,z', '4.5.1.4', 8)
		return term
	
	def nkrd_y(self):
		term = self.chi_k_y()*self.fy*self.a/gamma_m1
		self.add_rslt('nkrd_y', round(term*1e-3, 1), 'N.K,y,Rd', 'kN', '4.5.1.3', 7)
		return term
	
	def nkrd_z(self):
		term = self.chi_k_z()*self.fy*self.a/gamma_m1
		self.add_rslt('nkrd_z', round(term*1e-3, 1), 'N.K,z,Rd', 'kN', '4.5.1.3', 7)
		return term


