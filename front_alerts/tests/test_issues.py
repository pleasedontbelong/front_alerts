# from django.test import TestCase
import json
from unittest import TestCase
from django.test.client import RequestFactory
from front_alerts.handlers.github import GithubRequestEventHandler


class IssuesEventsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.parser = GithubRequestEventHandler()
        self.payload = {
            "action": "opened",
            "issue": {
                "url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/2",
                "labels_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/2/labels{/name}",
                "comments_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/2/comments",
                "events_url": "https://api.github.com/repos/baxterthehacker/public-repo/issues/2/events",
                "html_url": "https://github.com/baxterthehacker/public-repo/issues/2",
                "id": 73464126,
                "number": 2,
                "title": "Spelling error in the README file",
                "user": {
                    "login": "baxterthehacker",
                    "id": 6752317,
                },
                "labels": [
                    {
                        "url": "https://api.github.com/repos/baxterthehacker/public-repo/labels/bug",
                        "name": "comp:frontend",
                        "color": "fc2929"
                    }
                ],
                "state": "open",
                "locked": False,
                "assignee": None,
                "milestone": None,
                "comments": 0,
                "created_at": "2015-05-05T23:40:28Z",
                "updated_at": "2015-05-05T23:40:28Z",
                "closed_at": None,
                "body": "It looks like you accidently spelled 'commit' with two 't's."
            },
            "repository": {
                "id": 35129377,
                "name": "public-repo",
            },
            "sender": {
                "id": 6752317,
            }
        }

    def test_opened(self):
        request = self.factory.post(
            '/',
            data=json.dumps(self.payload),
            content_type="application/json",
            HTTP_X_GITHUB_EVENT='issues')
        self.parser.parse(request)


class IssueLabelEventTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.parser = GithubRequestEventHandler()
        self.payload = {
            "action": "labeled",
            "issue": {
                "url": "https://api.github.com/repos/botify-hq/botify/issues/2444",
                "labels_url": "https://api.github.com/repos/botify-hq/botify/issues/2444/labels{/name}",
                "comments_url": "https://api.github.com/repos/botify-hq/botify/issues/2444/comments",
                "events_url": "https://api.github.com/repos/botify-hq/botify/issues/2444/events",
                "html_url": "https://github.com/botify-hq/botify/issues/2444",
                "id": 127423253,
                "number": 2444,
                "title": "Auth on Swagger",
                "user": {
                    "login": "pleasedontbelong",
                    "id": 1785603,
                    "avatar_url": "https://avatars.githubusercontent.com/u/1785603?v=3",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/pleasedontbelong",
                    "html_url": "https://github.com/pleasedontbelong",
                    "followers_url": "https://api.github.com/users/pleasedontbelong/followers",
                    "following_url": "https://api.github.com/users/pleasedontbelong/following{/other_user}",
                    "gists_url": "https://api.github.com/users/pleasedontbelong/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/pleasedontbelong/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/pleasedontbelong/subscriptions",
                    "organizations_url": "https://api.github.com/users/pleasedontbelong/orgs",
                    "repos_url": "https://api.github.com/users/pleasedontbelong/repos",
                    "events_url": "https://api.github.com/users/pleasedontbelong/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/pleasedontbelong/received_events",
                    "type": "User",
                    "site_admin": False
                },
                "labels": [
                    {
                        "url": "https://api.github.com/repos/botify-hq/botify/labels/comp:%20API",
                        "name": "comp: API",
                        "color": "bfe5bf"
                    },
                    {
                        "url": "https://api.github.com/repos/botify-hq/botify/labels/comp:frontend",
                        "name": "comp:frontend",
                        "color": "006b75"
                    },
                    {
                        "url": "https://api.github.com/repos/botify-hq/botify/labels/on%20hold",
                        "name": "on hold",
                        "color": "e11d21"
                    },
                    {
                        "url": "https://api.github.com/repos/botify-hq/botify/labels/status:%202-this%20week",
                        "name": "status: 2-this week",
                        "color": "d4c5f9"
                    }
                ],
                "state": "open",
                "locked": False,
                "assignee": None,
                "milestone": {
                    "url": "https://api.github.com/repos/botify-hq/botify/milestones/42",
                    "html_url": "https://github.com/botify-hq/botify/milestones/API%20V1",
                    "labels_url": "https://api.github.com/repos/botify-hq/botify/milestones/42/labels",
                    "id": 1253629,
                    "number": 42,
                    "title": "API V1",
                    "description": "",
                    "creator": {
                        "login": "nathG",
                        "id": 7911717,
                        "avatar_url": "https://avatars.githubusercontent.com/u/7911717?v=3",
                        "gravatar_id": "",
                        "url": "https://api.github.com/users/nathG",
                        "html_url": "https://github.com/nathG",
                        "followers_url": "https://api.github.com/users/nathG/followers",
                        "following_url": "https://api.github.com/users/nathG/following{/other_user}",
                        "gists_url": "https://api.github.com/users/nathG/gists{/gist_id}",
                        "starred_url": "https://api.github.com/users/nathG/starred{/owner}{/repo}",
                        "subscriptions_url": "https://api.github.com/users/nathG/subscriptions",
                        "organizations_url": "https://api.github.com/users/nathG/orgs",
                        "repos_url": "https://api.github.com/users/nathG/repos",
                        "events_url": "https://api.github.com/users/nathG/events{/privacy}",
                        "received_events_url": "https://api.github.com/users/nathG/received_events",
                        "type": "User",
                        "site_admin": False
                    },
                    "open_issues": 38,
                    "closed_issues": 14,
                    "state": "open",
                    "created_at": "2015-08-13T13:48:11Z",
                    "updated_at": "2016-01-26T14:16:53Z",
                    "due_on": "2016-01-28T23:00:00Z",
                    "closed_at": None
                },
                "comments": 0,
                "created_at": "2016-01-19T11:17:04Z",
                "updated_at": "2016-01-27T16:17:31Z",
                "closed_at": None,
                "body": " Add authentification like done there https://gist.github.com/zallek/fe5188f70ca710f882ea.\r\n- [ ] You can define the security property at top level with the value DjangoRestToken\r\n- [ ] Override these security property for any endpoint which doesn't need to be authentificate (is there any ?)"
            },
            "label": {
                "url": "https://api.github.com/repos/botify-hq/botify/labels/on%20hold",
                "name": "on hold",
                "color": "e11d21"
            },
            "repository": {
                "id": 10640087,
                "name": "botify",
                "full_name": "botify-hq/botify",
                "owner": {
                    "login": "botify-hq",
                    "id": 540514,
                    "avatar_url": "https://avatars.githubusercontent.com/u/540514?v=3",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/botify-hq",
                    "html_url": "https://github.com/botify-hq",
                    "followers_url": "https://api.github.com/users/botify-hq/followers",
                    "following_url": "https://api.github.com/users/botify-hq/following{/other_user}",
                    "gists_url": "https://api.github.com/users/botify-hq/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/botify-hq/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/botify-hq/subscriptions",
                    "organizations_url": "https://api.github.com/users/botify-hq/orgs",
                    "repos_url": "https://api.github.com/users/botify-hq/repos",
                    "events_url": "https://api.github.com/users/botify-hq/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/botify-hq/received_events",
                    "type": "Organization",
                    "site_admin": False
                },
                "private": True,
                "html_url": "https://github.com/botify-hq/botify",
                "description": "Botify Main Repository",
                "fork": False,
                "url": "https://api.github.com/repos/botify-hq/botify",
                "forks_url": "https://api.github.com/repos/botify-hq/botify/forks",
                "keys_url": "https://api.github.com/repos/botify-hq/botify/keys{/key_id}",
                "collaborators_url": "https://api.github.com/repos/botify-hq/botify/collaborators{/collaborator}",
                "teams_url": "https://api.github.com/repos/botify-hq/botify/teams",
                "hooks_url": "https://api.github.com/repos/botify-hq/botify/hooks",
                "issue_events_url": "https://api.github.com/repos/botify-hq/botify/issues/events{/number}",
                "events_url": "https://api.github.com/repos/botify-hq/botify/events",
                "assignees_url": "https://api.github.com/repos/botify-hq/botify/assignees{/user}",
                "branches_url": "https://api.github.com/repos/botify-hq/botify/branches{/branch}",
                "tags_url": "https://api.github.com/repos/botify-hq/botify/tags",
                "blobs_url": "https://api.github.com/repos/botify-hq/botify/git/blobs{/sha}",
                "git_tags_url": "https://api.github.com/repos/botify-hq/botify/git/tags{/sha}",
                "git_refs_url": "https://api.github.com/repos/botify-hq/botify/git/refs{/sha}",
                "trees_url": "https://api.github.com/repos/botify-hq/botify/git/trees{/sha}",
                "statuses_url": "https://api.github.com/repos/botify-hq/botify/statuses/{sha}",
                "languages_url": "https://api.github.com/repos/botify-hq/botify/languages",
                "stargazers_url": "https://api.github.com/repos/botify-hq/botify/stargazers",
                "contributors_url": "https://api.github.com/repos/botify-hq/botify/contributors",
                "subscribers_url": "https://api.github.com/repos/botify-hq/botify/subscribers",
                "subscription_url": "https://api.github.com/repos/botify-hq/botify/subscription",
                "commits_url": "https://api.github.com/repos/botify-hq/botify/commits{/sha}",
                "git_commits_url": "https://api.github.com/repos/botify-hq/botify/git/commits{/sha}",
                "comments_url": "https://api.github.com/repos/botify-hq/botify/comments{/number}",
                "issue_comment_url": "https://api.github.com/repos/botify-hq/botify/issues/comments{/number}",
                "contents_url": "https://api.github.com/repos/botify-hq/botify/contents/{+path}",
                "compare_url": "https://api.github.com/repos/botify-hq/botify/compare/{base}...{head}",
                "merges_url": "https://api.github.com/repos/botify-hq/botify/merges",
                "archive_url": "https://api.github.com/repos/botify-hq/botify/{archive_format}{/ref}",
                "downloads_url": "https://api.github.com/repos/botify-hq/botify/downloads",
                "issues_url": "https://api.github.com/repos/botify-hq/botify/issues{/number}",
                "pulls_url": "https://api.github.com/repos/botify-hq/botify/pulls{/number}",
                "milestones_url": "https://api.github.com/repos/botify-hq/botify/milestones{/number}",
                "notifications_url": "https://api.github.com/repos/botify-hq/botify/notifications{?since,all,participating}",
                "labels_url": "https://api.github.com/repos/botify-hq/botify/labels{/name}",
                "releases_url": "https://api.github.com/repos/botify-hq/botify/releases{/id}",
                "deployments_url": "https://api.github.com/repos/botify-hq/botify/deployments",
                "created_at": "2013-06-12T09:45:27Z",
                "updated_at": "2016-01-11T17:49:50Z",
                "pushed_at": "2016-01-27T16:15:47Z",
                "git_url": "git://github.com/botify-hq/botify.git",
                "ssh_url": "git@github.com:botify-hq/botify.git",
                "clone_url": "https://github.com/botify-hq/botify.git",
                "svn_url": "https://github.com/botify-hq/botify",
                "homepage": "https://app.botify.com/",
                "size": 77227,
                "stargazers_count": 0,
                "watchers_count": 0,
                "language": "Python",
                "has_issues": True,
                "has_downloads": True,
                "has_wiki": True,
                "has_pages": False,
                "forks_count": 0,
                "mirror_url": None,
                "open_issues_count": 590,
                "forks": 0,
                "open_issues": 590,
                "watchers": 0,
                "default_branch": "devel"
            },
            "organization": {
                "login": "botify-hq",
                "id": 540514,
                "url": "https://api.github.com/orgs/botify-hq",
                "repos_url": "https://api.github.com/orgs/botify-hq/repos",
                "events_url": "https://api.github.com/orgs/botify-hq/events",
                "members_url": "https://api.github.com/orgs/botify-hq/members{/member}",
                "public_members_url": "https://api.github.com/orgs/botify-hq/public_members{/member}",
                "avatar_url": "https://avatars.githubusercontent.com/u/540514?v=3",
                "description": ""
            },
            "sender": {
                "login": "pleasedontbelong",
                "id": 1785603,
                "avatar_url": "https://avatars.githubusercontent.com/u/1785603?v=3",
                "gravatar_id": "",
                "url": "https://api.github.com/users/pleasedontbelong",
                "html_url": "https://github.com/pleasedontbelong",
                "followers_url": "https://api.github.com/users/pleasedontbelong/followers",
                "following_url": "https://api.github.com/users/pleasedontbelong/following{/other_user}",
                "gists_url": "https://api.github.com/users/pleasedontbelong/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/pleasedontbelong/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/pleasedontbelong/subscriptions",
                "organizations_url": "https://api.github.com/users/pleasedontbelong/orgs",
                "repos_url": "https://api.github.com/users/pleasedontbelong/repos",
                "events_url": "https://api.github.com/users/pleasedontbelong/events{/privacy}",
                "received_events_url": "https://api.github.com/users/pleasedontbelong/received_events",
                "type": "User",
                "site_admin": False
            }
        }

    def test_opened(self):
        request = self.factory.post(
            '/',
            data=json.dumps(self.payload),
            content_type="application/json",
            HTTP_X_GITHUB_EVENT='issues')
        self.parser.parse(request)
