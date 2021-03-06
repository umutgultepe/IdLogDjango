from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

#ForceSSL = False

urlpatterns = patterns('',
#    url(r'^admin/', include(admin.site.urls), {'SSL':ForceSSL}),
#    url(r'^logs/', include('logs.urls'), {'SSL':ForceSSL}),
#    url(r'^auth/', include('authenticate.urls'), {'SSL':ForceSSL}),
#    url(r'^$', "authenticate.views.login_page", {'SSL':ForceSSL}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logs/', include('logs.urls')),
    url(r'^auth/', include('authenticate.urls')),
    url(r'^$', "authenticate.views.login_page"),
    (r'^accounts/', include('allauth.urls')),
)

