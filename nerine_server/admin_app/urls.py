from django.conf.urls import url
from .views import (show_tepmlate_main,
                    show_tepmlate_admins,
                    show_tepmlate_users,
                    show_tepmlate_sites,
                    show_tepmlate_persons,
                    show_tepmlate_keywords,
                    login, logout)


urlpatterns = [
    url(r'^$', show_tepmlate_main, name='main'),
    url(r'^admins/', show_tepmlate_admins, name='admins'),
    url(r'^users/', show_tepmlate_users, name='users'),
    url(r'^sites/', show_tepmlate_sites, name='sites'),
    url(r'^persons/', show_tepmlate_persons, name='persons'),
    url(r'^keywords/', show_tepmlate_keywords, name='keywords'),
]

urlpatterns += [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout')
]