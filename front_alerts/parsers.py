import json
import slack
import github
from .constants import FRONTEND_LABELS


class GithubEvent(object):

    def should_alert(self, payload):
        """
        Check if we should send an alert to slack
        """
        return False

    def get_content(self, payload):
        return ""

    def get_attachments(self, payload):
        return None

    def to_slack(self, payload):
        if self.should_alert(payload):
            slack.post(content=self.get_content(payload), attachments=self.get_attachments(payload))


class Issues(GithubEvent):

    EVENT_NAME = "issues"

    def should_alert(self, payload):
        """
        If issue has one of the FRONTEND_LABELS
        """
        labels = [label['name'] for label in payload['issue']['labels']]
        return any([label for label in labels if label in FRONTEND_LABELS])

    def get_attachments(self, payload):
        plain = "Issue #{number} {action} {issue_url}: {title}\n{content}".format(
            issue_url=payload['issue']['html_url'],
            number=payload['issue']['number'],
            action=payload['action'],
            title=payload['issue']['title'],
            content=payload['issue']['body'][:140]
        )
        return [{
            "author_name": "Issue {}".format(payload['action']),
            "fallback": plain,
            "color": "#f4a62a",
            "title": payload['issue']['title'],
            "title_link": payload['issue']['html_url'],
            "text": payload['issue']['body'][:140],
            "fields": [
                {
                    "title": "Labels",
                    "value": ', '.join([label['name'] for label in payload['issue']['labels']]),
                    "short": False
                }
            ]
        }]


class PullRequests(GithubEvent):

    EVENT_NAME = "pull_request"

    def should_alert(self, payload):
        # get the labels from the issue object
        self.labels = github.get_issue_labels(issue_number=payload['number'])
        return any([label for label in self.labels if label in FRONTEND_LABELS])

    def get_slack_message(self, payload):
        content = payload['pull_request']['title'] if payload['action'] == "opened" else ""
        return "PR #{number} {action}: {content}".format(
            number=payload['pull_request']['number'],
            action=payload['action'],
            content=content
        )

    def get_attachments(self, payload):
        plain = "Pull Request #{number} {action} {issue_url}: {title}\n{content}".format(
            issue_url=payload['pull_request']['html_url'],
            number=payload['pull_request']['number'],
            action=payload['action'],
            title=payload['pull_request']['title'],
            content=payload['pull_request']['body'][:140]
        )
        return [{
            "author_name": "Pull Request {}".format(payload['action']),
            "fallback": plain,
            "color": "#2980b9",
            "title": payload['pull_request']['title'],
            "title_link": payload['pull_request']['html_url'],
            "text": payload['pull_request']['body'][:140],
            "fields": [
                {
                    "title": "Labels",
                    "value": ', '.join(self.labels),
                    "short": False
                }
            ]
        }]


class GithubRequestEventParser(object):

    EVENT_MAP = {
        Issues.EVENT_NAME: Issues,
        PullRequests.EVENT_NAME: PullRequests
    }

    def __init__(self, *args, **kwargs):
        self.payload = None
        self.action = ""
        super(GithubRequestEventParser, self).__init__(*args, **kwargs)

    def parse(self, request):
        self.action = request.META['HTTP_X_GITHUB_EVENT']
        self.payload = json.loads(request.body)
        self.event_class = self.EVENT_MAP[self.action]()
        self.event_class.to_slack(self.payload)
