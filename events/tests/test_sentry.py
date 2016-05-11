from django.test import TestCase, Client
from events.models import Event
from .fixtures import sentry_error_payload


class IssueLabelEventTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.payload = sentry_error_payload

    def test_labeled(self):
        response = self.client.post(
            '/sentry_event',
            data=self.payload,
            content_type="application/json")
        self.assertEquals(response.status_code, 200)
        event = Event.objects.get(event_id="120813073")
        self.assertEquals(event.event_name, "sentry_error")
