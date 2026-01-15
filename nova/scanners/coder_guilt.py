"""
😓 PROTOCOL B: THE "CODER GUILT" SCANNER (Emotional Dimension)
Detects signs of developer desperation and technical debt acknowledgment.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class GuiltMarker:
    """A single guilt marker found in code."""
    filepath: str
    line_number: int
    marker_type: str
    content: str
    severity: int  # 1-5


@dataclass
class FileGuiltMetrics:
    """Guilt metrics for a single file."""
    filepath: str
    line_count: int = 0
    markers: List[GuiltMarker] = field(default_factory=list)
    guilt_density: float = 0.0  # markers per 100 lines
    is_god_class: bool = False


@dataclass
class CoderGuiltReport:
    """Complete coder guilt analysis report."""
    total_markers: int = 0
    markers_by_type: Dict[str, int] = field(default_factory=dict)
    desperation_hotspots: List[FileGuiltMetrics] = field(default_factory=list)
    god_classes: List[FileGuiltMetrics] = field(default_factory=list)
    worst_offenders: List[GuiltMarker] = field(default_factory=list)
    guilt_index: float = 0.0  # 0-100
    total_lines_analyzed: int = 0


class CoderGuiltScanner:
    """
    😓 THE CODER GUILT SCANNER

    Scans code for signs of developer desperation:
    - TODO, FIXME, HACK markers
    - Desperate comments ("do not touch", "god help me")
    - God classes (>500 lines)
    - High guilt density zones
    """

    # Guilt markers with severity levels
    GUILT_PATTERNS = {
        # Severity 5: Critical desperation
        'DESPERATION': {
            'patterns': [
                r'god\s+help',
                r'please\s+work',
                r'why\s+does\s+this\s+work',
                r'no\s+idea\s+why',
                r'magic\s+number',
                r'don\'?t\s+ask',
                r'pray\s+this\s+works',
                r'¯\\\\\\_\(ツ\)_/¯',
                r'wtf',
                r'what\s+the\s+f',
            ],
            'severity': 5
        },
        # Severity 4: Danger zones
        'DANGER': {
            'patterns': [
                r'do\s+not\s+touch',
                r'don\'?t\s+touch',
                r'do\s+not\s+modify',
                r'don\'?t\s+modify',
                r'here\s+be\s+dragons',
                r'abandon\s+hope',
                r'will\s+break',
                r'breaks\s+everything',
                r'fragile',
            ],
            'severity': 4
        },
        # Severity 3: Technical debt acknowledgment
        'HACK': {
            'patterns': [
                r'\bHACK\b',
                r'\bKLUDGE\b',
                r'\bWORKAROUND\b',
                r'ugly\s+hack',
                r'dirty\s+hack',
                r'quick\s+and\s+dirty',
                r'temporary\s+fix',
                r'temp\s+fix',
                r'band[\s-]?aid',
            ],
            'severity': 3
        },
        # Severity 2: Known issues
        'FIXME': {
            'patterns': [
                r'\bFIXME\b',
                r'\bBUG\b:?',
                r'\bBROKEN\b',
                r'needs?\s+fix',
                r'should\s+be\s+fixed',
            ],
            'severity': 2
        },
        # Severity 1: Planned work
        'TODO': {
            'patterns': [
                r'\bTODO\b',
                r'\bXXX\b',
                r'\bREVIEW\b',
                r'\bOPTIMIZE\b',
                r'\bREFACTOR\b',
            ],
            'severity': 1
        }
    }

    # God class threshold
    GOD_CLASS_LINES = 500

    # File extensions to analyze
    CODE_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs',
        '.rb', '.php', '.c', '.cpp', '.h', '.hpp', '.cs', '.swift',
        '.kt', '.scala', '.vue', '.svelte'
    }

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self._compiled_patterns: Dict[str, List[Tuple[re.Pattern, int]]] = {}
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile all regex patterns for performance."""
        for marker_type, config in self.GUILT_PATTERNS.items():
            self._compiled_patterns[marker_type] = [
                (re.compile(pattern, re.IGNORECASE), config['severity'])
                for pattern in config['patterns']
            ]

    def scan(self) -> CoderGuiltReport:
        """Execute the full coder guilt scan."""
        report = CoderGuiltReport()
        file_metrics: Dict[str, FileGuiltMetrics] = {}

        # Scan all code files
        for root, _, files in self.repo_path.rglob('*'):
            pass  # rglob handles this

        for filepath in self.repo_path.rglob('*'):
            if not filepath.is_file():
                continue

            # Skip non-code files
            if filepath.suffix not in self.CODE_EXTENSIONS:
                continue

            # Skip hidden and vendor directories
            path_str = str(filepath)
            if any(skip in path_str for skip in ['.git', 'node_modules', 'vendor', '__pycache__', 'venv', '.venv']):
                continue

            metrics = self._analyze_file(filepath)
            if metrics:
                relative_path = str(filepath.relative_to(self.repo_path))
                metrics.filepath = relative_path
                file_metrics[relative_path] = metrics
                report.total_lines_analyzed += metrics.line_count

        # Aggregate results
        for filepath, metrics in file_metrics.items():
            # Count markers
            for marker in metrics.markers:
                report.total_markers += 1
                report.markers_by_type[marker.marker_type] = \
                    report.markers_by_type.get(marker.marker_type, 0) + 1
                report.worst_offenders.append(marker)

            # Track high guilt density
            if metrics.guilt_density > 1.0:  # More than 1 marker per 100 lines
                report.desperation_hotspots.append(metrics)

            # Track god classes
            if metrics.is_god_class:
                report.god_classes.append(metrics)

        # Sort worst offenders by severity
        report.worst_offenders.sort(key=lambda x: x.severity, reverse=True)
        report.worst_offenders = report.worst_offenders[:50]  # Top 50

        # Sort hotspots by guilt density
        report.desperation_hotspots.sort(key=lambda x: x.guilt_density, reverse=True)

        # Sort god classes by line count
        report.god_classes.sort(key=lambda x: x.line_count, reverse=True)

        # Calculate guilt index
        if report.total_lines_analyzed > 0:
            base_guilt = (report.total_markers / report.total_lines_analyzed) * 1000

            # Weight by severity
            severity_weight = sum(
                count * (6 - severity_level)
                for marker_type, count in report.markers_by_type.items()
                for severity_level in [self.GUILT_PATTERNS.get(marker_type, {}).get('severity', 1)]
            ) / max(report.total_markers, 1)

            # God class penalty
            god_class_penalty = len(report.god_classes) * 5

            report.guilt_index = min(100, base_guilt * severity_weight + god_class_penalty)

        return report

    def _analyze_file(self, filepath: Path) -> Optional[FileGuiltMetrics]:
        """Analyze a single file for guilt markers."""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return None

        lines = content.split('\n')
        metrics = FileGuiltMetrics(
            filepath=str(filepath),
            line_count=len(lines)
        )

        # Check for god class
        if len(lines) > self.GOD_CLASS_LINES:
            metrics.is_god_class = True

        # Scan for guilt markers
        for line_num, line in enumerate(lines, 1):
            for marker_type, patterns in self._compiled_patterns.items():
                for pattern, severity in patterns:
                    if pattern.search(line):
                        marker = GuiltMarker(
                            filepath=str(filepath),
                            line_number=line_num,
                            marker_type=marker_type,
                            content=line.strip()[:200],  # Truncate long lines
                            severity=severity
                        )
                        metrics.markers.append(marker)
                        break  # One marker per line per type

        # Calculate guilt density
        if metrics.line_count > 0:
            metrics.guilt_density = (len(metrics.markers) / metrics.line_count) * 100

        return metrics


