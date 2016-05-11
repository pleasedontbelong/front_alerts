import requests
import json
from requests.auth import HTTPBasicAuth


def get_issue(issue_number, route_config):
    response = requests.get(
        'https://api.github.com/repos/{owner}/{repo}/issues/{number}'.format(
            owner=route_config.get('github_owner'),
            repo=route_config.get('github_repo'),
            number=issue_number
        ),
        auth=HTTPBasicAuth(
            route_config.get('github_api_user'),
            route_config.get('github_api_token')
        )
    )
    response.raise_for_status()
    return json.loads(response.content)


def extract_labels(issue_data):
    return [label['name'] for label in issue_data['labels']]


def get_issue_labels(issue_number, route_config):
    issue = get_issue(issue_number, route_config)
    return extract_labels(issue)
