from django.contrib import admin

from .models import RawListing


@admin.register(RawListing)
class RawListingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'source', 'fetched_at', 'extracted_at']
    list_filter = ['source']
    search_fields = ['raw_title', 'url']
