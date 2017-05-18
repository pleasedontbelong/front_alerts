from django.test import TestCase
from django.test import Client
from .fixtures import release_tag
from events.models import Event


class PullRequestsEventsTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_X_GITHUB_EVENT='release')
        self.payload = release_tag

    def test_comment(self):
        response = self.client.post(
            '/github_events',
            data=self.payload,
            content_type="application/json")
        self.assertEquals(response.status_code, 200)
        event = Event.objects.get(event_id="17.5.0rc5")  # Tag
        self.assertEquals(event.event_name, "release-published")
