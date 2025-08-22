#!/usr/bin/env python3
"""
Append a specified suffix to all files in a directory.

Usage Examples:
    # Append "(2).HEIC" suffix to files in a specific directory
    python3 append_suffix_to_all_files.py /path/to/your/directory "(2).HEIC"

    # Append "_backup" suffix to files in current directory
    python3 append_suffix_to_all_files.py . "_backup"

    # Preview what would be renamed (dry-run mode)
    python3 append_suffix_to_all_files.py /path/to/directory ".copy" --dry-run

    # Get help
    python3 append_suffix_to_all_files.py --help
"""

import argparse
import os
import sys
from pathlib import Path

def append_suffix_to_files(directory, suffix, dry_run=False):
    """
    Append a specified suffix to all files in a directory.
    
    Args:
        directory (str): Path to the directory containing files
        suffix (str): Suffix to append to file names
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
        # Check if it's a file (not a directory)
        if file_path.is_file():
            # Add the suffix to the file name
            new_name = file_path.name + suffix
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
        description="Append a specified suffix to all files in a directory"
    )
    parser.add_argument(
        "directory", 
        help="Path to the directory containing files"
    )
    parser.add_argument(
        "suffix", 
        help="Suffix to append to file names"
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
        print(f"DRY RUN: Would append suffix '{suffix}' to files in directory: {directory}")
    else:
        print(f"Appending suffix '{suffix}' to files in directory: {directory}")
    print("-" * 60)
    
    append_suffix_to_files(directory=directory, suffix=suffix, dry_run=dry_run)

if __name__ == "__main__":
    main()
