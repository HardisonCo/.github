#!/bin/bash

# Script to fix broken markdown links after renaming directories and files
# Usage: ./fix-markdown-links.sh [directory] [--dry-run]

# Default settings
DRY_RUN=false
DIR="."
THREADS=4  # Number of parallel threads to use

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

echo "Starting link fixing process:"
echo "  Directory: $DIR"
echo "  Dry run: $DRY_RUN"
echo "  Threads: $THREADS"
echo

# Create temp directory for tracking
TEMP_DIR=$(mktemp -d)
COUNTFILE="$TEMP_DIR/count"
FIXEDFILE="$TEMP_DIR/fixed"
PROGRESSFILE="$TEMP_DIR/progress"

echo "0" > "$COUNTFILE"
echo "0" > "$FIXEDFILE"
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

# Function to fix links in a markdown file
fix_links() {
  local FILE="$1"
  local needs_fixing=false
  local temp_file="${TEMP_DIR}/$(basename "$FILE").tmp"
  
  # Copy file to temp location
  cp "$FILE" "$temp_file"
  
  # 1. Fix directory links (replace uppercase with lowercase and underscores with hyphens)
  # Find markdown links [text](path/to/DIRECTORY/file.md)
  if grep -q -E "\[.*\]\(.*[A-Z_].*\)" "$FILE"; then
    # Replace directory names in links
    perl -pe 's/(\[.*?\]\(.*?)([A-Z_][^()]*?)(\))/$1.lc($2).$3/ge' "$temp_file" | \
    perl -pe 's/(\[.*?\]\(.*?)(_)(.*?\))/$1-$3/g' > "${temp_file}.new"
    mv "${temp_file}.new" "$temp_file"
    needs_fixing=true
  fi
  
  # 2. Fix file links (replace uppercase with lowercase and underscores with hyphens)
  # Find markdown links [text](path/to/FILE_NAME.md)
  if grep -q -E "\[.*\]\(.*[A-Z_][^/]*\.md\)" "$FILE"; then
    # Replace file names in links
    perl -pe 's/(\[.*?\]\(.*?)([A-Z_][^/()]*?\.md)(\))/$1.lc($2).$3/ge' "$temp_file" | \
    perl -pe 's/(\[.*?\]\(.*?)(_)(.*?\.md\))/$1-$3/g' > "${temp_file}.new"
    mv "${temp_file}.new" "$temp_file"
    needs_fixing=true
  fi
  
  # Only update if changes were made
  if [ "$needs_fixing" = true ]; then
    if [ "$DRY_RUN" = true ]; then
      echo "[Dry run] Fixing links in: '$FILE'"
      diff -u "$FILE" "$temp_file" || true
    else
      echo "Fixing links in: '$FILE'"
      cp "$temp_file" "$FILE"
    fi
    
    # Increment fixed count
    local FIXED=$(cat "$FIXEDFILE")
    FIXED=$((FIXED + 1))
    echo "$FIXED" > "$FIXEDFILE"
  fi
  
  # Increment count
  local COUNT=$(cat "$COUNTFILE")
  COUNT=$((COUNT + 1))
  echo "$COUNT" > "$COUNTFILE"
  
  update_progress
}

# Count total markdown files for progress bar
TOTAL_FILES=$(find "$DIR" -type f -name "*.md" | wc -l | tr -d ' ')
echo "Total files to process: $TOTAL_FILES"
echo

# Export function so it can be used with parallel
export -f fix_links update_progress show_progress
export COUNTFILE FIXEDFILE PROGRESSFILE TOTAL_FILES TEMP_DIR DRY_RUN

# Use GNU parallel if available, otherwise fallback to sequential
if command -v parallel >/dev/null 2>&1; then
  find "$DIR" -type f -name "*.md" | parallel -j "$THREADS" fix_links
else
  echo "GNU parallel not found, using sequential processing"
  find "$DIR" -type f -name "*.md" | while read -r FILE; do
    fix_links "$FILE"
  done
fi

# Get final counts
COUNT=$(cat "$COUNTFILE")
FIXED=$(cat "$FIXEDFILE")

# Clean up temp files
rm -rf "$TEMP_DIR"

echo
echo
echo "Link fixing complete!"
echo "Files processed: $COUNT"
echo "Files with fixed links: $FIXED"
if [ "$DRY_RUN" = true ]; then
  echo "(No actual changes were made - dry run mode)"
fi