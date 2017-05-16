import json
from django.test import TestCase, Client
from events.models import Event
from mock import patch


class JenkinsEventsTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_X_GITHUB_EVENT='issues')

    @patch('events.handlers.jenkins.github.get_issue')
    def test_build_finished(self, get_issue_mock):
        payload = json.dumps({
            "name": "something-unittests",
            "url": "job/something-unittests/",
            "build": {
                "full_url": "http://jenkins.example.com/job/something-unittests/6173/",
                "number": 6173,
                "queue_id": 4810,
                "phase": "FINALIZED",
                "status": "SUCCESS",
                "url": "job/something-unittests/6173/",
                "scm": {
                    "url": "git@github.com:site/site.git",
                    "branch": "origin/1234-my_new_branch",
                    "commit": "0a25598effcddb79a437806718e7bcdb92a66e0d"
                },
                "parameters": {
                    "BRANCH": "origin/1234-my_new_branch"
                },
                "log": "",
                "artifacts": {}
            }
        })

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
            data=payload,
            content_type="application/json")
        self.assertEquals(response.status_code, 200)
        event = Event.objects.get(event_id="1234")
        self.assertEquals(event.event_name, "jenkins_build")

    @patch('events.handlers.jenkins.github.get_issue')
    def test_not_normalized_branch(self, get_issue_mock):
        """
        Should not log when branch name is not normalized
        """
        payload = json.dumps({
            "name": "something-unittests",
            "url": "job/something-unittests/",
            "build": {
                "full_url": "http://jenkins.example.com/job/something-unittests/6173/",
                "number": 6173,
                "queue_id": 4810,
                "phase": "FINALIZED",
                "status": "SUCCESS",
                "url": "job/something-unittests/6173/",
                "scm": {
                    "url": "git@github.com:site/site.git",
                    "branch": "origin/my_new_branch",
                    "commit": "0a25598effcddb79a437806718e7bcdb92a66e0d"
                },
                "parameters": {
                    "BRANCH": "origin/my_new_branch"
                },
                "log": "",
                "artifacts": {}
            }
        })

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
            data=payload,
            content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Event.objects.exists())
