"""User-configurable paths and defaults."""

from pathlib import Path

from pydantic import BaseModel, Field

from learnlog.models.enums import Visibility


class Settings(BaseModel):
    """Filesystem layout for a LearnLog repository."""

    root: Path = Field(default_factory=Path.cwd)
    data_root: str = "data"
    entries_dir: str = "data/entries"
    achievements_dir: str = "data/achievements"
    resources_dir: str = "data/resources"
    generated_dir: str = "data/generated"
    default_visibility: Visibility = Visibility.PRIVATE

    @property
    def entries_path(self) -> Path:
        return self.root / self.entries_dir

    @property
    def achievements_path(self) -> Path:
        return self.root / self.achievements_dir

    @property
    def resources_path(self) -> Path:
        return self.root / self.resources_dir

    @property
    def generated_path(self) -> Path:
        return self.root / self.generated_dir

    @classmethod
    def from_root(cls, root: Path) -> "Settings":
        """Load optional YAML config; otherwise use repository defaults."""
        root = root.resolve()
        config_path = root / "config" / "settings.yaml"
        if not config_path.exists():
            return cls(root=root)
        try:
            import yaml
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("PyYAML is required to load settings.yaml") from exc
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        block = raw.get("learnlog", raw)
        if not isinstance(block, dict):
            return cls(root=root)
        allowed = set(cls.model_fields)
        data = {key: block[key] for key in block if key in allowed and key != "root"}
        return cls(root=root, **data)


def find_repo_root(start: Path | None = None) -> Path:
    """Walk upward until a LearnLog data directory is found."""
    current = (start or Path.cwd()).resolve()
    for path in [current, *current.parents]:
        if (path / "data" / "entries").is_dir():
            return path
    return current
