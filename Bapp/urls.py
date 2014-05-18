from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Bapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/login/$',  'Bapp.views.login'),
    url(r'^accounts/auth/$',  'Bapp.views.auth_view'),
    url(r'^accounts/logout/$', 'Bapp.views.logout'),
    url(r'^accounts/loggedin/$', 'Bapp.views.loggedin'),
    url(r'^accounts/invalid/$', 'Bapp.views.invalid_login'),
    url(r'^accounts/register/$', 'Bapp.views.register_user'),
    url(r'^accounts/register_success/$', 'Bapp.views.register_success'),
)
