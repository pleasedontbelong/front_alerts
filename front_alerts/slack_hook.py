import requests
import json
from django.conf import settings
from .constants import FRONTEND_CHANNEL


def post(content, channel=FRONTEND_CHANNEL):
    r = requests.post(
        settings.SLACK_WEBHOOK_URL,
        data=json.dumps({
            "channel": channel,
            "text": content
        })
    )
    r.raise_for_status()
