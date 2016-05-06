# from django.test import TestCase
import json
from unittest import TestCase
from django.test.client import RequestFactory
from events.handlers.github import GithubRequestEventHandler
from .fixtures import pull_request_coment_payload


class PullRequestsEventsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.parser = GithubRequestEventHandler()
        self.payload = pull_request_coment_payload

    def test_opened(self):
        request = self.factory.post(
            '/',
            data=json.dumps(self.payload),
            content_type="application/json",
            HTTP_X_GITHUB_EVENT='pull_request_review_comment')
        self.parser.parse(request)
