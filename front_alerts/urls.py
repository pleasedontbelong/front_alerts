from django.conf.urls import patterns, include, url
from django.contrib import admin
from events.views import HookView, JenkinsPRView

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'front_alerts.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^jenkins_pr$', JenkinsPRView.as_view(), name='jenkins-pr'),
    url(r'^/$', HookView.as_view(), name='home'),

)
