from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('logs.views',
    url(r'^$', 'index'),
    url(r'^search/$', 'search'),
    url(r'^anonymous/$', 'anonymous'),
    url(r'^newentry/$', 'newEntry'),
    url(r'^submitEntry/$', 'submitEntry'),
    url(r'^searchResults/$', 'submitSearch'),
    url(r'^categories/$', 'categoryIndex'),
    url(r'^categories/newCategory/$', 'newCategory'),
    url(r'^categories/categoryEntries/(?P<categoryName>\S+)/$', 'categoryEntries'),
)
