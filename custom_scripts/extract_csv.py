#!/usr/bin/env python3
"""
Script to extract and display CSV data from specified files.

Usage:
    python extract_csv.py <filename> [column_index] [delimiter]

Examples:
    python extract_csv.py data.csv
    python extract_csv.py data.csv 2
    python extract_csv.py data.csv 1 "|"
"""

import csv
import sys
import argparse
from pathlib import Path


def extract_csv_column(filename, column_index=0, delimiter=","):
    """
    Extract a specific column from a CSV file.
    
    Args:
        filename (str): Path to the CSV file
        column_index (int): Index of column to extract (0-based)
        delimiter (str): CSV delimiter character
    
    Returns:
        list: Values from the specified column
    """
    try:
        with open(filename, newline="", encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            
            # Get header row
            header = next(csv_reader, None)
            if header is None:
                print(f"Error: File '{filename}' is empty")
                return []
            
            # Validate column index
            if column_index >= len(header):
                print(f"Error: Column index {column_index} is out of range")
                print(f"Available columns (0-{len(header)-1}): {header}")
                return []
            
            # Extract column values
            column_values = []
            for row_num, row in enumerate(csv_reader, start=2):
                if column_index < len(row):
                    column_values.append(row[column_index])
                else:
                    print(f"Warning: Row {row_num} has fewer columns than expected")
            
            return column_values
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return []
    except PermissionError:
        print(f"Error: Permission denied accessing '{filename}'")
        return []
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file '{filename}'. Try specifying encoding.")
        return []
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return []


def main():
    """Main function to handle command line arguments and execute CSV extraction."""
    parser = argparse.ArgumentParser(
        description="Extract and display CSV data from specified files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.csv              # Extract first column (index 0)
  %(prog)s data.csv 2            # Extract third column (index 2)
  %(prog)s data.csv 1 "|"        # Extract second column with pipe delimiter
  %(prog)s data.csv --header     # Show column headers
        """
    )
    
    parser.add_argument(
        'filename',
        help='CSV file to process'
    )
    
    parser.add_argument(
        'column_index',
        nargs='?',
        type=int,
        default=0,
        help='Column index to extract (0-based, default: 0)'
    )
    
    parser.add_argument(
        'delimiter',
        nargs='?',
        default=',',
        help='CSV delimiter character (default: ",")'
    )
    
    parser.add_argument(
        '--header',
        action='store_true',
        help='Show column headers'
    )
    
    parser.add_argument(
        '--count',
        action='store_true',
        help='Show count of extracted values'
    )
    
    args = parser.parse_args()
    
    # Validate file exists
    file_path = Path(args.filename)
    if not file_path.exists():
        print(f"Error: File '{args.filename}' does not exist")
        sys.exit(1)
    
    if not file_path.is_file():
        print(f"Error: '{args.filename}' is not a file")
        sys.exit(1)
    
    # Extract column data
    column_values = extract_csv_column(args.filename, args.column_index, args.delimiter)
    
    if not column_values:
        sys.exit(1)
    
    # Show headers if requested
    if args.header:
        try:
            with open(args.filename, newline="", encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=args.delimiter)
                header = next(csv_reader, None)
                if header:
                    print(f"Column headers: {header}")
                    print(f"Selected column {args.column_index}: '{header[args.column_index]}'")
                    print("-" * 50)
        except Exception as e:
            print(f"Warning: Could not read headers: {e}")
    
    # Display extracted values
    for i, value in enumerate(column_values, start=1):
        print(f"{i:3d}: {value}")
    
    # Show count if requested
    if args.count:
        print(f"\nTotal values extracted: {len(column_values)}")


if __name__ == "__main__":
    main()
