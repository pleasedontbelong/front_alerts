import json
import logging
from front_alerts import slack
from front_alerts import github
from django.conf import settings
from .exceptions import EventNotHandled
logger = logging.getLogger('django')


class GithubEvent(object):

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


class Issues(GithubEvent):

    EVENT_NAME = "issues"

    def should_send(self, payload, trigger_labels):
        """
        If issue has one of the FRONTEND_LABELS
        """
        labels = [label['name'] for label in payload['issue']['labels']]
        return any([label for label in labels if label in trigger_labels])

    def get_content(self, payload, review_request_label):
        action = payload['action']
        if action in ('labeled', 'unlabeled'):
            return u":label: Issue <{issue_url}|#{number} {title}> {action} *{label}*".format(
                number=payload['issue']['number'],
                title=payload['issue']['title'],
                issue_url=payload['issue']['html_url'],
                action=payload['action'],
                label=payload['label']['name']
            )
        return ""

    def get_event_id(self, payload):
        return payload['issue']['number']

    def get_attachments(self, payload):
        action = payload['action']
        if action in ('labeled', 'unlabeled'):
            return None

        plain = u"Issue #{number} {action} {issue_url}: {title}\n{content}".format(
            issue_url=payload['issue']['html_url'],
            number=payload['issue']['number'],
            action=payload['action'],
            title=payload['issue']['title'],
            content=payload['issue']['body'][:140]
        )
        return [{
            "author_name": u"Issue {}".format(payload['action']),
            "fallback": plain,
            "color": "#f4a62a",
            "title": payload['issue']['title'],
            "title_link": payload['issue']['html_url'],
            "text": payload['issue']['body'][:140],
            "fields": [
                {
                    "title": "Labels",
                    "value": ', '.join([label['name'] for label in payload['issue']['labels']]),
                    "short": False
                }
            ]
        }]


class PullRequests(GithubEvent):

    EVENT_NAME = "pull_request"

    def should_send(self, payload, trigger_labels):
        # get the labels from the issue object
        self.labels = github.get_issue_labels(issue_number=payload['number'])
        return any([label for label in self.labels if label in trigger_labels])

    def get_content(self, payload, review_request_label):
        action = payload['action']
        if action in ('labeled', 'unlabeled'):
            content = u":label: Pull Request <{pr_url}|#{number} {title}> {action} *{label}*".format(
                number=payload['pull_request']['number'],
                title=payload['pull_request']['title'],
                pr_url=payload['pull_request']['html_url'],
                action=action,
                label=payload['label']['name']
            )
            review_request_label = kwargs.get('review_request_label', '')
            if action == "labeled" and payload['label']['name'] == review_request_label:
                content = content + " <!here> Review Requested"
            return content

        if action == "synchronize":
            return u":pencil2: New commits on <{pr_url}|#{number} {title}>".format(
                pr_url=payload['pull_request']['html_url'],
                number=payload['pull_request']['number'],
                title=payload['pull_request']['title'],
            )

        return ""

    def get_event_id(self, payload):
        return payload['pull_request']['number']

    def get_attachments(self, payload):
        action = payload['action']
        if action in ('labeled', 'unlabeled'):
            return None

        if action == "synchronize":
            return None

        plain = u"Pull Request #{number} {action} {pr_url}: {title}\n{content}".format(
            pr_url=payload['pull_request']['html_url'],
            number=payload['pull_request']['number'],
            action=action,
            title=payload['pull_request']['title'],
            content=payload['pull_request']['body'][:140]
        )
        return [{
            "author_name": u"Pull Request {}".format(action),
            "fallback": plain,
            "color": "#2980b9",
            "title": payload['pull_request']['title'],
            "title_link": payload['pull_request']['html_url'],
            "text": payload['pull_request']['body'][:140],
            "fields": [
                {
                    "title": "Labels",
                    "value": ', '.join(self.labels),
                    "short": False
                }
            ]
        }]


class PullRequestsComment(GithubEvent):

    EVENT_NAME = "pull_request_review_comment"

    def should_send(self, payload, trigger_labels):
        # get the labels from the issue object
        self.labels = github.get_issue_labels(issue_number=payload['pull_request']['number'])
        return any([label for label in self.labels if label in trigger_labels])

    def get_attachments(self, payload):
        plain = u"@{commenter} commented on PR #{number} {comment_url}: \n{content}".format(
            commenter=payload['comment']['user']['login'],
            comment_url=payload['comment']['html_url'],
            number=payload['pull_request']['number'],
            content=payload['comment']['body'][:140]
        )
        return [{
            "author_name": u"@{} commented on @{}'s Pull Request Code #{} {}".format(
                payload['comment']['user']['login'],
                payload['pull_request']['user']['login'],
                payload['pull_request']['number'],
                payload['pull_request']['title'],
            ),
            "author_link": payload['pull_request']['html_url'],
            "fallback": plain,
            "color": "#16a085",
            "title": payload['comment']['path'],
            "title_link": payload['comment']['html_url'],
            "text": payload['comment']['body'][:140],
            "fields": [
                {
                    "title": "Labels",
                    "value": ', '.join(self.labels),
                    "short": False
                }
            ]
        }]

    def get_event_id(self, payload):
        return payload['pull_request']['number']


class IssueComment(GithubEvent):

    EVENT_NAME = "issue_comment"

    def should_send(self, payload, trigger_labels):
        # get the labels from the issue object
        self.labels = [label['name'] for label in payload['issue']['labels']]
        return any([label for label in self.labels if label in trigger_labels])

    def get_attachments(self, payload):
        action_title = u"@{} commented on @{}'s ".format(
            payload['comment']['user']['login'],
            payload['issue']['user']['login']
        )

        if 'pull_request' in payload['issue']:
            action_title += "Pull Request"
            color = "#54A4D9"
        else:
            action_title += "Issue"
            color = "#f6bb5a"
        plain = u"{action_title} #{number} {comment_url}: \n{content}".format(
            action_title=action_title,
            comment_url=payload['comment']['html_url'],
            number=payload['issue']['number'],
            content=payload['comment']['body'][:140]
        )
        return [{
            "title": u"{} #{} {}".format(
                action_title,
                payload['issue']['number'],
                payload['issue']['title'],
            ),
            "title_link": payload['comment']['html_url'],
            "fallback": plain,
            "color": color,
            "text": payload['comment']['body'][:140],
            "fields": [
                {
                    "title": "Labels",
                    "value": ', '.join(self.labels),
                    "short": False
                }
            ]
        }]

    def get_event_id(self, payload):
        return payload['issue']['number']


class GithubRequestEventHandler(object):

    EVENT_MAP = {
        Issues.EVENT_NAME: Issues,
        PullRequests.EVENT_NAME: PullRequests,
        PullRequestsComment.EVENT_NAME: PullRequestsComment,
        IssueComment.EVENT_NAME: IssueComment
    }

    def __init__(self, request):
        self.request = request
        self.action = self.request.META['HTTP_X_GITHUB_EVENT']
        if self.action not in self.EVENT_MAP:
            raise EventNotHandled("Event '%s' is not handled" % self.action)
        self.payload = json.loads(self.request.body)
        self.event_class = self.EVENT_MAP[self.action]()

    def send(self, slack_channels, review_request_label):
        self.event_class.send(self.payload, slack_channels, review_request_label)

    def should_send(self, trigger_labels):
        return self.event_class.should_send(self.payload, trigger_labels)

    @property
    def event_id(self):
        return self.event_class.get_event_id(self.payload)

    @property
    def event_name(self):
        return self.event_class.get_event_name(self.payload)
