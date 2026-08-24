"""CLI capture, search, and stats."""

from pathlib import Path

from learnlog.cli import main


def test_cli_add_list_search_stats(tmp_path: Path) -> None:
    root = str(tmp_path)
    assert (
        main(
            [
                "--root",
                root,
                "add",
                "--title",
                "Terraform state",
                "--summary",
                "Remote state and locking",
                "--date",
                "2026-03-01",
                "--topic",
                "terraform,aws",
                "--skill",
                "s3-backend",
                "--resource",
                "HashiCorp|documentation|State|https://developer.hashicorp.com",
            ]
        )
        == 0
    )
    assert (tmp_path / "data/entries/2026/03/01/terraform-state.md").exists()
    assert main(["--root", root, "list", "--topic", "terraform"]) == 0
    assert main(["--root", root, "search", "locking"]) == 0
    assert main(["--root", root, "stats"]) == 0
    assert (
        main(
            [
                "--root",
                root,
                "achievement",
                "add",
                "--title",
                "AWS CCP",
                "--provider",
                "AWS",
                "--date",
                "2026-08-01",
                "--visibility",
                "public",
            ]
        )
        == 0
    )
    assert (tmp_path / "data/generated/index.json").exists()
    assert (
        main(
            [
                "--root",
                root,
                "add",
                "--title",
                "Linux Foundation: file permissions",
                "--summary",
                "chmod and umask from LFS101x",
                "--date",
                "2026-08-10",
                "--visibility",
                "public",
                "--topic",
                "linux",
                "--resource",
                "Linux Foundation|course|Introduction to Linux|https://training.linuxfoundation.org/",
            ]
        )
        == 0
    )
    assert main(["--root", root, "publish"]) == 0
    progress = (tmp_path / "PROGRESS.md").read_text(encoding="utf-8")
    assert "Linux Foundation: file permissions" in progress
    assert "Terraform state" not in progress
