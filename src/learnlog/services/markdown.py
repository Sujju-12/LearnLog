"""Turn a LearningEntry into Markdown with YAML frontmatter."""

from __future__ import annotations

from datetime import date
from typing import Any

import yaml

from learnlog.models import Achievement, LearningEntry, Resource

SECTION_HEADINGS = (
    ("What I learned", "body"),
    ("Understanding", "understanding"),
    ("Key concepts", "key_concepts"),
    ("Hands-on work", "hands_on_work"),
    ("Knowledge gaps", "knowledge_gaps"),
    ("Next steps", "next_steps"),
)


def _stringify(value: Any) -> Any:
    if isinstance(value, date):
        return value.isoformat()
    if hasattr(value, "value"):
        return value.value
    return value


def _compact(data: dict[str, Any]) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}
    for key, value in data.items():
        if value in (None, "", [], {}):
            continue
        if isinstance(value, dict):
            nested = _compact(value)
            if nested:
                cleaned[key] = nested
        elif isinstance(value, list):
            items = []
            for item in value:
                if isinstance(item, dict):
                    compact_item = _compact(item)
                    if compact_item:
                        items.append(compact_item)
                elif item not in (None, ""):
                    items.append(_stringify(item))
            if items:
                cleaned[key] = items
        else:
            cleaned[key] = _stringify(value)
    return cleaned


def resource_to_dict(resource: Resource) -> dict[str, Any]:
    return _compact(resource.model_dump())


def entry_frontmatter(entry: LearningEntry) -> dict[str, Any]:
    payload = {
        "id": entry.id,
        "title": entry.title,
        "date": entry.date,
        "visibility": entry.visibility,
        "summary": entry.summary,
        "topics": entry.topics,
        "skills": entry.skills,
        "learning_type": entry.learning_type,
        "status": entry.status,
        "tags": entry.tags,
        "resources": [resource_to_dict(item) for item in entry.resources],
        "related_projects": entry.related_projects,
        "related_achievements": entry.related_achievements,
    }
    return _compact(payload)


def render_body(entry: LearningEntry) -> str:
    chunks: list[str] = [f"# {entry.title}", ""]
    if entry.body:
        chunks.extend(["## What I learned", "", entry.body.strip(), ""])
    elif entry.summary:
        chunks.extend(["## What I learned", "", entry.summary.strip(), ""])

    if entry.understanding:
        chunks.extend(["## Understanding", "", entry.understanding.strip(), ""])

    if entry.key_concepts:
        chunks.extend(["## Key concepts", ""])
        chunks.extend(f"- {item}" for item in entry.key_concepts)
        chunks.append("")

    if entry.hands_on_work:
        chunks.extend(["## Hands-on work", "", entry.hands_on_work.strip(), ""])

    if entry.knowledge_gaps:
        chunks.extend(["## Knowledge gaps", "", entry.knowledge_gaps.strip(), ""])

    if entry.next_steps:
        chunks.extend(["## Next steps", "", entry.next_steps.strip(), ""])

    return "\n".join(chunks).rstrip() + "\n"


def render_entry_markdown(entry: LearningEntry) -> str:
    frontmatter = yaml.safe_dump(
        entry_frontmatter(entry),
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).strip()
    return f"---\n{frontmatter}\n---\n\n{render_body(entry)}"


def render_achievement_yaml(achievement: Achievement) -> str:
    payload = _compact(achievement.model_dump())
    return yaml.safe_dump(
        payload,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    stripped = text.lstrip("\ufeff")
    if not stripped.startswith("---"):
        return {}, stripped
    rest = stripped[3:]
    end = rest.find("\n---")
    if end == -1:
        raise ValueError("unterminated YAML frontmatter")
    raw_yaml = rest[:end].strip("\n")
    body = rest[end + 4 :].lstrip("\n")
    data = yaml.safe_load(raw_yaml) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data, body


def parse_markdown_sections(body: str) -> dict[str, str | list[str]]:
    """Pull known ## sections out of the Markdown body."""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if line.startswith("# "):
            continue
        if current is not None:
            sections[current].append(line)

    result: dict[str, str | list[str]] = {}
    heading_to_field = {heading: field for heading, field in SECTION_HEADINGS}
    for heading, lines in sections.items():
        field = heading_to_field.get(heading)
        if not field:
            continue
        text = "\n".join(lines).strip()
        if field == "key_concepts":
            bullets = [
                line[2:].strip() for line in text.splitlines() if line.startswith("- ")
            ]
            result[field] = bullets
        else:
            result[field] = text
    return result
