from django.db import models
from django.utils import timezone

from catalog.models import Source


class RawListing(models.Model):
    source = models.ForeignKey(
        Source, on_delete=models.PROTECT, related_name='raw_listings', verbose_name='fonte'
    )
    url = models.URLField('endereço', max_length=500)
    raw_title = models.CharField('título original', max_length=500, blank=True)
    raw_text = models.TextField('texto original', blank=True)
    published_at = models.DateTimeField('publicado em', null=True, blank=True)
    fetched_at = models.DateTimeField('recolhido em', default=timezone.now)
    extracted_at = models.DateTimeField('extraído em', null=True, blank=True)
    skip_reason = models.CharField('motivo de exclusão', max_length=200, blank=True)

    class Meta:
        verbose_name = 'anúncio recolhido'
        verbose_name_plural = 'anúncios recolhidos'
        ordering = ['-fetched_at']
        constraints = [
            models.UniqueConstraint(fields=['source', 'url'], name='unique_raw_listing_per_source'),
        ]

    def __str__(self):
        return self.raw_title or self.url
