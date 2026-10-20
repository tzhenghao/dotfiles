# Personal agents

One set of agent charters and skills, generated for Claude Code, Codex, and pi.

| Agent | Tier | Role |
|---|---|---|
| `scout` | fast | Finds code and history; returns `path:line` hits |
| `log-reader` | fast | Extracts and classifies CI failures |
| `devils-advocate` | critic | Attacks a plan before it is built |
| `diff-critic` | critic | Reviews a local diff before push |
| `test-verifier` | fast | Runs the real tests and reports exactly what happened |
| `loc-splitter` | fast | Splits a branch's LOC change into implementation vs test |
| `planner` | deep | Writes the implementation plan, critiqued by `devils-advocate` |
| `architect` | frontier | Cross-component designs; most expensive, use sparingly |

## Files

- `agents/<name>.md`: the charters, the only place to edit an agent. Their
  frontmatter takes `name`, `tier`, `description`, `tools` (Claude Code
  names), and optionally `codex_sandbox` (`read-only` or `workspace-write`).
- `tiers.json`: the model and effort for each tier in each harness. A `null`
  Codex model inherits the calling session's model.
- `preamble.md`: rules appended to every agent. `codex-preamble.md` is
  appended for Codex only, `pi-preamble.md` for pi only.
- `memory/<name>.md` (created on first use): what each agent has
  learned. The sync inlines it into the generated prompt, so add lessons
  here (from an agent's `Memory candidate:` line) and re-run the sync.
- `skills/<name>/SKILL.md`: the skills, the only place to edit one. The
  folder name must match the `name` frontmatter field, and any other files in
  the folder (such as `references/`) are copied along. Write them to run in
  every harness: `$ARGUMENTS` is a Claude Code substitution, so refer to the
  user's target in words instead.
- `sync.py`: writes `~/.claude/agents/<name>.md`,
  `~/.codex/agents/<name>.toml`, and `~/.pi/agent/agents/<name>.md`, and
  copies each skill to `~/.claude/skills/<name>/`, `~/.codex/skills/<name>/`,
  and `~/.pi/agent/skills/<name>/`.

## Update the agents and skills

1. Edit a charter, a skill, `tiers.json`, a preamble, or a memory file.
2. Regenerate:

   ```bash
   python3 ~/.config/agents/sync.py
   ```

   `--check` reports drift without writing. The sync only replaces or removes
   files carrying its generated marker (for a skill, the marker in its
   `SKILL.md` covers the whole folder), and refuses to overwrite anything else.

3. Start a new Claude Code, Codex, or pi session to load the changes.

## Pi subagents

pi has no built-in subagent tool. Its shipped example extension reads the
agents sync.py generates from `~/.pi/agent/agents/` and runs each one in its
own `pi` process, inheriting the dispatching session's model. One-time
setup:

```bash
mkdir -p ~/.pi/agent/extensions
ln -s "$(npm root -g)/@earendil-works/pi-coding-agent/examples/extensions/subagent" \
  ~/.pi/agent/extensions/subagent
```

The tool is named `subagent`, the pi name for Claude Code's `Agent`. A
checkout that ships its own `subagent` tool (like modular) registers it
first, and pi keeps the first tool registered per name, so the personal
agents do not run there.

## Test the sync script

```bash
cd ~/.config/agents
uv run --no-project --python 3.10 --with pytest --with tomli python -m pytest -q tests
```
