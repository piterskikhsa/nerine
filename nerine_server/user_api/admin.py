
from django.contrib import admin
from .models import Pages, PersonPageRank, Persons, Sites, Keywords

admin.site.register(Pages)
admin.site.register(Persons)
admin.site.register(PersonPageRank)
admin.site.register(Sites)
admin.site.register(Keywords)
# Register your models here.
