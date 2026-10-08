# Personal agents

One set of agent charters, generated for Claude Code and Codex.

| Agent | Tier | Role |
|---|---|---|
| `scout` | fast | Finds code and history; returns `path:line` hits |
| `log-reader` | fast | Extracts and classifies CI failures |
| `devils-advocate` | critic | Attacks a plan before it is built |
| `diff-critic` | critic | Reviews a local diff before push |
| `test-verifier` | fast | Runs the real tests and reports exactly what happened |
| `planner` | deep | Writes the implementation plan, critiqued by `devils-advocate` |
| `architect` | frontier | Cross-component designs; most expensive, use sparingly |

## Files

- `agents/<name>.md`: the charters, the only place to edit an agent. Their
  frontmatter takes `name`, `tier`, `description`, `tools` (Claude Code
  names), and optionally `codex_sandbox` (`read-only` or `workspace-write`).
- `tiers.json`: the model and effort for each tier in each harness. A `null`
  Codex model inherits the calling session's model.
- `preamble.md`: rules appended to every agent. `codex-preamble.md` is
  appended for Codex only.
- `memory/<name>.md`: what each agent has learned. The sync inlines it into
  the generated prompt, so add lessons here (from an agent's
  `Memory candidate:` line) and re-run the sync.
- `sync.py`: writes `~/.claude/agents/<name>.md` and
  `~/.codex/agents/<name>.toml`.

## Update the agents

1. Edit a charter, `tiers.json`, a preamble, or a memory file.
2. Regenerate:

   ```bash
   python3 ~/.config/agents/sync.py
   ```

   `--check` reports drift without writing. The sync only replaces or removes
   files carrying its generated marker, and refuses to overwrite anything else.

3. Start a new Claude Code or Codex session to load the changes.

## Test the sync script

```bash
cd ~/.config/agents
uv run --no-project --python 3.10 --with pytest --with tomli python -m pytest -q tests
```
