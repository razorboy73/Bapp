from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Bapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^main/', include('main.urls')),
)

if settings.DEBUG:
    urlpatterns+=patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
         'serve',
         {'document_root':settings.MEDIA_ROOT}),)
