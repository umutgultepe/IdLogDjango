from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logs/', include('logs.urls')),
    url(r'^auth/', include('authenticate.urls')),
    url(r'^$', "authenticate.views.login_page"),
)

