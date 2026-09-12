"""Load and save Markdown entries and achievement YAML files."""

from __future__ import annotations

from pathlib import Path

from learnlog.models import Achievement, LearningEntry
from learnlog.services.markdown import (
    parse_frontmatter,
    parse_markdown_sections,
    render_achievement_yaml,
    render_entry_markdown,
)
from learnlog.settings import Settings
from learnlog.utils.slugs import slugify


def entry_path(settings: Settings, entry: LearningEntry) -> Path:
    day = entry.date
    return (
        settings.entries_path
        / f"{day.year:04d}"
        / f"{day.month:02d}"
        / f"{day.day:02d}"
        / f"{entry.filename_slug}.md"
    )


def achievement_path(settings: Settings, achievement: Achievement) -> Path:
    return settings.achievements_path / f"{slugify(achievement.id)}.yaml"


def save_entry(settings: Settings, entry: LearningEntry) -> Path:
    path = entry_path(settings, entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_entry_markdown(entry), encoding="utf-8")
    return path


def load_entry(path: Path) -> LearningEntry:
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    sections = parse_markdown_sections(body)
    data = {**meta}
    for key, value in sections.items():
        if key not in data or not data[key]:
            data[key] = value
    return LearningEntry.model_validate(data)


def iter_entry_files(settings: Settings) -> list[Path]:
    if not settings.entries_path.exists():
        return []
    return sorted(
        path for path in settings.entries_path.rglob("*.md") if path.is_file()
    )


def load_all_entries(settings: Settings) -> list[LearningEntry]:
    entries = [load_entry(path) for path in iter_entry_files(settings)]
    return sorted(entries, key=lambda item: (item.date, item.id), reverse=True)


def save_achievement(settings: Settings, achievement: Achievement) -> Path:
    path = achievement_path(settings, achievement)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_achievement_yaml(achievement), encoding="utf-8")
    return path


def load_achievement(path: Path) -> Achievement:
    import yaml

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return Achievement.model_validate(raw)


def load_all_achievements(settings: Settings) -> list[Achievement]:
    if not settings.achievements_path.exists():
        return []
    files = sorted(
        path for path in settings.achievements_path.glob("*.yaml") if path.is_file()
    )
    achievements = [load_achievement(path) for path in files]
    return sorted(
        achievements,
        key=lambda item: (item.date_earned, item.id),
        reverse=True,
    )
