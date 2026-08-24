"""Accept structured input, validate, and persist learning records."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from learnlog.models import Achievement, LearningEntry, Resource, Visibility
from learnlog.services import storage
from learnlog.settings import Settings
from learnlog.utils.dates import parse_date
from learnlog.utils.slugs import slugify


def parse_resource_spec(spec: str) -> Resource:
    """Parse ``provider|type|title|url`` (url optional)."""
    parts = [part.strip() for part in spec.split("|")]
    if len(parts) < 3:
        raise ValueError(
            "resource must be provider|type|title or provider|type|title|url"
        )
    url = parts[3] if len(parts) > 3 else ""
    return Resource(provider=parts[0], type=parts[1], title=parts[2], url=url)


def capture_entry(
    settings: Settings,
    *,
    title: str,
    summary: str,
    learned_on: date | str | None = None,
    visibility: str | Visibility | None = None,
    topics: list[str] | None = None,
    skills: list[str] | None = None,
    learning_type: list[str] | None = None,
    resources: list[Resource] | None = None,
    tags: list[str] | None = None,
    understanding: str = "",
    key_concepts: list[str] | None = None,
    hands_on_work: str = "",
    knowledge_gaps: str = "",
    next_steps: str = "",
    body: str = "",
    entry_id: str | None = None,
) -> tuple[LearningEntry, Path]:
    """Validate a learning session and write it under data/entries/YYYY/MM/DD/."""
    day = parse_date(learned_on) if learned_on else date.today()
    vis = (
        Visibility(visibility)
        if visibility is not None
        else settings.default_visibility
    )
    ident = entry_id or LearningEntry.build_id(day, title)
    entry = LearningEntry(
        id=ident,
        title=title,
        date=day,
        visibility=vis,
        summary=summary,
        topics=topics or [],
        skills=skills or [],
        learning_type=learning_type or [],
        resources=resources or [],
        tags=tags or [],
        understanding=understanding,
        key_concepts=key_concepts or [],
        hands_on_work=hands_on_work,
        knowledge_gaps=knowledge_gaps,
        next_steps=next_steps,
        body=body,
    )
    path = storage.save_entry(settings, entry)
    return entry, path


def capture_achievement(
    settings: Settings,
    *,
    title: str,
    provider: str,
    date_earned: date | str,
    visibility: str | Visibility | None = None,
    achievement_id: str | None = None,
    credential_url: str = "",
    skills: list[str] | None = None,
    related_topics: list[str] | None = None,
    notes: str = "",
) -> tuple[Achievement, Path]:
    ident = achievement_id or slugify(title)
    vis = (
        Visibility(visibility)
        if visibility is not None
        else settings.default_visibility
    )
    achievement = Achievement(
        id=ident,
        title=title,
        provider=provider,
        date_earned=parse_date(date_earned),
        visibility=vis,
        credential_url=credential_url,
        skills=skills or [],
        related_topics=related_topics or [],
        notes=notes,
    )
    path = storage.save_achievement(settings, achievement)
    return achievement, path


def search_entries(entries: list[LearningEntry], query: str) -> list[LearningEntry]:
    needle = query.lower().strip()
    if not needle:
        return entries
    matches: list[LearningEntry] = []
    for entry in entries:
        haystack = " ".join(
            [
                entry.id,
                entry.title,
                entry.summary,
                entry.understanding,
                entry.body,
                " ".join(entry.topics),
                " ".join(entry.skills),
                " ".join(entry.tags),
                " ".join(item.title for item in entry.resources),
                " ".join(item.provider for item in entry.resources),
            ]
        ).lower()
        if needle in haystack:
            matches.append(entry)
    return matches
