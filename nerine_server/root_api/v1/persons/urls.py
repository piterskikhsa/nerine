from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'', views.PersonViewSet, base_name='person')

urlpatterns = [

    url(r'', include(router.urls, namespace='persons')),
    url(r'^(?P<person_id>\d+)/keywords/', include('root_api.v1.persons.keywords.urls', namespace='keywords')),

]
