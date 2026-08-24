"""Domain model validation."""

from datetime import date

import pytest
from pydantic import ValidationError

from learnlog.models import Achievement, LearningEntry, Resource, Visibility


def test_resource_requires_provider_type_title() -> None:
    with pytest.raises(ValidationError):
        Resource(provider="", type="article", title="x")


def test_entry_supports_multiple_resources() -> None:
    entry = LearningEntry(
        id="2026-08-24-kubernetes-services",
        title="Kubernetes Services",
        date=date(2026, 8, 24),
        visibility=Visibility.PRIVATE,
        summary="ClusterIP, NodePort, LoadBalancer",
        topics=["kubernetes", "networking"],
        resources=[
            Resource(provider="IBM", type="article", title="Kubernetes Networking"),
            Resource(provider="OpenAI", type="ai_conversation", title="kube-proxy"),
            Resource(provider="AWS", type="documentation", title="EKS Networking"),
        ],
    )
    assert len(entry.resources) == 3
    assert entry.filename_slug == "kubernetes-services"


def test_visibility_rejects_unknown_values() -> None:
    with pytest.raises(ValidationError):
        LearningEntry(
            id="x",
            title="x",
            date=date(2026, 1, 1),
            visibility="secret",  # type: ignore[arg-type]
            summary="x",
        )


def test_achievement_public_portfolio_item() -> None:
    item = Achievement(
        id="aws-certified-cloud-practitioner",
        title="AWS Certified Cloud Practitioner",
        provider="AWS",
        date_earned=date(2026, 8, 1),
        visibility=Visibility.PUBLIC,
    )
    assert item.visibility is Visibility.PUBLIC
