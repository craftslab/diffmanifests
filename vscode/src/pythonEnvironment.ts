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
    public async installDiffManifests(upgrade: boolean = false): Promise<void> {
        const pythonPath = this.getPythonPath();
        const action = upgrade ? 'Upgrading' : 'Installing';
        const actionLower = upgrade ? 'upgrade' : 'install';
        const upgradeFlag = upgrade ? ' --upgrade' : '';

        return vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: `${action} diffmanifests package...`,
                cancellable: false
            },
            async (progress) => {
                try {
                    this.outputChannel.show(true);
                    this.outputChannel.appendLine(`${action} diffmanifests...`);

                    progress.report({ increment: 30, message: `Running pip ${actionLower}...` });

                    const { stdout, stderr } = await execAsync(
                        `"${pythonPath}" -m pip install${upgradeFlag} diffmanifests`,
                        { maxBuffer: 1024 * 1024 * 10 } // 10MB buffer
                    );

                    this.outputChannel.appendLine(stdout);
                    if (stderr) {
                        this.outputChannel.appendLine(stderr);
                    }

                    progress.report({ increment: 70, message: `${action} complete` });

                    vscode.window.showInformationMessage(`diffmanifests ${upgrade ? 'upgraded' : 'installed'} successfully`);
                    this.outputChannel.appendLine(`diffmanifests ${upgrade ? 'upgraded' : 'installed'} successfully`);
                } catch (error) {
                    const errorMessage = error instanceof Error ? error.message : String(error);
                    this.outputChannel.appendLine(`${action} failed: ${errorMessage}`);
                    throw new Error(`Failed to ${actionLower} diffmanifests: ${errorMessage}`);
                }
            }
        );
    }

    /**
     * Check if there's a newer version of diffmanifests available
     */
    public async checkForUpdates(): Promise<{ hasUpdate: boolean; currentVersion: string; latestVersion: string }> {
        try {
            const pythonPath = this.getPythonPath();

            // Get current version
            const { stdout: showOutput } = await execAsync(
                `"${pythonPath}" -m pip show diffmanifests`
            );
            const versionMatch = showOutput.match(/Version:\s*(.+)/);
            const currentVersion = versionMatch ? versionMatch[1].trim() : 'unknown';

            // Check latest version from PyPI
            const { stdout: indexOutput } = await execAsync(
                `"${pythonPath}" -m pip index versions diffmanifests`
            );
            const latestMatch = indexOutput.match(/diffmanifests\s+\((.+?)\)/);
            const latestVersion = latestMatch ? latestMatch[1].trim() : currentVersion;

            const hasUpdate = currentVersion !== latestVersion && latestVersion !== 'unknown';

            return { hasUpdate, currentVersion, latestVersion };
        } catch (error) {
            this.outputChannel.appendLine(`Failed to check for updates: ${error}`);
            return { hasUpdate: false, currentVersion: 'unknown', latestVersion: 'unknown' };
        }
    }

    /**
     * Upgrade diffmanifests package
     */
    public async upgradeDiffManifests(): Promise<void> {
        return this.installDiffManifests(true);
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
