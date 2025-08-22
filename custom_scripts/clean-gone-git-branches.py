#!/usr/bin/env python3
"""
Script to delete all stale branches marked as [gone] in git branch -v output.

Usage:
    python clean-gone-git-branches.py [--dry-run] [--force]

Options:
    --dry-run    Show what would be deleted without actually deleting
    --force      Skip confirmation prompt
"""

import argparse
import re
import subprocess
import sys

class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def log_info(message: str) -> None:
    """Log an info message."""
    print(f"{Colors.GREEN}[INFO]{Colors.NC} {message}")


def log_warning(message: str) -> None:
    """Log a warning message."""
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")


def log_error(message: str) -> None:
    """Log an error message."""
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")


def run_git_command(command: list[str]) -> tuple[bool, str]:
    """
    Run a git command and return success status and output.

    Args:
        command: List of command arguments

    Returns:
        Tuple of (success, output)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()


def is_git_repository() -> bool:
    """Check if current directory is a git repository."""
    success, _ = run_git_command(['git', 'rev-parse', '--git-dir'])
    return success


def get_gone_branches() -> list[str]:
    """
    Get list of branch names that are marked as [gone].

    First runs git fetch --prune to update remote tracking information.

    Returns:
        List of branch names
    """
    # First, fetch and prune to update remote tracking information
    log_info("Fetching latest remote information and pruning stale references...")
    success, output = run_git_command(['git', 'fetch', '--prune'])
    if not success:
        log_warning(f"Failed to fetch and prune: {output}")
        log_warning("Continuing anyway, but results may not be up to date")

    success, output = run_git_command(['git', 'branch', '-v'])
    if not success:
        log_error("Failed to get branch information")
        return []

    gone_branches = []
    for line in output.split('\n'):
        if '[gone]' in line:
            # Extract branch name (remove leading spaces and asterisk)
            branch_match = re.match(r'^[\s*]*([^\s]+)', line)
            if branch_match:
                gone_branches.append(branch_match.group(1))

    return gone_branches


def delete_branch(branch_name: str) -> bool:
    """
    Delete a git branch.

    Args:
        branch_name: Name of the branch to delete

    Returns:
        True if successful, False otherwise
    """
    success, output = run_git_command(['git', 'branch', '-D', branch_name])
    if not success:
        log_error(f"Failed to delete branch '{branch_name}': {output}")
    return success


def main() -> int:
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Delete all stale branches marked as [gone]"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be deleted without actually deleting'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompt'
    )

    args = parser.parse_args()

    if args.dry_run:
        print(f"{Colors.YELLOW}Running in dry-run mode - no branches will be deleted{Colors.NC}")
        print()

    # Check if we're in a git repository
    if not is_git_repository():
        log_error("Not in a git repository")
        return 1

    # Get gone branches
    gone_branches = get_gone_branches()

    if not gone_branches:
        log_info("No stale branches found with [gone] status")
        return 0

    print("Found the following stale branches marked as [gone]:")
    for branch in gone_branches:
        print(f"  - {branch}")
    print()

    if args.dry_run:
        log_info(f"Dry-run mode: Would delete {len(gone_branches)} branches")
        return 0

    # Confirm deletion unless --force is used
    if not args.force:
        try:
            confirmation = input("Do you want to delete these branches? [y/N]: ")
            if confirmation.lower() not in ['y', 'yes']:
                log_warning("Operation cancelled")
                return 0
        except KeyboardInterrupt:
            print()
            log_warning("Operation cancelled")
            return 0

    # Delete branches
    deleted_count = 0
    failed_count = 0

    for branch in gone_branches:
        log_info(f"Deleting branch: {branch}")
        if delete_branch(branch):
            deleted_count += 1
        else:
            failed_count += 1

    # Summary
    if failed_count == 0:
        log_info(f"Successfully deleted {deleted_count} stale branches")
    else:
        log_warning(f"Deleted {deleted_count} branches, failed to delete {failed_count} branches")

    return 0 if failed_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
