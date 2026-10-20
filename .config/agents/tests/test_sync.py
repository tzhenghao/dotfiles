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


SKILL = """---
name: auditor
description: "Audits things."
argument-hint: "<path>"
---

# Auditor

Audit the target.
"""


class Layout:
    def __init__(self, root: Path) -> None:
        self.source_dir = root / "source"
        self.claude_dir = root / "claude"
        self.codex_dir = root / "codex"
        self.pi_dir = root / "pi"
        self.skills_dirs = [root / "claude-skills", root / "codex-skills", root / "pi-skills"]
        (self.source_dir / "agents").mkdir(parents=True)
        (self.source_dir / "tiers.json").write_text(TIERS_JSON)
        (self.source_dir / "preamble.md").write_text("Shared rules.\n")
        (self.source_dir / "codex-preamble.md").write_text("Codex notes.\n")
        (self.source_dir / "pi-preamble.md").write_text("Pi notes.\n")
        self.add_charter("finder", FAST_CHARTER)
        self.add_charter("thinker", DEEP_CHARTER)

    def add_charter(self, name: str, text: str) -> None:
        (self.source_dir / "agents" / f"{name}.md").write_text(text)

    def add_skill(self, name: str, text: str, **extra_files: str) -> None:
        skill_dir = self.source_dir / "skills" / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(text)
        for relative_path, content in extra_files.items():
            (skill_dir / relative_path).parent.mkdir(parents=True, exist_ok=True)
            (skill_dir / relative_path).write_text(content)

    def run(self, *extra_args: str) -> int:
        return sync.main(
            [
                "--source-dir", str(self.source_dir),
                "--claude-dir", str(self.claude_dir),
                "--codex-dir", str(self.codex_dir),
                "--pi-dir", str(self.pi_dir),
                *[arg for skills_dir in self.skills_dirs for arg in ("--skills-dir", str(skills_dir))],
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


def test_pi_output_translates_tools_and_inherits_model(layout: Layout) -> None:
    assert layout.run() == 0
    finder = (layout.pi_dir / "finder.md").read_text()
    assert "tools: read, grep\n" in finder
    assert "model:" not in finder
    assert "Pi notes." in finder
    thinker = (layout.pi_dir / "thinker.md").read_text()
    assert "tools: read, subagent\n" in thinker


def test_memory_is_inlined_into_all_harnesses(layout: Layout) -> None:
    (layout.source_dir / "memory").mkdir()
    (layout.source_dir / "memory" / "finder.md").write_text("2026-10-08: prefer rg -n.\n")
    assert layout.run() == 0
    expected = "## Memory\n\n2026-10-08: prefer rg -n.\n"
    assert (layout.claude_dir / "finder.md").read_text().endswith(expected)
    codex = tomli.loads((layout.codex_dir / "finder.toml").read_text())
    assert codex["developer_instructions"].endswith(expected)
    assert (layout.pi_dir / "finder.md").read_text().endswith(expected)
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
    assert not (layout.pi_dir / "thinker.md").exists()
    assert hand_written.exists()


def test_refuses_to_overwrite_hand_written_file(layout: Layout) -> None:
    layout.claude_dir.mkdir()
    hand_written = layout.claude_dir / "finder.md"
    hand_written.write_text("my own finder\n")
    assert layout.run() == 2
    assert hand_written.read_text() == "my own finder\n"


def test_refuses_to_overwrite_hand_written_pi_file(layout: Layout) -> None:
    layout.pi_dir.mkdir()
    hand_written = layout.pi_dir / "finder.md"
    hand_written.write_text("my own pi finder\n")
    assert layout.run() == 2
    assert hand_written.read_text() == "my own pi finder\n"


@pytest.mark.parametrize(
    "charter_text",
    [
        FAST_CHARTER.replace("tier: fast", "tier: missing"),
        FAST_CHARTER.replace("name: finder", "name: other"),
        FAST_CHARTER.replace("tools: Read, Grep", "tools: Read, Teleport"),
        FAST_CHARTER.replace("codex_sandbox: read-only", "codex_sandbox: anything"),
        FAST_CHARTER.replace("tools: Read, Grep\n", ""),
        FAST_CHARTER.replace("tools: Read, Grep", "tools: WebSearch, WebFetch"),
    ],
)
def test_rejects_invalid_charter(layout: Layout, charter_text: str) -> None:
    layout.add_charter("finder", charter_text)
    assert layout.run() == 2
    assert not layout.claude_dir.exists()


def test_real_charters_render(tmp_path: Path) -> None:
    outputs = sync.desired_outputs(
        sync.SOURCE_DIR, tmp_path / "claude", tmp_path / "codex", tmp_path / "pi", [tmp_path / "skills"]
    )
    names = {path.stem for path in outputs}
    assert names == {
        "scout", "log-reader", "devils-advocate", "diff-critic",
        "test-verifier", "planner", "architect", "loc-splitter",
    }
    for path, content in outputs.items():
        if path.suffix == ".toml":
            assert tomli.loads(content)["name"] == path.stem
    assert "tools: read, grep, find, bash\n" in outputs[tmp_path / "pi" / "scout.md"]


def test_skill_is_copied_to_every_skills_dir_with_marker(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL, **{"references/notes.md": "Notes.\n"})
    assert layout.run() == 0
    for skills_dir in layout.skills_dirs:
        skill_file = (skills_dir / "auditor" / "SKILL.md").read_text()
        frontmatter, _, body = skill_file[len("---\n"):].partition("\n---\n")
        assert frontmatter == SKILL.split("---\n")[1].rstrip("\n")
        assert body.startswith(f"<!-- {sync.SKILL_GENERATED_MARKER} -->\n")
        assert skill_file.endswith("Audit the target.\n")
        assert (skills_dir / "auditor" / "references" / "notes.md").read_text() == "Notes.\n"


def test_second_sync_with_skills_changes_nothing(
    layout: Layout, capsys: pytest.CaptureFixture[str]
) -> None:
    layout.add_skill("auditor", SKILL, **{"references/notes.md": "Notes.\n"})
    assert layout.run() == 0
    capsys.readouterr()
    assert layout.run() == 0
    assert capsys.readouterr().out == "up to date\n"
    assert layout.run("--check") == 0


def test_check_reports_hand_edited_skill_without_writing(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL)
    assert layout.run() == 0
    edited = layout.skills_dirs[0] / "auditor" / "SKILL.md"
    edited.write_text(edited.read_text() + "hand edit\n")
    assert layout.run("--check") == 1
    assert edited.read_text().endswith("hand edit\n")
    assert layout.run() == 0
    assert not edited.read_text().endswith("hand edit\n")


def test_removes_stale_generated_skill_files_and_keeps_hand_written_skills(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL, **{"references/notes.md": "Notes.\n"})
    layout.add_skill("gone", SKILL.replace("auditor", "gone"))
    assert layout.run() == 0
    hand_written = layout.skills_dirs[0] / "mine" / "SKILL.md"
    hand_written.parent.mkdir()
    hand_written.write_text("---\nname: mine\ndescription: Mine.\n---\nmy own skill\n")
    (layout.source_dir / "skills" / "auditor" / "references" / "notes.md").unlink()
    (layout.source_dir / "skills" / "auditor" / "references").rmdir()
    (layout.source_dir / "skills" / "gone" / "SKILL.md").unlink()
    (layout.source_dir / "skills" / "gone").rmdir()

    assert layout.run() == 0
    for skills_dir in layout.skills_dirs:
        assert (skills_dir / "auditor" / "SKILL.md").exists()
        assert not (skills_dir / "auditor" / "references").exists()
        assert not (skills_dir / "gone").exists()
        assert skills_dir.is_dir()
    assert hand_written.exists()


def test_refuses_to_overwrite_hand_written_skill(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL, **{"references/notes.md": "Notes.\n"})
    hand_written = layout.skills_dirs[1] / "auditor" / "SKILL.md"
    hand_written.parent.mkdir(parents=True)
    hand_written.write_text("my own skill\n")
    assert layout.run() == 2
    assert hand_written.read_text() == "my own skill\n"
    assert not (hand_written.parent / "references").exists()


@pytest.mark.parametrize(
    "skill_text",
    [
        SKILL.replace("name: auditor", "name: other"),
        SKILL.replace('description: "Audits things."\n', ""),
        SKILL.replace("---\n", "", 1),
        SKILL.replace("\n---\n", "\n", 1),
    ],
)
def test_rejects_invalid_skill(layout: Layout, skill_text: str) -> None:
    layout.add_skill("auditor", skill_text)
    assert layout.run() == 2
    assert not layout.skills_dirs[0].exists()


def test_rejects_skill_folder_without_skill_file(layout: Layout) -> None:
    (layout.source_dir / "skills" / "empty").mkdir(parents=True)
    assert layout.run() == 2


def test_leaves_unmarked_skill_directories_alone(layout: Layout) -> None:
    system_skill = layout.skills_dirs[1] / ".system" / "SKILL.md"
    system_skill.parent.mkdir(parents=True)
    system_skill.write_text("---\nname: system\ndescription: Built in.\n---\n")
    layout.add_skill("auditor", SKILL)
    assert layout.run() == 0
    assert system_skill.read_text() == "---\nname: system\ndescription: Built in.\n---\n"


def test_refuses_skill_folder_that_has_no_skill_file(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL)
    hand_written = layout.skills_dirs[1] / "auditor" / "scripts" / "run.sh"
    hand_written.parent.mkdir(parents=True)
    hand_written.write_text("echo mine\n")
    assert layout.run() == 2
    assert hand_written.read_text() == "echo mine\n"
    assert not (hand_written.parents[1] / "SKILL.md").exists()


def test_rejects_non_text_skill_file(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL)
    (layout.source_dir / "skills" / "auditor" / "logo.png").write_bytes(b"\x89PNG\xff\xfe")
    assert layout.run() == 2
    assert not layout.skills_dirs[0].exists()


def test_ignores_finder_metadata_in_skill_source(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL)
    (layout.source_dir / "skills" / "auditor" / ".DS_Store").write_bytes(b"\x00\xff")
    assert layout.run() == 0
    assert not (layout.skills_dirs[0] / "auditor" / ".DS_Store").exists()


def test_check_reports_stale_skill_removal_without_writing(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL)
    assert layout.run() == 0
    (layout.source_dir / "skills" / "auditor" / "SKILL.md").unlink()
    (layout.source_dir / "skills" / "auditor").rmdir()
    assert layout.run("--check") == 1
    assert (layout.skills_dirs[0] / "auditor" / "SKILL.md").exists()


def test_removes_skill_file_last(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL, **{"references/notes.md": "Notes.\n", "a.md": "A.\n"})
    assert layout.run() == 0
    outputs = sync.desired_outputs(
        layout.source_dir, layout.claude_dir, layout.codex_dir, layout.pi_dir, layout.skills_dirs[:1]
    )
    kept = {path: text for path, text in outputs.items() if layout.skills_dirs[0] not in path.parents}
    changes = sync.plan_changes(
        kept, layout.claude_dir, layout.codex_dir, layout.pi_dir, layout.skills_dirs[:1]
    )
    removed = [change.path.name for change in changes if change.action == "remove"]
    assert removed[-1] == "SKILL.md"
    assert sorted(removed[:-1]) == ["a.md", "notes.md"]


def test_writes_skill_file_before_other_skill_files(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL, **{"A.md": "A.\n", "references/notes.md": "Notes.\n"})
    outputs = sync.desired_outputs(
        layout.source_dir, layout.claude_dir, layout.codex_dir, layout.pi_dir, layout.skills_dirs[:1]
    )
    changes = sync.plan_changes(
        outputs, layout.claude_dir, layout.codex_dir, layout.pi_dir, layout.skills_dirs[:1]
    )
    skill_writes = [
        change.path.name for change in changes if layout.skills_dirs[0] in change.path.parents
    ]
    assert skill_writes[0] == "SKILL.md"
    assert sorted(skill_writes[1:]) == ["A.md", "notes.md"]


def test_ignores_undecodable_skill_file_in_foreign_skill_folder(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL)
    foreign = layout.skills_dirs[1] / "foreign" / "SKILL.md"
    foreign.parent.mkdir(parents=True)
    foreign.write_bytes(b"\xff\xfe")
    assert layout.run() == 0
    assert foreign.read_bytes() == b"\xff\xfe"


def test_refuses_undecodable_skill_file_in_same_named_folder(layout: Layout) -> None:
    layout.add_skill("auditor", SKILL)
    foreign = layout.skills_dirs[1] / "auditor" / "SKILL.md"
    foreign.parent.mkdir(parents=True)
    foreign.write_bytes(b"\xff\xfe")
    assert layout.run("--check") == 2
    assert layout.run() == 2
    assert foreign.read_bytes() == b"\xff\xfe"
