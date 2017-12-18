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
