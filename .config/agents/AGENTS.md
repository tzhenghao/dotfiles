# My Standing Preferences

- **Coding Style**
  - Repo conventions win over anything below — read neighboring code first, match what's there.
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

- **Custom scripts**
  - `~/custom_scripts/` holds my personal helpers — check it before writing a new script from scratch.
  - `clean-gone-git-branches.py`: deletes local git branches whose upstream is gone (supports `--dry-run`, `--force`, and `--no-fetch`; keeps unmerged branches unless `--force`).
