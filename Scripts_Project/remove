#!/bin/bash

# Configuration
TRASH_DIR="/tmp/trash"
LOG_FILE="$TRASH_DIR/trash.log"

# Function to display usage message
usage() {
    echo "Usage: $0 [-r] file_or_directory [file_or_directory...]" >&2
    exit 1
}

# Check for -r flag
recursive=false
if [[ "$1" == "-r" ]]; then
    recursive=true
    shift
fi

# Check if there are any files to delete
if [[ "$#" -eq 0 ]]; then
    usage
fi

# Process each file or directory
for item in "$@"; do
    # Handle non-existent files
    if [[ ! -e "$item" ]]; then
        echo "Error: '$item' not found." >&2
        continue
    fi

    # Handle directory deletion without -r flag
    if [[ -d "$item" ]] && [[ "$recursive" == false ]]; then
        echo "Error: '$item' is a directory. Use -r for recursive deletion." >&2
        continue
    fi

    # Generate a unique trash name using a timestamp
    timestamp=$(date +"%Y%m%d%H%M%S")
    filename=$(basename "$item")
    trash_path="$TRASH_DIR/${filename}.${timestamp}"
    original_path=$(realpath "$item")

    # Move the item to the trash
    mv "$item" "$trash_path"
    if [[ $? -eq 0 ]]; then
        echo "Moved '$original_path' to trash as '$trash_path'"
        # Log the action
        echo "$original_path,$trash_path,$(date +"%Y-%m-%d %H:%M:%S")" >> "$LOG_FILE"
    else
        echo "Error: Failed to move '$item' to trash." >&2
    fi
done
