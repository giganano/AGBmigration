
__all__ = ["logplus12_bracket_conversion", "logNO_bracket_conversion"] 
import vice 
import math 


def logplus12_bracket_conversion(logplus12, Xsun = 0.73): 
	r""" 
	Convert log(O/H) + 12 into [O/H] 

	Parameters 
	----------
	logplus12 : real number 
		The value of log(O/H) + 12 
	Xsun : real number [default : 0.73] 
		The hydrogen mass fraction of the sun 

	Returns 
	-------
	oh : real number 
		The value of [O/H], calculated via: 

		.. math:: [O/H] = (\log(O/H) + 12) - 12 - \log(\mu_H/\mu_O) 
			- \log(Z_{O,\odot}/X_\odot) 

	Notes 
	-----
	This function assumes the Asplund et al. (2009) [1]_ solar abundance of 
	oxygen through VICE's ``solar_z`` dataframe. 

	.. [1] Asplund et al. (2009), ARA&A, 47, 481 
	""" 
	return logplus12 - 12 - math.log10(1.008 / 15.999) - math.log10(
		vice.solar_z['o'] / Xsun) 


def logNO_bracket_conversion(logNO): 
	r""" 
	Convert log(N/O) into [N/O] 

	Parameters 
	----------
	logNO : real number 
		The value of log(N/O) 

	Returns 
	-------
	no : real number 
		The value of [N/O], calculated via: 

		.. math:: \log(\mu_N / \mu_O) + \log(N/O) - 
			\log(Z_{N,\odot} / Z_{O,\odot}) 

	Notes 
	-----
	This function assumes the Asplund et al. (2009) [1]_ solar abundances of 
	oxygen and nitrogen through VICE's ``solar_z`` dataframe. 

	.. [1] Asplund et al. (2009), ARA&A, 47, 481 
	""" 
	return math.log10(14.006 / 15.999) + logNO - math.log10(
		vice.solar_z['n'] / vice.solar_z['o']) 

