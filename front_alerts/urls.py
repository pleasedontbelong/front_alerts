from django.conf.urls import patterns, include, url
from django.contrib import admin
from events.views import HookView, JenkinsPRView

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'front_alerts.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^jenkins_events$', JenkinsPRView.as_view(), name='jenkins-events'),
    url(r'^github_event$', HookView.as_view(), name='github-events'),

)
