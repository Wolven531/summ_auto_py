"""
	This is the MonsterType module
"""

from enum import Enum

class MonsterType(Enum):
	"""
		This is the enumeration for the five possible monster
		types
	"""
	DARK = 'DARK'
	FIRE = 'FIRE'
	WATER = 'WATER'
	WIND = 'WIND'
	LIGHT = 'LIGHT'

	@classmethod
	def has_value(cls, value):
		"""
			This method provides a way to check if a value is included
			in this enumeration
		"""
		return any(value == item.value for item in cls)
