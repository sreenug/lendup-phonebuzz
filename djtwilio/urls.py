from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #  Here we add our Twilio URLs
    url(r'^gather/$', 'djtwilio.views.gather_digits'),
    url(r'^respond/$', 'djtwilio.views.handle_response'),
    url(r'^phase2/', 'djtwilio.views.get_phase2'),
    url(r'^fizzbuzz/', 'djtwilio.views.home'),
    url(r'^phase3/', 'djtwilio.views.phase3'),
    url(r'^getcalls/', 'djtwilio.views.call_records_json'),
    url(r'^replay/?$', 'djtwilio.views.handle_replay_message'),
    url(r'^previouscall/?$', 'djtwilio.views.previous_call'),
    url(r'^makecall/?$', 'djtwilio.views.make_call'),
)
