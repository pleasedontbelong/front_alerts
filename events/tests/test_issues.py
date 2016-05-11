from django.test import TestCase, Client
from events.models import Event
from .fixtures import issue_labeled_payload, issue_opened_payload


class IssuesEventsTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_X_GITHUB_EVENT='issues')
        self.payload = issue_opened_payload

    def test_opened(self):
        response = self.client.post(
            '/github_event',
            data=self.payload,
            content_type="application/json")
        self.assertEquals(response.status_code, 200)
        event = Event.objects.get(event_id="2")
        self.assertEquals(event.event_name, "issues-opened")


class IssueLabelEventTestCase(TestCase):

    def setUp(self):
        self.client = Client(HTTP_X_GITHUB_EVENT='issues')
        self.payload = issue_labeled_payload

    def test_labeled(self):
        response = self.client.post(
            '/github_event',
            data=self.payload,
            content_type="application/json")
        self.assertEquals(response.status_code, 200)
        event = Event.objects.get(event_id="2444")
        self.assertEquals(event.event_name, "issues-labeled")
