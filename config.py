# Create a config_local.py file in the same directory as this file.
# Values set in config_local.py will override the values in this file.

SECRET_KEY = b'not_a_secret'

BASIC_AUTH_USERNAME = 'admin'
BASIC_AUTH_PASSWORD = 'abc123'

GENERATE_ENABLED = True

RECAPTCHA_KEY = 'change_me'

try:
    from config_local import *
except ImportError:
    pass
