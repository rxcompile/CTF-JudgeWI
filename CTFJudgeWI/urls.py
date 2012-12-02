from django.conf.urls import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Test.views.home', name='home'),
    # url(r'^Test/', include('Test.foo.urls')),
    url(r'^$', 'Scoreboard.views.scoreboard', name="scoreboard"),
    url(r'^team/(?P<team_id>\d+)/$', 'Scoreboard.views.team', name="team"),
    # Ajax
    url(r'^tsk/$', 'Scoreboard.views.task_info'),
    url(r'^chk/$', 'Scoreboard.views.send_check_flag'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
