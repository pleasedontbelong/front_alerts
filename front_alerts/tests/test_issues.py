import json
from unittest import TestCase
from django.test.client import RequestFactory
from front_alerts.parsers import GithubRequestEventParser


class IssuesEventsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.parser = GithubRequestEventParser()
        self.payload = {
            "action": "opened",
            "issue": {
                "url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/2",
                "labels_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/2/labels{/name}",
                "comments_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/2/comments",
                "events_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/2/events",
                "html_url": "https://github.com/baxterthehacker/public-repo/issues/2",
                "id": 73464126,
                "number": 2,
                "title": "Spelling error in the README file",
                "user": {
                    "login": "baxterthehacker",
                    "id": 6752317,
                },
                "labels": [
                    {
                        "url": "https://api.github.com/repos/baxterthehacker/public-repo/labels/bug",
                        "name": "comp:frontend",
                        "color": "fc2929"
                    }
                ],
                "state": "open",
                "locked": False,
                "assignee": None,
                "milestone": None,
                "comments": 0,
                "created_at": "2015-05-05T23:40:28Z",
                "updated_at": "2015-05-05T23:40:28Z",
                "closed_at": None,
                "body": "It looks like you accidently spelled 'commit' with two 't's."
            },
            "repository": {
                "id": 35129377,
                "name": "public-repo",
            },
            "sender": {
                "id": 6752317,
            }
        }

    def test_opened(self):
        request = self.factory.post(
            '/',
            data=json.dumps(self.payload),
            content_type="application/json",
            HTTP_X_GITHUB_EVENT='issues')
        self.parser.parse(request)
