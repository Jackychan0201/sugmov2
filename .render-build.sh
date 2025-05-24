#!/usr/bin/env bash
# This will run during deployment

# Install Git LFS and pull LFS files
apt-get update && apt-get install -y git-lfs
git lfs install
git lfs pull

# Install dependencies
pip install -r requirements.txt
