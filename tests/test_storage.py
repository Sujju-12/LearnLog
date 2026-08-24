"""Markdown round-trip and date-based paths."""

from datetime import date
from pathlib import Path

from learnlog.models import LearningEntry, Resource, Visibility
from learnlog.services.markdown import parse_frontmatter, render_entry_markdown
from learnlog.services.processor import capture_entry
from learnlog.services.storage import load_entry
from learnlog.settings import Settings


def test_save_and_load_round_trip(tmp_path: Path) -> None:
    settings = Settings(root=tmp_path)
    entry, path = capture_entry(
        settings,
        title="Kubernetes Services",
        summary="How ClusterIP and NodePort work",
        learned_on=date(2026, 8, 24),
        topics=["kubernetes", "networking"],
        skills=["clusterip"],
        resources=[
            Resource(provider="IBM", type="article", title="Kubernetes Networking"),
            Resource(provider="OpenAI", type="ai_conversation", title="kube-proxy"),
        ],
        understanding="Services are API objects plus kube-proxy rules.",
        key_concepts=["ClusterIP", "NodePort"],
        hands_on_work="Created a ClusterIP Service locally.",
    )
    assert path == tmp_path / "data/entries/2026/08/24/kubernetes-services.md"
    loaded = load_entry(path)
    assert loaded.id == entry.id
    assert loaded.title == entry.title
    assert loaded.topics == ["kubernetes", "networking"]
    assert len(loaded.resources) == 2
    assert loaded.resources[0].provider == "IBM"
    assert "ClusterIP" in loaded.key_concepts
    assert loaded.visibility is Visibility.PRIVATE


def test_example_entry_parses() -> None:
    example = Path(__file__).resolve().parents[1] / "examples" / "learning-entry.md"
    meta, body = parse_frontmatter(example.read_text(encoding="utf-8"))
    assert meta["id"] == "2026-08-24-kubernetes-services"
    assert len(meta["resources"]) == 3
    assert "What I learned" in body


def test_rendered_markdown_has_frontmatter() -> None:
    entry = LearningEntry(
        id="2026-01-01-demo",
        title="Demo",
        date=date(2026, 1, 1),
        summary="A demo",
        topics=["demo"],
    )
    text = render_entry_markdown(entry)
    assert text.startswith("---\n")
    assert "title: Demo" in text
    assert "# Demo" in text
