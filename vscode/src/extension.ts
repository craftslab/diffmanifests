import * as vscode from 'vscode';
import { PythonEnvironment } from './pythonEnvironment';
import { DiffManifestsRunner } from './diffManifestsRunner';
import { FileSelector } from './fileSelector';

let outputChannel: vscode.OutputChannel;
let pythonEnv: PythonEnvironment;
let runner: DiffManifestsRunner;

export function activate(context: vscode.ExtensionContext) {
    outputChannel = vscode.window.createOutputChannel('Diff Manifests');
    pythonEnv = new PythonEnvironment(outputChannel);
    runner = new DiffManifestsRunner(pythonEnv, outputChannel);

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

    context.subscriptions.push(
        compareCommand,
        compareSelectionCommand,
        openOutputCommand,
        outputChannel
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

export function deactivate() {
    if (outputChannel) {
        outputChannel.dispose();
    }
}
