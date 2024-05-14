#!/bin/bash

# Define the directory path
directory="/Users/tzhenghao/Downloads/SanFranciscoBayArea"

# Define the suffix to add to file names
suffix="(2).HEIC"

# Change to the specified directory
cd "$directory" || exit

# Loop through all files in the directory
for file in *; do
    # Check if the file is a regular file (not a directory)
    if [ -f "$file" ]; then
        # Add the suffix to the file name
        new_file_name="${file}${suffix}"
        # Rename the file with the new name
        mv "$file" "$new_file_name"
        echo "Renamed $file to $new_file_name"
    fi
  done
