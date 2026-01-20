import * as vscode from 'vscode';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export class PythonEnvironment {
    private outputChannel: vscode.OutputChannel;

    constructor(outputChannel: vscode.OutputChannel) {
        this.outputChannel = outputChannel;
    }

    private cachedPythonPath: string | null = null;

    /**
     * Get the Python executable path from settings
     */
    public getPythonPath(): string {
        const config = vscode.workspace.getConfiguration('diffmanifests');
        let pythonPath = config.get<string>('pythonPath', '');

        // If pythonPath is empty, try to use the Python extension's interpreter
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

        // If we have a cached Python path that was verified, use it
        if (!pythonPath && this.cachedPythonPath) {
            return this.cachedPythonPath;
        }

        // Default to python3, but will be verified in isPythonAvailable()
        return pythonPath || 'python3';
    }

    /**
     * Set the cached Python path after verification
     */
    private setCachedPythonPath(path: string): void {
        this.cachedPythonPath = path;
    }

    /**
     * Get the diffmanifests package path from settings
     */
    public getPackagePath(): string {
        const config = vscode.workspace.getConfiguration('diffmanifests');
        return config.get<string>('packagePath', '');
    }

    /**
     * Check if Python is available and verify it's Python 3
     */
    public async isPythonAvailable(): Promise<boolean> {
        const pythonPath = this.getPythonPath();
        const pythonCandidates = [pythonPath, 'python3', 'python'];

        for (const candidate of pythonCandidates) {
            try {
                const { stdout, stderr } = await execAsync(`${candidate} --version`, {
                    env: { ...process.env, PATH: process.env.PATH }
                });
                const versionOutput = stdout.trim() || stderr.trim(); // Python 2 outputs to stderr
                this.outputChannel.appendLine(`Testing ${candidate}: ${versionOutput}`);

                // Check if it's Python 3.x
                const isPython3 = /Python 3\.\d+/.test(versionOutput);
                if (isPython3) {
                    this.outputChannel.appendLine(`✓ Using ${candidate} (${versionOutput})`);
                    this.setCachedPythonPath(candidate);
                    return true;
                } else {
                    this.outputChannel.appendLine(`✗ ${candidate} is not Python 3 (${versionOutput})`);
                }
            } catch (error) {
                this.outputChannel.appendLine(`✗ ${candidate} not available`);
            }
        }

        this.outputChannel.appendLine(`Python 3 not found. Tried: ${pythonCandidates.join(', ')}`);
        return false;
    }

    /**
     * Check if diffmanifests package is installed
     */
    public async isDiffManifestsInstalled(): Promise<boolean> {
        // Method 1: Try to run diffmanifests directly (system-wide installation)
        try {
            const { stdout } = await execAsync('diffmanifests --version', {
                env: { ...process.env, PATH: process.env.PATH }
            });
            this.outputChannel.appendLine(`✓ diffmanifests found in PATH: ${stdout.split('\n').pop()?.trim()}`);
            return true;
        } catch (error) {
            this.outputChannel.appendLine('diffmanifests not found in PATH, checking pip installation...');
        }

        // Method 2: Check via pip show with verified Python 3
        const pythonPath = this.cachedPythonPath || this.getPythonPath();
        const pythonCommands = [pythonPath, 'python3', 'python'];

        for (const cmd of pythonCommands) {
            try {
                const { stdout } = await execAsync(`${cmd} -m pip show diffmanifests`, {
                    env: { ...process.env, PATH: process.env.PATH }
                });
                // Extract version from pip show output
                const versionMatch = stdout.match(/Version:\s*(.+)/);
                const version = versionMatch ? versionMatch[1].trim() : 'unknown';
                this.outputChannel.appendLine(`✓ diffmanifests package found via ${cmd} (version ${version})`);
                return true;
            } catch (error) {
                // Silent, will try next candidate
            }
        }

        this.outputChannel.appendLine('✗ diffmanifests package is not installed');
        return false;
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
                        `${pythonPath} -m pip install${upgradeFlag} diffmanifests`,
                        {
                            maxBuffer: 1024 * 1024 * 10, // 10MB buffer
                            env: { ...process.env, PATH: process.env.PATH }
                        }
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
            this.outputChannel.appendLine('Checking current diffmanifests version...');
            const { stdout: showOutput } = await execAsync(
                `${pythonPath} -m pip show diffmanifests`,
                { env: { ...process.env, PATH: process.env.PATH } }
            );
            const versionMatch = showOutput.match(/Version:\s*(.+)/);
            const currentVersion = versionMatch ? versionMatch[1].trim() : 'unknown';

            if (currentVersion === 'unknown') {
                this.outputChannel.appendLine('Could not determine current version');
                return { hasUpdate: false, currentVersion: 'unknown', latestVersion: 'unknown' };
            }

            this.outputChannel.appendLine(`Current version: ${currentVersion}`);

            // Use pip install --dry-run --upgrade to check if update is available
            // This is more reliable across different pip versions and platforms
            this.outputChannel.appendLine('Checking for available updates...');
            try {
                const { stdout: dryRunOutput, stderr: dryRunStderr } = await execAsync(
                    `${pythonPath} -m pip install diffmanifests --upgrade --dry-run`,
                    {
                        maxBuffer: 1024 * 1024 * 5,
                        env: { ...process.env, PATH: process.env.PATH }
                    }
                );

                // Log stderr for debugging (not necessarily an error)
                if (dryRunStderr && dryRunStderr.trim()) {
                    this.outputChannel.appendLine(`Dry-run stderr: ${dryRunStderr}`);
                }

                // Check if it would install a new version
                const wouldInstallMatch = dryRunOutput.match(/Would install diffmanifests-([0-9.]+)/i);
                if (wouldInstallMatch) {
                    const latestVersion = wouldInstallMatch[1].trim();
                    const hasUpdate = currentVersion !== latestVersion;
                    this.outputChannel.appendLine(`Latest version available: ${latestVersion}`);
                    this.outputChannel.appendLine(`Update available: ${hasUpdate}`);
                    return { hasUpdate, currentVersion, latestVersion };
                }

                // If no "Would install" message, package is up to date
                this.outputChannel.appendLine(`No updates found - package is up to date at version ${currentVersion}`);
                return { hasUpdate: false, currentVersion, latestVersion: currentVersion };
            } catch (dryRunError: any) {
                // Fallback: try pip index versions (may not work on older pip versions)
                this.outputChannel.appendLine(`Dry-run method failed: ${dryRunError.message || dryRunError}`);
                this.outputChannel.appendLine('Trying pip index versions as fallback...');
                try {
                    const { stdout: indexOutput } = await execAsync(
                        `${pythonPath} -m pip index versions diffmanifests`,
                        { env: { ...process.env, PATH: process.env.PATH } }
                    );
                    const latestMatch = indexOutput.match(/diffmanifests\s+\(([0-9.]+)\)/i);
                    if (latestMatch) {
                        const latestVersion = latestMatch[1].trim();
                        const hasUpdate = currentVersion !== latestVersion;
                        this.outputChannel.appendLine(`Latest version from index: ${latestVersion}`);
                        this.outputChannel.appendLine(`Update available: ${hasUpdate}`);
                        return { hasUpdate, currentVersion, latestVersion };
                    }
                } catch (indexError: any) {
                    this.outputChannel.appendLine(`pip index versions also failed: ${indexError.message || indexError}`);
                }

                // Last fallback: assume no update available
                this.outputChannel.appendLine('Could not determine if updates are available, assuming up to date');
                return { hasUpdate: false, currentVersion, latestVersion: currentVersion };
            }
        } catch (error: any) {
            this.outputChannel.appendLine(`Failed to check for updates: ${error.message || error}`);
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
            const pythonPath = this.cachedPythonPath || this.getPythonPath();
            const { stdout } = await execAsync(
                `${pythonPath} -m pip show diffmanifests | grep "Version:" || ${pythonPath} -m pip show diffmanifests | findstr /C:"Version:"`,
                { env: { ...process.env, PATH: process.env.PATH } }
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
        // Use cached Python path if available, otherwise get from config
        const pythonPath = this.cachedPythonPath || this.getPythonPath();
        const command = `${pythonPath} ${args.join(' ')}`;

        this.outputChannel.appendLine(`Executing: ${command}`);

        try {
            const result = await execAsync(command, {
                maxBuffer: 1024 * 1024 * 50, // 50MB buffer for large outputs
                env: { ...process.env, PATH: process.env.PATH }
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
