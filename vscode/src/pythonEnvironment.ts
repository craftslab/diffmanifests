import * as vscode from 'vscode';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export class PythonEnvironment {
    private outputChannel: vscode.OutputChannel;

    constructor(outputChannel: vscode.OutputChannel) {
        this.outputChannel = outputChannel;
    }

    /**
     * Get the Python executable path from settings
     */
    public getPythonPath(): string {
        const config = vscode.workspace.getConfiguration('diffmanifests');
        let pythonPath = config.get<string>('pythonPath', 'python');

        // If pythonPath is empty or 'python', try to use the Python extension's interpreter
        if (!pythonPath || pythonPath === 'python') {
            try {
                const pythonExtension = vscode.extensions.getExtension('ms-python.python');
                if (pythonExtension?.isActive) {
                    const pythonApi = pythonExtension.exports;
                    if (pythonApi?.settings?.getExecutionDetails) {
                        const execDetails = pythonApi.settings.getExecutionDetails();
                        if (execDetails?.execCommand) {
                            pythonPath = execDetails.execCommand[0];
                        }
                    }
                }
            } catch (error) {
                this.outputChannel.appendLine(`Could not get Python path from Python extension: ${error}`);
            }
        }

        return pythonPath || 'python';
    }

    /**
     * Get the diffmanifests package path from settings
     */
    public getPackagePath(): string {
        const config = vscode.workspace.getConfiguration('diffmanifests');
        return config.get<string>('packagePath', '');
    }

    /**
     * Check if Python is available
     */
    public async isPythonAvailable(): Promise<boolean> {
        try {
            const pythonPath = this.getPythonPath();
            const { stdout } = await execAsync(`"${pythonPath}" --version`);
            this.outputChannel.appendLine(`Python version: ${stdout.trim()}`);
            return true;
        } catch (error) {
            this.outputChannel.appendLine(`Python not found: ${error}`);
            return false;
        }
    }

    /**
     * Check if diffmanifests package is installed
     */
    public async isDiffManifestsInstalled(): Promise<boolean> {
        try {
            const pythonPath = this.getPythonPath();
            await execAsync(`"${pythonPath}" -m pip show diffmanifests`);
            this.outputChannel.appendLine('diffmanifests package is installed');
            return true;
        } catch (error) {
            this.outputChannel.appendLine('diffmanifests package is not installed');
            return false;
        }
    }

    /**
     * Install diffmanifests package
     */
    public async installDiffManifests(): Promise<void> {
        const pythonPath = this.getPythonPath();

        return vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: 'Installing diffmanifests package...',
                cancellable: false
            },
            async (progress) => {
                try {
                    this.outputChannel.show(true);
                    this.outputChannel.appendLine('Installing diffmanifests...');

                    progress.report({ increment: 30, message: 'Running pip install...' });

                    const { stdout, stderr } = await execAsync(
                        `"${pythonPath}" -m pip install diffmanifests`,
                        { maxBuffer: 1024 * 1024 * 10 } // 10MB buffer
                    );

                    this.outputChannel.appendLine(stdout);
                    if (stderr) {
                        this.outputChannel.appendLine(stderr);
                    }

                    progress.report({ increment: 70, message: 'Installation complete' });

                    vscode.window.showInformationMessage('diffmanifests installed successfully');
                    this.outputChannel.appendLine('diffmanifests installed successfully');
                } catch (error) {
                    const errorMessage = error instanceof Error ? error.message : String(error);
                    this.outputChannel.appendLine(`Installation failed: ${errorMessage}`);
                    throw new Error(`Failed to install diffmanifests: ${errorMessage}`);
                }
            }
        );
    }

    /**
     * Get diffmanifests version
     */
    public async getDiffManifestsVersion(): Promise<string> {
        try {
            const pythonPath = this.getPythonPath();
            const { stdout } = await execAsync(
                `"${pythonPath}" -m pip show diffmanifests | findstr /C:"Version:" || grep "Version:"`
            );
            const version = stdout.trim().split(':')[1]?.trim() || 'unknown';
            return version;
        } catch (error) {
            return 'unknown';
        }
    }

    /**
     * Execute a Python command
     */
    public async executePython(args: string[]): Promise<{ stdout: string; stderr: string }> {
        const pythonPath = this.getPythonPath();
        const command = `"${pythonPath}" ${args.join(' ')}`;

        this.outputChannel.appendLine(`Executing: ${command}`);

        try {
            const result = await execAsync(command, {
                maxBuffer: 1024 * 1024 * 50, // 50MB buffer for large outputs
                env: { ...process.env }
            });

            return result;
        } catch (error) {
            const execError = error as { stdout?: string; stderr?: string; message: string };
            this.outputChannel.appendLine(`Error executing Python: ${execError.message}`);
            if (execError.stdout) {
                this.outputChannel.appendLine(`stdout: ${execError.stdout}`);
            }
            if (execError.stderr) {
                this.outputChannel.appendLine(`stderr: ${execError.stderr}`);
            }
            throw error;
        }
    }
}
