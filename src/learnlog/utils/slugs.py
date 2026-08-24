"""URL-safe slugs for filenames and ids."""

import re
import unicodedata


def slugify(value: str, *, max_length: int = 80) -> str:
    """Turn a title into a lowercase hyphenated slug."""
    normalized = unicodedata.normalize("NFKD", value)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_only.lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    if not cleaned:
        cleaned = "entry"
    return cleaned[:max_length].strip("-")
