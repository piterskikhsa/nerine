"""nerine_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^administration/', admin.site.urls),
<<<<<<< HEAD
    url(r'^admin/', include('admin_app.urls')),
=======
    url(r'^', include('admin_app.urls')),
>>>>>>> d43379b329012fb820dac3a27079a96f58f5b778
    url(r'^api/', include('root_api.urls', namespace='root_api')),
    url(r'^api/user/', include('user_api.urls', namespace='user_api'))
]
