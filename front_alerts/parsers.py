import json
import slack_hook


class GithubEvent(object):
    FRONTEND_LABELS = ['comp:frontend']

    def has_front_label(self, payload):
        labels = self.get_labels(payload)
        return any([label for label in labels if label in self.FRONTEND_LABELS])

    def to_slack(self, payload):
        if self.has_front_label(payload):
            self.send_to_slack(self.get_slack_message(payload))

    def send_to_slack(self, message):
        slack_hook.post(message)


class Issues(GithubEvent):

    EVENT_NAME = "issues"

    def get_labels(self, payload):
        return [label['name'] for label in payload['issue']['labels']]

    def get_slack_message(self, payload):
        content = payload['issue']['body'][:140] if payload['action'] == "opened" else ""
        return "Issue #{number} {action}: {content}".format(
            number=payload['issue']['number'],
            action=payload['action'],
            content=content
        )


class PullRequests(GithubEvent):

    EVENT_NAME = "pull_requests"

    def get_labels(self, payload):
        return [payload['pull_request']['head']['label']]

    def get_slack_message(self, payload):
        content = payload['pull_request']['title'] if payload['action'] == "opened" else ""
        return "PR #{number} {action}: {content}".format(
            number=payload['pull_request']['number'],
            action=payload['action'],
            content=content
        )


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
