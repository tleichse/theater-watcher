from dataclasses import dataclass, field
from datetime import timedelta

from catalog.models import Action

from .models import DigestItem
from .schedule import ELIGIBILITY_MARGIN

CLOSING_SOON_WINDOW = timedelta(days=7)
Section = DigestItem.Section
PILLAR_SECTIONS = [Section.THEATRE, Section.CINEMA, Section.TV, Section.MARKETING, Section.DUBBING]


@dataclass
class Item:
    action: Action
    is_new: bool


@dataclass
class Selection:
    send_at: object
    sections: dict = field(default_factory=lambda: {section: [] for section in Section})

    @property
    def new_count(self):
        return sum(item.is_new for items in self.sections.values() for item in items)

    @property
    def closing_count(self):
        return len(self.sections[Section.CLOSING_SOON])

    @property
    def total(self):
        return sum(len(items) for items in self.sections.values())


def select(send_at):
    selection = Selection(send_at)
    shared_before = set(
        DigestItem.objects.filter(digest__scheduled_for__lt=send_at).values_list('action_id', flat=True)
    )
    approved = Action.objects.filter(status=Action.Status.APPROVED).select_related('organisation', 'source')
    for action in approved:
        if action.expires_at is not None and action.expires_at <= send_at + ELIGIBILITY_MARGIN:
            continue
        section = section_for(action, send_at)
        selection.sections[section].append(Item(action, is_new=action.pk not in shared_before))
    for items in selection.sections.values():
        items.sort(key=lambda item: (not item.is_new, item.action.expires_at is None, item.action.expires_at))
    return selection


def section_for(action, send_at):
    if action.always_open:
        return Section.ALWAYS_OPEN
    if action.kind == Action.Kind.SIGNAL:
        return Section.RADAR
    if action.expires_at <= send_at + CLOSING_SOON_WINDOW:
        return Section.CLOSING_SOON
    if action.kind == Action.Kind.TRAINING:
        return Section.TRAINING
    if action.kind == Action.Kind.GRANT:
        return Section.GRANTS
    return Section(action.pillar)
