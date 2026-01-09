from django.contrib import admin
from .models import Site, Typologie, Denomination, DateReference

admin.site.register(Site)
admin.site.register(Typologie)
admin.site.register(Denomination)
admin.site.register(DateReference)
