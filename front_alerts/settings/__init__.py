import os

APP_ENVIRONMENT = os.getenv('APP_ENVIRONMENT', 'local')

if APP_ENVIRONMENT == 'heroku':
    from .heroku import *  # NOQA

else:
    from .local import *  # NOQA
