#!/bin/bash

# Path to the marker file
MARKER_PATH="/var/run/first-run.marker"

# Check if the script has been run before by looking for the marker file
if [ -f "$MARKER_PATH" ]; then
    echo "Initialized already. Starting Bash..."
    exec /bin/bash
else
    echo "Initialize Pulumi..."
    echo "Logging in to Pulumi..."
    pulumi login

    echo "Creating Pulumi stacks..."
    pulumi stack select aws --create
    pulumi config set cloud_provider aws

    pulumi stack select --create gcp
    pulumi config set cloud_provider gcp
    pulumi config set gcp:project ${GCP_PROJECT_ID}

    # Creating the marker file
    touch "$MARKER_PATH"
    echo "Setup complete. Starting Bash..."
    exec /bin/bash
fi
