from django.contrib import admin

from .models import RawListing


@admin.register(RawListing)
class RawListingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'source', 'fetched_at', 'extracted_at', 'skip_reason']
    list_filter = ['source', ('extracted_at', admin.EmptyFieldListFilter)]
    search_fields = ['raw_title', 'url']
