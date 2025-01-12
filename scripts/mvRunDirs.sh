#!/bin/bash

# Script: mvRunDirs.sh
# Description: Moves specified 'frontera_run_XXX' directories from the source path to the destination path.
# Usage: ./mvRunDirs.sh

# --- Configuration ---

# Array of directory names to move
RUN_DIRS=("frontera_run_001" "frontera_run_002" "frontera_run_003" "frontera_run_004" "frontera_run_005" "frontera_run_006" "frontera_run_007" "frontera_run_008" "frontera_run_009" "frontera_run_010" "frontera_run_011" "frontera_run_012" "frontera_run_013" "frontera_run_014" "frontera_run_015" "frontera_run_016" "frontera_run_017" "frontera_run_018" "frontera_run_019" "frontera_run_020")

# Base source and destination directories
SOURCE_BASE_DIR="/scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests"
DEST_BASE_DIR="/work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1"

# Enable or disable confirmation prompt before moving
CONFIRM=true

# --- Function Definitions ---

# Function to display script usage
usage() {
    echo "Usage: $0"
    echo "Description: Moves specified 'frontera_run_XXX' directories from the source path to the destination path."
    exit 1
}

# Function to confirm moving directories
confirm_move() {
    if [ "$CONFIRM" = true ]; then
        echo "The following 'frontera_run_XXX' directories will be moved from:"
        echo "Source: $SOURCE_BASE_DIR"
        echo "Destination: $DEST_BASE_DIR"
        echo
        echo "Directories to move:"
        for DIR in "${RUN_DIRS[@]}"; do
            echo "- $DIR"
        done
        echo
        read -p "Are you sure you want to proceed? (y/n): " response
        case "$response" in
            [yY][eE][sS]|[yY]) 
                echo "Proceeding with moving directories..."
                ;;
            *)
                echo "Operation canceled by user."
                exit 0
                ;;
        esac
    fi
}

# Function to move a single directory
move_directory() {
    local dir_name="$1"
    local source_dir="${SOURCE_BASE_DIR}/${dir_name}"
    local dest_dir="${DEST_BASE_DIR}/${dir_name}"

    echo "Processing ${dir_name}..."

    if [ -d "$source_dir" ]; then
        # Create destination base directory if it doesn't exist
        if [ ! -d "$DEST_BASE_DIR" ]; then
            echo "Destination base directory does not exist. Creating: $DEST_BASE_DIR"
            mkdir -p "$DEST_BASE_DIR"
            if [ $? -ne 0 ]; then
                echo "Error: Failed to create destination base directory: $DEST_BASE_DIR" >&2
                return 1
            fi
        fi

        # Check if destination directory already exists to prevent overwriting
        if [ -d "$dest_dir" ]; then
            echo "Error: Destination directory already exists: $dest_dir. Skipping." >&2
            return 1
        fi

        # Move the directory
        mv "$source_dir" "$dest_dir"
        if [ $? -eq 0 ]; then
            echo "Successfully moved ${dir_name} to set1."
            return 0
        else
            echo "Error: Failed to move ${dir_name}." >&2
            return 1
        fi
    else
        echo "Warning: Source directory does not exist: $source_dir. Skipping." >&2
        return 1
    fi
}

# --- Main Script Execution ---

# Optional: Call usage function if needed (e.g., if adding arguments in the future)
# usage

# Confirm move if enabled
confirm_move

# Initialize counters for summary
success_count=0
failure_count=0
failed_dirs=()

# Iterate through each directory name and perform the move
for DIR in "${RUN_DIRS[@]}"; do
    move_directory "$DIR"
    if [ $? -eq 0 ]; then
        ((success_count++))
    else
        ((failure_count++))
        failed_dirs+=("$DIR")
    fi
done

# Summary of operations
echo "========================================"
echo "Move Operation Summary:"
echo "-----------------------"
echo "Successfully moved directories: $success_count"
echo "Failed to move directories: $failure_count"

if [ "$failure_count" -ne 0 ]; then
    echo "The following directories failed to move:"
    for DIR in "${failed_dirs[@]}"; do
        echo "- $DIR"
    done
    exit 1
else
    echo "All specified directories have been moved successfully."
    exit 0
fi



# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_001 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_001
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_002 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_002
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_003 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_003
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_004 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_004
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_005 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_005
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_006 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_006
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_007 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_007
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_008 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_008
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_009 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_009
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_010 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_010
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_011 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_011
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_012 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_012
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_013 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_013
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_014 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_014
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_015 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_015
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_016 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_016
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_017 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_017
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_018 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_018
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_019 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_019
# mv /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_020 /work2/09374/dgamdha/frontera/projects/leaphi/adm_runs/set1/frontera_run_020