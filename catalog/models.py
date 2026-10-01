from datetime import timedelta

from django.db import models
from django.utils import timezone

DEFAULT_LIFETIME = timedelta(days=30)


class Source(models.Model):
    class Tier(models.TextChoices):
        A = 'A', 'A — primária'
        B = 'B', 'B — quadro curado'
        C = 'C', 'C — agregador aberto'
        SIGNAL = 'signal', 'Sinal'

    class Method(models.TextChoices):
        RSS = 'rss', 'RSS'
        SITEMAP = 'sitemap', 'Sitemap'
        HTML = 'html', 'HTML'
        API = 'api', 'API'

    slug = models.SlugField('identificador', unique=True)
    name = models.CharField('nome', max_length=200, unique=True)
    url = models.URLField('endereço', max_length=500)
    tier = models.CharField('nível de confiança', max_length=10, choices=Tier)
    method = models.CharField('método de recolha', max_length=10, choices=Method)
    active = models.BooleanField('ativa', default=True)

    class Meta:
        verbose_name = 'fonte'
        verbose_name_plural = 'fontes'
        ordering = ['name']

    def __str__(self):
        return self.name


class Organisation(models.Model):
    name = models.CharField('nome', max_length=200, unique=True)
    website = models.URLField('sítio web', max_length=500, blank=True)
    validated = models.BooleanField(
        'validada',
        default=False,
        help_text='Tem atividade conhecida nos últimos dois anos (por exemplo, um apoio da DGArtes).',
    )

    class Meta:
        verbose_name = 'organização'
        verbose_name_plural = 'organizações'
        ordering = ['name']

    def __str__(self):
        return self.name


class Action(models.Model):
    class Kind(models.TextChoices):
        CASTING = 'casting', 'Casting'
        AUDITION = 'audition', 'Audição'
        TRAINING = 'training', 'Formação'
        GRANT = 'grant', 'Apoio'
        SIGNAL = 'signal', 'No radar'

    class Pillar(models.TextChoices):
        THEATRE = 'theatre', 'Teatro'
        CINEMA = 'cinema', 'Cinema'
        TV = 'tv', 'Televisão'
        MARKETING = 'marketing', 'Publicidade'
        DUBBING = 'dubbing', 'Dobragem'

    class Region(models.TextChoices):
        NORTH = 'north', 'Norte'
        CENTRE = 'centre', 'Centro'
        SOUTH = 'south', 'Sul'
        ISLANDS = 'islands', 'Ilhas'
        NATIONAL = 'national', 'Nacional'

    class Gender(models.TextChoices):
        ANY = 'any', 'Qualquer'
        FEMALE = 'female', 'Feminino'
        MALE = 'male', 'Masculino'
        OTHER = 'other', 'Outro'

    class Pay(models.TextChoices):
        PAID = 'paid', 'Pago'
        UNPAID = 'unpaid', 'Não pago'
        EXPENSES = 'expenses', 'Só despesas'
        UNKNOWN = 'unknown', 'Desconhecido'

    class Format(models.TextChoices):
        IN_PERSON = 'in_person', 'Presencial'
        ONLINE = 'online', 'Online'

    class Status(models.TextChoices):
        PENDING_REVIEW = 'pending_review', 'Por rever'
        APPROVED = 'approved', 'Aprovada'
        REJECTED = 'rejected', 'Rejeitada'
        EXPIRED = 'expired', 'Expirada'
        WITHDRAWN = 'withdrawn', 'Retirada'

    kind = models.CharField('tipo', max_length=20, choices=Kind)
    pillar = models.CharField('pilar', max_length=20, choices=Pillar)
    title = models.CharField('título', max_length=300)
    summary = models.TextField('resumo', blank=True)

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='actions',
        verbose_name='organização',
        help_text='Quem publica a oportunidade. Obrigatória para aprovar.',
    )
    location = models.CharField('local', max_length=200, blank=True)
    region = models.CharField('região', max_length=20, choices=Region)
    remote = models.BooleanField('à distância', default=False, help_text='Self-tape ou online.')
    age_min = models.PositiveSmallIntegerField('idade mínima', null=True, blank=True)
    age_max = models.PositiveSmallIntegerField('idade máxima', null=True, blank=True)
    gender = models.CharField('género', max_length=10, choices=Gender, blank=True)
    languages = models.CharField('línguas', max_length=200, blank=True)

    pay = models.CharField('remuneração', max_length=10, choices=Pay, default=Pay.UNKNOWN)
    fee_text = models.CharField('detalhe da remuneração', max_length=200, blank=True)
    price_eur = models.DecimalField(
        'preço (€)',
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Só para formação. 0 significa gratuita.',
    )
    format = models.CharField('formato', max_length=10, choices=Format, blank=True)

    published_at = models.DateTimeField('publicada em', null=True, blank=True)
    first_seen_at = models.DateTimeField('vista pela primeira vez em', default=timezone.now)
    deadline_at = models.DateTimeField('prazo', null=True, blank=True)
    event_start = models.DateTimeField('início', null=True, blank=True)
    event_end = models.DateTimeField('fim', null=True, blank=True)
    always_open = models.BooleanField('candidatura permanente', default=False)
    expires_at_override = models.DateTimeField(
        'expira em (manual)',
        null=True,
        blank=True,
        help_text='Substitui a data de expiração calculada.',
    )
    expires_at = models.DateTimeField('expira em', null=True, editable=False, db_index=True)

    source = models.ForeignKey(
        Source, on_delete=models.PROTECT, related_name='actions', verbose_name='fonte'
    )
    source_url = models.URLField('ligação original', max_length=500)
    fingerprint = models.CharField('impressão digital', max_length=64, blank=True, db_index=True)
    last_seen_at = models.DateTimeField('vista pela última vez em', null=True, blank=True)
    status = models.CharField(
        'estado', max_length=20, choices=Status, default=Status.PENDING_REVIEW, db_index=True
    )

    class Meta:
        verbose_name = 'ação'
        verbose_name_plural = 'ações'
        ordering = ['expires_at']
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(status='approved') | models.Q(organisation__isnull=False),
                name='approved_action_has_poster',
                violation_error_message='Uma ação aprovada tem de indicar quem a publica.',
            ),
        ]

    def __str__(self):
        return self.title

    def compute_expires_at(self):
        if self.expires_at_override:
            return self.expires_at_override
        if self.deadline_at:
            return self.deadline_at
        if self.always_open:
            return None
        if self.event_start:
            return self.event_start
        return (self.published_at or self.first_seen_at) + DEFAULT_LIFETIME

    def save(self, *args, **kwargs):
        self.expires_at = self.compute_expires_at()
        if kwargs.get('update_fields') is not None:
            kwargs['update_fields'] = {*kwargs['update_fields'], 'expires_at'}
        super().save(*args, **kwargs)
