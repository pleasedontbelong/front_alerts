import json
from front_alerts import github
from .exceptions import EventNotHandled
from .core import EventHandler
from events.constants import SLACK_COLORS


class Issues(EventHandler):

    EVENT_NAME = "issues"

    def should_send(self, payload, route_config):
        """
        If issue has one of the FRONTEND_LABELS
        """
        trigger_labels = route_config.get('github_labels')
        labels = [label['name'] for label in payload['issue']['labels']]
        return any([label for label in labels if label in trigger_labels])

    def get_content(self, payload, route_config):
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

    def get_attachments(self, payload, route_config):
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
            "color": SLACK_COLORS.WARNING,
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


class PullRequests(EventHandler):

    EVENT_NAME = "pull_request"

    def should_send(self, payload, route_config):
        # get the labels from the issue object
        trigger_labels = route_config.get('github_labels')
        self.labels = github.get_issue_labels(issue_number=payload['number'], route_config=route_config)
        return any([label for label in self.labels if label in trigger_labels])

    def get_content(self, payload, route_config):
        action = payload['action']
        if action in ('labeled', 'unlabeled'):
            content = u":label: Pull Request <{pr_url}|#{number} {title}> {action} *{label}*".format(
                number=payload['pull_request']['number'],
                title=payload['pull_request']['title'],
                pr_url=payload['pull_request']['html_url'],
                action=action,
                label=payload['label']['name']
            )
            if action == "labeled" and payload['label']['name'] in route_config.get('review_request_labels'):
                content = content + " <!here> Review Requested"
            return content

        if action == "synchronize":
            return u":pencil2: New commits on <{pr_url}|#{number} {title}>".format(
                pr_url=payload['pull_request']['html_url'],
                number=payload['pull_request']['number'],
                title=payload['pull_request']['title'],
            )
        if action == "review_requested":
            reviewers = map(lambda x: x['login'], payload['pull_request']['requested_reviewers'])
            return u":speech_balloon: {reviewers} a review was requested for <{pr_url}|#{number} {title}>".format(
                reviewers=",".join(reviewers),
                pr_url=payload['pull_request']['html_url'],
                number=payload['pull_request']['number'],
                title=payload['pull_request']['title'],
            )

        return ""

    def get_event_id(self, payload):
        return payload['pull_request']['number']

    def get_attachments(self, payload, route_config):
        action = payload['action']
        if action in ('labeled', 'unlabeled', 'synchronize', 'review_requested'):
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
            "color": SLACK_COLORS.PRIMARY,
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


class PullRequestsComment(EventHandler):

    EVENT_NAME = "pull_request_review_comment"

    def should_send(self, payload, route_config):
        action = payload['action']
        if action not in ["deleted", "created"]:
            return False

        # get the labels from the issue object
        trigger_labels = route_config.get('github_labels')
        self.labels = github.get_issue_labels(
            issue_number=payload['pull_request']['number'],
            route_config=route_config)
        return any([label for label in self.labels if label in trigger_labels])

    def get_attachments(self, payload, route_config):
        action = payload['action']
        if action == "deleted":
            action = "deleted comment"
        else:
            action = "commented"
        plain = u"@{commenter} {action} on PR #{number} {comment_url}: \n{content}".format(
            action=action,
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
            "color": SLACK_COLORS.INFO,
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


class IssueComment(EventHandler):

    EVENT_NAME = "issue_comment"

    def should_send(self, payload, route_config):
        action = payload['action']
        if action not in ["deleted", "created"]:
            return False
        # get the labels from the issue object
        trigger_labels = route_config.get('github_labels')
        self.labels = [label['name'] for label in payload['issue']['labels']]
        return any([label for label in self.labels if label in trigger_labels])

    def get_attachments(self, payload, route_config):
        action = payload['action']
        if action == "deleted":
            action = "deleted comment"
        else:
            action = "commented"
        action_title = u"@{} {} on @{}'s ".format(
            payload['comment']['user']['login'],
            action,
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


class PullRequestsReview(EventHandler):

    EVENT_NAME = "pull_request_review"

    def should_send(self, payload, route_config):
        action = payload['action']
        if action not in ["submitted"]:
            return False

        # get the labels from the issue object
        trigger_labels = route_config.get('github_labels')
        self.labels = github.get_issue_labels(
            issue_number=payload['pull_request']['number'],
            route_config=route_config)
        return any([label for label in self.labels if label in trigger_labels])

    def get_content(self, payload, route_config):
        states_map = {
            "commented": {
                "action": "made comments on",
                "icon": ":speech_balloon:"
            },
            "changes_requested": {
                "action": "requested changes on",
                "icon": ":memo:"
            },
            "approved": {
                "action": "approved",
                "icon": ":white_check_mark:"
            }
        }
        state = payload['review']['state']

        return u"{icon} @{reviewer} {action} @{author} 's PR <{pr_url}|#{number} {title}>".format(
            icon=states_map[state]["icon"],
            reviewer=payload['review']['user']['login'],
            action=states_map[state]["action"],
            author=payload['pull_request']['user']['login'],
            pr_url=payload['pull_request']['html_url'],
            number=payload['pull_request']['number'],
            title=payload['pull_request']['title'],
        )

    def get_event_id(self, payload):
        return payload['pull_request']['number']


class GithubRequestEventHandler(object):

    EVENT_MAP = {
        Issues.EVENT_NAME: Issues,
        PullRequests.EVENT_NAME: PullRequests,
        PullRequestsComment.EVENT_NAME: PullRequestsComment,
        IssueComment.EVENT_NAME: IssueComment,
        PullRequestsReview.EVENT_NAME: PullRequestsReview,
    }

    def __init__(self, request):
        self.request = request
        self.action = self.request.META['HTTP_X_GITHUB_EVENT']
        if self.action not in self.EVENT_MAP:
            raise EventNotHandled("Event '%s' is not handled" % self.action)
        self.payload = json.loads(self.request.body)
        self.event_class = self.EVENT_MAP[self.action]()

    def send(self, route_config):
        self.event_class.send(self.payload, route_config)

    def should_send(self, route_config):
        return self.event_class.should_send(self.payload, route_config)

    @property
    def event_id(self):
        return self.event_class.get_event_id(self.payload)

    @property
    def event_name(self):
        return self.event_class.get_event_name(self.payload)