def format_guilt_report(report: CoderGuiltReport) -> str:
    """Format the coder guilt report for display."""
    lines = [
        "😓 CODER GUILT ANALYSIS",
        "=" * 50,
        f"Total Lines Analyzed: {report.total_lines_analyzed:,}",
        f"Total Guilt Markers: {report.total_markers}",
        f"GUILT INDEX: {report.guilt_index:.1f}/100",
        "",
    ]

    # Markers breakdown
    if report.markers_by_type:
        lines.append("📊 MARKERS BY TYPE:")
        for marker_type, count in sorted(report.markers_by_type.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  - {marker_type}: {count}")

    # God classes
    if report.god_classes:
        lines.append(f"\n🦣 GOD CLASSES ({len(report.god_classes)} detected):")
        for gc in report.god_classes[:10]:
            lines.append(f"  - {gc.filepath}: {gc.line_count} lines")

    # Desperation hotspots
    if report.desperation_hotspots:
        lines.append(f"\n🔥 DESPERATION HOTSPOTS:")
        for hotspot in report.desperation_hotspots[:10]:
            lines.append(f"  - {hotspot.filepath}: {hotspot.guilt_density:.1f} markers/100 lines")

    # Worst offenders
    if report.worst_offenders:
        lines.append(f"\n⚠️ WORST OFFENDERS (by severity):")
        for marker in report.worst_offenders[:15]:
            severity_emoji = "🔴" if marker.severity >= 4 else "🟠" if marker.severity >= 3 else "🟡"
            lines.append(f"  {severity_emoji} [{marker.marker_type}] {marker.filepath}:{marker.line_number}")
            lines.append(f"      \"{marker.content[:100]}...\"" if len(marker.content) > 100 else f"      \"{marker.content}\"")

    return "\n".join(lines)
