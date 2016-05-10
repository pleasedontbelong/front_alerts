import json
import logging
from django.conf import settings
from front_alerts import slack
from front_alerts import github
from front_alerts.constants import FRONTEND_LABELS


class JenkinsRequestEventHandler(object):

    def __init__(self, *args, **kwargs):
        self.payload = None
        super(JenkinsRequestEventHandler, self).__init__(*args, **kwargs)

    def parse(self, request):
        payload = json.loads(request.body)
        pr_id = payload['build']['parameters']['ghprbPullId']

        self.issue = github.get_issue(pr_id)
        self.pr_labels = github.extract_labels(self.issue)

        if any([label for label in self.pr_labels if label in FRONTEND_LABELS]):
            attachments = self.get_attachments(payload)
            if not settings.SLACK_DRY_RUN:
                slack.post(attachments=attachments)
            else:
                logging.warning('Jenkins \tATTACHMENTS: %s' % attachments)

    def get_attachments(self, payload):
        plain = "Jenkins Job {} {}".format(
            self.issue['title'],
            payload['build']['status']
        )
        return [{
            "author_name": "Jenkins Job {}".format(payload['build']['status']),
            "author_link": payload['build']['full_url'],
            "fallback": plain,
            "color": "#c0392b" if payload['build']['status'] == "FAILURE" else "#2ecc71",
            "title": self.issue['title'],
            "title_link": self.issue['pull_request']['html_url'],
            "pretext": "@{} jenkins finished your PR's tests".format(self.issue['user']['login'])
        }]
