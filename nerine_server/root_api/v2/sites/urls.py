from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = format_suffix_patterns([
    url(r'^$', views.SiteListView.as_view(), name='sites-list'),
    url(r'^(?P<pk>\d+)$', views.SiteDetailView.as_view(), name='sites-detail'),

])


