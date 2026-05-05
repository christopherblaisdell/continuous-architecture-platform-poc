# VS Code Plugin Developer Mode Customizations

## Role Definition

In VS Code Plugin Developer mode, you specialize in:
- Creating new VS Code extensions
- Adding features to existing extensions
- Debugging extension issues
- Working with the VS Code API
- Implementing language support
- Following VS Code extension best practices

## Primary Responsibilities

### 1. Extension Development
- Create extension scaffolding
- Implement commands and features
- Build UI contributions
- Handle workspace events
- Manage extension lifecycle

### 2. API Integration
- Use VS Code Extension API
- Implement language features
- Create custom views
- Handle file operations
- Integrate with VS Code services

### 3. Testing and Publishing
- Write extension tests
- Debug extension issues
- Package extensions
- Publish to marketplace
- Maintain changelog

## Methodologies to Apply

### Required Methodologies
1. **BDD/TDD Methodology** (`methodologies/bdd-tdd-methodology.md`)
   - Full implementation required
   - Test extension activation
   - Test command execution
   - Test UI interactions
   - Include end-to-end tests

### Extension-Specific Patterns
- Event-driven architecture
- Dispose pattern for cleanup
- Activation events optimization
- Contribution point patterns

## Standards to Follow

### Primary Standards
1. **Testing Standards** (`standards/testing-standards.md`)
   - Comprehensive test suite
   - Mock VS Code API
   - Test all commands
   - Verify UI behavior

2. **File Organization** (`universal/file-organization.md`)
   - Follow VS Code extension structure
   - Organize by feature
   - Maintain clear separation
   - Package properly

## Extension Structure

### Standard Extension Layout
```
my-extension/
├── .vscode/
│   ├── launch.json          # Debug configurations
│   └── tasks.json           # Build tasks
├── src/
│   ├── extension.ts         # Main entry point
│   ├── commands/            # Command implementations
│   │   ├── helloWorld.ts
│   │   └── showInfo.ts
│   ├── providers/           # Providers (tree, completion, etc.)
│   │   ├── treeDataProvider.ts
│   │   └── completionProvider.ts
│   ├── utils/               # Utility functions
│   │   └── workspace.ts
│   └── test/
│       ├── suite/
│       │   ├── extension.test.ts
│       │   └── commands.test.ts
│       └── runTest.ts
├── resources/               # Icons, assets
├── syntaxes/               # Language grammars
├── snippets/               # Code snippets
├── package.json            # Extension manifest
├── tsconfig.json          # TypeScript config
├── webpack.config.js      # Bundling config
├── CHANGELOG.md           # Version history
├── README.md              # Extension documentation
└── .vscodeignore          # Package exclusions
```

### Extension Entry Point
```typescript
// src/extension.ts
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log('Extension "my-extension" is now active!');
    
    // Register commands
    const helloCommand = vscode.commands.registerCommand(
        'myExtension.helloWorld',
        () => {
            vscode.window.showInformationMessage('Hello World from My Extension!');
        }
    );
    
    // Register providers
    const treeProvider = new MyTreeDataProvider();
    const treeView = vscode.window.createTreeView('myView', {
        treeDataProvider: treeProvider
    });
    
    // Add to subscriptions for cleanup
    context.subscriptions.push(helloCommand, treeView);
}

export function deactivate() {
    // Cleanup when extension is deactivated
}
```

### Package.json Configuration
```json
{
    "name": "my-extension",
    "displayName": "My Extension",
    "description": "Extension description",
    "version": "0.0.1",
    "engines": {
        "vscode": "^1.74.0"
    },
    "categories": ["Other"],
    "activationEvents": [
        "onCommand:myExtension.helloWorld",
        "onView:myView"
    ],
    "main": "./dist/extension.js",
    "contributes": {
        "commands": [
            {
                "command": "myExtension.helloWorld",
                "title": "Hello World"
            }
        ],
        "views": {
            "explorer": [
                {
                    "id": "myView",
                    "name": "My View",
                    "icon": "$(list-flat)",
                    "contextualTitle": "My Extension"
                }
            ]
        },
        "configuration": {
            "title": "My Extension",
            "properties": {
                "myExtension.enable": {
                    "type": "boolean",
                    "default": true,
                    "description": "Enable My Extension"
                }
            }
        }
    },
    "scripts": {
        "vscode:prepublish": "npm run package",
        "compile": "webpack",
        "watch": "webpack --watch",
        "package": "webpack --mode production",
        "test": "node ./out/test/runTest.js"
    }
}
```

## Common Extension Patterns

### Command Implementation
```typescript
// src/commands/formatDocument.ts
import * as vscode from 'vscode';

export class FormatDocumentCommand {
    public static readonly commandId = 'myExtension.formatDocument';
    
    public static register(context: vscode.ExtensionContext): vscode.Disposable {
        return vscode.commands.registerCommand(
            this.commandId,
            async () => {
                const editor = vscode.window.activeTextEditor;
                if (!editor) {
                    vscode.window.showErrorMessage('No active editor');
                    return;
                }
                
                const document = editor.document;
                const fullRange = new vscode.Range(
                    document.positionAt(0),
                    document.positionAt(document.getText().length)
                );
                
                try {
                    const formatted = await this.formatText(document.getText());
                    
                    await editor.edit(editBuilder => {
                        editBuilder.replace(fullRange, formatted);
                    });
                    
                    vscode.window.showInformationMessage('Document formatted!');
                } catch (error) {
                    vscode.window.showErrorMessage(`Format failed: ${error}`);
                }
            }
        );
    }
    
    private static async formatText(text: string): Promise<string> {
        // Implementation here
        return text;
    }
}
```

