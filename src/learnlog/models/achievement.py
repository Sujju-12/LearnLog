"""A credential, badge, or certificate."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from learnlog.models.enums import AchievementStatus, Visibility


class Achievement(BaseModel):
    """Something earned while learning (cert, badge, course completion)."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    date_earned: date
    visibility: Visibility = Visibility.PRIVATE
    credential_url: str = ""
    skills: list[str] = Field(default_factory=list)
    related_topics: list[str] = Field(default_factory=list)
    badge_image: str = ""
    certificate_file: str = ""
    status: AchievementStatus = AchievementStatus.EARNED
    notes: str = ""

    @field_validator("id", "title", "provider")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value.strip()

    @field_validator("skills", "related_topics", mode="before")
    @classmethod
    def split_csv(cls, value: object) -> object:
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        return value
