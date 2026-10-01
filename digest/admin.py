from django.contrib import admin

from .models import Digest, DigestItem


class DigestItemInline(admin.TabularInline):
    model = DigestItem
    extra = 0
    autocomplete_fields = ['action']


@admin.register(Digest)
class DigestAdmin(admin.ModelAdmin):
    list_display = ['number', 'subject', 'scheduled_for', 'sent_at']
    inlines = [DigestItemInline]
