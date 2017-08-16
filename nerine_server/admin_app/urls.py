from django.conf.urls import url
from .views import (show_tepmlate_sites,
                    show_tepmlate_persons,
                    show_tepmlate_keywords)


urlpatterns = [
    url(r'^sites/', show_tepmlate_sites, name='sites'),
    url(r'^persons/', show_tepmlate_persons, name='persons'),
    url(r'^keywords/', show_tepmlate_keywords, name='keywords'),
]