# Diff Manifests VS Code 扩展

[English](README.md) | [简体中文](README_cn.md)

一个用于使用 `diffmanifests` Python 包比较 Android 清单文件的 Visual Studio Code 扩展。此扩展将 diffmanifests CLI 工具无缝集成到 VS Code 中，支持 Windows，Ubuntu 和 macOS 平台。

## 功能特性

- 🔍 **深度清单比较**：直接在 VS Code 中比较两个清单 XML 文件
- 🎯 **右键菜单集成**：在资源管理器中右键点击清单文件进行比较
- 📋 **侧边栏视图**：专用侧边栏，快速访问所有功能和设置
- ⚡ **快速操作**：从侧边栏比较清单、检查环境和管理设置
- 📂 **最近文件**：跟踪并快速访问最近比较的文件
- ⚙️ **可配置**：自定义 Python 路径、配置文件和输出格式
- 📊 **多种输出格式**：支持 JSON 和 Excel 输出格式
- 🔄 **自动安装**：自动提供安装 diffmanifests 包
- 📝 **输出面板**：查看详细的比较日志和结果
- 🌐 **跨平台**：支持 Windows、Linux (Ubuntu) 和 macOS

## 先决条件

- **Visual Studio Code**：1.75.0 或更高版本
- **Python**：3.7 或更高版本，需要 pip 包管理器
- **Node.js & npm**：16.x 或更高版本（用于从源代码构建）

## 安装

> 📖 有关详细的平台特定安装说明，请参阅 [INSTALL.md](INSTALL.md)

### 快速安装（推荐）

#### Windows
```powershell
# 安装 Python 包
pip install diffmanifests

# 导航到扩展目录
cd C:\path\to\diffmanifests\vscode

# 构建扩展
npm install
npm run compile

# 打包扩展
npm install -g @vscode/vsce
vsce package

# 在 VS Code 中安装
code --install-extension diffmanifests-1.0.0.vsix
```

#### Ubuntu/Linux
```bash
# 安装 Python 包
pip3 install diffmanifests

# 导航到扩展目录
cd /path/to/diffmanifests/vscode

# 构建扩展
npm install
npm run compile

# 打包扩展
npm install -g @vscode/vsce
vsce package

# 在 VS Code 中安装
code --install-extension diffmanifests-1.0.0.vsix
```

### 安装方法

#### 方法 1：从 VSIX 文件安装（本地安装）

1. **构建扩展：**
   ```bash
   cd vscode
   npm install
   npm run compile
   vsce package
   ```

2. **通过命令行安装：**
   ```bash
   code --install-extension diffmanifests-1.0.0.vsix
   ```

3. **或通过 VS Code UI 安装：**
   - 按 `Ctrl+Shift+P` (Windows/Linux) 或 `Cmd+Shift+P` (macOS)
   - 输入 "Extensions: Install from VSIX"
   - 选择生成的 `.vsix` 文件

#### 方法 2：开发模式（用于测试）

1. 在 VS Code 中打开 `vscode` 文件夹
2. 按 `F5` 启动扩展开发宿主
3. 在新窗口中测试扩展

#### 方法 3：从 VS Code 市场安装（发布后）

1. 打开 VS Code
2. 转到扩展 (`Ctrl+Shift+X`)
3. 搜索 "Diff Manifests"
4. 点击安装

### 安装后设置

#### 配置 Python 路径

安装后，为您的平台配置 Python 路径：

**Windows (`settings.json`)：**
```json
{
  "diffmanifests.pythonPath": "python"
}
```

**Ubuntu/Linux (`settings.json`)：**
```json
{
  "diffmanifests.pythonPath": "python3"
}
```

#### 验证安装

```bash
# 检查扩展是否已安装
code --list-extensions | grep diffmanifests

# 检查 Python 包是否已安装
pip show diffmanifests  # Windows
pip3 show diffmanifests  # Ubuntu/Linux
```

## 使用方法

### 方法 1：侧边栏（推荐）

1. 点击活动栏（左侧边栏）中的 Diff Manifests 图标
2. 在侧边栏中，您将看到：
   - **操作**：快速访问比较清单和其他操作
   - **最近文件**：最近比较的文件列表，便于快速访问
   - **设置**：查看和修改扩展设置
   - **快速链接**：访问文档和 GitHub 仓库

3. 点击"比较清单"开始新的比较
4. 按照提示选择文件
5. 在输出面板中查看结果或打开结果文件

### 方法 2：命令面板

1. 按 `Ctrl+Shift+P` (Windows/Linux) 或 `Cmd+Shift+P` (macOS)
2. 输入 "Diff Manifests: Compare Two Manifest Files"
3. 选择第一个清单文件 (manifest1)
4. 选择第二个清单文件 (manifest2)
5. 选择或确认配置文件
6. 选择输出文件位置
7. 查看结果

