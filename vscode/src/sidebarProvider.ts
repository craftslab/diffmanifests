import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export class SidebarProvider implements vscode.TreeDataProvider<SidebarItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<SidebarItem | undefined | null | void> = new vscode.EventEmitter<SidebarItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<SidebarItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private context: vscode.ExtensionContext) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: SidebarItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: SidebarItem): Thenable<SidebarItem[]> {
        if (!element) {
            // Root level items
            return Promise.resolve([
                new SidebarItem(
                    'Actions',
                    vscode.TreeItemCollapsibleState.Expanded,
                    'actions',
                    'folder'
                ),
                new SidebarItem(
                    'Recent Files',
                    vscode.TreeItemCollapsibleState.Collapsed,
                    'recent',
                    'folder'
                ),
                new SidebarItem(
                    'Quick Links',
                    vscode.TreeItemCollapsibleState.Collapsed,
                    'links',
                    'folder'
                )
            ]);
        } else if (element.contextValue === 'actions') {
            // Action items
            return Promise.resolve([
                new SidebarItem(
                    'Compare Manifests',
                    vscode.TreeItemCollapsibleState.None,
                    'action-compare',
                    'symbol-file',
                    'diffmanifests.compare',
                    'Compare two manifest files'
                ),
                new SidebarItem(
                    'Open Output File',
                    vscode.TreeItemCollapsibleState.None,
                    'action-output',
                    'go-to-file',
                    'diffmanifests.openOutput',
                    'Open a comparison result file'
                ),
                new SidebarItem(
                    'Refresh Environment',
                    vscode.TreeItemCollapsibleState.None,
                    'action-refresh',
                    'refresh',
                    'diffmanifests.checkEnvironment',
                    'Check Python and diffmanifests installation'
                )
            ]);
        } else if (element.contextValue === 'recent') {
            // Recent files
            return this.getRecentFiles();
        } else if (element.contextValue === 'settings') {
            // Settings items
            return this.getSettingsItems();
        } else if (element.contextValue === 'links') {
            // Quick links
            return Promise.resolve([
                new SidebarItem(
                    'GitHub Repository',
                    vscode.TreeItemCollapsibleState.None,
                    'link-github',
                    'github',
                    'diffmanifests.openGitHub',
                    'Open GitHub repository'
                ),
                new SidebarItem(
                    'Documentation',
                    vscode.TreeItemCollapsibleState.None,
                    'link-docs',
                    'book',
                    'diffmanifests.openDocs',
                    'Open documentation'
                ),
                new SidebarItem(
                    'Report Issue',
                    vscode.TreeItemCollapsibleState.None,
                    'link-issues',
                    'bug',
                    'diffmanifests.reportIssue',
                    'Report an issue on GitHub'
                )
            ]);
        }

        return Promise.resolve([]);
    }

    private async getRecentFiles(): Promise<SidebarItem[]> {
        const recentFiles = this.context.globalState.get<string[]>('recentFiles', []);

        if (recentFiles.length === 0) {
            return [
                new SidebarItem(
                    'No recent files',
                    vscode.TreeItemCollapsibleState.None,
                    'empty',
                    'info',
                    undefined,
                    'No comparison results yet'
                )
            ];
        }

        return recentFiles
            .filter(file => fs.existsSync(file))
            .slice(0, 10) // Show last 10 files
            .map(file => {
                const item = new SidebarItem(
                    path.basename(file),
                    vscode.TreeItemCollapsibleState.None,
                    'recent-file',
                    'file',
                    undefined,
                    file
                );
                item.resourceUri = vscode.Uri.file(file);
                item.command = {
                    command: 'vscode.open',
                    title: 'Open File',
                    arguments: [vscode.Uri.file(file)]
                };
                return item;
            });
    }

    private async getSettingsItems(): Promise<SidebarItem[]> {
        const config = vscode.workspace.getConfiguration('diffmanifests');
        const pythonPath = config.get<string>('pythonPath', 'python');
        const packagePath = config.get<string>('packagePath', '');
        const configFile = config.get<string>('configFile', 'Not set');
        const outputFormat = config.get<string>('outputFormat', '.json');
        const autoInstall = config.get<boolean>('autoInstall', true);
        const showOutputPanel = config.get<boolean>('showOutputPanel', true);

        const items = [
            new SidebarItem(
                `Python: ${pythonPath}`,
                vscode.TreeItemCollapsibleState.None,
                'setting-python',
                'symbol-namespace',
                'diffmanifests.configurePythonPath',
                'Configure Python path'
            )
        ];

        // Only show Package Path if Auto Install is disabled
        if (!autoInstall) {
            const packageDisplay = packagePath ? path.basename(packagePath) : 'Not set';
            items.push(
                new SidebarItem(
                    `Package: ${packageDisplay}`,
                    vscode.TreeItemCollapsibleState.None,
                    'setting-package',
                    'package',
                    'diffmanifests.configurePackagePath',
                    packagePath || 'Configure package path'
                )
            );
        }

        items.push(
            new SidebarItem(
                `Config: ${path.basename(configFile)}`,
                vscode.TreeItemCollapsibleState.None,
                'setting-config',
                'settings-gear',
                'diffmanifests.configureConfigFile',
                configFile
            ),
            new SidebarItem(
                `Format: ${outputFormat}`,
                vscode.TreeItemCollapsibleState.None,
                'setting-format',
                'symbol-enum',
                'diffmanifests.configureOutputFormat',
                'Configure output format'
            ),
            new SidebarItem(
                `Auto Install: ${autoInstall ? 'On' : 'Off'}`,
                vscode.TreeItemCollapsibleState.None,
                'setting-auto',
                'symbol-boolean',
                'diffmanifests.toggleAutoInstall',
                'Toggle auto-install feature'
            ),
            new SidebarItem(
                `Show Output: ${showOutputPanel ? 'On' : 'Off'}`,
                vscode.TreeItemCollapsibleState.None,
                'setting-output',
                'output',
                'diffmanifests.toggleShowOutput',
                'Toggle auto-show output panel'
            ),
            new SidebarItem(
                'Open Settings',
                vscode.TreeItemCollapsibleState.None,
                'setting-open',
                'settings',
                'diffmanifests.openSettings',
                'Open extension settings'
            )
        );

        return items;
    }

    public addRecentFile(filePath: string): void {
        const recentFiles = this.context.globalState.get<string[]>('recentFiles', []);

        // Remove if already exists
        const filtered = recentFiles.filter(f => f !== filePath);

        // Add to front
        filtered.unshift(filePath);

        // Keep only last 20
        const updated = filtered.slice(0, 20);

        this.context.globalState.update('recentFiles', updated);
        this.refresh();
    }

    public clearRecentFiles(): void {
        this.context.globalState.update('recentFiles', []);
        this.refresh();
    }
}

class SidebarItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly contextValue: string,
        public readonly iconId?: string,
        public readonly commandId?: string,
        public readonly description?: string
    ) {
        super(label, collapsibleState);

        this.tooltip = description || label;
        this.description = collapsibleState === vscode.TreeItemCollapsibleState.None ? description : undefined;

        if (iconId) {
            this.iconPath = new vscode.ThemeIcon(iconId);
        }

        if (commandId) {
            this.command = {
                command: commandId,
                title: label,
                arguments: []
            };
        }
    }
}
