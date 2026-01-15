# Diff Manifests VS Code Extension

[English](README.md) | [简体中文](README_cn.md)

A Visual Studio Code extension for comparing Android manifest files using the `diffmanifests` Python package. This extension provides a seamless integration of the diffmanifests CLI tool into VS Code, supporting Windows, Ubuntu and macOS platforms.

## Features

- 🔍 **Deep Manifest Comparison**: Compare two manifest XML files directly from VS Code
- 🎯 **Context Menu Integration**: Right-click on manifest files in the explorer to compare
- ⚙️ **Configurable**: Customize Python path, config file, and output format
- 📊 **Multiple Output Formats**: Support for JSON and Excel output formats
- 🔄 **Auto-Installation**: Automatically offers to install the diffmanifests package
- 📝 **Output Panel**: View detailed comparison logs and results
- 🌐 **Cross-Platform**: Works on Windows, Linux (Ubuntu), and macOS

## Prerequisites

- **Visual Studio Code**: Version 1.75.0 or higher
- **Python**: Version 3.7 or higher with pip package manager
- **Node.js & npm**: Version 16.x or higher (for building from source)

## Installation

> 📖 For detailed platform-specific installation instructions, see [INSTALL.md](INSTALL.md)

### Quick Install (Recommended)

#### Windows
```powershell
# Install Python package
pip install diffmanifests

# Navigate to extension directory
cd C:\path\to\diffmanifests\vscode

# Build extension
npm install
npm run compile

# Package extension
npm install -g @vscode/vsce
vsce package

# Install in VS Code
code --install-extension diffmanifests-1.0.0.vsix
```

#### Ubuntu/Linux
```bash
# Install Python package
pip3 install diffmanifests

# Navigate to extension directory
cd /path/to/diffmanifests/vscode

# Build extension
npm install
npm run compile

# Package extension
npm install -g @vscode/vsce
vsce package

# Install in VS Code
code --install-extension diffmanifests-1.0.0.vsix
```

### Installation Methods

#### Method 1: From VSIX File (Local Installation)

1. **Build the extension:**
   ```bash
   cd vscode
   npm install
   npm run compile
   vsce package
   ```

2. **Install via command line:**
   ```bash
   code --install-extension diffmanifests-1.0.0.vsix
   ```

3. **Or install via VS Code UI:**
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
   - Type "Extensions: Install from VSIX"
   - Select the generated `.vsix` file

#### Method 2: Development Mode (For Testing)

1. Open the `vscode` folder in VS Code
2. Press `F5` to launch Extension Development Host
3. Test the extension in the new window

#### Method 3: From VS Code Marketplace (When Published)

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for "Diff Manifests"
4. Click Install

### Post-Installation Setup

#### Configure Python Path

After installation, configure the Python path for your platform:

**Windows (`settings.json`):**
```json
{
  "diffmanifests.pythonPath": "python"
}
```

**Ubuntu/Linux (`settings.json`):**
```json
{
  "diffmanifests.pythonPath": "python3"
}
```

#### Verify Installation

```bash
# Check extension is installed
code --list-extensions | grep diffmanifests

# Check Python package is installed
pip show diffmanifests  # Windows
pip3 show diffmanifests  # Ubuntu/Linux
```

## Usage

### Method 1: Command Palette

1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
2. Type "Diff Manifests: Compare Two Manifest Files"
3. Select the first manifest file (manifest1)
4. Select the second manifest file (manifest2)
5. Select or confirm the config file
6. Choose the output file location
7. View the results

### Method 2: Context Menu

1. Right-click on a manifest XML file in the Explorer
2. Select "Diff Manifests: Compare Selected Files"
3. Follow the prompts to select the second manifest and config file
4. Choose the output file location
5. View the results

### Method 3: Using Settings

Configure default settings for faster workflow:

1. Open Settings (`Ctrl+,`)
2. Search for "diffmanifests"
3. Configure:
   - Python Path (if not using system default)
   - Default Config File path
   - Output Format (JSON or Excel)
   - Auto-install preference
   - Output panel visibility

## Configuration

The extension provides the following configuration options:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `diffmanifests.pythonPath` | string | `"python"` | Path to Python executable |
| `diffmanifests.configFile` | string | `""` | Path to default config.json file |
| `diffmanifests.outputFormat` | string | `".json"` | Output format (.json or .xlsx) |
| `diffmanifests.autoInstall` | boolean | `true` | Auto-install diffmanifests if not found |
| `diffmanifests.showOutputPanel` | boolean | `true` | Show output panel when running |

### Example Configuration

Add to your `settings.json`:

```json
{
  "diffmanifests.pythonPath": "python3",
  "diffmanifests.configFile": "/path/to/config.json",
  "diffmanifests.outputFormat": ".json",
  "diffmanifests.autoInstall": true,
  "diffmanifests.showOutputPanel": true
}
```

## Python Package Installation

The extension requires the `diffmanifests` Python package. It will offer to install it automatically on first use, or you can install it manually:

**Windows:**
```powershell
pip install diffmanifests
pip show diffmanifests  # Verify installation
```

**Ubuntu/Linux:**
```bash
pip3 install diffmanifests
# Or with --user flag if permission denied
pip3 install --user diffmanifests
pip3 show diffmanifests  # Verify installation
```

**macOS:**
```bash
pip3 install diffmanifests
pip3 show diffmanifests  # Verify installation
```

