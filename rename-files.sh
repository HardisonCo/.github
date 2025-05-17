#!/bin/bash

# Script to rename files, replacing underscores with hyphens and converting to lowercase
# Usage: ./rename-files.sh [directory] [--dry-run]

# Default settings
DRY_RUN=false
DIR="."

# Parse arguments
for arg in "$@"; do
  if [ "$arg" = "--dry-run" ]; then
    DRY_RUN=true
  elif [ "${arg:0:1}" != "-" ]; then
    DIR="$arg"
  fi
done

echo "Starting file renaming process:"
echo "  Directory: $DIR"
echo "  Dry run: $DRY_RUN"
echo

# Create temp files to store counts
COUNTFILE=$(mktemp)
echo "0" > "$COUNTFILE"
RENAMEFILE=$(mktemp)
echo "0" > "$RENAMEFILE"

# This function does the actual work of renaming
process_file() {
  local FILE="$1"
  
  # Extract directory and base name
  DIRNAME=$(dirname "$FILE")
  FILENAME=$(basename "$FILE")
  EXTENSION="${FILENAME##*.}"
  BASENAME="${FILENAME%.*}"
  
  # Convert to lowercase hyphenated
  NEW_BASENAME=$(echo "$BASENAME" | tr '[:upper:]' '[:lower:]' | tr '_' '-' | sed 's/ /-/g')
  NEW_PATH="$DIRNAME/$NEW_BASENAME.$EXTENSION"
  
  # Increment count
  local COUNT=$(cat "$COUNTFILE")
  COUNT=$((COUNT + 1))
  echo "$COUNT" > "$COUNTFILE"
  
  # Show progress
  if [ $((COUNT % 50)) -eq 0 ]; then
    echo "Processed $COUNT files so far..."
  fi
  
  # Only rename if different
  if [ "$FILE" != "$NEW_PATH" ]; then
    if [ "$DRY_RUN" = true ]; then
      echo "[Dry run] Renaming: '$FILE' -> '$NEW_PATH'"
    else
      echo "Renaming: '$FILE' -> '$NEW_PATH'"
      mv -- "$FILE" "$NEW_PATH"
    fi
    
    # Increment renamed count
    local RENAMED=$(cat "$RENAMEFILE")
    RENAMED=$((RENAMED + 1))
    echo "$RENAMED" > "$RENAMEFILE"
  fi
}

# Export function so it can be used with xargs
export -f process_file
export COUNTFILE
export RENAMEFILE
export DRY_RUN

# Loop through all files and rename them
find "$DIR" -type f | while read -r FILE; do
  process_file "$FILE"
done

# Get final counts
COUNT=$(cat "$COUNTFILE")
RENAMED=$(cat "$RENAMEFILE")

# Clean up temp files
rm -f "$COUNTFILE" "$RENAMEFILE"

echo
echo "Renaming complete!"
echo "Files processed: $COUNT"
echo "Files renamed: $RENAMED"
if [ "$DRY_RUN" = true ]; then
  echo "(No actual changes were made - dry run mode)"
fi