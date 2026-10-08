# My Standing Preferences

- **Coding Style**
  - Repo conventions win over anything below — read neighboring code first, match what's there.
  - Multiple agents may be working on this repo at once. Each session must run in its own git worktree on its own branch. 
    - Before making changes:
      - Run `git rev-parse --show-toplevel` and `git branch --show-current`. If you are in the primary checkout or on `main`, stop and ask. Do not edit files.
  - Rules:
     - Only modify files inside your current worktree.
     - Do not check out, reset, or delete branches you did not create.
     - Do not run `git worktree remove` or `git clean` on paths outside your own worktree.
     - Use the DB and port from this worktree's `.env` (do not use defaults).
  - Naming: spell things out (`remainingRetries` not `rr`); include units/state (`timeoutMs`, `isDraft`); booleans as assertions (`hasAccess`); verb-phrase functions named for outcome, not mechanism; short names OK in tiny scopes; never abbreviate domain terms.
  - DRY: refactor into shared functions/methods/interfaces/classes instead of duplicating.
  - Comments: only for *why* — no restating code, no edit narration, no unsolicited TODOs.
  - Start feature branches with the `tzhenghao/` prefix.
  - Explicit over clever; handle errors meaningfully; immutable by default; small pure functions over shared state; follow the project's linter/formatter; no dead code.
  - Strict typing (e.g. Python: `Mapping`, `TypedDict`, `NamedTuple` over loose dicts).
  - Keep docs and agent skills in sync with the change.
  - Before handing back: run real tests to confirm it works — don't just eyeball it.

- **Pull Requests**
  - Short, plain-language description: problem → solution → tests. No line-by-line itemization of source changes.

- **Communication (Slack / Linear / PR comments)**
  - Never send or reply directly — draft it as a reply block in-session for me to copy/paste myself.

- **Delegation (personal agents)**
  - Searches spanning more than a couple of files → `scout`; run several in parallel for independent questions.
  - CI or PR failures → `log-reader` first, then diagnose from its report.
  - Non-trivial plans → `planner` (it runs `devils-advocate` itself) before showing me. Use `architect` only for cross-component or design-doc work, or when I ask.
  - Before handing back code → `test-verifier` and `diff-critic` in parallel.
  - When a repo ships its own agent for the job, prefer it.
  - When an agent's reply ends with a `Memory candidate:` worth keeping, append it to `~/.config/agents/memory/<agent>.md` and re-run the sync.
  - Charters live in `~/.config/agents/agents/`. Edit them there and run `python3 ~/.config/agents/sync.py`; never edit the generated files in `~/.claude/agents/` or `~/.codex/agents/`.

- **Custom scripts**
  - `~/custom_scripts/` is a symlink to `custom_scripts/` in my dotfiles repo (`~/personal/dotfiles`) — version control is the source of truth. Check there before writing a new script from scratch, and commit any changes.
  - `clean-gone-git-branches.py`: deletes local git branches whose upstream is gone (supports `--dry-run`, `--force`, and `--no-fetch`; keeps unmerged branches unless `--force`).