### Platform-Specific Setup

#### Windows
- Ensure Python is added to PATH during installation
- Check "Add Python to PATH" when installing Python
- Use `python` command by default
- Use forward slashes or double backslashes in path settings

#### Ubuntu/Linux
- Use `python3` command (Python 2 may be installed as `python`)
- Install pip if not available: `sudo apt install python3-pip`
- Update the `diffmanifests.pythonPath` setting to `python3`
- Use `--user` flag for pip install if permission denied

#### macOS
- Use `python3` command (similar to Linux)
- Install Python 3 via Homebrew: `brew install python3`
- Update the `diffmanifests.pythonPath` setting to `python3`

## Commands

The extension provides the following commands:

- `Diff Manifests: Compare Two Manifest Files` - Start a new comparison
- `Diff Manifests: Compare Selected Files` - Compare using selected file
- `Diff Manifests: Open Output File` - Open a previous output file

## Config File Format

The extension requires a config.json file with Gerrit and Gitiles API configuration:

```json
{
  "gerrit": {
    "host": "your-gerrit-host.com",
    "port": 443,
    "protocol": "https",
    "user": "your-username",
    "pass": "your-password"
  },
  "gitiles": {
    "host": "your-gitiles-host.com",
    "port": 443,
    "protocol": "https"
  }
}
```

## Output Formats

### JSON Output
Provides detailed comparison results in structured JSON format:
- Project differences
- Commit information
- Hashtags
- Change details

### Excel Output
Creates an Excel spreadsheet with:
- Summary sheet
- Detailed changes per project
- Easy filtering and sorting
- Formatted tables

## Troubleshooting

> 📖 For comprehensive troubleshooting, see [INSTALL.md](INSTALL.md#troubleshooting)

### Common Issues

#### Python Not Found

**Windows:**
```powershell
# Add Python to PATH manually
# 1. Find Python installation: C:\Users\<user>\AppData\Local\Programs\Python\Python3X
# 2. Add to System Environment Variables > Path
# 3. Restart VS Code
```

**Ubuntu/Linux:**
```bash
# Use python3 instead of python
# Update extension settings to use python3
python3 --version
```

#### Package Not Installed

**Windows:**
```powershell
pip install diffmanifests
pip show diffmanifests
```

**Ubuntu/Linux:**
```bash
pip3 install diffmanifests
# Or with --user flag if permission denied
pip3 install --user diffmanifests
pip3 show diffmanifests
```

#### Extension Not Working

1. Check if extension is installed:
   ```bash
   code --list-extensions | grep diffmanifests
   ```

2. Reload VS Code:
   - Press `Ctrl+Shift+P`
   - Type "Reload Window"

3. Check the Output panel:
   - View > Output
   - Select "Diff Manifests" from dropdown

#### diffmanifests Command Not Found

1. Verify Python package is installed:
   ```bash
   python -m pip show diffmanifests    # Windows
   python3 -m pip show diffmanifests   # Ubuntu/Linux
   ```

2. Test running directly:
   ```bash
   python -m diffmanifests --help      # Windows
   python3 -m diffmanifests --help     # Ubuntu/Linux
   ```

3. Check the extension output panel for detailed error messages

#### Permission Errors

**Ubuntu/Linux:**
```bash
# Install with --user flag
pip3 install --user diffmanifests

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install diffmanifests
```

**Windows:**
```powershell
# Run as administrator or use --user flag
pip install --user diffmanifests
```

#### Output File Not Created

1. Check the Output panel (`View > Output > Diff Manifests`) for error messages
2. Verify config.json format is correct (see Config File Format section)
3. Ensure manifest files are valid XML
4. Check network connectivity for Gerrit/Gitiles API access
5. Verify output directory has write permissions

## Development

### Setup

```bash
cd vscode
npm install
```

### Compile

```bash
npm run compile
```

### Watch Mode

```bash
npm run watch
```

### Package

```bash
npm install -g @vscode/vsce
vsce package
```

## Additional Resources

- 📖 [Installation Guide](INSTALL.md) - Detailed platform-specific installation instructions
- 🚀 [Quick Start Guide](QUICKSTART.md) - Get started quickly
- 👨‍💻 [Development Guide](DEVELOPMENT.md) - For contributors and developers
- 📝 [Changelog](CHANGELOG.md) - Version history and updates
- 🔗 [GitHub Repository](https://github.com/craftslab/diffmanifests)
- 📦 [PyPI Package](https://pypi.org/project/diffmanifests/)
- 🐛 [Issue Tracker](https://github.com/craftslab/diffmanifests/issues)

## Getting Help

- **Detailed Installation**: See [INSTALL.md](INSTALL.md) for step-by-step platform-specific instructions
- **Troubleshooting**: Check [INSTALL.md#troubleshooting](INSTALL.md#troubleshooting) for solutions
- **Quick Reference**: See [QUICKSTART.md](QUICKSTART.md) for common tasks
- **Report Issues**: Use our [Issue Tracker](https://github.com/craftslab/diffmanifests/issues)

## Uninstallation

**Remove VS Code Extension:**
```bash
code --uninstall-extension craftslab.diffmanifests
```

**Remove Python Package:**
```bash
pip uninstall diffmanifests    # Windows
pip3 uninstall diffmanifests   # Ubuntu/Linux
```

## License

Apache-2.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

For development setup and guidelines, see [DEVELOPMENT.md](DEVELOPMENT.md).
