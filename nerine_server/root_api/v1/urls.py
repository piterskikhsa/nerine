from django.conf.urls import url, include

urlpatterns = [
    url(r'^persons/', include('root_api.v1.persons.urls')),
    url(r'^sites/', include('root_api.v1.sites.urls', namespace='sites')),
]
