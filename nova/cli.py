"""
🌌 NOVA v3.1 CLI - THE FORENSIC CODE AUDITOR
Main command-line interface.
"""

import os
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from nova import __version__
from nova.utils.display import NovaConsole
from nova.scanners import CodeRotScanner, CoderGuiltScanner, SecurityScanner, PerformanceScanner
from nova.scanners.code_rot import format_rot_report
from nova.scanners.coder_guilt import format_guilt_report
from nova.scanners.security import format_security_report
from nova.scanners.performance import format_performance_report

# Create CLI app
app = typer.Typer(
    name="nova",
    help="🌌 NOVA v3.1 - THE FORENSIC CODE AUDITOR",
    add_completion=False
)

console = Console()
nova_console = NovaConsole()


def validate_repo_path(path: str) -> Path:
    """Validate that the path exists and is a git repository."""
    repo_path = Path(path).resolve()

    if not repo_path.exists():
        console.print(f"[red]Error:[/red] Path does not exist: {repo_path}")
        raise typer.Exit(1)

    if not repo_path.is_dir():
        console.print(f"[red]Error:[/red] Path is not a directory: {repo_path}")
        raise typer.Exit(1)

    git_dir = repo_path / ".git"
    if not git_dir.exists():
        console.print(f"[yellow]Warning:[/yellow] Not a git repository: {repo_path}")
        console.print("[dim]Some features (Code Rot analysis) may be limited.[/dim]")

    return repo_path


@app.command()
def scan(
    repo_path: str = typer.Argument(
        ".",
        help="Path to the repository to scan"
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path for the report (default: NOVA_FORENSIC.md)"
    ),
    full: bool = typer.Option(
        False,
        "--full", "-f",
        help="Run full analysis with LLM interpretation (requires ANTHROPIC_API_KEY)"
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet", "-q",
        help="Minimal output, just save the report"
    ),
    protocol: Optional[str] = typer.Option(
        None,
        "--protocol", "-p",
        help="Run specific protocol only: rot, guilt, security, performance"
    ),
):
    """
    🔬 Perform a forensic scan of a repository.

    NOVA analyzes your codebase across 4 dimensions:
    - Code Rot: Stale files and chaotic zones
    - Coder Guilt: Technical debt markers
    - Security: Vulnerabilities and secrets
    - Performance: Complexity bottlenecks
    """

    # Display banner
    if not quiet:
        nova_console.print_banner()

    # Validate path
    repo_path = validate_repo_path(repo_path)
    repo_name = repo_path.name

    if not quiet:
        nova_console.print_info(f"Target: {repo_path}")
        nova_console.print_info(f"Repository: {repo_name}")

    # Determine output path
    if output is None:
        output = str(repo_path / "NOVA_FORENSIC.md")

    # Single protocol mode
    if protocol:
        run_single_protocol(repo_path, protocol, quiet)
        return

    # Full analysis with LLM
    if full:
        run_full_analysis(repo_path, repo_name, output, quiet)
        return

    # Quick scan (no LLM)
    run_quick_scan(repo_path, repo_name, output, quiet)


def run_single_protocol(repo_path: Path, protocol: str, quiet: bool):
    """Run a single analysis protocol."""
    protocol = protocol.lower()

    if not quiet:
        nova_console.print_phase("scanning", f"Running Protocol: {protocol.upper()}")

    if protocol == "rot":
        scanner = CodeRotScanner(str(repo_path))
        report = scanner.scan()
        console.print(format_rot_report(report))

    elif protocol == "guilt":
        scanner = CoderGuiltScanner(str(repo_path))
        report = scanner.scan()
        console.print(format_guilt_report(report))

    elif protocol == "security":
        scanner = SecurityScanner(str(repo_path))
        report = scanner.scan()
        console.print(format_security_report(report))

    elif protocol == "performance":
        scanner = PerformanceScanner(str(repo_path))
        report = scanner.scan()
        console.print(format_performance_report(report))

    else:
        console.print(f"[red]Unknown protocol:[/red] {protocol}")
        console.print("Available: rot, guilt, security, performance")
        raise typer.Exit(1)


