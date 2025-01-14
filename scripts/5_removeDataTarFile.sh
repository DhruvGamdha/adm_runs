#!/bin/bash

# Script: 5_removeDataTarFile.sh
# Description: Removes specified 'data.tar.gz' files within 'frontera_run_XXX' directories under 'tests'.
# Usage: ./5_removeDataTarFile.sh

# --- Configuration ---

# Array of directory names to remove 'data.tar.gz' files from
DIRS_TO_REMOVE=("frontera_run_012" 
                "frontera_run_013" 
                "frontera_run_015"
                "frontera_run_016")

# Base directory path where 'frontera_run_XXX' directories reside
BASE_DIR="tests"

# Enable or disable confirmation prompt before deletion (true/false)
CONFIRM=true

# --- Function Definitions ---

# Function to display script usage
usage() {
    echo "Usage: $0"
    echo "Description: Removes specified 'data.tar.gz' files within 'frontera_run_XXX' directories under 'tests'."
    exit 1
}

# Function to confirm deletion (if CONFIRM is true)
confirm_deletion() {
    if [ "$CONFIRM" = true ]; then
        echo "The following 'data.tar.gz' files will be removed:"
        for DIR in "${DIRS_TO_REMOVE[@]}"; do
            echo "${BASE_DIR}/${DIR}/data.tar.gz"
        done
        echo
        read -p "Are you sure you want to proceed? (y/n): " response
        case "$response" in
            [yY][eE][sS]|[yY]) 
                echo "Proceeding with deletion..."
                ;;
            *)
                echo "Operation canceled by user."
                exit 0
                ;;
        esac
    fi
}

# --- Main Script Execution ---

# Optional: Call usage function if needed (e.g., if adding arguments in the future)
# usage

# Confirm deletion if enabled
confirm_deletion

# Initialize counters for summary
success_count=0
failure_count=0
failed_dirs=()

# Iterate through each directory and remove 'data.tar.gz' files
for DIR in "${DIRS_TO_REMOVE[@]}"; do
    TARGET_DIR="${BASE_DIR}/${DIR}/data.tar.gz"
    echo "Processing: ${TARGET_DIR}"
    
    if [ -f "$TARGET_DIR" ]; then
        rm -rf "$TARGET_DIR"
        if [ $? -eq 0 ]; then
            echo "Successfully removed: ${TARGET_DIR}"
            ((success_count++))
        else
            echo "Error: Failed to remove ${TARGET_DIR}" >&2
            ((failure_count++))
            failed_dirs+=("$TARGET_DIR")
        fi
    else
        echo "Warning: Directory does not exist, skipping: ${TARGET_DIR}"
    fi
    
    echo "----------------------------------------"
done

# Summary of operations
echo "Deletion Summary:"
echo "-----------------"
echo "Successfully removed directories: $success_count"
echo "Failed to remove directories: $failure_count"

if [ "$failure_count" -ne 0 ]; then
    echo "Directories that failed to remove:"
    for failed_dir in "${failed_dirs[@]}"; do
        echo "- $failed_dir"
    done
    exit 1
else
    echo "All specified directories have been removed successfully."
    exit 0
fi

    

# rm -rf tests/frontera_run_002/data


# rm -rf tests/frontera_run_005/data
# rm -rf tests/frontera_run_006/data
# rm -rf tests/frontera_run_007/data

# rm -rf tests/frontera_run_009/data
# rm -rf tests/frontera_run_010/data
# rm -rf tests/frontera_run_011/data
# rm -rf tests/frontera_run_012/data

# rm -rf tests/frontera_run_014/data


# rm -rf tests/frontera_run_017/data
