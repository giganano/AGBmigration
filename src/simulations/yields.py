r""" 
This file declares the nucleosynthetic yields for use in these models 
""" 

import numbers 
import vice 
from vice.yields.presets import JW20 
vice.yields.sneia.settings['fe'] *= 10**0.1 


class amplified_agb(vice.yields.agb.interpolator): 

	def __init__(self, element, study = "cristallo11", prefactor = 1): 
		super().__init__(element, study = study) 
		self.prefactor = prefactor 

	def __call__(self, mass, metallicity): 
		return self.prefactor * super().__call__(mass, metallicity) 

	@property 
	def prefactor(self): 
		r""" 
		Type : float 

		Default : 1 

		The multiplicative factor by which the yields are amplified. Must be 
		non-negative. 
		""" 
		return self._prefactor 

	@prefactor.setter 
	def prefactor(self, value): 
		if isinstance(value, numbers.Number): 
			if value >= 0: 
				self._prefactor = float(value) 
			else: 
				raise ValueError("Prefactor must be non-negative.") 
		else: 
			raise TypeError("Prefactor must be a numerical value. Got: %s" % (
				type(value))) 


class agb_no_zdep(amplified_agb): 

	def __init__(self, element, study = "cristallo11", prefactor = 1, 
		Zvalue = 0.014): 
		super().__init__(element, study = study, prefactor = prefactor) 

	def __call__(self, mass, metallicity): 
		return super().__call__(mass, self.Zvalue) 

	@property 
	def Zvalue(self): 
		r""" 
		Type : float 

		Default : 0.014 

		The metallicity by mass Z to assume for the AGB yield of all stellar 
		populations. Must be non-negative. 
		""" 
		return self._Zvalue 

	@Zvalue.setter 
	def Zvalue(self, value): 
		if isinstance(value, numbers.Number): 
			if value >= 0: 
				self._Zvalue = float(value) 
			else: 
				raise ValueError("Zvalue must be non-negative.") 
		else: 
			raise TypeError("Zvalue must be a numerical value. Got: %s" % (
				type(value))) 


def zero_agb_yield(mass, metallicity): 
	return 0.0 


class no_timedep_agb_yield(vice.toolkit.interpolation.interp_scheme_1d): 

	cc_yield = 4.15e-4 

	def __init__(self): 
		current_ccsn_yield = vice.yields.ccsne.settings['n'] 
		current_snia_yield = vice.yields.sneia.settings['n'] 
		current_agb_yield = vice.yields.agb.settings['n'] 
		vice.yields.ccsne.settings['n'] = 0 
		vice.yields.sneia.settings['n'] = 0 
		vice.yields.agb.settings['n'] = amplified_agb('n', 
			study = "cristallo11", prefactor = 4) 
		MoverH = [-3 + 0.01 * _ for _ in range(401)] 
		Z = [0.014 * 10**_ for _ in MoverH] 
		yields = len(MoverH) * [0.0] 
		mstar = 1.e6 
		for i in range(len(MoverH)): 
			mass, times = vice.single_stellar_population('n', mstar = mstar, 
				Z = Z[i], time = 13.2) 
			yields[i] = mass[-1] / mstar 
		super().__init__(Z, yields) 
		vice.yields.ccsne.settings['n'] = current_ccsn_yield 
		vice.yields.sneia.settings['n'] = current_snia_yield 
		vice.yields.agb.settings['n'] = current_agb_yield 

	def __call__(self, Z): 
		return self.cc_yield + super().__call__(Z) 


class linear_agb_yield: 

	r"""
	Describes the AGB yield as: 

	.. math:: y = \xi m_\text{to}Z 

	where :math:`\xi` is the slope of the linear relation.  
	""" 

	def __init__(self, slope = 0.05): 
		self.slope = slope 

	def __call__(self, mass, metallicity): 
		return self._slope * mass * metallicity 

	@property 
	def slope(self): 
		r""" 
		Type : float 

		The slope of the linear dependence, in units of :math:`M_\odot^{-1}`. 
		""" 
		return self._slope 

	@slope.setter 
	def slope(self, value): 
		if isinstance(value, numbers.Number): 
			if value >= 0: 
				self._slope = float(value) 
			else: 
				raise ValueError("Attribute 'slope' must be positive.") 
		else: 
			raise TypeError("""Attribute 'slope' must be a numerical value. \
Got: %s""" % (type(value))) 


# fiducial set of yields 
vice.yields.sneia.settings['n'] = 0 
vice.yields.ccsne.settings['n'] = 4.15e-4 
vice.yields.agb.settings['n'] = amplified_agb('n', study = "cristallo11", 
	prefactor = 4) 
# vice.yields.agb.settings['n'] = amplified_agb('n', study = "ventura13", 
# 	prefactor = 2) 
# vice.yields.agb.settings['n'] = "karakas10" 
# vice.yields.agb.settings['n'] = linear_agb_yield(slope = 0.05) 

# set with no time-dependence to the AGB yield 
# vice.yields.sneia.settings['n'] = 0 
# vice.yields.ccsne.settings['n'] = no_timedep_agb_yield() 
# vice.yields.agb.settings['n'] = zero_agb_yield 

# set with no metallicity dependence to the AGB yield 
# vice.yields.sneia.settings['n'] = 0 
# vice.yields.ccsne.settings['n'] = 4.15e-4 
# vice.yields.agb.settings['n'] = agb_no_zdep('n', study = "cristallo11", 
# 	prefactor = 5)  

