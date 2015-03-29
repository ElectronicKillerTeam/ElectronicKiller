"""
Definition of urls for ElectronicKiller.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from source.forms import BootstrapAuthenticationForm
from source import controllers

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
    url(r'^online$','source.controllers.gaming.onlinePage'),
    url(r'^onlinesocket$','source.controllers.gaming.onlineSocket'),

    url(r'^getcards$','source.controllers.gaming.getCards'),
    url(r'^usecard','source.controllers.gaming.useCard'),

    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
