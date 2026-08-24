"""Shared enumerations. Provider and resource type stay open strings."""

from enum import StrEnum


class Visibility(StrEnum):
    """Whether a record may appear on a future public portfolio."""

    PRIVATE = "private"
    PUBLIC = "public"


class EntryStatus(StrEnum):
    """Lifecycle of a captured learning session."""

    CAPTURED = "captured"
    REVIEWED = "reviewed"
    ARCHIVED = "archived"


class AchievementStatus(StrEnum):
    """Lifecycle of a credential or badge."""

    EARNED = "earned"
    IN_PROGRESS = "in_progress"
    EXPIRED = "expired"
