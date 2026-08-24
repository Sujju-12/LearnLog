"""Build topic / provider indexes and counts as JSON."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from learnlog.models import Achievement, LearningEntry
from learnlog.services.storage import load_all_achievements, load_all_entries
from learnlog.settings import Settings


def build_stats(
    entries: list[LearningEntry],
    achievements: list[Achievement],
) -> dict[str, object]:
    topics: Counter[str] = Counter()
    skills: Counter[str] = Counter()
    providers: Counter[str] = Counter()
    visibility: Counter[str] = Counter()

    for entry in entries:
        visibility[entry.visibility.value] += 1
        topics.update(entry.topics)
        skills.update(entry.skills)
        providers.update(resource.provider for resource in entry.resources)

    for achievement in achievements:
        visibility[f"achievement:{achievement.visibility.value}"] += 1
        topics.update(achievement.related_topics)
        skills.update(achievement.skills)
        providers.update([achievement.provider])

    return {
        "entry_count": len(entries),
        "achievement_count": len(achievements),
        "topics": dict(topics.most_common()),
        "skills": dict(skills.most_common()),
        "providers": dict(providers.most_common()),
        "visibility": dict(visibility),
        "entries": [
            {
                "id": entry.id,
                "title": entry.title,
                "date": entry.date.isoformat(),
                "visibility": entry.visibility.value,
                "topics": entry.topics,
            }
            for entry in entries
        ],
        "achievements": [
            {
                "id": item.id,
                "title": item.title,
                "provider": item.provider,
                "date_earned": item.date_earned.isoformat(),
                "visibility": item.visibility.value,
            }
            for item in achievements
        ],
    }


def write_generated_index(settings: Settings) -> Path:
    entries = load_all_entries(settings)
    achievements = load_all_achievements(settings)
    payload = build_stats(entries, achievements)
    settings.generated_path.mkdir(parents=True, exist_ok=True)
    path = settings.generated_path / "index.json"
    serialized = json.dumps(payload, indent=2, sort_keys=False) + "\n"
    path.write_text(serialized, encoding="utf-8")
    return path
