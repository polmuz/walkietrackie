from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'walkietrackie.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('allauth.urls')),
    url(r'^api/v1/walks$', 'walks.views.walk_list_api'),
    url(r'^', "walks.views.main"),
)
