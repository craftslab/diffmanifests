import * as vscode from 'vscode';
import * as path from 'path';

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
     * Select a config JSON file
     */
    public static async selectConfigFile(): Promise<string | undefined> {
        const config = vscode.workspace.getConfiguration('diffmanifests');
        const defaultConfigPath = config.get<string>('configFile', '');

        // If a default config is set and exists, ask if user wants to use it
        if (defaultConfigPath) {
            const useDefault = await vscode.window.showQuickPick(
                ['Use default config', 'Select different config'],
                {
                    placeHolder: `Use default config: ${defaultConfigPath}?`
                }
            );

            if (useDefault === 'Use default config') {
                return defaultConfigPath;
            }
        }

        const files = await vscode.window.showOpenDialog({
            canSelectFiles: true,
            canSelectFolders: false,
            canSelectMany: false,
            filters: {
                'JSON Files': ['json'],
                'All Files': ['*']
            },
            title: 'Select config file'
        });

        if (files && files.length > 0) {
            const selectedPath = files[0].fsPath;

            // Ask if user wants to save as default
            const saveAsDefault = await vscode.window.showQuickPick(
                ['Yes', 'No'],
                {
                    placeHolder: 'Save this as default config file?'
                }
            );

            if (saveAsDefault === 'Yes') {
                await config.update('configFile', selectedPath, vscode.ConfigurationTarget.Workspace);
            }

            return selectedPath;
        }
        return undefined;
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
