#!/bin/bash

# Your GitHub username
USERNAME="dakuranga"

# Your Personal Access Token
TOKEN="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"

# URL of the remote repository
REPO_URL="https://github.com/dakuranga/jobber"

# Branch name
BRANCH="main"

# Configure Git to use your credentials
git config credential.helper store
echo "https://$USERNAME:$TOKEN@github.com" > ~/.git-credentials

# Pull changes from the specified branch
git pull origin "$BRANCH"

# Remove the stored credentials
rm ~/.git-credentials
