from django.contrib import admin
from domains.models import Domain


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'available')
    search_fields = ('name',)
    list_filter = ('available',)

admin.site.register(Domain, DomainAdmin )
