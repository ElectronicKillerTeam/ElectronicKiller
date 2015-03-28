"""
Definition of urls for ElectronicKiller.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from source.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'source.views.home', name='home'),
    url(r'^chat$', 'source.views.chat'),
    url(r'^echo$', 'source.views.echo'),
    url(r'^echoindex$', 'source.views.echo_index'),
    url(r'^login$','source.views.login'),
    url(r'^getUserList','source.views.get_user_list'),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
