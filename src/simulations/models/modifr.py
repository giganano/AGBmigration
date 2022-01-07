
from .utils import constant, sinusoid
from .normalize import normalize_ifrmode
from .gradient import gradient

class modifr(constant):

	def __init__(self, radius, dt = 0.01, dr = 0.1):
		super().__init__()
		# self.sinusoid = sinusoid(amplitude = 0.75, frequency = 0.5)
		self.sinusoid = sinusoid(amplitude = 0., frequency = 0.5)
		prefactor = normalize_ifrmode(self, gradient, radius, dt = dt, dr = dr)
		self.amplitude *= prefactor

	def __call__(self, time):
		return super().__call__(time) * (1 + self.sinusoid(time))

