# from django.test import TestCase
import json
from unittest import TestCase
from django.test.client import RequestFactory
from events.handlers.github import GithubRequestEventHandler
from .fixtures import issue_comment_payload


class PullRequestsEventsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.parser = GithubRequestEventHandler()
        self.payload = issue_comment_payload

    def test_opened(self):
        # @TODO mock github.get_issue_labels()
        request = self.factory.post(
            '/',
            data=json.dumps(self.payload),
            content_type="application/json",
            HTTP_X_GITHUB_EVENT='issue_comment')
        self.parser.parse(request)
