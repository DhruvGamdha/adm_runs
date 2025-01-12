#!/bin/bash

# Script: receiveDirs_remoteToLocal.sh
# Description: Copies a directory from a remote server to the local machine using scp.
# Usage: ./receiveDirs_remoteToLocal.sh username remote_host

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
REMOTE_BASE_DIR="/path/to/remote/directory"
LOCAL_BASE_DIR="/path/to/local/directory"
DIRS_TO_COPY=("frontera_run_001" "frontera_run_002" "frontera_run_003")

SUCCESS=true

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