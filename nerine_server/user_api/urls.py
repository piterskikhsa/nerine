from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import FilterView

urlpatterns = [
   url(r'api-token-auth/', obtain_jwt_token),
   url(r'personrank/', FilterView.as_view())
]

#Для теста:
#curl -X POST -d "username=test2&password=Dragonage" http://127.0.0.1:8000/api/login/
#curl -H "Authorization: JWT <token>" http://127.0.0.1:8000/personrank/