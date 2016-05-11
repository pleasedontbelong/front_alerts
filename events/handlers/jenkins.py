import json
from front_alerts import github
from .core import EventHandler


class JenkinsBuildFinishedEvent(EventHandler):

    def __init__(self, *args, **kwargs):
        self.payload = None
        self._labels = None
        self._issue = None
        super(JenkinsBuildFinishedEvent, self).__init__(*args, **kwargs)

    def get_attachments(self, payload):
        issue = self.get_issue(payload)
        plain = "Jenkins Job {} {}".format(
            issue['title'],
            payload['build']['status']
        )
        return [{
            "author_name": "Jenkins Job {}".format(payload['build']['status']),
            "author_link": payload['build']['full_url'],
            "fallback": plain,
            "color": "#c0392b" if payload['build']['status'] == "FAILURE" else "#2ecc71",
            "title": issue['title'],
            "title_link": issue['pull_request']['html_url'],
            "pretext": "@{} jenkins finished your PR's tests".format(issue['user']['login'])
        }]

    def get_labels(self, payload):
        if not self._labels:
            issue = self.get_issue(payload)
            self._labels = github.extract_labels(issue)
        return self._labels

    def get_issue(self, payload):
        if not self._issue:
            pr_id = payload['build']['parameters']['ghprbPullId']
            self._issue = github.get_issue(pr_id)
        return self._issue

    def should_send(self, payload, trigger_labels):
        pr_labels = self.get_labels(payload)
        return any([label for label in pr_labels if label in trigger_labels])

    def get_event_id(self, payload):
        return payload['build']['parameters']['ghprbPullId']

    def get_event_name(self, payload):
        return u"jenkins_build"


class JenkinsEventHandler(object):

    def __init__(self, request):
        self.request = request
        self.payload = json.loads(self.request.body)
        self.event_class = JenkinsBuildFinishedEvent()

    def send(self, slack_channels, review_request_label):
        self.event_class.send(self.payload, slack_channels, review_request_label)

    def should_send(self, trigger_labels):
        return self.event_class.should_send(self.payload, trigger_labels)

    @property
    def event_id(self):
        return self.event_class.get_event_id(self.payload)

    @property
    def event_name(self):
        return self.event_class.get_event_name(self.payload)
