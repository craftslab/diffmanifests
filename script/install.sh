#!/bin/bash

set -e  # Exit on any error

echo "🔧 Installing diffmanifests and building binary..."

# Get the Ubuntu version for naming (from environment variable or default)
UBUNTU_VERSION=${UBUNTU_VERSION:-"local"}
BINARY_NAME="diffmanifests"
if [ "$UBUNTU_VERSION" != "local" ]; then
    BINARY_NAME="diffmanifests-linux-ubuntu${UBUNTU_VERSION}"
fi

# Function to check if Python has shared library support
has_shared_lib() {
    local python_bin=$1
    $python_bin -c "import sysconfig; import sys; sys.exit(0 if sysconfig.get_config_var('Py_ENABLE_SHARED') == 1 else 1)" 2>/dev/null
    return $?
}

# Detect Python binary with shared library support
# Priority: setup-python's python > system python3 > /usr/bin/python3
PYTHON_BIN=""
PYTHON_CANDIDATES=("python" "python3" "/usr/bin/python3")

echo "🔍 Searching for Python with shared library support..."
for candidate in "${PYTHON_CANDIDATES[@]}"; do
    if command -v $candidate &> /dev/null; then
        echo "   Checking: $candidate ($(command -v $candidate 2>/dev/null || echo $candidate))"
        if has_shared_lib $candidate; then
            PYTHON_BIN=$candidate
            echo "✅ Found compatible Python: $PYTHON_BIN"
            break
        else
            echo "   ❌ No shared library support"
        fi
    fi
done

# Fallback if no Python with shared library found
if [ -z "$PYTHON_BIN" ]; then
    echo "⚠️  No Python with shared library found, trying default python3..."
    PYTHON_BIN="python3"
fi

# Display Python information
PYTHON_VERSION=$($PYTHON_BIN --version 2>&1 | awk '{print $2}')
PYTHON_PATH=$(which $PYTHON_BIN 2>/dev/null || echo $PYTHON_BIN)
echo "📍 Using Python: $PYTHON_PATH"
echo "📍 Python version: $PYTHON_VERSION"

# Determine pip install flags based on environment
# In GitHub Actions with setup-python, we don't need --break-system-packages
# In dev containers or system Python, we might need it
PIP_FLAGS=""
if [[ -n "${GITHUB_ACTIONS}" ]]; then
    echo "📍 Running in GitHub Actions"
    PIP_FLAGS=""
else
    echo "📍 Running in local/dev environment"
    # Try to detect if we need --break-system-packages
    if $PYTHON_BIN -m pip install --help 2>&1 | grep -q "break-system-packages"; then
        PIP_FLAGS="--break-system-packages"
        echo "📍 Using --break-system-packages flag"
    fi
fi

# Update pip and install build dependencies
echo "📦 Installing dependencies..."
$PYTHON_BIN -m pip install --upgrade pip $PIP_FLAGS
$PYTHON_BIN -m pip install pyinstaller $PIP_FLAGS

# Install the package in development mode for proper imports
echo "🏗️ Installing diffmanifests package..."
$PYTHON_BIN -m pip install -e . $PIP_FLAGS

# Build binary with comprehensive configuration
echo "🚀 Building binary with PyInstaller..."
$PYTHON_BIN -m PyInstaller --onefile \
  --clean \
  --name "$BINARY_NAME" \
  --add-data "diffmanifests/config:diffmanifests/config" \
  --hidden-import diffmanifests \
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
  --hidden-import openpyxl \
  --hidden-import openpyxl.workbook \
  --hidden-import openpyxl.worksheet \
  --hidden-import openpyxl.styles \
  --exclude-module tkinter \
  --exclude-module _tkinter \
  --exclude-module test \
  --exclude-module tests \
  --noupx \
  --noconfirm \
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
