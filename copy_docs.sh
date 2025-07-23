#!/bin/bash

# Script to copy all .md files from a source directory to a destination directory
# while preserving the subdirectory hierarchy

# Function to display usage information
usage() {
    echo "Usage: $0 <source_directory> <destination_directory>"
    echo ""
    echo "Arguments:"
    echo "  source_directory      Path to the root directory containing documentation files"
    echo "  destination_directory Path where the .md files should be copied"
    echo ""
    echo "Description:"
    echo "  This script recursively finds all .md files in the source directory"
    echo "  and copies them to the destination directory while preserving the"
    echo "  original subdirectory structure."
    echo ""
    echo "Example:"
    echo "  $0 /path/to/docs /path/to/backup/docs"
    exit 1
}

# Check if correct number of arguments provided
if [ $# -ne 2 ]; then
    echo "Error: Incorrect number of arguments."
    usage
fi

SOURCE_DIR="$1"
DEST_DIR="$2"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist."
    exit 1
fi

# Convert to absolute paths to avoid issues with relative paths
SOURCE_DIR=$(realpath "$SOURCE_DIR")

# For destination, create the directory first if it doesn't exist, then get realpath
mkdir -p "$DEST_DIR"
DEST_DIR=$(realpath "$DEST_DIR")

echo "Copying .md files from '$SOURCE_DIR' to '$DEST_DIR'..."

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Counter for copied files
copied_files=0

# Find all .md files and copy them while preserving directory structure
while IFS= read -r -d '' file; do
    # Get the relative path from source directory
    relative_path="${file#$SOURCE_DIR/}"
    
    # Create the destination path
    dest_file="$DEST_DIR/$relative_path"
    
    # Create the destination directory if it doesn't exist
    dest_dir=$(dirname "$dest_file")
    mkdir -p "$dest_dir"
    
    # Copy the file
    if cp "$file" "$dest_file"; then
        echo "Copied: $relative_path"
        ((copied_files++))
    else
        echo "Error: Failed to copy $relative_path"
    fi
done < <(find "$SOURCE_DIR" -type f -name "*.md" -print0)

echo ""
echo "Copy operation completed."
echo "Total files copied: $copied_files"

# Display summary of what was copied
if [ $copied_files -gt 0 ]; then
    echo ""
    echo "Directory structure created in '$DEST_DIR':"
    find "$DEST_DIR" -type d | sort
fi
