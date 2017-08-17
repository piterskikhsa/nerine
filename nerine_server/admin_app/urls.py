from django.conf.urls import url
from .views import (show_tepmlate_admin_auth,
                    show_tepmlate_admins,
                    show_tepmlate_users,
                    show_tepmlate_sites,
                    show_tepmlate_persons,
                    show_tepmlate_keywords)


urlpatterns = [
    url(r'^', show_tepmlate_admin_auth),
    url(r'^admins/', show_tepmlate_admins, name='admins'),
    url(r'^users/', show_tepmlate_users, name='users'),
    url(r'^sites/', show_tepmlate_sites, name='sites'),
    url(r'^persons/', show_tepmlate_persons, name='persons'),
    url(r'^keywords/', show_tepmlate_keywords, name='keywords'),
]