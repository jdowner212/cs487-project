"""Contains values and functions used in many modules."""

APP_NAME = "CS487"

BACKGROUND = '#2E9F60'
FOREGROUND = 'white'
ERROR_FOREGROUND = 'red'

def is_float(value):
    """check whether it's float but also not throw error when it's string"""
    try:
        return isinstance(float(value), float)
    except ValueError:
        return False


def is_integer(value):
    """check whether it can be an int but also not throw error when it's string"""
    try:
        return isinstance(int(value), int)
    except ValueError:
        return False
