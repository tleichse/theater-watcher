from django.contrib import admin, messages
from django.db.models import Q

from digest.schedule import ELIGIBILITY_MARGIN, misses_next_issue, next_send_at

from .models import Action, Organisation, Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'tier', 'method', 'active']
    list_filter = ['tier', 'method', 'active']
    search_fields = ['name', 'url']


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'validated', 'website']
    list_filter = ['validated']
    search_fields = ['name']


class MissesNextIssueFilter(admin.SimpleListFilter):
    title = 'falha a próxima edição'
    parameter_name = 'misses_next_issue'

    def lookups(self, request, model_admin):
        return [('yes', 'Sim'), ('no', 'Não')]

    def queryset(self, request, queryset):
        cutoff = next_send_at() + ELIGIBILITY_MARGIN
        if self.value() == 'yes':
            return queryset.filter(expires_at__lte=cutoff)
        if self.value() == 'no':
            return queryset.filter(Q(expires_at__gt=cutoff) | Q(expires_at__isnull=True))
        return queryset


class HasPosterFilter(admin.SimpleListFilter):
    title = 'quem publica'
    parameter_name = 'has_poster'

    def lookups(self, request, model_admin):
        return [('no', 'Sem quem publica'), ('yes', 'Com quem publica')]

    def queryset(self, request, queryset):
        if self.value() == 'no':
            return queryset.filter(organisation__isnull=True)
        if self.value() == 'yes':
            return queryset.filter(organisation__isnull=False)
        return queryset


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'kind', 'pillar', 'region', 'organisation', 'source', 'status', 'expires_at',
        'misses_next_issue',
    ]
    list_filter = [
        'status', MissesNextIssueFilter, HasPosterFilter, 'pillar', 'kind', 'region', 'source', 'always_open',
    ]
    search_fields = ['title', 'summary', 'location', 'organisation__name']
    autocomplete_fields = ['organisation']
    readonly_fields = ['expires_at', 'fingerprint']
    date_hierarchy = 'expires_at'
    actions = ['approve', 'reject']
    fieldsets = [
        (None, {'fields': ['status', 'kind', 'pillar', 'title', 'summary']}),
        ('Quem e onde', {'fields': [
            'organisation', 'location', 'region', 'remote', 'age_min', 'age_max', 'gender',
            'languages',
        ]}),
        ('Remuneração e preço', {'fields': ['pay', 'fee_text', 'price_eur', 'format']}),
        ('Datas', {'fields': [
            'published_at', 'first_seen_at', 'deadline_at', 'event_start', 'event_end',
            'always_open', 'expires_at_override', 'expires_at',
        ]}),
        ('Origem', {'fields': ['source', 'source_url', 'fingerprint', 'last_seen_at']}),
    ]

    @admin.display(boolean=True, description='falha a próxima edição')
    def misses_next_issue(self, obj):
        return misses_next_issue(obj.expires_at)

    @admin.action(description='Aprovar as ações selecionadas')
    def approve(self, request, queryset):
        skipped = queryset.filter(organisation__isnull=True).count()
        queryset.filter(organisation__isnull=False).update(status=Action.Status.APPROVED)
        if skipped:
            self.message_user(
                request,
                f'{skipped} ação(ões) não aprovada(s): falta indicar quem a publica.',
                messages.WARNING,
            )

    @admin.action(description='Rejeitar as ações selecionadas')
    def reject(self, request, queryset):
        queryset.update(status=Action.Status.REJECTED)
