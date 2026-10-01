from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from jinja2 import Environment, FileSystemLoader, select_autoescape
from premailer import transform

from catalog.models import Action

from .models import Digest
from .schedule import LISBON
from .selection import PILLAR_SECTIONS, Section

TEMPLATES = Path(__file__).parent / 'email'
OUTPUT_DIR = settings.DATA_DIR / 'digests'
LOGO = settings.BASE_DIR / 'design' / 'logo' / 'logo-120.png'
LOGO_CID = 'logo'
MONTHS = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
COLOURS = {
    Section.CLOSING_SOON: '#D9480F',
    Section.THEATRE: '#C2255C',
    Section.CINEMA: '#3B5BDB',
    Section.TV: '#7048E8',
    Section.MARKETING: '#E67700',
    Section.DUBBING: '#0C8599',
    Section.TRAINING: '#2B8A3E',
    Section.GRANTS: '#5F3DC4',
    Section.RADAR: '#495057',
    Section.ALWAYS_OPEN: '#495057',
}
PILLAR_COLOURS = {pillar.value: COLOURS[Section(pillar.value)] for pillar in Action.Pillar}
PAY_LABELS = {
    Action.Pay.PAID: 'Pago',
    Action.Pay.UNPAID: 'Não pago',
    Action.Pay.EXPENSES: 'Só despesas',
}

NAME = 'relATOR'
# The email reads as three blocks: what closes this week, then castings by pillar, then the rest.
# Each later block opens with a labelled band.
BLOCK_BANDS = {'pillars': 'Castings e audições', 'more': 'Formação e outras oportunidades'}


@dataclass
class Rendered:
    number: int
    subject: str
    html: str
    text: str


def render(selection):
    sent = Digest.objects.filter(scheduled_for=selection.send_at).values_list('number', flat=True).first()
    number = sent or (Digest.objects.order_by('-number').values_list('number', flat=True).first() or 0) + 1
    subject = f'{NAME} #{number} · {_counts_line(selection)}'
    environment = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(['html']),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    environment.filters.update(short_date=short_date)
    context = {
        'name': NAME,
        'logo_src': f'cid:{LOGO_CID}',
        'number': number,
        'subject': subject,
        'date': long_date(selection.send_at),
        'counts': _counts_line(selection),
        'sections': _sections(selection),
        'colours': COLOURS,
        'pillar_colours': PILLAR_COLOURS,
        'facts': facts,
        'deadline_chip': lambda action: deadline_chip(action, selection.send_at),
    }
    html = transform(environment.get_template('issue.html').render(context), disable_validation=True)
    text = environment.get_template('issue.txt').render(context)
    return Rendered(number=number, subject=subject, html=html, text=text)


def write(rendered, send_at):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = OUTPUT_DIR / f'issue-{rendered.number}-{send_at.astimezone(LISBON).date().isoformat()}'
    html_path, text_path = stem.with_suffix('.html'), stem.with_suffix('.txt')
    # The email embeds the logo (cid:); a preview opened in a browser loads it from disk instead.
    html_path.write_text(rendered.html.replace(f'cid:{LOGO_CID}', LOGO.as_uri()), encoding='utf-8')
    text_path.write_text(rendered.text, encoding='utf-8')
    return html_path, text_path


def _sections(selection):
    sections = []
    for section in Section:
        items = selection.sections[section]
        if items or section in PILLAR_SECTIONS:
            # In a pillar section the heading already says the pillar, so items don't repeat it.
            is_pillar = section in PILLAR_SECTIONS
            block = 'urgent' if section == Section.CLOSING_SOON else 'pillars' if is_pillar else 'more'
            sections.append({
                'key': section.value, 'label': section.label, 'items': items,
                'is_pillar': is_pillar, 'block': block, 'band': None,
            })
    for previous, section in zip([None] + sections, sections):
        if previous is None or previous['block'] != section['block']:
            section['band'] = BLOCK_BANDS.get(section['block'])
    return sections


def _counts_line(selection):
    new = selection.new_count
    closing = selection.closing_count
    parts = [f'{new} nova ação' if new == 1 else f'{new} novas ações']
    if closing:
        parts.append(f'{closing} a fechar')
    return ', '.join(parts)


def facts(action):
    parts = []
    if action.location:
        parts.append(action.location)
    elif action.remote:
        parts.append('À distância')
    if action.kind == Action.Kind.TRAINING:
        if action.price_eur is not None:
            parts.append('Gratuito' if action.price_eur == 0 else f'{action.price_eur.normalize():f} €')
    elif action.fee_text:
        parts.append(action.fee_text)
    elif action.pay in PAY_LABELS:
        parts.append(PAY_LABELS[action.pay])
    if action.age_min and action.age_max:
        parts.append(f'{action.age_min}–{action.age_max} anos')
    elif action.age_min:
        parts.append(f'+{action.age_min} anos')
    return ' · '.join(parts)


def deadline_chip(action, send_at):
    if action.always_open:
        return ''
    today = send_at.astimezone(LISBON).date()
    if action.deadline_at:
        day = action.deadline_at.astimezone(LISBON).date()
        days = (day - today).days
        if days <= 1:
            return 'Fecha amanhã' if days == 1 else 'Fecha hoje'
        if days <= 7:
            return f'Fecha em {days} dias'
        return f'Candidaturas até {short_date(action.deadline_at)}'
    if action.event_start:
        return f'Começa a {short_date(action.event_start)}'
    return ''


def short_date(value):
    local = value.astimezone(LISBON)
    return f'{local.day} {MONTHS[local.month - 1]}'


def long_date(value):
    local = value.astimezone(LISBON)
    return f'{local.day} {MONTHS[local.month - 1]} {local.year}'
