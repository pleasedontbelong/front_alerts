from .base import *  # NOQA
import dj_database_url

DEBUG = True
SLACK_DRY_RUN = False
# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# Enable Persistent Connections
DATABASES['default']['CONN_MAX_AGE'] = 500
