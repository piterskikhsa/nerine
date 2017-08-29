from django.conf.urls import url
from .views import (show_tepmlate_main,
                    show_tepmlate_admins,
                    show_tepmlate_users,
                    show_tepmlate_sites,
                    show_tepmlate_persons,
                    show_tepmlate_keywords,
                    users_registration,
                    admins_registration,
                    login, logout, delete_user, delete_admin,
                    delete_site, delete_person, delete_keyword)


urlpatterns = [
    url(r'^$', show_tepmlate_main, name='main'),
    url(r'^admins/$', show_tepmlate_admins, name='admins'),
    url(r'^users/$', show_tepmlate_users, name='users'),
    url(r'^sites/$', show_tepmlate_sites, name='sites'),
    url(r'^persons/$', show_tepmlate_persons, name='persons'),
    url(r'^keywords/$', show_tepmlate_keywords, name='keywords'),
]

urlpatterns += [
    url(r'^admins/registration/$', admins_registration, name='admins_registration'),
    url(r'^users/registration/$', users_registration, name='users_registration'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout')
]

urlpatterns += [
    url(r'^delete/admin/(\d+)$', delete_admin, name='delete_admin'),
    url(r'^delete/user/(\d+)$', delete_user, name='delete_user'),
    url(r'^delete/site/(\d+)$', delete_site, name='delete_site'),
    url(r'^delete/person/(\d+)$', delete_person, name='delete_person'),
    url(r'^delete/keyword/(\d+)$', delete_keyword, name='delete_keyword'),
]
