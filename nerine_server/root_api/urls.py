from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1.0/', include('root_api.v1.urls')),
    url(r'^v2.0/', include('root_api.v2.urls')),
]
