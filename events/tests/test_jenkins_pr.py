# from django.test import TestCase
import json
from unittest import TestCase
from django.test.client import RequestFactory
from events.handlers.jenkins import JenkinsRequestEventHandler
from mock import patch
from front_alerts.constants import FRONTEND_LABELS


class PullRequestsEventsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.parser = JenkinsRequestEventHandler()
        self.payload = {
            "name": "botify-pull-request",
            "url": "job/botify-pull-request/",
            "build": {
                "full_url": "https://ci.botify.com/job/botify-pull-request/3053/",
                "number": 3053,
                "queue_id": 14871,
                "phase": "FINALIZED",
                "status": "FAILURE",
                "url": "job/botify-pull-request/3053/",
                "scm": {
                    "url": "git@github.com:botify-hq/botify",
                    "branch": "feature/2205/allow_user_to_change_his_credit_card",
                    "commit": "093f520c99b35297710f5c5b807c61ef83dd03fa"
                },
                "parameters": {
                    "ghprbTriggerAuthorEmail": "",
                    "ghprbTargetBranch": "devel",
                    "ghprbSourceBranch": "feature/2205/allow_user_to_change_his_credit_card",
                    "ghprbActualCommitAuthor": "Adele Delamarche",
                    "sha1": "origin/pr/2262/merge",
                    "ghprbPullLink": "https://github.com/botify-hq/botify/pull/2262",
                    "ghprbActualCommit": "d563eb491dc46cef7c2b77abb559bd43143d0b46",
                    "GIT_BRANCH": "feature/2205/allow_user_to_change_his_credit_card",
                    "ghprbPullAuthorEmail": "",
                    "ghprbTriggerAuthor": "",
                    "ghprbActualCommitAuthorEmail": "adele.delamarche@gmail.com",
                    "ghprbPullId": "2262",
                    "ghprbPullTitle": "Feature/2205/allow user to change his credit card",
                    "ghprbPullDescription": "GitHub pull request #2262 of commit d563eb491dc46cef7c2b77abb559bd43143d0b46 automatically merged."
                },
                "log": "",
                "artifacts": {}
            }
        }

    @patch('events.handlers.jenkins.github.get_issue_labels', lambda issue_number: FRONTEND_LABELS)
    @patch('events.handlers.jenkins.github.get_issue')
    def test_opened(self, get_issue_mock):
        get_issue_mock.return_value = {
            'title': "Test Issue",
            'pull_request': {
                'html_url': "http://test.com"
            },
            'user': {
                'login': "john"
            },
            'labels': [{'name': label for label in FRONTEND_LABELS}]
        }
        request = self.factory.post(
            '/',
            data=json.dumps(self.payload),
            content_type="application/json")
        self.parser.parse(request)