def run_quick_scan(repo_path: Path, repo_name: str, output: str, quiet: bool):
    """Run quick scan without LLM interpretation."""

    if not quiet:
        nova_console.print_phase("scanning", "Running all forensic protocols...")

    scan_results = {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:

        # Protocol A: Code Rot
        task = progress.add_task("[cyan]Protocol A: Code Rot...", total=None)
        try:
            scanner = CodeRotScanner(str(repo_path))
            report = scanner.scan()
            scan_results["code_rot"] = {
                "rot_score": report.rot_score,
                "abandoned_files": [{"path": f.filepath, "days_stale": f.days_stale} for f in report.abandoned_files[:10]],
                "chaotic_files": [{"path": f.filepath, "churn": f.monthly_churn} for f in report.chaotic_files[:10]],
                "total_files": report.total_files_analyzed
            }
        except Exception as e:
            scan_results["code_rot"] = {"error": str(e)}
        progress.remove_task(task)

        # Protocol B: Coder Guilt
        task = progress.add_task("[cyan]Protocol B: Coder Guilt...", total=None)
        try:
            scanner = CoderGuiltScanner(str(repo_path))
            report = scanner.scan()
            scan_results["coder_guilt"] = {
                "guilt_index": report.guilt_index,
                "total_markers": report.total_markers,
                "markers_by_type": report.markers_by_type,
                "god_classes": [{"path": gc.filepath, "lines": gc.line_count} for gc in report.god_classes[:10]],
                "total_lines": report.total_lines_analyzed
            }
        except Exception as e:
            scan_results["coder_guilt"] = {"error": str(e)}
        progress.remove_task(task)

        # Protocol C: Security
        task = progress.add_task("[cyan]Protocol C: Security...", total=None)
        try:
            scanner = SecurityScanner(str(repo_path))
            report = scanner.scan()
            scan_results["security"] = {
                "vulnerability_score": report.vulnerability_score,
                "secret_leaks": [{"path": s.filepath, "type": s.secret_type} for s in report.secret_leaks[:10]],
                "sql_injections": len(report.sql_injections),
                "unprotected_endpoints": [{"endpoint": e.endpoint, "method": e.method} for e in report.unprotected_endpoints[:10]],
                "total_scanned": report.total_files_scanned
            }
        except Exception as e:
            scan_results["security"] = {"error": str(e)}
        progress.remove_task(task)

        # Protocol D: Performance
        task = progress.add_task("[cyan]Protocol D: Performance...", total=None)
        try:
            scanner = PerformanceScanner(str(repo_path))
            report = scanner.scan()
            scan_results["performance"] = {
                "performance_score": report.performance_score,
                "maintainability_index": report.maintainability_index,
                "complex_functions": [{"name": f.function_name, "complexity": f.cyclomatic_complexity} for f in report.complex_functions[:10]],
                "big_o_concerns": [{"name": b.function_name, "complexity": b.estimated_complexity} for b in report.big_o_estimates[:10]],
                "heavy_imports": len(report.heavy_imports)
            }
        except Exception as e:
            scan_results["performance"] = {"error": str(e)}
        progress.remove_task(task)

    # Display summary
    if not quiet:
        nova_console.print_scan_results_summary(scan_results)

    # Generate quick report
    report_content = generate_quick_report(repo_name, scan_results)

    # Save report
    with open(output, 'w', encoding='utf-8') as f:
        f.write(report_content)

    if not quiet:
        nova_console.print_success(f"Report saved to: {output}")
        console.print("\n[dim]Run with --full flag for LLM-powered deep analysis[/dim]")


def run_full_analysis(repo_path: Path, repo_name: str, output: str, quiet: bool):
    """Run full analysis with LLM interpretation (Ralph Loop)."""

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print("[red]Error:[/red] ANTHROPIC_API_KEY environment variable not set")
        console.print("[dim]Set it with: export ANTHROPIC_API_KEY=your_key[/dim]")
        raise typer.Exit(1)

    if not quiet:
        nova_console.print_phase("initializing", "Starting full forensic analysis with Ralph Loop...")

    try:
        from nova.agents import run_nova_analysis

        # Run the full pipeline
        result = run_nova_analysis(str(repo_path), repo_name)

        # Check for errors
        if result.get("error"):
            nova_console.print_error(result["error"])
            raise typer.Exit(1)

        # Display critique info
        if not quiet and result.get("critique"):
            nova_console.print_critique_feedback(result["critique"])

        # Get the final report
        final_report = result.get("final_report_markdown", "")

        if not final_report:
            nova_console.print_error("Failed to generate report")
            raise typer.Exit(1)

        # Save report
        with open(output, 'w', encoding='utf-8') as f:
            f.write(final_report)

        if not quiet:
            nova_console.print_success(f"Full forensic report saved to: {output}")

            # Optionally display report
            show_report = typer.confirm("Display report in terminal?", default=False)
            if show_report:
                nova_console.print_report(final_report)

    except ImportError as e:
        console.print(f"[red]Error:[/red] Missing dependencies for full analysis: {e}")
        console.print("[dim]Install with: pip install langchain langchain-anthropic langgraph[/dim]")
        raise typer.Exit(1)


def generate_quick_report(repo_name: str, scan_results: dict) -> str:
    """Generate a quick report without LLM interpretation."""

    # Calculate overall severity
    rot_score = scan_results.get("code_rot", {}).get("rot_score", 0)
    guilt_index = scan_results.get("coder_guilt", {}).get("guilt_index", 0)
    vuln_score = scan_results.get("security", {}).get("vulnerability_score", 0)
    perf_score = scan_results.get("performance", {}).get("performance_score", 100)

    entropy = (rot_score + guilt_index + (vuln_score * 10) + (100 - perf_score)) / 4

    if entropy > 60 or vuln_score > 5:
        severity = "Critical"
    elif entropy > 40:
        severity = "High"
    elif entropy > 20:
        severity = "Medium"
    else:
        severity = "Low"

    lines = [
        f"# 👁️ NOVA FORENSIC REPORT: {repo_name}",
        f"**Severity Level:** {severity} | **Entropy Score:** {entropy:.0f}/100",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "---",
        "",
        "## 💀 I. THE GRAVEYARD (Code Rot & Stagnation)",
        "> Quick scan results - run with --full for detailed analysis",
        "",
    ]

    # Code Rot section
    rot = scan_results.get("code_rot", {})
    if "error" not in rot:
        lines.append(f"**Rot Score:** {rot.get('rot_score', 0):.1f}/100")
        lines.append(f"**Files Analyzed:** {rot.get('total_files', 0)}")
        if rot.get("abandoned_files"):
            lines.append("\n### Abandoned Files:")
            for f in rot["abandoned_files"][:5]:
                lines.append(f"- {f['path']} ({f['days_stale']} days stale)")
        if rot.get("chaotic_files"):
            lines.append("\n### Chaotic Files:")
            for f in rot["chaotic_files"][:5]:
                lines.append(f"- {f['path']} ({f['churn']} changes/month)")
    else:
        lines.append(f"*Scan error: {rot['error']}*")

    lines.extend(["", "---", "", "## 😓 II. THE CONFESSIONAL (Coder Guilt)", ""])

    # Coder Guilt section
    guilt = scan_results.get("coder_guilt", {})
    if "error" not in guilt:
        lines.append(f"**Guilt Index:** {guilt.get('guilt_index', 0):.1f}/100")
        lines.append(f"**Total Markers:** {guilt.get('total_markers', 0)}")
        if guilt.get("markers_by_type"):
            lines.append("\n### Markers by Type:")
            for mtype, count in guilt["markers_by_type"].items():
                lines.append(f"- {mtype}: {count}")
        if guilt.get("god_classes"):
            lines.append("\n### God Classes:")
            for gc in guilt["god_classes"][:5]:
                lines.append(f"- {gc['path']}: {gc['lines']} lines")
    else:
        lines.append(f"*Scan error: {guilt['error']}*")

    lines.extend(["", "---", "", "## 🛡️ III. THE FORTRESS (Security)", ""])

    # Security section
    security = scan_results.get("security", {})
    if "error" not in security:
        lines.append(f"**Vulnerability Score:** {security.get('vulnerability_score', 0):.1f}/10")
        lines.append(f"**Files Scanned:** {security.get('total_scanned', 0)}")
        if security.get("secret_leaks"):
            lines.append("\n### 🔐 Secret Leaks Detected:")
            for leak in security["secret_leaks"][:5]:
                lines.append(f"- [{leak['type']}] {leak['path']}")
        if security.get("sql_injections"):
            lines.append(f"\n**SQL Injection Risks:** {security['sql_injections']}")
        if security.get("unprotected_endpoints"):
            lines.append("\n### 🚪 Unprotected Endpoints:")
            for ep in security["unprotected_endpoints"][:5]:
                lines.append(f"- [{ep['method']}] {ep['endpoint']}")
    else:
        lines.append(f"*Scan error: {security['error']}*")

    lines.extend(["", "---", "", "## ⚡ IV. THE ENGINE (Performance)", ""])

    # Performance section
    perf = scan_results.get("performance", {})
    if "error" not in perf:
        lines.append(f"**Performance Score:** {perf.get('performance_score', 0):.1f}/100")
        lines.append(f"**Maintainability Index:** {perf.get('maintainability_index', 0):.1f}/100")
        if perf.get("complex_functions"):
            lines.append("\n### Complex Functions:")
            for func in perf["complex_functions"][:5]:
                lines.append(f"- {func['name']}() - Complexity: {func['complexity']}")
        if perf.get("big_o_concerns"):
            lines.append("\n### Big O Concerns:")
            for concern in perf["big_o_concerns"][:5]:
                lines.append(f"- {concern['name']}() - {concern['complexity']}")
    else:
        lines.append(f"*Scan error: {perf['error']}*")

    lines.extend([
        "",
        "---",
        "",
        "## 🌌 V. TRANSMUTATION",
        "",
        "*Run with `--full` flag for LLM-powered refactoring recommendations*",
        "",
        "---",
        "",
        "*Report generated by NOVA v3.1 - The Forensic Code Auditor*",
        "",
        "```",
        "🌌 \"In the darkness of technical debt, NOVA brings light.\"",
        "```",
    ])

    return "\n".join(lines)


@app.command()
def version():
    """Show NOVA version information."""
    nova_console.print_banner()
    console.print(f"[bold]Version:[/bold] {__version__}")
    console.print("[bold]Codename:[/bold] THE MIRROR")


@app.command()
def protocols():
    """List available analysis protocols."""
    nova_console.print_banner()

    console.print("\n[bold]Available Protocols:[/bold]\n")

    protocols_info = [
        ("💀", "rot", "Code Rot Detector", "Analyzes git history for stale/chaotic files"),
        ("😓", "guilt", "Coder Guilt Scanner", "Detects TODO, FIXME, HACK markers"),
        ("🛡️", "security", "Iron Dome", "Finds secrets, SQL injection, weak endpoints"),
        ("🚀", "performance", "Velocity & Physics", "Cyclomatic complexity, Big O estimation"),
    ]

    for icon, name, title, desc in protocols_info:
        console.print(f"{icon} [bold cyan]{name}[/bold cyan] - {title}")
        console.print(f"   [dim]{desc}[/dim]\n")

    console.print("[dim]Run specific protocol: nova scan --protocol <name>[/dim]")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
