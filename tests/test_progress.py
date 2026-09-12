"""Public PROGRESS.md used on GitHub."""

from datetime import date
from pathlib import Path

from learnlog.models import Visibility
from learnlog.services.processor import capture_entry
from learnlog.services.progress import render_progress_markdown
from learnlog.services.storage import load_all_achievements, load_all_entries
from learnlog.settings import Settings


def test_progress_lists_only_public_entries(tmp_path: Path) -> None:
    settings = Settings(root=tmp_path)
    capture_entry(
        settings,
        title="Private lab notes",
        summary="Scratch notes",
        learned_on=date(2026, 8, 1),
        visibility=Visibility.PRIVATE,
        topics=["linux"],
    )
    capture_entry(
        settings,
        title="Linux Foundation: users and permissions",
        summary="chmod, chown, and umask from LFS101.",
        learned_on=date(2026, 8, 2),
        visibility=Visibility.PUBLIC,
        topics=["linux"],
    )
    page = render_progress_markdown(
        settings,
        load_all_entries(settings),
        load_all_achievements(settings),
    )
    assert "Linux Foundation: users and permissions" in page
    assert "Private lab notes" not in page
    assert "data/entries/2026/08/02/" in page
