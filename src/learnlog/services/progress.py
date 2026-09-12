"""GitHub-visible progress page from public records only."""

from __future__ import annotations

from pathlib import Path

from learnlog.models import Achievement, LearningEntry, Visibility
from learnlog.services.storage import achievement_path, entry_path
from learnlog.settings import Settings


def public_entries(entries: list[LearningEntry]) -> list[LearningEntry]:
    return [item for item in entries if item.visibility is Visibility.PUBLIC]


def public_achievements(items: list[Achievement]) -> list[Achievement]:
    return [item for item in items if item.visibility is Visibility.PUBLIC]


def render_progress_markdown(
    settings: Settings,
    entries: list[LearningEntry],
    achievements: list[Achievement],
) -> str:
    shown = public_entries(entries)
    creds = public_achievements(achievements)
    lines = [
        "# Learning progress",
        "",
        "Public learning captured in this repository.",
        "Private sessions stay in Git and are **not** listed here.",
        "",
        f"- Public sessions: **{len(shown)}**",
        f"- Public achievements: **{len(creds)}**",
        "",
        "## Timeline",
        "",
    ]
    if not shown:
        lines.extend(
            [
                "_No public sessions yet. Capture with "
                "`learnlog add --visibility public`._",
                "",
            ]
        )
    else:
        lines.extend(["| Date | Topics | Title |", "| --- | --- | --- |"])
        for entry in shown:
            rel = entry_path(settings, entry).as_posix()
            try:
                href = entry_path(settings, entry).relative_to(settings.root).as_posix()
            except ValueError:
                href = rel
            topics = ", ".join(entry.topics) if entry.topics else "—"
            title = f"[{entry.title}]({href})"
            lines.append(f"| {entry.date.isoformat()} | {topics} | {title} |")
        lines.append("")

    lines.extend(["## Achievements", ""])
    if not creds:
        lines.extend(
            [
                "_No public achievements yet. "
                "`learnlog achievement add --visibility public`._",
                "",
            ]
        )
    else:
        lines.extend(["| Date | Provider | Title |", "| --- | --- | --- |"])
        for item in creds:
            try:
                href = (
                    achievement_path(settings, item)
                    .relative_to(settings.root)
                    .as_posix()
                )
            except ValueError:
                href = achievement_path(settings, item).as_posix()
            title = f"[{item.title}]({href})"
            extra = ""
            if item.credential_url:
                extra = f" ([credential]({item.credential_url}))"
            lines.append(
                f"| {item.date_earned.isoformat()} | {item.provider} | {title}{extra} |"
            )
        lines.append("")

    topic_counts: dict[str, int] = {}
    for entry in shown:
        for topic in entry.topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
    lines.extend(["## Topics", ""])
    if not topic_counts:
        lines.append("_Topics appear when public sessions include `--topic`._")
        lines.append("")
    else:
        for name, count in sorted(
            topic_counts.items(),
            key=lambda pair: (-pair[1], pair[0]),
        ):
            lines.append(f"- **{name}**: {count} session(s)")
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "Regenerate this file with `learnlog publish`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_progress_markdown(
    settings: Settings,
    entries: list[LearningEntry],
    achievements: list[Achievement],
) -> Path:
    path = settings.root / "PROGRESS.md"
    path.write_text(
        render_progress_markdown(settings, entries, achievements),
        encoding="utf-8",
    )
    return path
