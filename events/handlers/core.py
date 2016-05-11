import logging
from front_alerts import slack
from django.conf import settings
logger = logging.getLogger('django')


class EventHandler(object):

    def should_send(self, payload, route_config):
        """
        Check if we should send an alert to slack
        """
        return False

    def get_content(self, payload, route_config):
        return ""

    def get_attachments(self, payload, route_config):
        return None

    def get_event_id(self, payload):
        return ""

    def get_event_name(self, payload):
        return u"{}-{}".format(self.EVENT_NAME, payload['action'])

    def send(self, payload, route_config):
        slack_channels = route_config.get('slack_channels')
        content = self.get_content(payload, route_config)
        attachments = self.get_attachments(payload, route_config)
        if not settings.SLACK_DRY_RUN:
            for channel in slack_channels:
                slack.post(content=content, channel=channel, attachments=attachments)
        else:
            logger.info('\nCHANNELS: %s\nCONTENT: %s\nATTACHMENTS: %s' % (
                ",".join(slack_channels), content, attachments)
            )
