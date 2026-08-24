"""Command-line capture tool. Thin adapter over services."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from learnlog.services.index import build_stats, write_generated_index
from learnlog.services.processor import (
    capture_achievement,
    capture_entry,
    parse_resource_spec,
    search_entries,
)
from learnlog.services.progress import write_progress_markdown
from learnlog.services.storage import load_all_achievements, load_all_entries
from learnlog.settings import Settings, find_repo_root


def _csv(values: list[str] | None) -> list[str]:
    if not values:
        return []
    parts: list[str] = []
    for value in values:
        parts.extend(item.strip() for item in value.split(",") if item.strip())
    return parts


def _settings(root: str | None) -> Settings:
    base = Path(root).resolve() if root else find_repo_root()
    return Settings.from_root(base)


def _refresh_derived(settings: Settings) -> Path:
    write_generated_index(settings)
    return write_progress_markdown(
        settings,
        load_all_entries(settings),
        load_all_achievements(settings),
    )


def _add_parser(sub: argparse._SubParsersAction) -> None:
    add = sub.add_parser("add", help="Capture a learning session as Markdown")
    add.add_argument("--title", required=True, help="Short title of what you learned")
    add.add_argument("--summary", required=True, help="One-paragraph description")
    add.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    add.add_argument(
        "--visibility",
        choices=("private", "public"),
        default=None,
        help="Defaults to config (usually private)",
    )
    add.add_argument(
        "--topic",
        action="append",
        default=[],
        help="Repeatable; or comma-separated",
    )
    add.add_argument("--skill", action="append", default=[], help="Repeatable skill")
    add.add_argument(
        "--type",
        dest="learning_type",
        action="append",
        default=[],
        help="How you learned: documentation, hands-on, course, …",
    )
    add.add_argument(
        "--resource",
        action="append",
        default=[],
        help="provider|type|title or provider|type|title|url (repeatable)",
    )
    add.add_argument("--tag", action="append", default=[], help="Free-form tag")
    add.add_argument("--understanding", default="", help="Your own explanation")
    add.add_argument("--concept", action="append", default=[], help="Key concept")
    add.add_argument("--hands-on", default="", dest="hands_on", help="Labs or practice")
    add.add_argument("--gaps", default="", help="Open questions")
    add.add_argument("--next", dest="next_steps", default="", help="Follow-up steps")
    add.set_defaults(handler=_cmd_add)


def _achievement_parser(sub: argparse._SubParsersAction) -> None:
    ach = sub.add_parser("achievement", help="Record a badge, cert, or completion")
    ach_sub = ach.add_subparsers(dest="achievement_command", required=True)
    add = ach_sub.add_parser("add", help="Add an achievement YAML file")
    add.add_argument("--title", required=True)
    add.add_argument("--provider", required=True)
    add.add_argument("--date", required=True, help="Date earned (YYYY-MM-DD)")
    add.add_argument("--visibility", choices=("private", "public"), default=None)
    add.add_argument("--url", default="", help="Credential URL")
    add.add_argument("--skill", action="append", default=[])
    add.add_argument("--topic", action="append", default=[])
    add.add_argument("--notes", default="")
    add.set_defaults(handler=_cmd_achievement_add)
    listed = ach_sub.add_parser("list", help="List achievements")
    listed.set_defaults(handler=_cmd_achievement_list)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="learnlog",
        description=(
            "Git-native personal learning diary. "
            "Capture topics, sources, and skills as Markdown."
        ),
    )
    parser.add_argument(
        "--root",
        default=None,
        help="LearnLog repository root (defaults to current or nearest data/entries)",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    _add_parser(sub)

    listed = sub.add_parser("list", help="List captured learning entries")
    listed.add_argument("--topic", default=None, help="Filter by topic")
    listed.set_defaults(handler=_cmd_list)

    show = sub.add_parser("show", help="Print one entry by id")
    show.add_argument("entry_id")
    show.set_defaults(handler=_cmd_show)

    search = sub.add_parser(
        "search",
        help="Search titles, topics, summaries, and sources",
    )
    search.add_argument("query")
    search.set_defaults(handler=_cmd_search)

    stats = sub.add_parser("stats", help="Show counts by topic, skill, and provider")
    stats.add_argument(
        "--write",
        action="store_true",
        help="Also write data/generated/index.json",
    )
    stats.set_defaults(handler=_cmd_stats)

    publish = sub.add_parser(
        "publish",
        help="Rewrite PROGRESS.md from public entries (GitHub-visible)",
    )
    publish.set_defaults(handler=_cmd_publish)
    _achievement_parser(sub)
    return parser


def _cmd_add(args: argparse.Namespace) -> int:
    settings = _settings(args.root)
    resources = [parse_resource_spec(spec) for spec in args.resource]
    entry, path = capture_entry(
        settings,
        title=args.title,
        summary=args.summary,
        learned_on=args.date,
        visibility=args.visibility,
        topics=_csv(args.topic),
        skills=_csv(args.skill),
        learning_type=_csv(args.learning_type),
        resources=resources,
        tags=_csv(args.tag),
        understanding=args.understanding,
        key_concepts=_csv(args.concept),
        hands_on_work=args.hands_on,
        knowledge_gaps=args.gaps,
        next_steps=args.next_steps,
    )
    _refresh_derived(settings)
    print(f"Captured {entry.id}")
    shown = (
        path.relative_to(settings.root) if path.is_relative_to(settings.root) else path
    )
    print(shown)
    return 0


def _cmd_list(args: argparse.Namespace) -> int:
    settings = _settings(args.root)
    entries = load_all_entries(settings)
    if args.topic:
        needle = args.topic.lower()
        entries = [
            entry
            for entry in entries
            if needle in [topic.lower() for topic in entry.topics]
        ]
    if not entries:
        print("No learning entries yet. Use: learnlog add --title ... --summary ...")
        return 0
    for entry in entries:
        topics = ",".join(entry.topics) if entry.topics else "-"
        vis = entry.visibility.value
        print(f"{entry.date}  {vis:7}  {entry.id}  [{topics}]  {entry.title}")
    return 0


def _cmd_show(args: argparse.Namespace) -> int:
    settings = _settings(args.root)
    entries = {item.id: item for item in load_all_entries(settings)}
    entry = entries.get(args.entry_id)
    if entry is None:
        print(f"Unknown entry: {args.entry_id}", file=sys.stderr)
        return 1
    print(f"{entry.title} ({entry.date}, {entry.visibility.value})")
    print(entry.summary)
    if entry.topics:
        print("topics:", ", ".join(entry.topics))
    if entry.skills:
        print("skills:", ", ".join(entry.skills))
    for resource in entry.resources:
        extra = f" {resource.url}" if resource.url else ""
        print(f"- {resource.provider} / {resource.type}: {resource.title}{extra}")
    return 0


def _cmd_search(args: argparse.Namespace) -> int:
    settings = _settings(args.root)
    matches = search_entries(load_all_entries(settings), args.query)
    if not matches:
        print("No matches.")
        return 0
    for entry in matches:
        print(f"{entry.date}  {entry.id}  {entry.title}")
    return 0


def _cmd_stats(args: argparse.Namespace) -> int:
    settings = _settings(args.root)
    payload = build_stats(load_all_entries(settings), load_all_achievements(settings))
    print(f"entries: {payload['entry_count']}")
    print(f"achievements: {payload['achievement_count']}")
    print("topics:")
    topics = payload["topics"]
    assert isinstance(topics, dict)
    if not topics:
        print("  (none yet)")
    for name, count in topics.items():
        print(f"  {name}: {count}")
    print("providers:")
    providers = payload["providers"]
    assert isinstance(providers, dict)
    if not providers:
        print("  (none yet)")
    for name, count in providers.items():
        print(f"  {name}: {count}")
    if args.write:
        path = write_generated_index(settings)
        print(f"wrote {path}")
    return 0


def _cmd_publish(args: argparse.Namespace) -> int:
    settings = _settings(args.root)
    path = _refresh_derived(settings)
    print(path)
    return 0


def _cmd_achievement_add(args: argparse.Namespace) -> int:
    settings = _settings(args.root)
    achievement, path = capture_achievement(
        settings,
        title=args.title,
        provider=args.provider,
        date_earned=args.date,
        visibility=args.visibility,
        credential_url=args.url,
        skills=_csv(args.skill),
        related_topics=_csv(args.topic),
        notes=args.notes,
    )
    _refresh_derived(settings)
    print(f"Recorded {achievement.id}")
    print(path)
    return 0


def _cmd_achievement_list(args: argparse.Namespace) -> int:
    settings = _settings(args.root)
    items = load_all_achievements(settings)
    if not items:
        print("No achievements yet.")
        return 0
    for item in items:
        vis = item.visibility.value
        print(f"{item.date_earned}  {vis:7}  {item.provider}  {item.title}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 2
    return int(handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
