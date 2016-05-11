from .base import *  # NOQA
from mock import ANY

DEBUG = True
SLACK_DRY_RUN = False

MESSAGES_ROUTING = {
    "default": {
        "github_api_token": "",
        "github_api_user": "",
        "github_repo": "",
        "github_owner": "",
    },
    "frontend": {
        "github_labels": [ANY],
        "slack_channels": ["#ops-playground"],
        "review_request_labels": ["test Ready for review"],
        "sentry_projects": [ANY]
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'bare': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'bare',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': "WARNING",
            'propagate': False,
        },
    }
}
