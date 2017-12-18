"""
    This is the LinkType module
"""

from enum import Enum

class LinkType(Enum):
    """
        This is the enumeration for the possible link types
        that get parsed
    """
    DARK = 'DARK'
    FIRE = 'FIRE'
    WATER = 'WATER'
    WIND = 'WIND'
    LIGHT = 'LIGHT'
    IMAGE_SLEEPY = 'IMAGE_SLEEPY'
    IMAGE_AWAKE = 'IMAGE_AWAKE'

    @classmethod
    def generate_link_dict(cls, initial_val=''):
        """
            This method returns a dictionary populated with keys for
            every possible value of LinkType, with an optional initial
            value string
        """
        link_mapping = {}
        for link_type in LinkType:
            link_mapping[link_type] = initial_val
        return link_mapping

    @classmethod
    def has_value(cls, value):
        """
            This method provides a way to check if a value is included
            in this enumeration
        """
        return any(value == item.value for item in cls)
