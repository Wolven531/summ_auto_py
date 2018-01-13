"""
	This is the Rating module
"""

from enum import Enum

class Rating(Enum):
	"""
		This is the enumeration for the four possible monster
		ratings
	"""
	KEEP_IT = 'KEEP_IT'
	FOOD = 'FOOD'
	THE_BEST = 'THE_BEST'
	MEH = 'MEH'

	@classmethod
	def generate_rating_dict(cls, initial_val=0):
		"""
			This method returns a dictionary populated with keys for
			every possible value of Rating, with an optional initial
			value
		"""
		rating_mapping = {}
		for rating in Rating:
			rating_mapping[rating] = initial_val
		return rating_mapping