### 方法 3：右键菜单

1. 在资源管理器中右键点击清单 XML 文件
2. 选择 "Diff Manifests: Compare Selected Files"
3. 按照提示选择第二个清单和配置文件
4. 选择输出文件位置
5. 查看结果

### 方法 4：使用设置

配置默认设置以加快工作流程：

1. 打开设置 (`Ctrl+,`)
2. 搜索 "diffmanifests"
3. 配置：
   - Python 路径（如果不使用系统默认）
   - 默认配置文件路径
   - 输出格式（JSON 或 Excel）
   - 自动安装偏好
   - 输出面板可见性

## 配置

扩展提供以下配置选项：

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `diffmanifests.pythonPath` | string | `"python"` | Python 可执行文件路径 |
| `diffmanifests.packagePath` | string | `""` | diffmanifests 包路径（仅在关闭自动安装时使用） |
| `diffmanifests.configFile` | string | `""` | 默认 config.json 文件路径 |
| `diffmanifests.outputFormat` | string | `".json"` | 输出格式（.json 或 .xlsx） |
| `diffmanifests.autoInstall` | boolean | `true` | 如果未找到，则自动安装 diffmanifests |
| `diffmanifests.showOutputPanel` | boolean | `true` | 运行时显示输出面板 |

### 配置示例

添加到您的 `settings.json`：

```json
{
  "diffmanifests.pythonPath": "python3",
  "diffmanifests.packagePath": "",
  "diffmanifests.configFile": "/path/to/config.json",
  "diffmanifests.outputFormat": ".json",
  "diffmanifests.autoInstall": true,
  "diffmanifests.showOutputPanel": true
}
```

### 从侧边栏快速配置

您也可以直接从侧边栏配置设置：
1. 打开 Diff Manifests 侧边栏
2. 展开"设置"部分
3. 点击任何设置项来修改它：
   - **Python 路径**：更改 Python 可执行文件路径   - **包路径**：设置自定义 diffmanifests 安装路径（仅在关闭自动安装时显示）   - **配置文件**：选择默认 config.json 文件
   - **输出格式**：在 JSON 和 Excel 之间切换
   - **自动安装**：切换自动安装功能
   - **显示输出**：切换输出面板可见性
   - **打开设置**：访问完整的扩展设置

## 可用命令

所有命令都可以通过命令面板 (`Ctrl+Shift+P`) 访问：

- **Diff Manifests: Compare Two Manifest Files** - 开始新的比较
- **Diff Manifests: Compare Selected Files** - 从选定文件比较
- **Diff Manifests: Open Output File** - 打开结果文件
- **Diff Manifests: Check Environment** - 验证 Python 和包安装
- **Refresh**（侧边栏）- 刷新侧边栏视图
- **Open Settings** - 打开扩展设置
- **Configure Python Path** - 设置 Python 可执行文件路径
- **Configure Config File** - 设置默认配置文件
- **Configure Output Format** - 选择输出格式
- **Toggle Auto Install** - 启用/禁用自动安装
- **Toggle Show Output Panel** - 启用/禁用自动显示输出
- **Clear Recent Files** - 清除最近文件列表

## Python 包安装

扩展需要 `diffmanifests` Python 包。它会在首次使用时自动提供安装，或者您可以手动安装：

**Windows：**
```powershell
pip install diffmanifests
pip show diffmanifests  # 验证安装
```

**Ubuntu/Linux：**
```bash
pip3 install diffmanifests
# 如果权限被拒绝，使用 --user 标志
pip3 install --user diffmanifests
pip3 show diffmanifests  # 验证安装
```

**macOS：**
```bash
pip3 install diffmanifests
pip3 show diffmanifests  # 验证安装
```

### 平台特定设置

#### Windows
- 确保在安装期间将 Python 添加到 PATH
- 安装 Python 时勾选 "Add Python to PATH"
- 默认使用 `python` 命令
- 在路径设置中使用正斜杠或双反斜杠

#### Ubuntu/Linux
- 使用 `python3` 命令（Python 2 可能安装为 `python`）
- 如果不可用，安装 pip：`sudo apt install python3-pip`
- 将 `diffmanifests.pythonPath` 设置更新为 `python3`
- 如果权限被拒绝，使用 `--user` 标志进行 pip 安装

#### macOS
- 使用 `python3` 命令（类似于 Linux）
- 通过 Homebrew 安装 Python 3：`brew install python3`
- 将 `diffmanifests.pythonPath` 设置更新为 `python3`

## 命令

扩展提供以下命令：

