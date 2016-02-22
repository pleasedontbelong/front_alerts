# from django.test import TestCase
import json
from unittest import TestCase
from django.test.client import RequestFactory
from front_alerts.handlers.github import GithubRequestEventHandler


class PullRequestsEventsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.parser = GithubRequestEventHandler()
        self.payload = {
            "action": "opened",
            "number": 2637,
            "pull_request": {
                "url": "https://api.github.com/repos/baxterthehacker/public-repo/pulls/1",
                "id": 34778301,
                "html_url": "https://github.com/baxterthehacker/public-repo/pull/1",
                "diff_url": "https://github.com/baxterthehacker/public-repo/pull/1.diff",
                "patch_url": "https://github.com/baxterthehacker/public-repo/pull/1.patch",
                "issue_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/1",
                "number": 2637,
                "state": "open",
                "locked": False,
                "title": "Just testing alerts",
                "user": {
                    "login": "baxterthehacker",
                    "id": 6752317
                },
                "body": "This is a pretty simple change that we need to pull into master.",
                "created_at": "2015-05-05T23: 40: 27Z",
                "updated_at": "2015-05-05T23: 40: 27Z",
                "closed_at": None,
                "merged_at": None,
                "merge_commit_sha": None,
                "assignee": None,
                "milestone": None,
                "commits_url": "https://api.github.com/repos/baxterthehacker/public-repo/pulls/1/commits",
                "review_comments_url": "https://api.github.com/repos/baxterthehacker/public-repo/pulls/1/comments",
                "review_comment_url": "https://api.github.com/repos/baxterthehacker/public-repo/pulls/comments{/number}",
                "comments_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/1/comments",
                "statuses_url": "https://api.github.com/repos/baxterthehacker/public-repo/statuses/0d1a26e67d8f5eaf1f6ba5c57fc3c7d91ac0fd1c",
                "head": {
                    "label": "baxterthehacker: changes",
                    "ref": "changes",
                    "sha": "0d1a26e67d8f5eaf1f6ba5c57fc3c7d91ac0fd1c",
                    "user": {
                        "login": "baxterthehacker",
                        "id": 6752317
                    },
                    "repo": {
                        "id": 35129377,
                        "name": "public-repo",
                        "full_name": "baxterthehacker/public-repo",
                        "owner": {
                            "login": "baxterthehacker",
                            "id": 6752317
                        },
                        "private": False,
                        "html_url": "https://github.com/baxterthehacker/public-repo",
                        "description": "",
                        "default_branch": "master"
                    }
                },
                "base": {
                    "label": "baxterthehacker: master",
                    "ref": "master",
                    "sha": "9049f1265b7d61be4a8904a9a27120d2064dab3b",
                    "user": {
                        "login": "baxterthehacker",
                        "id": 6752317
                    },
                    "repo": {
                        "id": 35129377,
                        "name": "public-repo",
                        "full_name": "baxterthehacker/public-repo",
                        "owner": {
                            "login": "baxterthehacker",
                            "id": 6752317
                        },
                        "private": False,
                        "html_url": "https://github.com/baxterthehacker/public-repo",
                        "description": "",
                        "fork": False,
                        "url": "https://api.github.com/repos/baxterthehacker/public-repo",
                        "default_branch": "master"
                    }
                },
                "_links": {
                    "self": {
                        "href": "https://api.github.com/repos/baxterthehacker/public-repo/pulls/1"
                    },
                    "html": {
                        "href": "https://github.com/baxterthehacker/public-repo/pull/1"
                    }
                },
                "merged": False,
                "mergeable": None,
                "mergeable_state": "unknown",
                "merged_by": None,
                "comments": 0,
                "review_comments": 0,
                "commits": 1,
                "additions": 1,
                "deletions": 1,
                "changed_files": 1
            },
            "repository": {
                "id": 35129377,
                "name": "public-repo",
                "full_name": "baxterthehacker/public-repo",
                "owner": {
                    "login": "baxterthehacker",
                    "id": 6752317
                },
                "private": False,
                "html_url": "https://github.com/baxterthehacker/public-repo",
                "description": "",
                "default_branch": "master"
            },
            "sender": {
                "login": "baxterthehacker",
                "id": 6752317,
                "avatar_url": "https://avatars.githubusercontent.com/u/6752317?v=3",
                "gravatar_id": "",
                "url": "https://api.github.com/users/baxterthehacker"
            }
        }

    def test_opened(self):
        request = self.factory.post(
            '/',
            data=json.dumps(self.payload),
            content_type="application/json",
            HTTP_X_GITHUB_EVENT='pull_request')
        self.parser.parse(request)
