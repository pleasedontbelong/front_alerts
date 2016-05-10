import requests
import json
from django.conf import settings


def post(content="", channel="", attachments=None):
    r = requests.post(
        settings.SLACK_WEBHOOK_URL,
        data=json.dumps({
            "channel": channel,
            "text": content,
            "attachments": attachments
        })
    )
    r.raise_for_status()
