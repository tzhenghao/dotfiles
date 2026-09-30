#!/usr/bin/env python3
"""Delete local git branches whose upstream is gone (deleted on the remote).

Usage:
    clean-gone-git-branches.py [--dry-run] [--force] [--no-fetch]

Options:
    --dry-run    Show what would be deleted without deleting anything
    --force      Skip confirmation prompts and force-delete unmerged branches
    --no-fetch   Skip the `git fetch --prune` refresh of remote-tracking refs

By default only fully merged branches are deleted (git branch -d); branches
with unmerged commits are kept and listed unless explicitly confirmed or
forced.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys


class Colors:
    """ANSI color codes for terminal output; empty strings when disabled."""

    def __init__(self, enabled: bool) -> None:
        self.RED = '\033[0;31m' if enabled else ''
        self.GREEN = '\033[0;32m' if enabled else ''
        self.YELLOW = '\033[1;33m' if enabled else ''
        self.NC = '\033[0m' if enabled else ''


COLORS = Colors(sys.stdout.isatty() and 'NO_COLOR' not in os.environ)


def log_info(message: str) -> None:
    print(f"{COLORS.GREEN}[INFO]{COLORS.NC} {message}")


def log_warning(message: str) -> None:
    print(f"{COLORS.YELLOW}[WARNING]{COLORS.NC} {message}")


def log_error(message: str) -> None:
    print(f"{COLORS.RED}[ERROR]{COLORS.NC} {message}")


def run_git_command(command: list[str]) -> tuple[bool, str]:
    """
    Run a git command and return success status and output.

    On failure, prefers stderr, which is where git reports its errors.

    Args:
        command: Git command as a list of arguments

    Returns:
        Tuple of (success, output)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, (e.stderr or e.stdout or '').strip()


def is_git_repository() -> bool:
    """Return True if the current directory is inside a git repository."""
    success, _ = run_git_command(['git', 'rev-parse', '--git-dir'])
    return success


def get_gone_branches() -> list[str] | None:
    """
    Return local branches whose upstream is gone, or None if listing failed.

    Uses %(upstream:track) rather than scraping `git branch -v` output, so
    commit subjects or branch names cannot produce a false [gone] match.

    Returns:
        List of branch names, or None on git failure
    """
    success, output = run_git_command([
        'git', 'for-each-ref',
        '--format=%(refname:short)\t%(upstream:track,nobracket)',
        'refs/heads',
    ])
    if not success:
        log_error(f"Failed to list branches: {output}")
        return None

    gone_branches = []
    for line in output.split('\n'):
        branch_name, _, track_state = line.partition('\t')
        if track_state == 'gone':
            gone_branches.append(branch_name)
    return gone_branches


def get_current_branch() -> str:
    """Return the checked-out branch name, or '' when HEAD is detached."""
    success, branch_name = run_git_command(['git', 'symbolic-ref', '--short', 'HEAD'])
    return branch_name if success else ''


def delete_branch(branch_name: str, force: bool) -> tuple[bool, str]:
    """
    Delete a git branch.

    With force=False uses -d, so git refuses branches whose commits are
    not merged into HEAD or any upstream.

    Args:
        branch_name: Name of the branch to delete
        force: Use -D and delete even if unmerged

    Returns:
        Tuple of (success, output)
    """
    flag = '-D' if force else '-d'
    return run_git_command(['git', 'branch', flag, branch_name])


def confirm(prompt: str) -> bool:
    """
    Ask the user to confirm an action.

    A closed or interrupted stdin counts as 'no', so piped or unattended
    invocations never crash or delete anything without explicit consent.

    Args:
        prompt: Question to display

    Returns:
        True only on an explicit yes
    """
    try:
        answer = input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        log_warning("No answer available — treating as 'no'. Use --force to skip prompts.")
        return False
    return answer.strip().lower() in ('y', 'yes')


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="Delete local git branches whose upstream is gone"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='show what would be deleted without deleting anything'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='skip confirmation prompts and force-delete unmerged branches'
    )
    parser.add_argument(
        '--no-fetch',
        action='store_true',
        help='skip the `git fetch --prune` refresh of remote-tracking refs'
    )
    args = parser.parse_args()

    if args.dry_run:
        print(f"{COLORS.YELLOW}Running in dry-run mode - no branches will be deleted{COLORS.NC}")
        print()

    if shutil.which('git') is None:
        log_error("git not found on PATH")
        return 1

    if not is_git_repository():
        log_error("Not in a git repository")
        return 1

    # Refresh remote-tracking refs first, so [gone] reflects the remotes'
    # current state. --all also prunes non-origin remotes.
    if not args.no_fetch:
        log_info("Fetching latest remote information and pruning stale references...")
        success, output = run_git_command(['git', 'fetch', '--prune', '--all'])
        if not success:
            log_warning(f"Failed to fetch and prune: {output}")
            log_warning("Continuing anyway, but results may not be up to date")

    gone_branches = get_gone_branches()
    if gone_branches is None:
        return 1

    current_branch = get_current_branch()
    if current_branch in gone_branches:
        log_warning(f"Skipping '{current_branch}': it is the current branch (check out another to delete it)")
        gone_branches.remove(current_branch)

    if not gone_branches:
        log_info("No stale branches with a gone upstream")
        return 0

    print("Found the following branches whose upstream is gone:")
    for branch_name in gone_branches:
        print(f"  - {branch_name}")
    print()

    if args.dry_run:
        log_info(f"Dry-run mode: would delete {len(gone_branches)} branches")
        return 0

    if not args.force:
        if not confirm("Do you want to delete these branches? [y/N]: "):
            log_warning("Operation cancelled")
            return 0

    deleted: list[str] = []
    unmerged: list[str] = []
    kept_unmerged: list[str] = []
    failed: list[str] = []

    for branch_name in gone_branches:
        log_info(f"Deleting branch: {branch_name}")
        success, output = delete_branch(branch_name, args.force)
        if success:
            deleted.append(branch_name)
        elif 'not fully merged' in output:
            unmerged.append(branch_name)
        else:
            log_error(f"Failed to delete branch '{branch_name}': {output}")
            failed.append(branch_name)

    if unmerged:
        print()
        log_warning("Kept branches with commits not merged anywhere reachable:")
        for branch_name in unmerged:
            print(f"  - {branch_name}")
        if confirm("Force delete them anyway? [y/N]: "):
            for branch_name in unmerged:
                log_info(f"Force deleting branch: {branch_name}")
                success, output = delete_branch(branch_name, force=True)
                if success:
                    deleted.append(branch_name)
                else:
                    log_error(f"Failed to delete branch '{branch_name}': {output}")
                    failed.append(branch_name)
        else:
            kept_unmerged = unmerged

    if failed:
        log_warning(
            f"Deleted {len(deleted)} branches, failed to delete {len(failed)} branches"
        )
        return 1

    summary = f"Successfully deleted {len(deleted)} stale branches"
    if kept_unmerged:
        summary += f", kept {len(kept_unmerged)} unmerged branches"
    log_info(summary)
    return 0


if __name__ == '__main__':
    sys.exit(main())
