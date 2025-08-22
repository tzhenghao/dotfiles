#!/usr/bin/env python3
"""
Remove a specified suffix from all files in a directory.

Usage Examples:
    # Remove .HEIC suffix from files in a specific directory
    python3 remove_suffix_from_all_files.py /path/to/your/directory .HEIC

    # Remove .txt suffix from files in current directory
    python3 remove_suffix_from_all_files.py . .txt

    # Preview what would be renamed (dry-run mode)
    python3 remove_suffix_from_all_files.py /path/to/directory .jpg --dry-run

    # Get help
    python3 remove_suffix_from_all_files.py --help
"""

import argparse
import os
import sys
from pathlib import Path

def remove_suffix_from_files(directory, suffix, dry_run=False):
    """
    Remove a specified suffix from all files in a directory.
    
    Args:
        directory (str): Path to the directory containing files
        suffix (str): Suffix to remove from file names
        dry_run (bool): If True, show what would be renamed without actually renaming
    """
    # Convert to Path object for better handling
    dir_path = Path(directory)
    
    # Check if directory exists
    if not dir_path.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)
    
    if not dir_path.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        sys.exit(1)
    
    # Change to the specified directory
    try:
        os.chdir(directory)
    except OSError as e:
        print(f"Error changing to directory '{directory}': {e}")
        sys.exit(1)
    
    # Counter for renamed files
    renamed_count = 0
    
    # Loop through all files in the directory
    for file_path in dir_path.iterdir():
        # Check if it's a file and has the specified suffix
        if file_path.is_file() and file_path.name.endswith(suffix):
            # Remove the suffix from the file name
            new_name = file_path.name[:-len(suffix)]
            new_file_path = file_path.parent / new_name
            
            if dry_run:
                print(f"Would rename {file_path.name} to {new_name}")
                renamed_count += 1
            else:
                try:
                    # Rename the file
                    file_path.rename(new_file_path)
                    print(f"Renamed {file_path.name} to {new_name}")
                    renamed_count += 1
                except OSError as e:
                    print(f"Error renaming {file_path.name}: {e}")
    
    if dry_run:
        print(f"\nTotal files that would be renamed: {renamed_count}")
    else:
        print(f"\nTotal files renamed: {renamed_count}")

def main():    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Remove a specified suffix from all files in a directory"
    )
    parser.add_argument(
        "directory", 
        help="Path to the directory containing files"
    )
    parser.add_argument(
        "suffix", 
        help="Suffix to remove from file names"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Show what would be renamed without actually renaming files"
    )
    
    args = parser.parse_args()
    
    directory = args.directory
    suffix = args.suffix
    dry_run = args.dry_run
    
    if dry_run:
        print(f"DRY RUN: Would remove suffix '{suffix}' from files in directory: {directory}")
    else:
        print(f"Removing suffix '{suffix}' from files in directory: {directory}")
    print("-" * 60)
    
    remove_suffix_from_files(directory, suffix, dry_run)

if __name__ == "__main__":
    main()
