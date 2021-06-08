r""" 
This file implements a version of the inside-out SFH whose SFH exhibits 
sinusoidal variations at the 25% level. 
""" 

from .insideout import insideout, _TAU_RISE_ 
from .utils import sinusoid 
from .normalize import normalize 
from .gradient import gradient 


class modulated(insideout): 


	def __init__(self, radius, dt = 0.01, dr = 0.1): 
		super().__init__(radius, norm = False) 
		self.sinusoid = sinusoid(amplitude = 0.25, frequency = 0.5) 
		self.norm *= normalize(self, gradient, radius, dt = dt, dr = dr) 

	def __call__(self, time): 
		return super().__call__(time) * (1 + self.sinusoid(time)) 


