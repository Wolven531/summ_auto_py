"""
    This is the Rating module
"""

from enum import Enum

class Rating(Enum):
    """
        This is the enumeration for the four possible monster
        ratings
    """
    KEEP_IT = 1
    FOOD = 2
    THE_BEST = 3
    MEH = 4
