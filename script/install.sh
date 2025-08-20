#!/bin/bash

set -e  # Exit on any error

echo "🔧 Installing diffmanifests and building binary..."

# Get the Ubuntu version for naming (from environment variable or default)
UBUNTU_VERSION=${UBUNTU_VERSION:-"local"}
BINARY_NAME="diffmanifests"
if [ "$UBUNTU_VERSION" != "local" ]; then
    BINARY_NAME="diffmanifests-linux-ubuntu${UBUNTU_VERSION}"
fi

# Update pip and install build dependencies
echo "📦 Installing dependencies..."
python3 -m pip install --upgrade pip
pip3 install pyinstaller

# Install the package in development mode for proper imports
echo "🏗️ Installing diffmanifests package..."
pip3 install -e .

# Build binary with comprehensive configuration
echo "🚀 Building binary with PyInstaller..."
pyinstaller --onefile \
  --clean \
  --name "$BINARY_NAME" \
  --add-data "diffmanifests/config:diffmanifests/config" \
  --hidden-import diffmanifests \
  --hidden-import diffmanifests.config \
  --hidden-import diffmanifests.cmd \
  --hidden-import diffmanifests.cmd.argument \
  --hidden-import diffmanifests.cmd.banner \
  --hidden-import diffmanifests.cmd.version \
  --hidden-import diffmanifests.differ \
  --hidden-import diffmanifests.differ.differ \
  --hidden-import diffmanifests.gerrit \
  --hidden-import diffmanifests.gerrit.gerrit \
  --hidden-import diffmanifests.gitiles \
  --hidden-import diffmanifests.gitiles.gitiles \
  --hidden-import diffmanifests.logger \
  --hidden-import diffmanifests.logger.logger \
  --hidden-import diffmanifests.printer \
  --hidden-import diffmanifests.printer.printer \
  --hidden-import diffmanifests.proto \
  --hidden-import diffmanifests.proto.proto \
  --hidden-import diffmanifests.querier \
  --hidden-import diffmanifests.querier.querier \
  --hidden-import colorama \
  --hidden-import requests \
  --hidden-import xmltodict \
  --hidden-import json \
  --hidden-import sys \
  --hidden-import os \
  diff.py

# Test the binary
echo "🧪 Testing the binary..."
if [ -f "./dist/$BINARY_NAME" ]; then
    chmod +x "./dist/$BINARY_NAME"
    echo "✅ Binary built successfully: ./dist/$BINARY_NAME"
    echo "🔍 Testing binary help..."
    "./dist/$BINARY_NAME" --help
    echo "🎉 Binary test passed!"
else
    echo "❌ Binary build failed - file not found: ./dist/$BINARY_NAME"
    exit 1
fi

echo "✅ Installation and binary build completed successfully!"
