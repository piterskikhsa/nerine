from django.conf.urls import url
from user_api import views

urlpatterns = [
    url(r'^rank/(?P<data>(\d{4}-\d{2}-\d{2}))/$', views.rank_detail),
    url(r'^rank/$', views.ranks_list)
]