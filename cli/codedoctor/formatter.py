import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()

class CLIFormatter:
    @staticmethod
    def print_diagnostics(res, output_json: bool = False):
        if output_json:
            print(json.dumps(res.dict() if hasattr(res, 'dict') else res, indent=2))
            return

        console.print(Panel(f"[bold cyan]CODE DOCTOR DIAGNOSIS REPORT[/bold cyan]\nFile: {res.file_path} | Issues: {res.total_issues} | Health Score: {res.health_score}/100", title="Code Doctor v1.0"))

        if not res.issues:
            console.print("[bold green]✓ No diagnostic issues detected! Code is healthy.[/bold green]")
            return

        table = Table(title="Diagnostic Issues")
        table.add_column("Rule ID", style="magenta")
        table.add_column("Line", style="yellow")
        table.add_column("Severity", style="bold red")
        table.add_column("Category", style="blue")
        table.add_column("Title & Root Cause", style="white")

        for issue in res.issues:
            table.add_row(
                issue.rule_id,
                str(issue.line),
                f"[{'red' if issue.severity in ('CRITICAL', 'HIGH') else 'yellow'}]{issue.severity}[/]",
                issue.category,
                f"{issue.title}\n[dim]{issue.explanation or issue.message}[/dim]"
            )

        console.print(table)

    @staticmethod
    def print_project_report(res, output_json: bool = False):
        if output_json:
            print(json.dumps(res, indent=2))
            return

        console.print(Panel(f"[bold green]CODE DOCTOR PROJECT HEALTH REPORT[/bold green]\nScanned Files: {res['scanned_files_count']} | Total Issues: {res['total_issues']} | Health Score: {res['health_score']}/100", title="Project Scan"))

        if res.get("issues"):
            table = Table(title="Discovered Issues Across Project")
            table.add_column("File", style="cyan")
            table.add_column("Line", style="yellow")
            table.add_column("Severity", style="bold red")
            table.add_column("Title", style="white")
            for issue in res["issues"]:
                table.add_row(
                    issue["file"],
                    str(issue["line"]),
                    issue["severity"],
                    issue["title"]
                )
            console.print(table)
