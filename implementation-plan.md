# Directory and File Standardization Implementation Plan

This plan outlines the steps to standardize directory and file naming conventions across the project, cleanup duplicate files, and fix broken links resulting from these changes.

## Objectives

1. Convert all directory names to lowercase hyphenated format
2. Convert all file names to lowercase hyphenated format
3. Replace underscores with hyphens in all file and directory names
4. Remove redundant files with "copy" in their names
5. Fix broken markdown links resulting from these changes
6. Implement multi-threaded processing and progress monitoring

## Implementation Steps

### 1. Preparation

- Create backup of the entire directory structure
- Run all scripts with `--dry-run` flag to identify potential issues
- Verify there are no critical issues that would block implementation

```bash
# Create backup
cp -r /path/to/directory /path/to/backup

# Run dry runs to verify each script
./CLEAN-UP.sh --dry-run
```

### 2. Directory Standardization

- Run the renaming script to convert all directories to lowercase hyphenated format
- The script processes directories from deepest to shallowest to avoid conflicts

```bash
./CLEAN-UP.sh --threads=8
```

### 3. Cleanup Phase

- Remove duplicate files with `-COPY` or similar in their names
- Convert filenames to lowercase hyphenated format
- Fix broken markdown links resulting from the renaming

```bash
# After running CLEAN-UP.sh, run link fixing
./fix-markdown-links.sh --threads=8
```

### 4. Verification

- Run integrity checks to ensure all links are working
- Check for any remaining uppercase or underscore files
- Verify documentation builds correctly after changes

```bash
# Verify no uppercase or underscore files remain
find . -type f -name "*[A-Z]*" -o -name "*_*" | grep -v node_modules

# Verify documentation builds
cd /path/to/docs && npm run build
```

### 5. Rollback Plan

In case of issues, the implementation can be rolled back using the backup created in step 1:

```bash
# Rollback if needed
rm -rf /path/to/directory
cp -r /path/to/backup /path/to/directory
```

## Implementation Timeline

1. **Preparation & Dry Run**: 30 minutes
2. **Directory Standardization**: 1 hour
3. **File Cleanup & Renaming**: 2 hours
4. **Link Fixing**: 1 hour
5. **Verification**: 1 hour

Total estimated time: 5.5 hours

## Implementation Scripts

Three main scripts have been created to handle the implementation:

1. **CLEAN-UP.sh** - Main script that handles:
   - Converting directories to lowercase hyphenated format
   - Converting files to lowercase hyphenated format
   - Removing duplicate -COPY files
   - Multi-threading for faster processing
   - Progress monitoring with visual progress bar

2. **rename-directories.sh** - Standalone script for directory renaming only

3. **rename-files.sh** - Standalone script for file renaming only

4. **fix-markdown-links.sh** - Standalone script to fix broken markdown links

## Usage Instructions

```bash
# Full cleanup with default settings
./CLEAN-UP.sh

# Cleanup with 8 threads
./CLEAN-UP.sh --threads=8

# Dry run to see what would be changed
./CLEAN-UP.sh --dry-run

# Fix markdown links only
./fix-markdown-links.sh

# Fix markdown links with more threads
./fix-markdown-links.sh --threads=8
```

## Monitoring and Logging

All scripts provide real-time progress monitoring:
- Visual progress bar showing percentage complete
- Counts of items processed, renamed, and removed
- Summary statistics upon completion

## Post-Implementation Tasks

After successful implementation:
1. Commit changes to version control
2. Update any documentation referencing file or directory paths
3. Notify team members of the changes
4. Consider automating these checks for future contributions