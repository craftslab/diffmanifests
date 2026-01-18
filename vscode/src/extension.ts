import * as vscode from 'vscode';
import { PythonEnvironment } from './pythonEnvironment';
import { DiffManifestsRunner } from './diffManifestsRunner';
import { FileSelector } from './fileSelector';
import { SidebarProvider } from './sidebarProvider';

let outputChannel: vscode.OutputChannel;
let pythonEnv: PythonEnvironment;
let runner: DiffManifestsRunner;
let sidebarProvider: SidebarProvider;

export function activate(context: vscode.ExtensionContext) {
    outputChannel = vscode.window.createOutputChannel('Diff Manifests');
    pythonEnv = new PythonEnvironment(outputChannel);
    runner = new DiffManifestsRunner(pythonEnv, outputChannel);

    // Initialize sidebar provider
    sidebarProvider = new SidebarProvider(context);
    const treeView = vscode.window.createTreeView('diffmanifests-explorer', {
        treeDataProvider: sidebarProvider,
        showCollapseAll: true
    });

    // Register commands
    const compareCommand = vscode.commands.registerCommand(
        'diffmanifests.compare',
        () => compareManifests()
    );

    const compareSelectionCommand = vscode.commands.registerCommand(
        'diffmanifests.compareSelection',
        (uri: vscode.Uri) => compareManifestsFromSelection(uri)
    );

    const openOutputCommand = vscode.commands.registerCommand(
        'diffmanifests.openOutput',
        () => openOutputFile()
    );

    const checkEnvironmentCommand = vscode.commands.registerCommand(
        'diffmanifests.checkEnvironment',
        () => checkEnvironment()
    );

    const refreshSidebarCommand = vscode.commands.registerCommand(
        'diffmanifests.refreshSidebar',
        () => sidebarProvider.refresh()
    );

    const openGitHubCommand = vscode.commands.registerCommand(
        'diffmanifests.openGitHub',
        () => vscode.env.openExternal(vscode.Uri.parse('https://github.com/craftslab/diffmanifests'))
    );

    const openDocsCommand = vscode.commands.registerCommand(
        'diffmanifests.openDocs',
        () => vscode.env.openExternal(vscode.Uri.parse('https://github.com/craftslab/diffmanifests#readme'))
    );

    const reportIssueCommand = vscode.commands.registerCommand(
        'diffmanifests.reportIssue',
        () => vscode.env.openExternal(vscode.Uri.parse('https://github.com/craftslab/diffmanifests/issues'))
    );

    const configurePythonPathCommand = vscode.commands.registerCommand(
        'diffmanifests.configurePythonPath',
        () => configurePythonPath()
    );

    const configurePackagePathCommand = vscode.commands.registerCommand(
        'diffmanifests.configurePackagePath',
        () => configurePackagePath()
    );

    const configureConfigFileCommand = vscode.commands.registerCommand(
        'diffmanifests.configureConfigFile',
        () => configureConfigFile()
    );

    const configureOutputFormatCommand = vscode.commands.registerCommand(
        'diffmanifests.configureOutputFormat',
        () => configureOutputFormat()
    );

    const toggleAutoInstallCommand = vscode.commands.registerCommand(
        'diffmanifests.toggleAutoInstall',
        () => toggleAutoInstall()
    );

    const toggleShowOutputCommand = vscode.commands.registerCommand(
        'diffmanifests.toggleShowOutput',
        () => toggleShowOutput()
    );

    const openSettingsCommand = vscode.commands.registerCommand(
        'diffmanifests.openSettings',
        () => vscode.commands.executeCommand('workbench.action.openSettings', 'diffmanifests')
    );

    const clearRecentFilesCommand = vscode.commands.registerCommand(
        'diffmanifests.clearRecentFiles',
        () => {
            sidebarProvider.clearRecentFiles();
            vscode.window.showInformationMessage('Recent files cleared');
        }
    );

    context.subscriptions.push(
        compareCommand,
        compareSelectionCommand,
        openOutputCommand,
        checkEnvironmentCommand,
        refreshSidebarCommand,
        openGitHubCommand,
        openDocsCommand,
        reportIssueCommand,
        configurePythonPathCommand,
        configurePackagePathCommand,
        configureConfigFileCommand,
        configureOutputFormatCommand,
        toggleAutoInstallCommand,
        toggleShowOutputCommand,
        openSettingsCommand,
        clearRecentFilesCommand,
        outputChannel,
        treeView
    );

    // Check Python environment on activation
    checkEnvironment();
}

