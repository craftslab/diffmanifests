# Installation Guide - Diff Manifests VS Code Extension

This guide covers installation on both **Windows** and **Ubuntu** platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Windows Installation](#windows-installation)
- [Ubuntu Installation](#ubuntu-installation)
- [Verification](#verification)
- [First Run](#first-run)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Common Requirements (Both Platforms)

1. **Visual Studio Code**
   - Version 1.75.0 or higher
   - Download from: https://code.visualstudio.com/

2. **Python**
   - Version 3.7 or higher
   - Python package manager (pip)

3. **Node.js & npm** (for building from source)
   - Version 16.x or higher
   - Download from: https://nodejs.org/

---

## Windows Installation

### Step 1: Install Python

```powershell
# Check if Python is installed
python --version

# If not installed, download from https://www.python.org/downloads/
# During installation, make sure to check "Add Python to PATH"
```

### Step 2: Install diffmanifests Package

```powershell
# Install via pip
pip install diffmanifests

# Verify installation
pip show diffmanifests
```

### Step 3: Build the VS Code Extension

```powershell
# Navigate to vscode directory
cd C:\path\to\diffmanifests\vscode

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# OR use the build script
.\build.bat
```

### Step 4: Package the Extension (Optional)

```powershell
# Install vsce globally
npm install -g @vscode/vsce

# Package the extension
vsce package

# This creates a .vsix file
```

### Step 5: Install in VS Code

**Option A: From VSIX file**
```powershell
# Install via command line
code --install-extension diffmanifests-1.0.0.vsix
```

**Option B: Via VS Code UI**
1. Open VS Code
2. Press `Ctrl+Shift+P`
3. Type "Extensions: Install from VSIX"
4. Select the generated `.vsix` file

**Option C: Development Mode (for testing)**
1. Open the `vscode` folder in VS Code
2. Press `F5` to launch Extension Development Host
3. Test the extension in the new window

---

## Ubuntu Installation

### Step 1: Install Python

```bash
# Check Python version
python3 --version

# If not installed or version < 3.7
sudo apt update
sudo apt install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

### Step 2: Install diffmanifests Package

```bash
# Install via pip
pip3 install diffmanifests

# Or with --user flag if permission denied
pip3 install --user diffmanifests

# Verify installation
pip3 show diffmanifests
```

### Step 3: Install Node.js

```bash
# Install Node.js and npm
sudo apt update
sudo apt install nodejs npm

# Verify installation
node --version
npm --version

# If version is too old, install from NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### Step 4: Build the VS Code Extension

```bash
# Navigate to vscode directory
cd /path/to/diffmanifests/vscode

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# OR use the build script
chmod +x build.sh
./build.sh
```

### Step 5: Package the Extension (Optional)

```bash
# Install vsce globally
sudo npm install -g @vscode/vsce

# Or without sudo
npm install -g @vscode/vsce

# Package the extension
vsce package

# This creates a .vsix file
```

### Step 6: Install in VS Code

**Option A: From VSIX file**
```bash
# Install via command line
code --install-extension diffmanifests-1.0.0.vsix
```

**Option B: Via VS Code UI**
1. Open VS Code
2. Press `Ctrl+Shift+P`
3. Type "Extensions: Install from VSIX"
4. Select the generated `.vsix` file

**Option C: Development Mode (for testing)**
1. Open the `vscode` folder in VS Code
2. Press `F5` to launch Extension Development Host
3. Test the extension in the new window

---

## Verification

After installation, verify the extension is working:

### 1. Check Extension is Installed

```bash
# List installed extensions
code --list-extensions | grep diffmanifests
```

### 2. Check Python and diffmanifests

**Windows:**
```powershell
python --version
pip show diffmanifests
```

**Ubuntu:**
```bash
python3 --version
pip3 show diffmanifests
```

### 3. Test the Extension

1. Open VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
3. Type "Diff Manifests"
4. You should see the extension commands:
   - Diff Manifests: Compare Two Manifest Files
   - Diff Manifests: Compare Selected Files
   - Diff Manifests: Open Output File

---

## First Run

### 1. Configure Python Path (if needed)

Open VS Code Settings (`Ctrl+,`) and search for "diffmanifests":

**Windows:**
```json
{
  "diffmanifests.pythonPath": "python"
}
```

**Ubuntu:**
```json
{
  "diffmanifests.pythonPath": "python3"
}
```

### 2. Set Default Config File

```json
{
  "diffmanifests.configFile": "/path/to/your/config.json"
}
```

### 3. Run Your First Comparison

1. Press `Ctrl+Shift+P`
2. Type "Diff Manifests: Compare Two Manifest Files"
3. Select your manifest files
4. Choose config file
5. Select output location
6. View results!

---

## Troubleshooting

### Windows Issues

#### Issue: Python not found
```powershell
# Add Python to PATH manually
# 1. Find Python installation: C:\Users\<user>\AppData\Local\Programs\Python\Python3X
# 2. Add to System Environment Variables > Path
# 3. Restart VS Code
```

#### Issue: Permission denied during pip install
```powershell
# Run as administrator or use --user flag
pip install --user diffmanifests
```

#### Issue: npm install fails
```powershell
# Clear npm cache
npm cache clean --force
# Try again
npm install
```

### Ubuntu Issues

#### Issue: Python command not found
```bash
# Use python3 instead of python
# Update extension settings to use python3
```

#### Issue: pip not found
```bash
# Install pip for Python 3
sudo apt install python3-pip
```

#### Issue: Permission denied during npm install
```bash
# Use --prefix to install locally
npm install --prefix ~/.npm-global

# Or change npm default directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
```

#### Issue: vsce package fails
```bash
# Make sure all dependencies are installed
npm install
# Try again
vsce package
```

### Common Issues (Both Platforms)

#### Issue: Extension doesn't appear in VS Code

1. Check if it's installed:
   ```bash
   code --list-extensions
   ```

2. Reload VS Code:
   - Press `Ctrl+Shift+P`
   - Type "Reload Window"

3. Check the Output panel for errors:
   - View > Output
   - Select "Diff Manifests" from dropdown

#### Issue: diffmanifests command not found

1. Verify Python package is installed:
   ```bash
   python -m pip show diffmanifests
   # or
   python3 -m pip show diffmanifests
   ```

2. Test running directly:
   ```bash
   python -m diffmanifests --help
   # or
   python3 -m diffmanifests --help
   ```

3. Check the extension output panel for detailed error messages

#### Issue: Comparison fails

1. Verify config.json format is correct
2. Check manifest XML files are valid
3. Ensure network connectivity for Gerrit/Gitiles API
4. Check the Output panel for detailed error messages

---

## Getting Help

- **GitHub Issues**: https://github.com/craftslab/diffmanifests/issues
- **Documentation**: See README.md in the extension directory
- **PyPI Package**: https://pypi.org/project/diffmanifests/

---

## Uninstallation

### Remove VS Code Extension

**Via Command Line:**
```bash
code --uninstall-extension craftslab.diffmanifests
```

**Via VS Code UI:**
1. Open Extensions view (`Ctrl+Shift+X`)
2. Search for "Diff Manifests"
3. Click "Uninstall"

### Remove Python Package

**Windows:**
```powershell
pip uninstall diffmanifests
```

**Ubuntu:**
```bash
pip3 uninstall diffmanifests
```

---

## Next Steps

After successful installation:

1. Read the [README.md](README.md) for usage instructions
2. Check [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines
3. Review [CHANGELOG.md](CHANGELOG.md) for version history
4. Configure your settings for optimal workflow

Enjoy using Diff Manifests! 🎉
