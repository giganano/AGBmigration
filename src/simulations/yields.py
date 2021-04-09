r""" 
This file declares the nucleosynthetic yields for use in these models 
""" 

import vice 
from vice.yields.presets import JW20 

PREFACTOR = 5 
class amplified_agb(vice.yields.agb.interpolator): 

	def __call__(self, mass, metallicity): 
		return PREFACTOR * super().__call__(mass, metallicity) 

vice.yields.sneia.settings['fe'] *= 10**0.1 
vice.yields.sneia.settings['n'] = 0 
vice.yields.ccsne.settings['n'] = 4.15e-4 
vice.yields.agb.settings['n'] = amplified_agb('n', study = "cristallo11") 