async function checkEnvironment() {
    const config = vscode.workspace.getConfiguration('diffmanifests');
    const autoInstall = config.get<boolean>('autoInstall', true);

    try {
        const isInstalled = await pythonEnv.isDiffManifestsInstalled();
        if (!isInstalled && autoInstall) {
            const answer = await vscode.window.showWarningMessage(
                'diffmanifests package is not installed. Would you like to install it now?',
                'Yes',
                'No',
                'Don\'t Ask Again'
            );

            if (answer === 'Yes') {
                await pythonEnv.installDiffManifests();
            } else if (answer === 'Don\'t Ask Again') {
                await config.update('autoInstall', false, vscode.ConfigurationTarget.Global);
            }
        }
    } catch (error) {
        outputChannel.appendLine(`Error checking environment: ${error}`);
    }
}

async function compareManifests() {
    try {
        // Select manifest files
        const manifest1 = await FileSelector.selectManifestFile('Select first manifest file (manifest1)');
        if (!manifest1) {
            return;
        }

        const manifest2 = await FileSelector.selectManifestFile('Select second manifest file (manifest2)');
        if (!manifest2) {
            return;
        }

        // Select config file
        const config = await FileSelector.selectConfigFile();
        if (!config) {
            return;
        }

        // Select output file
        const output = await FileSelector.selectOutputFile();
        if (!output) {
            return;
        }

        // Run comparison
        await runner.runComparison(manifest1, manifest2, config, output);

        // Add to recent files
        sidebarProvider.addRecentFile(output);

        // Ask if user wants to open the output file
        const openFile = await vscode.window.showInformationMessage(
            'Comparison completed successfully. Open output file?',
            'Yes',
            'No'
        );

        if (openFile === 'Yes') {
            const doc = await vscode.workspace.openTextDocument(output);
            await vscode.window.showTextDocument(doc);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Comparison failed: ${error}`);
    }
}

async function compareManifestsFromSelection(uri: vscode.Uri) {
    try {
        if (!uri) {
            vscode.window.showWarningMessage('Please select a manifest file in the explorer');
            return;
        }

        // Use the selected file as manifest1
        const manifest1 = uri.fsPath;

        // Select manifest2
        const manifest2 = await FileSelector.selectManifestFile('Select second manifest file (manifest2)');
        if (!manifest2) {
            return;
        }

        // Select config file
        const config = await FileSelector.selectConfigFile();
        if (!config) {
            return;
        }

        // Select output file
        const output = await FileSelector.selectOutputFile();
        if (!output) {
            return;
        }

        // Run comparison
        await runner.runComparison(manifest1, manifest2, config, output);

        // Add to recent files
        sidebarProvider.addRecentFile(output);

        // Ask if user wants to open the output file
        const openFile = await vscode.window.showInformationMessage(
            'Comparison completed successfully. Open output file?',
            'Yes',
            'No'
        );

        if (openFile === 'Yes') {
            const doc = await vscode.workspace.openTextDocument(output);
            await vscode.window.showTextDocument(doc);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Comparison failed: ${error}`);
    }
}

async function openOutputFile() {
    const files = await vscode.window.showOpenDialog({
        canSelectFiles: true,
        canSelectFolders: false,
        canSelectMany: false,
        filters: {
            'Comparison Results': ['json', 'xlsx']
        },
        title: 'Select Output File'
    });

    if (files && files.length > 0) {
        const doc = await vscode.workspace.openTextDocument(files[0]);
        await vscode.window.showTextDocument(doc);
    }
}

