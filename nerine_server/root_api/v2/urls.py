from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^persons/', include('root_api.v2.persons.urls')),
    url(r'^sites/', include('root_api.v2.sites.urls')),
    url(r'^persons/(?P<person_id>\d+)/keywords/', include('root_api.v2.keywords.urls')),
    url(r'^api-auth/', obtain_auth_token),
]
