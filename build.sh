#!/bin/bash
# Install system dependencies
apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
    build-essential \
    python3-dev

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt 