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
    url(r'^tsk/$','Scoreboard.views.task_info'),
    url(r'^chk/$', 'Scoreboard.views.send_check_flag'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

#Gypnocat
from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^robots.txt$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'path': "robots.txt"}),
        (r'^favicon.ico$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'path': "favicon.ico"}),
        url(r'^media/$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )