#!/bin/bash

# Configuration
LOG_FILE="/tmp/trash/trash.log"

# Check if a filename was provided
if [[ "$#" -ne 1 ]]; then
    echo "Usage: $0 filename_or_partial_match" >&2
    exit 1
fi

# Find the most recent matching log entry
log_entry=$(grep "$1" "$LOG_FILE" | tail -n 1)

# Check if a match was found
if [[ -z "$log_entry" ]]; then
    echo "Error: No matching file found in trash log for '$1'." >&2
    exit 1
fi

# Parse the log entry
IFS=',' read -r original_path trash_path timestamp <<< "$log_entry"

# Handle conflicts by renaming the restored file if the original path is in use
if [[ -e "$original_path" ]]; then
    echo "Warning: File already exists at '$original_path'."
    original_path="${original_path}.restored"
    echo "Restoring to '$original_path' to avoid conflict."
fi

# Create the original parent directory if it doesn't exist
parent_dir=$(dirname "$original_path")
mkdir -p "$parent_dir"

# Restore the file
mv "$trash_path" "$original_path"
if [[ $? -eq 0 ]]; then
    echo "Successfully restored '$original_path' from trash."
else
    echo "Error: Failed to restore '$original_path'." >&2
fi
