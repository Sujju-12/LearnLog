"""A captured learning session."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from learnlog.models.enums import EntryStatus, Visibility
from learnlog.models.resource import Resource
from learnlog.utils.slugs import slugify


class LearningEntry(BaseModel):
    """What was learned, when, from which sources, and on which topics."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    date: date
    visibility: Visibility = Visibility.PRIVATE
    summary: str = Field(min_length=1)

    topics: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    learning_type: list[str] = Field(default_factory=list)
    status: EntryStatus = EntryStatus.CAPTURED
    resources: list[Resource] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    related_projects: list[str] = Field(default_factory=list)
    related_achievements: list[str] = Field(default_factory=list)

    understanding: str = ""
    key_concepts: list[str] = Field(default_factory=list)
    hands_on_work: str = ""
    knowledge_gaps: str = ""
    next_steps: str = ""
    body: str = ""

    @field_validator("id", "title", "summary")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value.strip()

    @field_validator(
        "topics",
        "skills",
        "learning_type",
        "tags",
        "related_projects",
        "related_achievements",
        "key_concepts",
        mode="before",
    )
    @classmethod
    def split_csv(cls, value: object) -> object:
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        return value

    @property
    def filename_slug(self) -> str:
        """Path slug without the date prefix (the directory already has the date)."""
        prefix = f"{self.date.isoformat()}-"
        if self.id.startswith(prefix):
            remainder = self.id[len(prefix) :]
            return remainder or slugify(self.title)
        return slugify(self.id)

    @classmethod
    def build_id(cls, learned_on: date, title: str) -> str:
        return f"{learned_on.isoformat()}-{slugify(title)}"
