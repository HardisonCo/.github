#!/bin/bash

# Script to rename directories to lowercase-hyphenated format
# Usage: ./rename-directories.sh [directory] [--dry-run]

# Default settings
DRY_RUN=false
DIR="."
EXCLUDE_DIRS=".git .claude"

# Parse arguments
for arg in "$@"; do
  if [ "$arg" = "--dry-run" ]; then
    DRY_RUN=true
  elif [ "${arg:0:1}" != "-" ]; then
    DIR="$arg"
  fi
done

echo "Starting directory renaming process:"
echo "  Directory: $DIR"
echo "  Dry run: $DRY_RUN"
echo

# Create temp files to store counts
COUNTFILE=$(mktemp)
echo "0" > "$COUNTFILE"
RENAMEFILE=$(mktemp)
echo "0" > "$RENAMEFILE"

# Function to check if a directory should be excluded
should_exclude() {
  local dir_name="$(basename "$1")"
  for exclude in $EXCLUDE_DIRS; do
    if [ "$dir_name" = "$exclude" ]; then
      return 0  # true, should exclude
    fi
  done
  return 1  # false, should not exclude
}

# Function to rename a directory
rename_directory() {
  local DIR_PATH="$1"
  
  # Skip excluded directories
  if should_exclude "$DIR_PATH"; then
    return
  fi
  
  # Extract parent directory and directory name
  local PARENT_DIR=$(dirname "$DIR_PATH")
  local DIR_NAME=$(basename "$DIR_PATH")
  
  # Convert to lowercase hyphenated
  local NEW_NAME=$(echo "$DIR_NAME" | tr '[:upper:]' '[:lower:]' | tr '_' '-' | tr ' ' '-')
  local NEW_PATH="$PARENT_DIR/$NEW_NAME"
  
  # Increment count
  local COUNT=$(cat "$COUNTFILE")
  COUNT=$((COUNT + 1))
  echo "$COUNT" > "$COUNTFILE"
  
  # Show progress
  if [ $((COUNT % 10)) -eq 0 ]; then
    echo "Processed $COUNT directories so far..."
  fi
  
  # Only rename if different
  if [ "$DIR_PATH" != "$NEW_PATH" ]; then
    if [ "$DRY_RUN" = true ]; then
      echo "[Dry run] Renaming directory: '$DIR_PATH' -> '$NEW_PATH'"
    else
      echo "Renaming directory: '$DIR_PATH' -> '$NEW_PATH'"
      # Create a temporary directory name to avoid case sensitivity issues on some filesystems
      local TEMP_PATH="${PARENT_DIR}/.tmp_rename_${RANDOM}"
      mv -- "$DIR_PATH" "$TEMP_PATH" && mv -- "$TEMP_PATH" "$NEW_PATH"
    fi
    
    # Increment renamed count
    local RENAMED=$(cat "$RENAMEFILE")
    RENAMED=$((RENAMED + 1))
    echo "$RENAMED" > "$RENAMEFILE"
  fi
}

# Process directories bottom-up (deepest first)
find "$DIR" -type d -depth | while read -r DIR_PATH; do
  rename_directory "$DIR_PATH"
done

# Get final counts
COUNT=$(cat "$COUNTFILE")
RENAMED=$(cat "$RENAMEFILE")

# Clean up temp files
rm -f "$COUNTFILE" "$RENAMEFILE"

echo
echo "Directory renaming complete!"
echo "Directories processed: $COUNT"
echo "Directories renamed: $RENAMED"
if [ "$DRY_RUN" = true ]; then
  echo "(No actual changes were made - dry run mode)"
fi