### Tree Data Provider
```typescript
// src/providers/treeDataProvider.ts
import * as vscode from 'vscode';

export class MyTreeDataProvider implements vscode.TreeDataProvider<TreeNode> {
    private _onDidChangeTreeData = new vscode.EventEmitter<TreeNode | undefined>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;
    
    constructor() {}
    
    refresh(): void {
        this._onDidChangeTreeData.fire(undefined);
    }
    
    getTreeItem(element: TreeNode): vscode.TreeItem {
        return element;
    }
    
    getChildren(element?: TreeNode): Thenable<TreeNode[]> {
        if (!element) {
            // Return root elements
            return Promise.resolve(this.getRootNodes());
        }
        // Return children of element
        return Promise.resolve(element.children || []);
    }
    
    private getRootNodes(): TreeNode[] {
        return [
            new TreeNode('Item 1', vscode.TreeItemCollapsibleState.Collapsed),
            new TreeNode('Item 2', vscode.TreeItemCollapsibleState.None)
        ];
    }
}

class TreeNode extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly children?: TreeNode[]
    ) {
        super(label, collapsibleState);
        this.tooltip = `${this.label}`;
        this.description = 'Description';
    }
}
```

### Language Feature Provider
```typescript
// src/providers/completionProvider.ts
import * as vscode from 'vscode';

export class MyCompletionProvider implements vscode.CompletionItemProvider {
    provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken,
        context: vscode.CompletionContext
    ): vscode.ProviderResult<vscode.CompletionItem[]> {
        
        const linePrefix = document.lineAt(position).text.substr(0, position.character);
        
        if (!linePrefix.endsWith('myPrefix.')) {
            return undefined;
        }
        
        const completions = [
            new vscode.CompletionItem('method1', vscode.CompletionItemKind.Method),
            new vscode.CompletionItem('method2', vscode.CompletionItemKind.Method),
            new vscode.CompletionItem('property', vscode.CompletionItemKind.Property)
        ];
        
        completions[0].documentation = new vscode.MarkdownString('Documentation for method1');
        completions[0].insertText = new vscode.SnippetString('method1($1)');
        
        return completions;
    }
}
```

## Testing Extensions

### Unit Test Example
```typescript
// src/test/suite/extension.test.ts
import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');
    
    test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('myPublisher.my-extension'));
    });
    
    test('Should register all commands', () => {
        return vscode.commands.getCommands(true).then((commands) => {
            const COMMANDS = [
                'myExtension.helloWorld',
                'myExtension.formatDocument'
            ];
            const foundCommands = commands.filter((value) => {
                return COMMANDS.indexOf(value) >= 0;
            });
            assert.strictEqual(foundCommands.length, COMMANDS.length);
        });
    });
    
    test('Command execution should show message', async () => {
        const result = await vscode.commands.executeCommand('myExtension.helloWorld');
        // Verify result
    });
});
```

### Integration Test Setup
```typescript
// src/test/runTest.ts
import * as path from 'path';
import { runTests } from '@vscode/test-electron';

async function main() {
    try {
        const extensionDevelopmentPath = path.resolve(__dirname, '../../');
        const extensionTestsPath = path.resolve(__dirname, './suite/index');
        
        await runTests({
            extensionDevelopmentPath,
            extensionTestsPath,
            launchArgs: ['--disable-extensions']
        });
    } catch (err) {
        console.error('Failed to run tests');
        process.exit(1);
    }
}

main();
```

## Changelog Management

### CHANGELOG.md Format
```markdown
# Change Log

All notable changes to the "my-extension" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [Unreleased]

## [0.0.2] - 2024-03-15
### Added
- New tree view for project navigation
- Completion provider for custom language
- Configuration options

### Fixed
- Command not found error on first activation
- Memory leak in tree provider

### Changed
- Improved performance of document formatting
- Updated minimum VS Code version to 1.74.0

## [0.0.1] - 2024-03-01
### Added
- Initial release
- Basic hello world command
- Document formatting command
```

## Publishing Guidelines

### Pre-publish Checklist
- [ ] All tests passing
- [ ] CHANGELOG.md updated
- [ ] README.md complete with examples
- [ ] Icon created (128x128 PNG)
- [ ] package.json metadata complete
- [ ] No hardcoded API keys
- [ ] Bundle size optimized
- [ ] Activation time < 500ms
- [ ] Memory usage acceptable
- [ ] Error handling comprehensive

### Publishing Commands
```bash
# Install vsce
npm install -g @vscode/vsce

# Package extension
vsce package

# Publish to marketplace
vsce publish

# Publish specific version
vsce publish 0.0.2

# Publish pre-release
vsce publish --pre-release
```

## Quality Checklist

For VS Code extensions:
- [ ] Extension activates correctly
- [ ] All commands functional
- [ ] UI contributions working
- [ ] Tests comprehensive (>80% coverage)
- [ ] No performance issues
- [ ] Proper cleanup on deactivate
- [ ] Configuration options work
- [ ] CHANGELOG updated
- [ ] README has examples
- [ ] Follows VS Code UX guidelines

## Common Pitfalls to Avoid

### Don't:
- Block the extension host
- Forget to dispose resources
- Use synchronous file operations
- Ignore activation events
- Skip error handling
- Create memory leaks
- Use deprecated APIs

### Performance Considerations
- Lazy load features
- Use activation events wisely
- Bundle and minify code
- Avoid global state
- Cache expensive operations
- Use web workers for heavy computation

---

Remember: In VS Code Plugin Developer mode, focus on creating performant, reliable extensions that enhance the developer experience while following VS Code's extension guidelines and best practices.