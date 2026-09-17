import argparse
import os
import sys
from codedoctor.client import LocalEngineClient
from codedoctor.formatter import CLIFormatter

VERSION = "1.0.0"

def main():
    parser = argparse.ArgumentParser(prog="codedoctor", description="Code Doctor — Universal Intelligent Code Diagnosis & Repair Platform")
    parser.add_argument("--version", "-v", action="version", version=f"codedoctor v{VERSION}")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: scan
    scan_parser = subparsers.add_parser("scan", help="Scan a file or project directory for diagnostic errors")
    scan_parser.add_argument("target", help="File or directory path to scan")
    scan_parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (text or json)")
    scan_parser.add_argument("--level", choices=["Beginner", "Intermediate", "Advanced"], default="Beginner", help="Explanation learning level")

    # Command: diagnose
    diag_parser = subparsers.add_parser("diagnose", help="Diagnose specific code or error trace file")
    diag_parser.add_argument("target", help="File containing code or compiler error trace")
    diag_parser.add_argument("--format", choices=["text", "json"], default="text")

    # Command: fix
    fix_parser = subparsers.add_parser("fix", help="Run Code Surgery to repair target file")
    fix_parser.add_argument("target", help="File path to repair")
    fix_parser.add_argument("--apply", action="store_true", help="Apply fix to file after preview")

    # Command: health
    health_parser = subparsers.add_parser("health", help="Display Code Health Score for file or project")
    health_parser.add_argument("target", help="Target file or project folder")
    health_parser.add_argument("--format", choices=["text", "json"], default="text")

    # Command: report
    report_parser = subparsers.add_parser("report", help="Generate full project analysis report")
    report_parser.add_argument("target", help="Target project folder")
    report_parser.add_argument("--format", choices=["text", "json"], default="text")

    args = parser.parse_args()
    client = LocalEngineClient()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command in ("scan", "diagnose"):
        if os.path.isdir(args.target):
            res = client.scan_project(args.target, learning_level=getattr(args, 'level', 'Beginner'))
            CLIFormatter.print_project_report(res, output_json=(args.format == "json"))
        else:
            res = client.scan_file(args.target, learning_level=getattr(args, 'level', 'Beginner'))
            CLIFormatter.print_diagnostics(res, output_json=(args.format == "json"))

    elif args.command == "health":
        if os.path.isdir(args.target):
            res = client.scan_project(args.target)
            CLIFormatter.print_project_report(res, output_json=(args.format == "json"))
        else:
            res = client.scan_file(args.target)
            CLIFormatter.print_diagnostics(res, output_json=(args.format == "json"))

    elif args.command == "fix":
        if not os.path.isfile(args.target):
            print(f"Error: Target file not found: {args.target}")
            sys.exit(1)
        res = client.scan_file(args.target)
        if not res.issues:
            print("No issues detected in file to repair.")
        else:
            target_issue = res.issues[0]
            from app.core.surgery import CodeSurgeryEngine
            from app.core.verification import FixVerificationEngine
            with open(args.target, "r", encoding="utf-8") as f:
                code = f.read()
            patched, diff_patch, summary = CodeSurgeryEngine.generate_fix(code, target_issue)
            print(f"\n--- CODE SURGERY DIFF PREVIEW FOR {args.target} ---")
            print(diff_patch)
            
            # Run Safe Verification
            ver_res = FixVerificationEngine.verify_patch(code, patched, language=res.language, rule_id=target_issue.rule_id)
            print(f"\nVerification Status: {ver_res.status} ({ver_res.details})")

            if args.apply and ver_res.passed:
                with open(args.target, "w", encoding="utf-8") as f:
                    f.writelines(patched)
                print(f"✓ Applied verified fix to {args.target}")
            elif args.apply:
                print("✗ Fix failed verification, change not applied.")

    elif args.command == "report":
        res = client.scan_project(args.target if os.path.isdir(args.target) else os.path.dirname(args.target) or ".")
        CLIFormatter.print_project_report(res, output_json=(args.format == "json"))

if __name__ == "__main__":
    main()