- `Diff Manifests: Compare Two Manifest Files` - 开始新的比较
- `Diff Manifests: Compare Selected Files` - 使用选定的文件进行比较
- `Diff Manifests: Open Output File` - 打开以前的输出文件

## 配置文件格式

扩展需要一个包含 Gerrit 和 Gitiles API 配置的 config.json 文件：

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

## 输出格式

### JSON 输出
以结构化 JSON 格式提供详细的比较结果：
- 项目差异
- 提交信息
- 标签
- 更改详情

### Excel 输出
创建 Excel 电子表格，包含：
- 摘要工作表
- 每个项目的详细更改
- 易于过滤和排序
- 格式化表格

## 故障排除

> 📖 有关全面的故障排除，请参阅 [INSTALL.md](INSTALL.md#troubleshooting)

### 常见问题

#### 找不到 Python

**Windows：**
```powershell
# 手动将 Python 添加到 PATH
# 1. 找到 Python 安装位置：C:\Users\<user>\AppData\Local\Programs\Python\Python3X
# 2. 添加到系统环境变量 > Path
# 3. 重启 VS Code
```

**Ubuntu/Linux：**
```bash
# 使用 python3 而不是 python
# 更新扩展设置以使用 python3
python3 --version
```

#### 包未安装

**Windows：**
```powershell
pip install diffmanifests
pip show diffmanifests
```

**Ubuntu/Linux：**
```bash
pip3 install diffmanifests
# 如果权限被拒绝，使用 --user 标志
pip3 install --user diffmanifests
pip3 show diffmanifests
```

#### 扩展不工作

1. 检查扩展是否已安装：
   ```bash
   code --list-extensions | grep diffmanifests
   ```

2. 重新加载 VS Code：
   - 按 `Ctrl+Shift+P`
   - 输入 "Reload Window"

3. 检查输出面板：
   - 查看 > 输出
   - 从下拉菜单中选择 "Diff Manifests"

#### 找不到 diffmanifests 命令

1. 验证 Python 包是否已安装：
   ```bash
   python -m pip show diffmanifests    # Windows
   python3 -m pip show diffmanifests   # Ubuntu/Linux
   ```

2. 测试直接运行：
   ```bash
   python -m diffmanifests --help      # Windows
   python3 -m diffmanifests --help     # Ubuntu/Linux
   ```

3. 检查扩展输出面板以获取详细的错误消息

#### 权限错误

**Ubuntu/Linux：**
```bash
# 使用 --user 标志安装
pip3 install --user diffmanifests

# 或使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install diffmanifests
```

**Windows：**
```powershell
# 以管理员身份运行或使用 --user 标志
pip install --user diffmanifests
```

#### 未创建输出文件

1. 检查输出面板（`查看 > 输出 > Diff Manifests`）以获取错误消息
2. 验证 config.json 格式是否正确（参见配置文件格式部分）
3. 确保清单文件是有效的 XML
4. 检查 Gerrit/Gitiles API 访问的网络连接
5. 验证输出目录具有写入权限

## 开发

### 设置

```bash
cd vscode
npm install
```

### 编译

```bash
npm run compile
```

### 监视模式

```bash
npm run watch
```

### 打包

```bash
npm install -g @vscode/vsce
vsce package
```

## 其他资源

- 📖 [安装指南](INSTALL.md) - 详细的平台特定安装说明
- 🚀 [快速入门指南](QUICKSTART.md) - 快速开始
- 👨‍💻 [开发指南](DEVELOPMENT.md) - 面向贡献者和开发人员
- 📝 [更新日志](CHANGELOG.md) - 版本历史和更新
- 🔗 [GitHub 仓库](https://github.com/craftslab/diffmanifests)
- 📦 [PyPI 包](https://pypi.org/project/diffmanifests/)
- 🐛 [问题跟踪器](https://github.com/craftslab/diffmanifests/issues)

## 获取帮助

- **详细安装**：请参阅 [INSTALL.md](INSTALL.md) 获取分步平台特定说明
- **故障排除**：查看 [INSTALL.md#troubleshooting](INSTALL.md#troubleshooting) 获取解决方案
- **快速参考**：请参阅 [QUICKSTART.md](QUICKSTART.md) 了解常见任务
- **报告问题**：使用我们的 [问题跟踪器](https://github.com/craftslab/diffmanifests/issues)

## 卸载

**移除 VS Code 扩展：**
```bash
code --uninstall-extension craftslab.diffmanifests
```

**移除 Python 包：**
```bash
pip uninstall diffmanifests    # Windows
pip3 uninstall diffmanifests   # Ubuntu/Linux
```

## 许可证

Apache-2.0

## 贡献

欢迎贡献！请随时提交 Pull Request。

有关开发设置和指南，请参阅 [DEVELOPMENT.md](DEVELOPMENT.md)。
