---
name: audit-tests
description: "Prune duplicated or valueless tests and consolidate copy-pasted fixtures in a directory, package or tool, without losing coverage."
argument-hint: "<path | package | tool> [--report-only]"
---

# Audit tests

Scope: the path, package or tool the user named, and whether they passed
`--report-only`. If no target was named, ask for one before starting.

**Rule:** remove a test only after showing a named surviving test fails for
the same defect. Never weaken assertions or tolerances, or edit code under
test. If you can't prove it, keep it and flag it.

1. **Scope.** Find the tests for the target, including tests elsewhere that
   exercise it and tests disabled or excluded from CI. Record the case list,
   pass/fail and runtime with the project's own test runner.
2. **Find.** Look for:
   - identical or subsumed tests, and copy-pasted tests that only need
     parametrizing;
   - fixtures and helpers copied across files, and setup repeated in 3+
     tests;
   - tests that never run: never registered or called, shadowed by a later
     definition, or not wired into the build or test config;
   - stale skips, and tests that only check mocks.
3. **Rule out false duplicates:** the same body with different imports,
   fixtures or config; the same file run under different flags, environments
   or platforms; different types or boundary sizes; regression tests; and
   error-path or golden-output tests.
4. **Report.** A table of location, verdict, evidence and survivor. Stop
   here if `--report-only`.
5. **Apply** in batches, in this order: wire, hoist, merge, remove. Update
   the build or test config as you go.
   - **Merges and hoists:** the case list is unchanged.
   - **Removals:** line coverage on the code under test is unchanged, where
     coverage tooling exists. Otherwise, break the code, confirm the
     survivor fails, then revert.
   - Rerun the full scoped suite.
