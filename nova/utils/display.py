"""
🌌 NOVA Console Display Utilities
Rich terminal output for the forensic auditor.
"""

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from rich.live import Live
from rich.layout import Layout
from typing import Optional
import time


class NovaConsole:
    """Rich console interface for NOVA."""

    NOVA_BANNER = """
    ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗     ██╗   ██╗██████╗    ██╗
    ████╗  ██║██╔═══██╗██║   ██║██╔══██╗    ██║   ██║╚════██╗  ███║
    ██╔██╗ ██║██║   ██║██║   ██║███████║    ██║   ██║ █████╔╝  ╚██║
    ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║    ╚██╗ ██╔╝ ╚═══██╗   ██║
    ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║     ╚████╔╝ ██████╔╝██╗██║
    ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝      ╚═══╝  ╚═════╝ ╚═╝╚═╝
                    THE FORENSIC CODE AUDITOR
    """

    def __init__(self):
        self.console = Console()

    def print_banner(self):
        """Display the NOVA banner."""
        self.console.print(
            Panel(
                Text(self.NOVA_BANNER, style="bold cyan"),
                border_style="bright_blue",
                subtitle="[dim]v3.1 - The Mirror[/dim]"
            )
        )

    def print_phase(self, phase: str, description: str = ""):
        """Display a phase transition."""
        phase_icons = {
            "scanning": "🔬",
            "analyzing": "🧠",
            "critiquing": "🎭",
            "generating": "📜",
            "complete": "✅",
            "failed": "❌"
        }
        icon = phase_icons.get(phase.lower(), "⚡")

        self.console.print()
        self.console.print(
            Panel(
                f"{icon}  [bold]{phase.upper()}[/bold]\n[dim]{description}[/dim]",
                border_style="yellow"
            )
        )

    def print_scanning_progress(self, phases: list[str]):
        """Display a progress bar for scanning phases."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            task = progress.add_task("[cyan]Initializing NOVA...", total=len(phases))

            for phase in phases:
                progress.update(task, description=f"[cyan]{phase}")
                time.sleep(0.5)  # Simulated delay
                progress.advance(task)

    def print_scan_results_summary(self, results: dict):
        """Display a summary table of scan results."""
        table = Table(title="🔬 Scan Results Summary", border_style="blue")

        table.add_column("Protocol", style="cyan", justify="left")
        table.add_column("Status", style="green", justify="center")
        table.add_column("Score", style="yellow", justify="right")
        table.add_column("Key Findings", style="white", justify="left")

        # Code Rot
        rot = results.get("code_rot", {})
        rot_score = rot.get("rot_score", 0)
        rot_status = "🔴" if rot_score > 50 else "🟠" if rot_score > 25 else "🟢"
        rot_findings = f"{len(rot.get('abandoned_files', []))} abandoned, {len(rot.get('chaotic_files', []))} chaotic"
        table.add_row("💀 Code Rot", rot_status, f"{rot_score:.1f}/100", rot_findings)

        # Coder Guilt
        guilt = results.get("coder_guilt", {})
        guilt_score = guilt.get("guilt_index", 0)
        guilt_status = "🔴" if guilt_score > 50 else "🟠" if guilt_score > 25 else "🟢"
        guilt_findings = f"{guilt.get('total_markers', 0)} markers, {len(guilt.get('god_classes', []))} god classes"
        table.add_row("😓 Coder Guilt", guilt_status, f"{guilt_score:.1f}/100", guilt_findings)

        # Security
        security = results.get("security", {})
        sec_score = security.get("vulnerability_score", 0)
        sec_status = "🔴" if sec_score > 5 else "🟠" if sec_score > 2 else "🟢"
        sec_findings = f"{len(security.get('secret_leaks', []))} leaks, {len(security.get('unprotected_endpoints', []))} endpoints"
        table.add_row("🛡️ Security", sec_status, f"{sec_score:.1f}/10", sec_findings)

        # Performance
        perf = results.get("performance", {})
        perf_score = perf.get("performance_score", 100)
        perf_status = "🔴" if perf_score < 50 else "🟠" if perf_score < 75 else "🟢"
        perf_findings = f"{len(perf.get('complex_functions', []))} complex, {len(perf.get('big_o_concerns', []))} O(n²+)"
        table.add_row("🚀 Performance", perf_status, f"{perf_score:.1f}/100", perf_findings)

        self.console.print()
        self.console.print(table)

    def print_critique_feedback(self, critique: dict):
        """Display Ralph's critique feedback."""
        passed = critique.get("passed", False)
        iteration = critique.get("iteration", 0)
        max_iter = critique.get("max_iterations", 3)

        status = "[green]PASSED[/green]" if passed else "[red]FAILED[/red]"

        self.console.print()
        self.console.print(
            Panel(
                f"[bold]🎭 RALPH'S VERDICT:[/bold] {status}\n"
                f"[dim]Iteration {iteration}/{max_iter}[/dim]",
                border_style="magenta"
            )
        )

        if critique.get("issues"):
            self.console.print("\n[bold red]Issues Found:[/bold red]")
            for issue in critique["issues"]:
                self.console.print(f"  • {issue}")

        if critique.get("suggestions"):
            self.console.print("\n[bold yellow]Suggestions:[/bold yellow]")
            for suggestion in critique["suggestions"]:
                self.console.print(f"  • {suggestion}")

    def print_report(self, markdown_content: str):
        """Display the final report."""
        self.console.print()
        self.console.print(
            Panel(
                Markdown(markdown_content),
                title="📜 NOVA FORENSIC REPORT",
                border_style="green"
            )
        )

    def print_error(self, message: str):
        """Display an error message."""
        self.console.print()
        self.console.print(
            Panel(
                f"[bold red]ERROR:[/bold red] {message}",
                border_style="red"
            )
        )

    def print_success(self, message: str):
        """Display a success message."""
        self.console.print()
        self.console.print(
            Panel(
                f"[bold green]SUCCESS:[/bold green] {message}",
                border_style="green"
            )
        )

    def print_info(self, message: str):
        """Display an info message."""
        self.console.print(f"[dim]ℹ️  {message}[/dim]")

    def create_live_display(self):
        """Create a live updating display."""
        return Live(console=self.console, refresh_per_second=4)
