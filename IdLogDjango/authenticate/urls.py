from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('authenticate.views',
    url(r'^$', 'login_page'),
    url(r'^login/$', 'login_page'),
    url(r'^recieveLogin/$', 'recieveLogin'),
    url(r'^failure/$', 'failure'),
    url(r'^logout/$', 'logout_page'),
    url(r'^success/$', 'success'),
)

