"""Smoke tests for the installable package."""

from learnlog import __version__


def test_version_is_semver_string() -> None:
    assert __version__ == "0.2.0"
