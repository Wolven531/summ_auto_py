"""
    This is the ConsoleUtil module. It uses values from
    http://ozzmaker.com/add-colour-to-text-in-python/
"""

from enum import Enum

class ConsoleColor(Enum):
    """
        This is the enumeration for the possible colors
        to use in the console
    """
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37

class ConsoleBackgroundColor(Enum):
    """
        This is the enumeration for the possible background colors
        to use in the console
    """
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47

class ConsoleStyle(Enum):
    """
        This is the enumeration for the possible styles
        to use in the console
    """
    NONE = 0
    BOLD = 1
    UNDERLINE = 2
    NEGATIVE1 = 3
    NEGATIVE2 = 5

class ConsoleUtil():
    """
        This class provides methods to interact in special
        ways with the console
    """

    ESCAPE_CODE = '\033['
    # NOTE: for resetting style and colors
    DEFAULT_SCHEME = (f'{ESCAPE_CODE}{ConsoleStyle.NONE.value};' +
                      f'{ConsoleColor.WHITE.value};{ConsoleBackgroundColor.BLACK.value}m')

    @staticmethod
    def norm(msg):
        """
            This method outputs a message to std out with a pre-defined
            format to signify a normal message
        """
        ConsoleUtil.spit(
            msg,
            ConsoleColor.WHITE,
            ConsoleBackgroundColor.BLACK,
            ConsoleStyle.NONE)

    @staticmethod
    def info(msg):
        """
            This method outputs a message to std out with a pre-defined
            format to signify an informational message
        """
        ConsoleUtil.spit(
            msg,
            ConsoleColor.WHITE,
            ConsoleBackgroundColor.BLUE,
            ConsoleStyle.NONE)

    @staticmethod
    def success(msg):
        """
            This method outputs a message to std out with a pre-defined
            format to signify a successful message
        """
        ConsoleUtil.spit(
            msg,
            ConsoleColor.WHITE,
            ConsoleBackgroundColor.GREEN,
            ConsoleStyle.BOLD)

    @staticmethod
    def warn(msg):
        """
            This method outputs a message to std out with a pre-defined
            format to signify warning
        """
        ConsoleUtil.spit(
            msg,
            ConsoleColor.RED,
            ConsoleBackgroundColor.YELLOW,
            ConsoleStyle.BOLD)

    @staticmethod
    def spit(msg,
             color=ConsoleColor.WHITE,
             background=ConsoleBackgroundColor.BLACK,
             style=ConsoleStyle.NONE):
        """
            This method prints to std out with some customizable
            styles
        """
        print(
            f'{ConsoleUtil.ESCAPE_CODE}{style.value};{color.value};{background.value}m{msg}' +
            ConsoleUtil.DEFAULT_SCHEME) # reset colors
