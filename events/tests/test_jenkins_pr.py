import json
from django.test import TestCase, Client
from events.models import Event
from mock import patch


class JenkinsEventsTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_X_GITHUB_EVENT='issues')
        self.payload = json.dumps({
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
                    "ghprbPullDescription": "GitHub pull request #2262 of commit d563eb491 automatically merged."
                },
                "log": "",
                "artifacts": {}
            }
        })

    @patch('events.handlers.jenkins.github.get_issue')
    def test_build_finished(self, get_issue_mock):
        get_issue_mock.return_value = {
            'title': "Test Issue",
            'pull_request': {
                'html_url': "http://test.com"
            },
            'user': {
                'login': "john"
            },
            'labels': [{'name': "my-label"}]
        }
        response = self.client.post(
            '/jenkins_events',
            data=self.payload,
            content_type="application/json")
        self.assertEquals(response.status_code, 200)
        event = Event.objects.get(event_id="2262")
        self.assertEquals(event.event_name, "jenkins_build")
