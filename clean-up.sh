#!/bin/bash

# Clean-up script to convert file/directory names and remove redundant files
# Usage: ./CLEAN-UP.sh [directory] [--dry-run]

# Default settings
DRY_RUN=false
DIR="."
THREADS=33  # Number of parallel threads to use

# Parse arguments
for arg in "$@"; do
  if [ "$arg" = "--dry-run" ]; then
    DRY_RUN=true
  elif [[ "$arg" =~ ^--threads=([0-9]+)$ ]]; then
    THREADS="${BASH_REMATCH[1]}"
  elif [ "${arg:0:1}" != "-" ]; then
    DIR="$arg"
  fi
done

echo "Starting cleanup process:"
echo "  Directory: $DIR"
echo "  Dry run: $DRY_RUN"
echo "  Threads: $THREADS"
echo

# Create temp directory for tracking
TEMP_DIR=$(mktemp -d)
COUNTFILE="$TEMP_DIR/count"
RENAMEFILE="$TEMP_DIR/renamed"
REMOVEDFILE="$TEMP_DIR/removed"
PROGRESSFILE="$TEMP_DIR/progress"

echo "0" > "$COUNTFILE"
echo "0" > "$RENAMEFILE"
echo "0" > "$REMOVEDFILE"
echo "0" > "$PROGRESSFILE"

# Function to show progress bar
show_progress() {
  local total=$1
  local current=$2
  local width=50
  local percent=$((current * 100 / total))
  local completed=$((width * current / total))
  local remaining=$((width - completed))
  
  printf "\r[%${completed}s%${remaining}s] %d%% (%d/%d)" \
         "$(printf '%0.s#' $(seq 1 $completed))" \
         "$(printf '%0.s-' $(seq 1 $remaining))" \
         "$percent" "$current" "$total"
}

# Function to update progress
update_progress() {
  local progress=$(cat "$PROGRESSFILE")
  progress=$((progress + 1))
  echo "$progress" > "$PROGRESSFILE"
  
  if [ -n "$TOTAL_FILES" ]; then
    show_progress "$TOTAL_FILES" "$progress"
  fi
}

# This function does the actual work of renaming
process_file() {
  local FILE="$1"
  
  # Extract directory and base name
  DIRNAME=$(dirname "$FILE")
  FILENAME=$(basename "$FILE")
  EXTENSION="${FILENAME##*.}"
  BASENAME="${FILENAME%.*}"
  
  # Check if this is a copy file that should be removed
  if [[ "$BASENAME" =~ .*-COPY$ ]] || [[ "$BASENAME" =~ .*-COPY-[0-9]+$ ]] || 
     [[ "$BASENAME" =~ ".*copy$" ]] || [[ "$BASENAME" =~ ".*Copy$" ]]; then
    if [ "$DRY_RUN" = true ]; then
      echo "[Dry run] Removing: '$FILE'"
    else
      echo "Removing: '$FILE'"
      rm -f -- "$FILE"
    fi
    
    # Increment removed count
    local REMOVED=$(cat "$REMOVEDFILE")
    REMOVED=$((REMOVED + 1))
    echo "$REMOVED" > "$REMOVEDFILE"
    update_progress
    return
  fi
  
  # Convert to lowercase hyphenated
  NEW_BASENAME=$(echo "$BASENAME" | tr '[:upper:]' '[:lower:]' | tr '_' '-' | sed 's/ /-/g')
  NEW_PATH="$DIRNAME/$NEW_BASENAME.$EXTENSION"
  
  # Increment count
  local COUNT=$(cat "$COUNTFILE")
  COUNT=$((COUNT + 1))
  echo "$COUNT" > "$COUNTFILE"
  
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
  
  update_progress
}

# Process directories to lowercase hyphenated
process_directory() {
  local DIR_PATH="$1"
  
  # Skip excluded directories
  if [[ "$DIR_PATH" == *"/.git"* ]] || [[ "$DIR_PATH" == *"/.claude"* ]]; then
    update_progress
    return
  fi
  
  # Extract parent directory and directory name
  local PARENT_DIR=$(dirname "$DIR_PATH")
  local DIR_NAME=$(basename "$DIR_PATH")
  
  # Convert to lowercase hyphenated
  local NEW_NAME=$(echo "$DIR_NAME" | tr '[:upper:]' '[:lower:]' | tr '_' '-' | tr ' ' '-')
  local NEW_PATH="$PARENT_DIR/$NEW_NAME"
  
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
  
  update_progress
}

# Count total files and directories for progress bar
TOTAL_FILES=$(find "$DIR" -type f -o -type d | wc -l | tr -d ' ')
echo "Total items to process: $TOTAL_FILES"

# Process directories bottom-up (deepest first)
echo "Phase 1: Renaming directories to lowercase hyphenated format..."
find "$DIR" -type d -depth | while read -r DIR_PATH; do
  process_directory "$DIR_PATH"
done

# Reset progress for files
echo "0" > "$PROGRESSFILE"
echo
echo "Phase 2: Processing files..."

# Export function so it can be used with parallel
export -f process_file update_progress
export COUNTFILE RENAMEFILE REMOVEDFILE PROGRESSFILE TOTAL_FILES DRY_RUN

# Use GNU parallel if available, otherwise fallback to sequential
if command -v parallel >/dev/null 2>&1; then
  find "$DIR" -type f | parallel -j "$THREADS" process_file
else
  echo "GNU parallel not found, using sequential processing"
  find "$DIR" -type f | while read -r FILE; do
    process_file "$FILE"
  done
fi

# Get final counts
COUNT=$(cat "$COUNTFILE")
RENAMED=$(cat "$RENAMEFILE")
REMOVED=$(cat "$REMOVEDFILE")

# Clean up temp files
rm -rf "$TEMP_DIR"

echo
echo
echo "Cleanup complete!"
echo "Files processed: $COUNT"
echo "Items renamed: $RENAMED"
echo "Files removed: $REMOVED"
if [ "$DRY_RUN" = true ]; then
  echo "(No actual changes were made - dry run mode)"
fi

echo
echo "Next steps:"
echo "1. Run './fix-markdown-links.sh' to update broken links"
echo "2. Review changes with 'git status'"
echo "3. Commit changes with 'git commit -am \"Update file structure\"'"
