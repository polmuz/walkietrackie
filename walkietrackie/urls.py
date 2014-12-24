from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # Auth
    (r'^accounts/', include('allauth.urls')),

    # API v1
    url(r'^api/v1/token-auth$',
        'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api/v1/walks/(?P<pk>[0-9]+)$', 'walks.views.walk_detail'),
    url(r'^api/v1/walks$', 'walks.views.walk_list_api'),

    # Main view for single page app
    url(r'^', "walks.views.main"),
)
