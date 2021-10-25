r""" 
This file declares the nucleosynthetic yields for use in these models 
""" 

import numbers 
import vice 
from vice.yields.presets import JW20 
vice.yields.sneia.settings['fe'] *= 10**0.1 
from vice.core._cutils import progressbar
import os


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


class prompt_agb_yield(vice.toolkit.interpolation.interp_scheme_1d):

	cc_yield = 3.6e-4

	def __init__(self, datafile = "integrated_agb_n_yields.out"):
		if not datafile in os.listdir(os.getcwd()): self.produce_table(
			outfile = datafile)
		with open(datafile, "r") as f:
			xvals = []
			yvals = []
			while True:
				line = f.readline()
				if line == "": break
				if line[0] == '#': continue
				line = [float(_) for _ in line.split()]
				xvals.append(line[0])
				yvals.append(line[1])
			f.close()
		super().__init__(xvals, yvals)


	def __call__(self, Z):
		return self.cc_yield + super().__call__(Z)


	@staticmethod
	def produce_table(outfile = "integrated_agb_n_yields.out"):
		current_ccsne_yield = vice.yields.ccsne.settings['n']
		current_sneia_yield = vice.yields.sneia.settings['n']
		current_agb_yield = vice.yields.agb.settings['n']
		vice.yields.ccsne.settings['n'] = 0
		vice.yields.sneia.settings['n'] = 0
		vice.yields.agb.settings['n'] = linear_agb_yield(slope = 9.0e-4)
		MoverH = [-3 + 0.001 * _ for _ in range(4000)]
		Z = [0.014 * 10**_ for _ in MoverH]
		with progressbar(maxval = len(MoverH)) as pbar:
			with open(outfile, "w") as out:
				out.write("# Z\ty_N_AGB\n")
				mstar = 1.e6
				for i in range(len(Z)):
					mass, times = vice.single_stellar_population('n',
						mstar = mstar, Z = Z[i], time = 13.2)
					y = mass[-1] / mstar
					out.write("%.5e\t%.5e\n" % (Z[i], y))
					pbar.update(i + 1)
				out.close()
		vice.yields.ccsne.settings['n'] = current_ccsne_yield
		vice.yields.sneia.settings['n'] = current_sneia_yield
		vice.yields.agb.settings['n'] = current_agb_yield



class linear_agb_yield: 

	r"""
	Describes the AGB yield as: 

	.. math:: y = \xi m_\text{to}Z 

	where :math:`\xi` is the slope of the linear relation. 
	""" 

	def __init__(self, slope = 3.0e-4, Zsun = 0.014): 
		self.slope = slope 
		self.Zsun = Zsun 

	def __call__(self, mass, metallicity): 
		return self._slope * mass * (metallicity / self.Zsun) 

	@property 
	def slope(self): 
		r""" 
		Type : float 

		Default : 3.0e-4

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

	@property 
	def Zsun(self): 
		r""" 
		Type : float 

		Default : 0.014 

		The metallicity by mass of the sun :math:`Z_\odot`. 
		""" 
		return self._Zsun 

	@Zsun.setter 
	def Zsun(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				self._Zsun = float(value) 
			else: 
				raise ValueError("Attribute 'Zsun' must be positive.") 
		else: 
			raise TypeError("""Attribute 'Zsun' must be a numerical value. \
Got: %s""" % (type(value))) 

class linear_agb_yield_no_zdep(linear_agb_yield):

	def __init__(self, Zvalue = 0.014, **kwargs):
		self.Zvalue = Zvalue
		super().__init__(**kwargs)

	def __call__(self, mass, metallicity):
		return super().__call__(mass, self.Zvalue)

	@property
	def Zvalue(self):
		return self._Zvalue

	@Zvalue.setter
	def Zvalue(self, value):
		if isinstance(value, numbers.Number):
			if value >= 0:
				self._Zvalue = float(value)
			else:
				raise ValueError("Must be non-negative.")
		else:
			raise TypeError("Must be a numerical value. Got: %s" % (
				type(value)))

def broken_cc_yield(z): 
	y = 3.6e-4 
	return max(y, linear_cc_yield(z)) 


def linear_cc_yield(z): 
	return 3.6e-4 * (z / 0.014) 


# The mass-lifetime relation to adopt 
# vice.mlr.setting = "ka1997" 
vice.mlr.setting = "larson1974"


# fiducial set of yields 
# vice.yields.ccsne.settings['n'] = prompt_agb_yield()
vice.yields.sneia.settings['n'] = 0
# vice.yields.agb.settings['n'] = zero_agb_yield
# vice.yields.agb.settings['n'] = linear_agb_yield_no_zdep(slope = 9.0e-4)
# vice.yields.sneia.settings['n'] = 0 
vice.yields.ccsne.settings['n'] = 3.6e-4
# vice.yields.ccsne.settings['n'] = broken_cc_yield 
# vice.yields.ccsne.settings['n'] = linear_cc_yield 
# vice.yields.agb.settings['n'] = amplified_agb('n', study = "cristallo11", 
	# prefactor = 3) 
# vice.yields.agb.settings['n'] = "cristallo11"
# vice.yields.agb.settings['n'] = amplified_agb('n', study = "ventura13", 
# 	prefactor = 2) 
# vice.yields.agb.settings['o'] = "ventura13" 
# vice.yields.agb.settings['n'] = "karakas10" 
# vice.yields.agb.settings['o'] = "karakas10" 
# vice.yields.agb.settings['fe'] = "karakas10" 
# vice.yields.agb.settings['n'] = "karakas16" 
# vice.yields.agb.settings['o'] = "karakas16" 
# vice.yields.agb.settings['fe'] = "karakas16" 
vice.yields.agb.settings['n'] = linear_agb_yield(slope = 9.0e-4) 

# set with no time-dependence to the AGB yield 
# vice.yields.sneia.settings['n'] = 0 
# vice.yields.ccsne.settings['n'] = no_timedep_agb_yield() 
# vice.yields.agb.settings['n'] = zero_agb_yield 

# set with no metallicity dependence to the AGB yield 
# vice.yields.sneia.settings['n'] = 0 
# vice.yields.ccsne.settings['n'] = 4.15e-4 
# vice.yields.agb.settings['n'] = agb_no_zdep('n', study = "cristallo11", 
# 	prefactor = 5)  

# halved set of yields 
# vice.yields.ccsne.settings['o'] = 0.0075
# vice.yields.sneia.settings['o'] = 0.

# vice.yields.ccsne.settings['fe'] = 0.0006
# vice.yields.sneia.settings['fe'] = 0.00107

# vice.yields.ccsne.settings['n'] = 1.8e-4
# vice.yields.sneia.settings['n'] = 0
# vice.yields.agb.settings['n'] = amplified_agb('n', study = "cristallo11",
# 	prefactor = 1.5)

# doubled set of yields
# vice.yields.ccsne.settings['o'] = 0.03
# vice.yields.sneia.settings['o'] = 0.

# vice.yields.ccsne.settings['fe'] = 0.0024
# vice.yields.sneia.settings['fe'] = 0.00428

# vice.yields.ccsne.settings['n'] = 7.3e-4
# vice.yields.sneia.settings['n'] = 0
# vice.yields.agb.settings['n'] = amplified_agb('n', study = "cristallo11",
# 	prefactor = 6)

# one-third set of yields
# vice.yields.ccsne.settings['o'] = 0.005
# vice.yields.sneia.settings['o'] = 0.
# vice.yields.agb.settings['n'] = "cristallo11"

# vice.yields.ccsne.settings['fe'] = 0.0004
# vice.yields.sneia.settings['fe'] = 0.000713
# vice.yields.agb.settings['n'] = "cristallo11"

# vice.yields.ccsne.settings['n'] = 1.2e-4
# vice.yields.sneia.settings['n'] = 0.
# vice.yields.agb.settings['n'] = "cristallo11"


# vice.yields.ccsne.settings["mg"] = 0.0015 # 0.000497 
# vice.yields.ccsne.settings["ba"] = 2.5e-8 # 2.83-9 
# vice.yields.ccsne.settings["y"] = 1.5e-8 # 2.47e-9 