async function configurePythonPath() {
    const config = vscode.workspace.getConfiguration('diffmanifests');
    const currentPath = config.get<string>('pythonPath', 'python');

    const newPath = await vscode.window.showInputBox({
        prompt: 'Enter Python executable path',
        value: currentPath,
        placeHolder: 'python, python3, or /path/to/python'
    });

    if (newPath !== undefined) {
        await config.update('pythonPath', newPath, vscode.ConfigurationTarget.Global);
        vscode.window.showInformationMessage(`Python path updated to: ${newPath}`);
        sidebarProvider.refresh();
    }
}

async function configurePackagePath() {
    const config = vscode.workspace.getConfiguration('diffmanifests');
    const currentPath = config.get<string>('packagePath', '');

    // Give user options to browse or manually enter
    const action = await vscode.window.showQuickPick(
        ['Browse for File/Directory', 'Enter Path Manually', 'Clear Path (Use pip-installed package)'],
        {
            placeHolder: 'Choose how to set the package path'
        }
    );

    if (!action) {
        return;
    }

    if (action === 'Clear Path (Use pip-installed package)') {
        await config.update('packagePath', '', vscode.ConfigurationTarget.Global);
        vscode.window.showInformationMessage('Package path cleared. Will use pip-installed package.');
        sidebarProvider.refresh();
        return;
    }

    if (action === 'Browse for File/Directory') {
        const files = await vscode.window.showOpenDialog({
            canSelectFiles: true,
            canSelectFolders: true,
            canSelectMany: false,
            title: 'Select diffmanifests package directory or script',
            openLabel: 'Select'
        });

        if (files && files.length > 0) {
            const newPath = files[0].fsPath;
            await config.update('packagePath', newPath, vscode.ConfigurationTarget.Global);
            vscode.window.showInformationMessage(`Package path updated to: ${newPath}`);
            sidebarProvider.refresh();
        }
    } else if (action === 'Enter Path Manually') {
        const newPath = await vscode.window.showInputBox({
            prompt: 'Enter diffmanifests package path',
            value: currentPath,
            placeHolder: '/path/to/diffmanifests or /path/to/diffmanifests/__main__.py'
        });

        if (newPath !== undefined) {
            await config.update('packagePath', newPath, vscode.ConfigurationTarget.Global);
            vscode.window.showInformationMessage(`Package path updated to: ${newPath}`);
            sidebarProvider.refresh();
        }
    }
}

async function configureConfigFile() {
    const files = await vscode.window.showOpenDialog({
        canSelectFiles: true,
        canSelectFolders: false,
        canSelectMany: false,
        filters: {
            'JSON Files': ['json'],
            'All Files': ['*']
        },
        title: 'Select config.json file'
    });

    if (files && files.length > 0) {
        const config = vscode.workspace.getConfiguration('diffmanifests');
        await config.update('configFile', files[0].fsPath, vscode.ConfigurationTarget.Workspace);
        vscode.window.showInformationMessage('Config file path updated');
        sidebarProvider.refresh();
    }
}

async function configureOutputFormat() {
    const format = await vscode.window.showQuickPick(
        ['.json', '.xlsx'],
        {
            placeHolder: 'Select output format'
        }
    );

    if (format) {
        const config = vscode.workspace.getConfiguration('diffmanifests');
        await config.update('outputFormat', format, vscode.ConfigurationTarget.Global);
        vscode.window.showInformationMessage(`Output format set to: ${format}`);
        sidebarProvider.refresh();
    }
}

async function toggleAutoInstall() {
    const config = vscode.workspace.getConfiguration('diffmanifests');
    const current = config.get<boolean>('autoInstall', true);
    await config.update('autoInstall', !current, vscode.ConfigurationTarget.Global);
    vscode.window.showInformationMessage(`Auto install ${!current ? 'enabled' : 'disabled'}`);
    sidebarProvider.refresh();
}

async function toggleShowOutput() {
    const config = vscode.workspace.getConfiguration('diffmanifests');
    const current = config.get<boolean>('showOutputPanel', true);
    await config.update('showOutputPanel', !current, vscode.ConfigurationTarget.Global);
    vscode.window.showInformationMessage(`Auto-show output panel ${!current ? 'enabled' : 'disabled'}`);
    sidebarProvider.refresh();
}

export function deactivate() {
    if (outputChannel) {
        outputChannel.dispose();
    }
}
