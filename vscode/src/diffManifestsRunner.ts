import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { PythonEnvironment } from './pythonEnvironment';

export class DiffManifestsRunner {
    private pythonEnv: PythonEnvironment;
    private outputChannel: vscode.OutputChannel;

    constructor(pythonEnv: PythonEnvironment, outputChannel: vscode.OutputChannel) {
        this.pythonEnv = pythonEnv;
        this.outputChannel = outputChannel;
    }

    /**
     * Run diffmanifests comparison
     */
    public async runComparison(
        manifest1: string,
        manifest2: string,
        configFile: string,
        outputFile: string
    ): Promise<void> {
        return vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: 'Comparing manifests...',
                cancellable: false
            },
            async (progress) => {
                try {
                    // Verify Python is available
                    const pythonAvailable = await this.pythonEnv.isPythonAvailable();
                    if (!pythonAvailable) {
                        throw new Error('Python is not available. Please install Python and configure the path in settings.');
                    }

                    // Verify diffmanifests is installed
                    const diffmanifestsInstalled = await this.pythonEnv.isDiffManifestsInstalled();
                    if (!diffmanifestsInstalled) {
                        throw new Error('diffmanifests is not installed. Please install it first.');
                    }

                    // Verify input files exist
                    this.verifyFileExists(manifest1, 'Manifest 1');
                    this.verifyFileExists(manifest2, 'Manifest 2');
                    this.verifyFileExists(configFile, 'Config file');

                    // Create output directory if it doesn't exist
                    const outputDir = path.dirname(outputFile);
                    if (!fs.existsSync(outputDir)) {
                        fs.mkdirSync(outputDir, { recursive: true });
                    }

                    progress.report({ increment: 20, message: 'Preparing arguments...' });

                    // Build command arguments
                    const packagePath = this.pythonEnv.getPackagePath();
                    let args: string[];

                    if (packagePath && packagePath.trim() !== '') {
                        // Use custom package path (direct script path or directory with __main__.py)
                        this.outputChannel.appendLine(`Using custom package path: ${packagePath}`);
                        args = [
                            this.escapeArg(packagePath),
                            '-c', this.escapeArg(configFile),
                            '-m', this.escapeArg(manifest1),
                            '-n', this.escapeArg(manifest2),
                            '-o', this.escapeArg(outputFile)
                        ];
                    } else {
                        // Use pip-installed package
                        this.outputChannel.appendLine('Using pip-installed package');
                        args = [
                            '-m', 'diffmanifests',
                            '-c', this.escapeArg(configFile),
                            '-m', this.escapeArg(manifest1),
                            '-n', this.escapeArg(manifest2),
                            '-o', this.escapeArg(outputFile)
                        ];
                    }

                    // Show configuration
                    const config = vscode.workspace.getConfiguration('diffmanifests');
                    const showOutputPanel = config.get<boolean>('showOutputPanel', true);

                    if (showOutputPanel) {
                        this.outputChannel.show(true);
                    }

                    this.outputChannel.appendLine('='.repeat(80));
                    this.outputChannel.appendLine('Starting diffmanifests comparison');
                    this.outputChannel.appendLine('='.repeat(80));
                    this.outputChannel.appendLine(`Manifest 1: ${manifest1}`);
                    this.outputChannel.appendLine(`Manifest 2: ${manifest2}`);
                    this.outputChannel.appendLine(`Config: ${configFile}`);
                    this.outputChannel.appendLine(`Output: ${outputFile}`);
                    this.outputChannel.appendLine('='.repeat(80));

                    progress.report({ increment: 30, message: 'Running comparison...' });

                    // Execute diffmanifests
                    const { stdout, stderr } = await this.pythonEnv.executePython(args);

                    // Output results
                    if (stdout) {
                        this.outputChannel.appendLine(stdout);
                    }
                    if (stderr) {
                        this.outputChannel.appendLine(`Warnings/Errors:\n${stderr}`);
                    }

                    progress.report({ increment: 50, message: 'Comparison complete' });

                    // Verify output file was created
                    if (!fs.existsSync(outputFile)) {
                        throw new Error('Output file was not created. Check the output panel for errors.');
                    }

                    this.outputChannel.appendLine('='.repeat(80));
                    this.outputChannel.appendLine('Comparison completed successfully');
                    this.outputChannel.appendLine(`Output file: ${outputFile}`);
                    this.outputChannel.appendLine('='.repeat(80));

                } catch (error) {
                    const errorMessage = error instanceof Error ? error.message : String(error);
                    this.outputChannel.appendLine(`Error: ${errorMessage}`);
                    throw error;
                }
            }
        );
    }

    /**
     * Verify that a file exists
     */
    private verifyFileExists(filePath: string, description: string): void {
        if (!fs.existsSync(filePath)) {
            throw new Error(`${description} not found: ${filePath}`);
        }
    }

    /**
     * Escape argument for command line
     */
    private escapeArg(arg: string): string {
        // Handle Windows paths and spaces
        if (process.platform === 'win32') {
            // On Windows, wrap in double quotes if contains spaces
            if (arg.includes(' ')) {
                return `"${arg}"`;
            }
        } else {
            // On Unix-like systems, escape spaces
            if (arg.includes(' ')) {
                return `"${arg}"`;
            }
        }
        return arg;
    }
}
