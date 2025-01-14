#!/bin/bash

# Script: 6_receiveDirs_remoteToLocal.sh
# Description: Copies a directory from a remote server to the local machine using scp.
# Usage: ./6_receiveDirs_remoteToLocal.sh username remote_host

# Function to display usage
usage() {
    echo "Usage: $0 username remote_host"
    exit 1
}

# Check for minimum number of arguments
if [ "$#" -lt 2 ]; then 
    usage
fi

USERNAME="$1"
REMOTE_HOST="$2"
REMOTE_BASE_DIR="/scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests"
LOCAL_BASE_DIR="/media/dgamdha/dataSSD/dhruv_ssd/ISU/PhD/Projects/LEAP_HI/runs/adm_runs/tests/set2"
DIRS_TO_COPY=(  "frontera_run_012" 
                "frontera_run_013" 
                "frontera_run_015"
                "frontera_run_016")

SUCCESS=true

confirm_remote_dirs() {
    local user="$1"
    local host="$2"
    for DIR in "${DIRS_TO_COPY[@]}"; do
        if ssh "${user}@${host}" "[ -d '${REMOTE_BASE_DIR}/${DIR}' ]"; then
            echo "Directory exists on remote: ${REMOTE_BASE_DIR}/${DIR}"
        else
            echo "Warning: Directory does not exist on remote: ${REMOTE_BASE_DIR}/${DIR}" >&2
        fi
    done
}

confirm_remote_dirs

# Loop through each directory and perform scp
for DIR in "${DIRS_TO_COPY[@]}"; do
    echo "Copying $DIR from $REMOTE_HOST..."
    
    scp -r "${USERNAME}@${REMOTE_HOST}:${REMOTE_BASE_DIR}/${DIR}" "${LOCAL_BASE_DIR}/"
    
    # Check if scp was successful for the current directory
    if [ $? -ne 0 ]; then
        echo "Error: Failed to copy ${DIR}."
        SUCCESS=false
    else
        echo "Successfully copied ${DIR}."
    fi
done

# Final status message
if [ "$SUCCESS" = true ]; then
    echo "All directories copied successfully."
    exit 0
else
    echo "Some directories failed to copy. Please check the errors above."
    exit 1
fi