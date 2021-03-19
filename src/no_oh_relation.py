
import numbers 
import math as m 
import vice 

class Henry2000: 

	r""" 
	This class implements the [N/O] - [O/H] relation as parameterized by 
	Henry, Edmunds & Koeppen (2000) [1]_. 

	Notes 
	-----
	This function adopts the solar_z dataframe in VICE as the solar composition, 
	which defaults to the Asplund et al. (2009) [2]_ photospheric abundance 
	measurements. 

	The functional form built into this object is defined according to 
	equation (7) in the Henry, Edmunds & Koeppen (2000) paper, and default 
	values are assigned according to the values they quote in the text of their 
	section 4. 

	.. [1] Henry, Edmunds & Koeppen, 2000, ApJ, 541, 660 
	.. [2] Asplund et al., 2009, ARA&A, 47, 481 
	""" 

	def __init__(self, y_o = 0.01, y_pn = 0.00022, y_sn = 0.285, 
		y_pc = 0.0012, y_sc = 0.9, acc_ratio = 0.9): 
		self.y_o = y_o 
		self.y_pn = y_pn 
		self.y_sn = y_sn 
		self.y_pc = y_pc 
		self.y_sc = y_sc 
		self.acc_ratio = acc_ratio 

	def __call__(self, oh): 
		z_o = vice.solar_z['o'] * 10**oh 
		if 1 - self._acc_ratio * z_o / self._y_o > 0: 
			term1 = (
					self._y_pn / self._y_o + 
					self._y_pc * self._y_sn / (self._acc_ratio * self._y_o) + 
					self._y_sc * self._y_sn / self._acc_ratio**2 
				) * z_o 
			term2 = (
					self._y_pc / self._y_o + self._y_sc / self._acc_ratio 
				) * (
					self._y_o * self._y_sn / self._acc_ratio**2 
				) * (
					1 - self._acc_ratio * z_o / self._y_o 
				) * m.log(
					1 - self._acc_ratio * z_o / self._y_o 
				) 
			term3 = (
					self._y_o * self._y_sc * self._y_sn / (
						2 * self._acc_ratio**3
					) 
				) * (
					1 - self._acc_ratio * z_o / self._y_o 
				) * m.log(
					1 - self._acc_ratio * z_o / self._y_o 
				)**2 
			z_n = term1 + term2 - term3 
			nh = m.log10(z_n / vice.solar_z['n']) 
			return nh - oh # [N/O] = [N/H] - [O/H] 
		else: 
			return float("nan") # math domain error 


	@property 
	def y_o(self): 
		r""" 
		Type : float 

		Default : 0.01 

		The yield of oxygen. 
		""" 
		return self._y_o 

	@y_o.setter 
	def y_o(self, value): 
		if isinstance(value, numbers.Number): 
			self._y_o = float(value) 
		else: 
			raise TypeError("Must be a numerical value.") 

	@property 
	def y_pn(self): 
		r""" 
		Type : float 

		Default : 0.00022 

		The primary nitrogen yield. 
		""" 
		return self._y_pn 

	@y_pn.setter 
	def y_pn(self, value): 
		if isinstance(value, numbers.Number): 
			self._y_pn = float(value) 
		else: 
			raise TypeError("Must be a numerical value.") 

	@property 
	def y_sn(self): 
		r""" 
		Type : float 

		Default : 0.285 

		The secondary nitrogen yield. 
		""" 
		return self._y_sn 

	@y_sn.setter 
	def y_sn(self, value): 
		if isinstance(value, numbers.Number): 
			self._y_sn = float(value) 
		else: 
			raise TypeError("Must be a numerical value.") 

	@property 
	def y_pc(self): 
		r""" 
		Type : float 

		Default : 0.0012 

		The primary carbon yield. 
		""" 
		return self._y_pc 

	@y_pc.setter 
	def y_pc(self, value): 
		if isinstance(value, numbers.Number): 
			self._y_pc = float(value) 
		else: 
			raise TypeError("Must be a numerical value.") 

	@property 
	def y_sc(self): 
		r""" 
		Type : float 

		Default : 0.9 

		The secondary carbon yield. 
		""" 
		return self._y_sc 

	@y_sc.setter 
	def y_sc(self, value): 
		if isinstance(value, numbers.Number): 
			self._y_sc = float(value) 
		else: 
			raise TypeError("Must be a numerical value.") 

	@property 
	def acc_ratio(self): 
		r""" 
		Type : float 

		Default : 0.1 

		The ratio of accretion to star formation rates. 
		""" 
		return self._acc_ratio 

	@acc_ratio.setter 
	def acc_ratio(self, value): 
		if isinstance(value, numbers.Number): 
			if value >= 0: 
				self._acc_ratio = float(value) 
			else: 
				raise ValueError("Must be non-negative.") 
		else: 
			raise TypeError("Must be a numerical value.") 
