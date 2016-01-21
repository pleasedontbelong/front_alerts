import requests
import json
from requests.auth import HTTPBasicAuth
from django.conf import settings


def get_issue_labels(issue_number):
    response = requests.get(
        'https://api.github.com/repos/{owner}/{repo}/issues/{number}'.format(
            owner=settings.GITHUB_OWNER,
            repo=settings.GITHUB_REPO,
            number=issue_number
        ),
        auth=HTTPBasicAuth(
            settings.GITHUB_API_USER,
            settings.GITHUB_API_TOKEN
        )
    )
    response.raise_for_status()
    json_content = json.loads(response.content)
    return [label['name'] for label in json_content['labels']]
