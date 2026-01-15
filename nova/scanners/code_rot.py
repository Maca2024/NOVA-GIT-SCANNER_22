"""
💀 PROTOCOL A: THE "CODE ROT" DETECTOR (Time Dimension)
Analyzes git history to detect staleness and chaos zones.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict

from git import Repo, InvalidGitRepositoryError
from git.exc import GitCommandError


@dataclass
class FileRotMetrics:
    """Metrics for a single file's rot analysis."""
    filepath: str
    last_modified: Optional[datetime] = None
    days_stale: int = 0
    commit_count: int = 0
    monthly_churn: int = 0
    authors: List[str] = field(default_factory=list)
    is_abandoned: bool = False
    is_chaotic: bool = False
    imported_by: List[str] = field(default_factory=list)


@dataclass
class CodeRotReport:
    """Complete code rot analysis report."""
    abandoned_files: List[FileRotMetrics] = field(default_factory=list)
    chaotic_files: List[FileRotMetrics] = field(default_factory=list)
    silent_dependencies: List[Tuple[str, List[str]]] = field(default_factory=list)
    total_files_analyzed: int = 0
    average_staleness_days: float = 0.0
    rot_score: float = 0.0  # 0-100


class CodeRotScanner:
    """
    💀 THE CODE ROT DETECTOR

    Scans git history to identify:
    - Abandoned Zones: Files untouched > 1 year that are still imported
    - Chaos Zones: Files with excessive churn (>50 commits/month)
    - Silent Dependencies: Stale files imported by active code
    """

    STALE_THRESHOLD_DAYS = 365  # 1 year
    CHURN_THRESHOLD = 50  # commits per month

    # File extensions to analyze
    CODE_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs',
        '.rb', '.php', '.c', '.cpp', '.h', '.hpp', '.cs', '.swift',
        '.kt', '.scala', '.vue', '.svelte'
    }

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo: Optional[Repo] = None
        self._file_metrics: Dict[str, FileRotMetrics] = {}

    def initialize(self) -> bool:
        """Initialize git repository connection."""
        try:
            self.repo = Repo(self.repo_path)
            return True
        except InvalidGitRepositoryError:
            return False

    def scan(self) -> CodeRotReport:
        """Execute the full code rot scan."""
        if not self.repo:
            if not self.initialize():
                raise ValueError(f"Invalid git repository: {self.repo_path}")

        report = CodeRotReport()

        # Phase 1: Analyze all code files
        self._analyze_file_history()

        # Phase 2: Detect import relationships
        self._analyze_dependencies()

        # Phase 3: Classify files
        now = datetime.now()
        total_staleness = 0

        for filepath, metrics in self._file_metrics.items():
            report.total_files_analyzed += 1

            if metrics.last_modified:
                staleness = (now - metrics.last_modified).days
                metrics.days_stale = staleness
                total_staleness += staleness

                # Check if abandoned (stale + still imported)
                if staleness > self.STALE_THRESHOLD_DAYS:
                    metrics.is_abandoned = True
                    report.abandoned_files.append(metrics)

                    if metrics.imported_by:
                        report.silent_dependencies.append(
                            (filepath, metrics.imported_by)
                        )

            # Check for chaos (high churn)
            if metrics.monthly_churn >= self.CHURN_THRESHOLD:
                metrics.is_chaotic = True
                report.chaotic_files.append(metrics)

        # Calculate averages and score
        if report.total_files_analyzed > 0:
            report.average_staleness_days = total_staleness / report.total_files_analyzed

            # Rot score: weighted combination of abandonment and chaos
            abandonment_ratio = len(report.abandoned_files) / report.total_files_analyzed
            chaos_ratio = len(report.chaotic_files) / report.total_files_analyzed
            dependency_penalty = len(report.silent_dependencies) * 5

            report.rot_score = min(100, (
                (abandonment_ratio * 40) +
                (chaos_ratio * 30) +
                dependency_penalty +
                (report.average_staleness_days / 365 * 20)
            ))

        return report

    def _analyze_file_history(self):
        """Analyze git history for all code files."""
        # Get all code files
        for root, _, files in os.walk(self.repo_path):
            for filename in files:
                filepath = Path(root) / filename

                # Skip hidden and non-code files
                if filename.startswith('.') or filepath.suffix not in self.CODE_EXTENSIONS:
                    continue

                # Skip git directory
                if '.git' in str(filepath):
                    continue

                relative_path = str(filepath.relative_to(self.repo_path))
                self._file_metrics[relative_path] = FileRotMetrics(filepath=relative_path)

        # Analyze commit history
        try:
            one_month_ago = datetime.now() - timedelta(days=30)

            for commit in self.repo.iter_commits('HEAD', max_count=5000):
                commit_date = datetime.fromtimestamp(commit.committed_date)

                for filepath in commit.stats.files.keys():
                    if filepath in self._file_metrics:
                        metrics = self._file_metrics[filepath]
                        metrics.commit_count += 1

                        # Track last modification
                        if metrics.last_modified is None or commit_date > metrics.last_modified:
                            metrics.last_modified = commit_date

                        # Track monthly churn
                        if commit_date > one_month_ago:
                            metrics.monthly_churn += 1

                        # Track authors
                        author = commit.author.name
                        if author not in metrics.authors:
                            metrics.authors.append(author)

        except GitCommandError:
            pass  # Handle repos with no commits

    def _analyze_dependencies(self):
        """Analyze import relationships between files."""
        import_patterns = {
            '.py': self._extract_python_imports,
            '.js': self._extract_js_imports,
            '.ts': self._extract_js_imports,
            '.jsx': self._extract_js_imports,
            '.tsx': self._extract_js_imports,
        }

        for filepath, metrics in self._file_metrics.items():
            path = self.repo_path / filepath
            suffix = path.suffix

            if suffix in import_patterns and path.exists():
                try:
                    content = path.read_text(encoding='utf-8', errors='ignore')
                    imports = import_patterns[suffix](content, filepath)

                    # Mark imported files
                    for imported_file in imports:
                        if imported_file in self._file_metrics:
                            self._file_metrics[imported_file].imported_by.append(filepath)
                except Exception:
                    pass

    def _extract_python_imports(self, content: str, current_file: str) -> List[str]:
        """Extract Python import statements."""
        import re
        imports = []

        # Match: from X import Y, import X
        patterns = [
            r'^from\s+([\w.]+)\s+import',
            r'^import\s+([\w.]+)',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                module = match.group(1)
                # Convert module path to file path
                possible_file = module.replace('.', '/') + '.py'
                imports.append(possible_file)

        return imports

    def _extract_js_imports(self, content: str, current_file: str) -> List[str]:
        """Extract JavaScript/TypeScript import statements."""
        import re
        imports = []

        # Match: import X from 'Y', require('Y')
        patterns = [
            r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
            r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        ]

        current_dir = str(Path(current_file).parent)

        for pattern in patterns:
            for match in re.finditer(pattern, content):
                module = match.group(1)
                if module.startswith('.'):
                    # Resolve relative imports
                    resolved = str((Path(current_dir) / module).resolve())
                    for ext in ['.js', '.ts', '.jsx', '.tsx']:
                        imports.append(resolved + ext)

        return imports


def format_rot_report(report: CodeRotReport) -> str:
    """Format the code rot report for display."""
    lines = [
        "💀 CODE ROT ANALYSIS",
        "=" * 50,
        f"Total Files Analyzed: {report.total_files_analyzed}",
        f"Average Staleness: {report.average_staleness_days:.0f} days",
        f"ROT SCORE: {report.rot_score:.1f}/100",
        "",
    ]

    if report.abandoned_files:
        lines.append("🪦 ABANDONED FILES (>1 year untouched):")
        for f in sorted(report.abandoned_files, key=lambda x: x.days_stale, reverse=True)[:10]:
            lines.append(f"  - {f.filepath} ({f.days_stale} days stale)")

    if report.chaotic_files:
        lines.append("\n🌀 CHAOTIC FILES (High Churn):")
        for f in sorted(report.chaotic_files, key=lambda x: x.monthly_churn, reverse=True)[:10]:
            lines.append(f"  - {f.filepath} ({f.monthly_churn} commits/month)")

    if report.silent_dependencies:
        lines.append("\n⚠️ SILENT DEPENDENCIES (Stale but imported):")
        for stale_file, importers in report.silent_dependencies[:10]:
            lines.append(f"  - {stale_file}")
            for importer in importers[:3]:
                lines.append(f"      ← imported by: {importer}")

    return "\n".join(lines)
