from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1.0/', include('root_api.v1.urls')),
]
