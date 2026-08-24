"""A single learning source used during a session."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Resource(BaseModel):
    """One article, course, lab, repo, or conversation.

    ``provider`` and ``type`` are unconstrained strings so new sources
    (IBM, OpenAI, YouTube, a personal lab, …) do not require a code change.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    provider: str = Field(min_length=1)
    type: str = Field(min_length=1)
    title: str = Field(min_length=1)
    url: str = ""
    notes: str = ""
    author: str | None = None
    accessed_date: date | None = None

    @field_validator("provider", "type", "title")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value.strip()
