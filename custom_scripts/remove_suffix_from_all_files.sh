#!/bin/bash

# Define the directory path
directory="/Users/tzhenghao/Downloads/SanFranciscoBayArea"

# Define the suffix to remove from file names
suffix=".HEIC"

# Change to the specified directory
cd "$directory" || exit

# Loop through all files in the directory
for file in *"$suffix"; do
    # Check if the file is a regular file (not a directory)
    if [ -f "$file" ]; then
        # Remove the suffix from the file name
        new_file_name="${file%"$suffix"}"
        # Rename the file with the new name
        mv "$file" "$new_file_name"
        echo "Renamed $file to $new_file_name"
    fi
done

