"""Contains values and functions used in many modules."""

MY_ID = -1
CUSTOMER_ABSENT, CUSTOMER_LOGIN, CUSTOMER_EMAIL = (0, 1, 2)

APP_NAME = "CS 487: Coffee Shop"
ADMIN_PERM = 1

BACKGROUND = 'darkseagreen4'
FOREGROUND = 'darkseagreen1'
ERROR_FOREGROUND = 'red'


def is_float(value):
    """check if float"""
    try:
        return isinstance(float(value), float)
    except ValueError:
        return False


def is_integer(value):
    """check if int"""
    try:
        return isinstance(int(value), int)
    except ValueError:
        return False
