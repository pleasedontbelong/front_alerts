import os

APP_ENVIRONMENT = os.getenv('APP_ENVIRONMENT')
if APP_ENVIRONMENT is None:
    raise ValueError('APP_ENVIRONMENT is a mandatory variable!')

if APP_ENVIRONMENT == 'heroku':
    from .heroku import *  # NOQA

else:
    from .local import *  # NOQA
