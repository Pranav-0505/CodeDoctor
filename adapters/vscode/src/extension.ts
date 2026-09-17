import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    const diagnosticCollection = vscode.languages.createDiagnosticCollection('codedoctor');

    const analyzeCmd = vscode.commands.registerCommand('codedoctor.analyzeFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage('No active code editor found.');
            return;
        }

        const document = editor.document;
        const code = document.getText();
        const file_path = document.fileName;
        const language = document.languageId;

        const config = vscode.workspace.getConfiguration('codedoctor');
        const apiUrl = config.get<string>('apiUrl', 'http://127.0.0.1:8000/api/v1');
        const learningLevel = config.get<string>('learningLevel', 'Beginner');

        try {
            vscode.window.showInformationMessage('Code Doctor: Diagnosing active buffer...');
            const response = await fetch(`${apiUrl}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code,
                    language,
                    file_path,
                    learning_level: learningLevel,
                    platform: 'vscode'
                })
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            const data: any = await response.json();
            const diagnostics: vscode.Diagnostic[] = [];

            for (const issue of data.issues) {
                const line = Math.max(0, issue.line - 1);
                const range = new vscode.Range(line, 0, line, 100);
                const severity = issue.severity === 'CRITICAL' || issue.severity === 'HIGH'
                    ? vscode.DiagnosticSeverity.Error
                    : vscode.DiagnosticSeverity.Warning;

                const diag = new vscode.Diagnostic(range, `[Code Doctor ${issue.rule_id}] ${issue.title}: ${issue.explanation || issue.message}`, severity);
                diag.source = 'Code Doctor';
                diagnostics.push(diag);
            }

            diagnosticCollection.set(document.uri, diagnostics);
            vscode.window.showInformationMessage(`Code Doctor Scan Complete: ${data.total_issues} issue(s) found. Health Score: ${data.health_score}/100.`);

        } catch (err: any) {
            vscode.window.showErrorMessage(`Code Doctor Connection Failed: ${err.message}. Is backend running on http://127.0.0.1:8000?`);
        }
    });

    context.subscriptions.push(analyzeCmd, diagnosticCollection);
}

export function deactivate() {}
