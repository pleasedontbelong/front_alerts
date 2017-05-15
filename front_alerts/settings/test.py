from .base import *  # NOQA
from mock import ANY

DEBUG = True
SLACK_DRY_RUN = True

# MESSAGES_ROUTING = {
#     "default": {
#         "github_api_token": "",
#         "github_api_user": "",
#         "github_repo": "",
#         "github_owner": "",
#     },
#     "team1": {
#         "github_labels": ["team1"],
#         "slack_channels": ["#team1"],
#         "review_request_labels": ["test Ready for review"],
#         "sentry_projects": [ANY]
#     },
#     "team2": {
#         "github_labels": ["team2"],
#         "slack_channels": ["#team2"],
#         "review_request_labels": ["test Ready for review"],
#         "sentry_projects": [ANY]
#     },
# }

MESSAGES_ROUTING = {
    "default": {
        "github_api_token": "",
        "github_api_user": "",
        "github_repo": "",
        "github_owner": "",
    },
    "test": {
        "github_labels": [ANY],
        "slack_channels": ["#test"],
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
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'bare',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': "INFO",
            'propagate': False,
        },
    }
}

# pleasedontbelong.slack
SLACK_WEBHOOK = "https://hooks.slack.com/services/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"
