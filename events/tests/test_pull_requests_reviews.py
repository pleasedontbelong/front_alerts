from django.test import TestCase
from django.test import Client
from .fixtures import (pull_request_review_commented, pull_request_review_rejected,
                       pull_request_review_approved)
from events.models import Event
from mock import patch


class PullRequestReviewsEventsTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_X_GITHUB_EVENT='pull_request_review')

    @patch('events.handlers.github.github.get_issue_labels', lambda issue_number, route_config: ["test"])
    def test_comment(self):
        response = self.client.post(
            '/github_events',
            data=pull_request_review_commented,
            content_type="application/json")
        self.assertEquals(response.status_code, 200)
        event = Event.objects.get(event_id="9")  # PR number
        self.assertEquals(event.event_name, "pull_request_review-submitted")

    @patch('events.handlers.github.github.get_issue_labels', lambda issue_number, route_config: ["test"])
    def test_approve(self):
        response = self.client.post(
            '/github_events',
            data=pull_request_review_approved,
            content_type="application/json")
        self.assertEquals(response.status_code, 200)
        event = Event.objects.get(event_id="9")  # PR number
        self.assertEquals(event.event_name, "pull_request_review-submitted")

    @patch('events.handlers.github.github.get_issue_labels', lambda issue_number, route_config: ["test"])
    def test_reject(self):
        response = self.client.post(
            '/github_events',
            data=pull_request_review_rejected,
            content_type="application/json")
        self.assertEquals(response.status_code, 200)
        event = Event.objects.get(event_id="9")  # PR number
        self.assertEquals(event.event_name, "pull_request_review-submitted")
