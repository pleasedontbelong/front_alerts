import logging
from front_alerts import slack
from django.conf import settings
logger = logging.getLogger('django')


class EventHandler(object):

    def should_send(self, payload, trigger_labels):
        """
        Check if we should send an alert to slack
        """
        return False

    def get_content(self, payload, review_request_label):
        return ""

    def get_attachments(self, payload):
        return None

    def get_event_id(self, payload):
        return ""

    def get_event_name(self, payload):
        return u"{}-{}".format(self.EVENT_NAME, payload['action'])

    def send(self, payload, slack_channels, review_request_label):
        content = self.get_content(payload, review_request_label)
        attachments = self.get_attachments(payload)
        if not settings.SLACK_DRY_RUN:
            for channel in slack_channels:
                slack.post(content=content, channel=channel, attachments=attachments)
        else:
            logger.info('\nCHANNELS: %s\nCONTENT: %s\nATTACHMENTS: %s' % (
                ",".join(slack_channels), content, attachments)
            )
