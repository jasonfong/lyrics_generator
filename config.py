# Create a config_local.py file in the same directory as this file.
# Values set in config_local.py will override the values in this file.

SECRET_KEY = b'not_a_secret'

BASIC_AUTH_USERNAME = 'not_a_username'
BASIC_AUTH_PASSWORD = 'not_a_password'

try:
    from config_local import *
except ImportError:
    pass
