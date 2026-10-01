from django.db import models

from catalog.models import Action


class Digest(models.Model):
    number = models.PositiveIntegerField('número', unique=True)
    scheduled_for = models.DateTimeField('agendada para', unique=True)
    sent_at = models.DateTimeField('enviada em', null=True, blank=True)
    subject = models.CharField('assunto', max_length=200)

    class Meta:
        verbose_name = 'edição'
        verbose_name_plural = 'edições'
        ordering = ['-number']

    def __str__(self):
        return f'#{self.number}'


class DigestItem(models.Model):
    class Section(models.TextChoices):
        CLOSING_SOON = 'closing_soon', 'Últimos dias'
        THEATRE = 'theatre', 'Teatro'
        CINEMA = 'cinema', 'Cinema'
        TV = 'tv', 'Televisão'
        MARKETING = 'marketing', 'Publicidade'
        DUBBING = 'dubbing', 'Dobragem'
        TRAINING = 'training', 'Formação'
        GRANTS = 'grants', 'Apoios e oportunidades'
        RADAR = 'radar', 'No radar'
        ALWAYS_OPEN = 'always_open', 'Candidaturas permanentes'

    digest = models.ForeignKey(
        Digest, on_delete=models.CASCADE, related_name='items', verbose_name='edição'
    )
    action = models.ForeignKey(
        Action, on_delete=models.PROTECT, related_name='digest_items', verbose_name='ação'
    )
    section = models.CharField('secção', max_length=20, choices=Section)
    position = models.PositiveSmallIntegerField('posição')
    was_new = models.BooleanField('novidade', default=False)

    class Meta:
        verbose_name = 'item da edição'
        verbose_name_plural = 'itens da edição'
        ordering = ['digest', 'section', 'position']
        constraints = [
            models.UniqueConstraint(fields=['digest', 'action'], name='unique_action_per_digest'),
        ]

    def __str__(self):
        return f'{self.digest} · {self.action}'
