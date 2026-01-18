import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';

export class FileSelector {
    /**
     * Select a manifest XML file
     */
    public static async selectManifestFile(prompt: string): Promise<string | undefined> {
        const files = await vscode.window.showOpenDialog({
            canSelectFiles: true,
            canSelectFolders: false,
            canSelectMany: false,
            filters: {
                'Manifest Files': ['xml'],
                'All Files': ['*']
            },
            title: prompt
        });

        if (files && files.length > 0) {
            return files[0].fsPath;
        }
        return undefined;
    }

    /**
     * Generate config file from settings
     */
    public static async selectConfigFile(): Promise<string | undefined> {
        return this.generateConfigFromSettings();
    }

    /**
     * Generate a temporary config file from VS Code settings
     */
    private static generateConfigFromSettings(): string {
        const config = vscode.workspace.getConfiguration('diffmanifests');

        // Build config object from settings
        const configObj = {
            gerrit: {
                url: config.get<string>('gerrit.url', 'https://android-review.googlesource.com'),
                user: config.get<string>('gerrit.user', ''),
                pass: config.get<string>('gerrit.password', ''),
                query: {
                    option: config.get<string[]>('gerrit.queryOptions', ['CURRENT_REVISION'])
                }
            },
            gitiles: {
                url: config.get<string>('gitiles.url', 'https://android.googlesource.com'),
                user: config.get<string>('gitiles.user', ''),
                pass: config.get<string>('gitiles.password', ''),
                timeout: config.get<number>('gitiles.timeout', -1),
                retry: config.get<number>('gitiles.retry', 1)
            }
        };

        // Create temporary config file
        const tempDir = os.tmpdir();
        const tempConfigPath = path.join(tempDir, `diffmanifests-config-${Date.now()}.json`);

        fs.writeFileSync(tempConfigPath, JSON.stringify(configObj, null, 2), 'utf8');

        vscode.window.showInformationMessage('Using configuration from extension settings');

        return tempConfigPath;
    }

    /**
     * Select output file location
     */
    public static async selectOutputFile(): Promise<string | undefined> {
        const config = vscode.workspace.getConfiguration('diffmanifests');
        const outputFormat = config.get<string>('outputFormat', '.json');

        // Get workspace folder as default location
        const workspaceFolders = vscode.workspace.workspaceFolders;
        let defaultUri: vscode.Uri | undefined;

        if (workspaceFolders && workspaceFolders.length > 0) {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
            const defaultFileName = `manifest-diff-${timestamp}${outputFormat}`;
            defaultUri = vscode.Uri.file(
                path.join(workspaceFolders[0].uri.fsPath, defaultFileName)
            );
        }

        const file = await vscode.window.showSaveDialog({
            defaultUri: defaultUri,
            filters: outputFormat === '.json'
                ? { 'JSON Files': ['json'] }
                : { 'Excel Files': ['xlsx'] },
            title: 'Save comparison output'
        });

        if (file) {
            return file.fsPath;
        }
        return undefined;
    }
}
