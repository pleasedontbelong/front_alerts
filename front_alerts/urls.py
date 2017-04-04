from django.conf.urls import include, url
from django.contrib import admin
from events.views import GithubView, JenkinsPRView, SentryView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jenkins_events$', JenkinsPRView.as_view(), name='jenkins-events'),
    url(r'^github_events$', GithubView.as_view(), name='github-events'),
    url(r'^sentry_events$', SentryView.as_view(), name='github-events'),
]
