"""Application services (storage, generation, indexing)."""

from learnlog.services.index import build_stats, write_generated_index
from learnlog.services.processor import (
    capture_achievement,
    capture_entry,
    search_entries,
)
from learnlog.services.progress import write_progress_markdown
from learnlog.services.storage import (
    load_all_achievements,
    load_all_entries,
    save_entry,
)

__all__ = [
    "build_stats",
    "capture_achievement",
    "capture_entry",
    "load_all_achievements",
    "load_all_entries",
    "save_entry",
    "search_entries",
    "write_generated_index",
    "write_progress_markdown",
]
