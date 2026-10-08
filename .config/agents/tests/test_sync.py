from pathlib import Path

import pytest
import tomli

import sync

TIERS_JSON = """{
  "fast": {"claude": {"model": "haiku", "effort": null}, "codex": {"model": null, "effort": "low"}},
  "deep": {"claude": {"model": "opus", "effort": "xhigh"}, "codex": {"model": "gpt-test", "effort": "high"}}
}"""

FAST_CHARTER = """---
name: finder
tier: fast
description: "Finds things: quickly."
tools: Read, Grep
codex_sandbox: read-only
---

Find it.
"""

DEEP_CHARTER = '''---
name: thinker
tier: deep
description: "Thinks hard."
tools: Read, Agent
---

Body with a backslash \\d and a triple quote """ inside.
'''


class Layout:
    def __init__(self, root: Path) -> None:
        self.source_dir = root / "source"
        self.claude_dir = root / "claude"
        self.codex_dir = root / "codex"
        (self.source_dir / "agents").mkdir(parents=True)
        (self.source_dir / "tiers.json").write_text(TIERS_JSON)
        (self.source_dir / "preamble.md").write_text("Shared rules.\n")
        (self.source_dir / "codex-preamble.md").write_text("Codex notes.\n")
        self.add_charter("finder", FAST_CHARTER)
        self.add_charter("thinker", DEEP_CHARTER)

    def add_charter(self, name: str, text: str) -> None:
        (self.source_dir / "agents" / f"{name}.md").write_text(text)

    def run(self, *extra_args: str) -> int:
        return sync.main(
            [
                "--source-dir", str(self.source_dir),
                "--claude-dir", str(self.claude_dir),
                "--codex-dir", str(self.codex_dir),
                *extra_args,
            ]
        )


@pytest.fixture
def layout(tmp_path: Path) -> Layout:
    return Layout(tmp_path)


def test_claude_output_maps_tier_model_and_effort(layout: Layout) -> None:
    assert layout.run() == 0
    finder = (layout.claude_dir / "finder.md").read_text()
    thinker = (layout.claude_dir / "thinker.md").read_text()
    assert "model: haiku\n" in finder
    assert "effort:" not in finder
    assert 'description: "Finds things: quickly."' in finder
    assert "tools: Read, Grep\n" in finder
    assert "Shared rules." in finder
    assert "## Memory" not in finder
    assert "model: opus\neffort: xhigh\n" in thinker


def test_codex_output_is_valid_toml_with_tier_settings(layout: Layout) -> None:
    assert layout.run() == 0
    finder = tomli.loads((layout.codex_dir / "finder.toml").read_text())
    thinker = tomli.loads((layout.codex_dir / "thinker.toml").read_text())

    assert finder["name"] == "finder"
    assert "model" not in finder
    assert finder["model_reasoning_effort"] == "low"
    assert finder["sandbox_mode"] == "read-only"
    assert "Codex notes." in finder["developer_instructions"]
    assert "Allowed tools: Read, Grep. Use no others." in finder["developer_instructions"]

    assert thinker["model"] == "gpt-test"
    assert "sandbox_mode" not in thinker
    assert 'backslash \\d and a triple quote """ inside.' in thinker["developer_instructions"]


def test_memory_is_inlined_into_both_harnesses(layout: Layout) -> None:
    (layout.source_dir / "memory").mkdir()
    (layout.source_dir / "memory" / "finder.md").write_text("2026-10-08: prefer rg -n.\n")
    assert layout.run() == 0
    expected = "## Memory\n\n2026-10-08: prefer rg -n.\n"
    assert (layout.claude_dir / "finder.md").read_text().endswith(expected)
    codex = tomli.loads((layout.codex_dir / "finder.toml").read_text())
    assert codex["developer_instructions"].endswith(expected)
    assert "## Memory" not in (layout.claude_dir / "thinker.md").read_text()


def test_second_sync_changes_nothing(layout: Layout, capsys: pytest.CaptureFixture[str]) -> None:
    assert layout.run() == 0
    capsys.readouterr()
    assert layout.run() == 0
    assert capsys.readouterr().out == "up to date\n"
    assert layout.run("--check") == 0


def test_check_reports_hand_edited_output_without_writing(layout: Layout) -> None:
    assert layout.run() == 0
    edited = layout.claude_dir / "finder.md"
    edited.write_text(edited.read_text() + "hand edit\n")
    assert layout.run("--check") == 1
    assert edited.read_text().endswith("hand edit\n")
    assert layout.run() == 0
    assert not edited.read_text().endswith("hand edit\n")


def test_removes_stale_generated_files_and_keeps_hand_written_ones(layout: Layout) -> None:
    assert layout.run() == 0
    hand_written = layout.claude_dir / "mine.md"
    hand_written.write_text("---\nname: mine\n---\nmy own agent\n")
    (layout.source_dir / "agents" / "thinker.md").unlink()

    assert layout.run() == 0
    assert not (layout.claude_dir / "thinker.md").exists()
    assert not (layout.codex_dir / "thinker.toml").exists()
    assert hand_written.exists()


def test_refuses_to_overwrite_hand_written_file(layout: Layout) -> None:
    layout.claude_dir.mkdir()
    hand_written = layout.claude_dir / "finder.md"
    hand_written.write_text("my own finder\n")
    assert layout.run() == 2
    assert hand_written.read_text() == "my own finder\n"


@pytest.mark.parametrize(
    "charter_text",
    [
        FAST_CHARTER.replace("tier: fast", "tier: missing"),
        FAST_CHARTER.replace("name: finder", "name: other"),
        FAST_CHARTER.replace("tools: Read, Grep", "tools: Read, Teleport"),
        FAST_CHARTER.replace("codex_sandbox: read-only", "codex_sandbox: anything"),
        FAST_CHARTER.replace("tools: Read, Grep\n", ""),
    ],
)
def test_rejects_invalid_charter(layout: Layout, charter_text: str) -> None:
    layout.add_charter("finder", charter_text)
    assert layout.run() == 2
    assert not layout.claude_dir.exists()


def test_real_charters_render(tmp_path: Path) -> None:
    outputs = sync.desired_outputs(sync.SOURCE_DIR, tmp_path / "claude", tmp_path / "codex")
    names = {path.stem for path in outputs}
    assert names == {
        "scout", "log-reader", "devils-advocate", "diff-critic",
        "test-verifier", "planner", "architect",
    }
    for path, content in outputs.items():
        if path.suffix == ".toml":
            assert tomli.loads(content)["name"] == path.stem
