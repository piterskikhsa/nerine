from django.contrib import admin
from .models import Page, PersonPageRank, Person, Site, KeyWord


admin.site.register(Page)
admin.site.register(Person)
admin.site.register(PersonPageRank)
admin.site.register(Site)
admin.site.register(KeyWord)

