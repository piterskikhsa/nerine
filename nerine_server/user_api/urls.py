from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import (
    SitesPeriodViewer,
    SitesPersonViewer,
    SitesViewer,
    UserUpdatePassword
)

urlpatterns = [
    url(r'api-token-auth/', obtain_jwt_token),
    url(r'personrank/', SitesPersonViewer.as_view()),
    url(r'sites/$', SitesViewer.as_view()),
    url(r'user_pass/(?P<username>\w+)/$', UserUpdatePassword.as_view()),
    url(r'period/', SitesPeriodViewer.as_view()),
]

#Для теста:
#curl -X POST -d "username=test2&password=Dragonage" http://127.0.0.1:8000/api/login/
#curl -H "Authorization: JWT <token>" http://127.0.0.1:8000/personrank/