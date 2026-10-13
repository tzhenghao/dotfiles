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
     - Use this worktree's own config (`.env`, ports, DB), not defaults.
  - Naming: spell things out (`remainingRetries` not `rr`); include units/state (`timeoutMs`, `isDraft`); booleans as assertions (`hasAccess`); verb-phrase functions named for outcome, not mechanism; short names OK in tiny scopes; never abbreviate domain terms.
  - DRY: refactor into shared functions/methods/interfaces/classes instead of duplicating.
  - Comments: only for *why* — no restating code, no edit narration, no unsolicited TODOs.
    - Describe present-tense behavior; never frame code as "legacy", "old", or "mirrors X". Migration context belongs in the PR description.
    - Build, packaging, and CI config files (Dockerfiles, workflow yaml, build targets) get no comments on why a value was chosen or who consumes it. Rationale goes in the commit message.
    - Docstrings on small helpers/components: one short sentence on what it is and does. Skip "centralizes…" / "avoids duplication…".
  - No re-export shims or needless indirection: repoint consumers to the canonical module. Verify with a typecheck, since multi-line imports hide usage from grep.
  - Work in a scratch worktree is volatile: commit it to its branch once green, since a branch survives `git worktree remove` and an uncommitted tree does not. A local commit is fine without asking; pushing still waits for me.
  - Start feature branches with the `tzhenghao/` prefix.
  - Explicit over clever; handle errors meaningfully; immutable by default; small pure functions over shared state; follow the project's linter/formatter; no dead code.
  - Strict typing (e.g. Python: `Mapping`, `TypedDict`, `NamedTuple` over loose dicts).
  - Keep docs and agent skills in sync with the change.
  - Before handing back: run real tests to confirm it works — don't just eyeball it.

- **Pull Requests**
  - Short, plain-language description: problem → solution → tests. No line-by-line itemization of source changes.
  - Default to splitting multi-step work into stacked PRs, one concern each (no-behavior-change carve, source of truth, each consumer, UI). When unsure, split. State the stack plan up front and confirm it before committing to it.
  - Prove no-behavior-change UI refactors with a real-browser A/B of DOM signatures against a `main` worktree, not just unit tests. Self-diff two runs on identical code before trusting the A/B.

- **Communication (Slack / Linear / PR comments)**
  - Never send or reply directly — draft it as a reply block in-session for me to copy/paste myself.
  - Numbers derived from telemetry: write the derivation into the ticket and doc, split by provenance (measured / derived / assumed), then audit your own claims before calling it done. Pull percentiles, not just means, and state what was not validated end to end.

- **Delegation (personal agents)**
  - Searches spanning more than a couple of files → `scout`; run several in parallel for independent questions.
  - CI or PR failures → `log-reader` first, then diagnose from its report.
  - Non-trivial plans → `planner` (it runs `devils-advocate` itself) before showing me. Use `architect` only for cross-component or design-doc work, or when I ask.
  - Before handing back code → `test-verifier` and `diff-critic` in parallel.
  - Run these unprompted at every stage they apply, build them into the plan rather than appending them at the end, and fix confirmed findings before pushing. Any red CI check goes to `log-reader` first, even when another agent is handling it. For a PR stack, also run one `diff-critic` over the whole stack from main. Say which agents ran and which did not, with the reason.
  - When a repo ships its own agent for the job, prefer it.
  - When an agent's reply ends with a `Memory candidate:` worth keeping, append it to `~/.config/agents/memory/<agent>.md` and re-run the sync.
  - Charters live in `~/.config/agents/agents/`. Edit them there and run `python3 ~/.config/agents/sync.py`; never edit the generated files in `~/.claude/agents/` or `~/.codex/agents/`.

- **Custom scripts**
  - `~/custom_scripts/` is a symlink to `custom_scripts/` in my dotfiles repo (`~/personal/dotfiles`) — version control is the source of truth. Check there before writing a new script from scratch, and commit any changes.
  - `clean-gone-git-branches.py`: deletes local git branches whose upstream is gone (supports `--dry-run`, `--force`, and `--no-fetch`; keeps unmerged branches unless `--force`).
