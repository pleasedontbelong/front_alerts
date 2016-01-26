import requests
import json
from requests.auth import HTTPBasicAuth
from django.conf import settings


def get_issue(issue_number):
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
    return json.loads(response.content)


def extract_labels(issue_data):
    return [label['name'] for label in issue_data['labels']]


def get_issue_labels(issue_number):
    issue = get_issue(issue_number)
    return extract_labels(issue)
