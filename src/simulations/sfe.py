
from vice.toolkit import J21_sf_law 
from .models.utils import sinusoid 


class sfe(J21_sf_law, sinusoid): 

	def __init__(self, area, amplitude = 0.5, frequency = 0.5, phase = 0, 
		mode = "sfr", **kwargs): 

		J21_sf_law.__init__(self, area, mode = mode, **kwargs) 
		sinusoid.__init__(self, amplitude = amplitude, frequency = frequency, 
			phase = phase) 

	def __call__(self, time, arg2): 
		return J21_sf_law.__call__(self, time, arg2) * (
			1 + sinusoid.__call__(self, time)) 

