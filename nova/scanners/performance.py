"""
🚀 PROTOCOL D: VELOCITY & PHYSICS (Performance Scanner)
Analyzes code complexity, Big O estimation, and performance bottlenecks.
"""

import ast
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ComplexityLevel(Enum):
    """Complexity classification levels."""
    SIMPLE = "A"      # 1-5
    LOW = "B"         # 6-10
    MODERATE = "C"    # 11-20
    HIGH = "D"        # 21-30
    VERY_HIGH = "E"   # 31-40
    UNMAINTAINABLE = "F"  # 41+


@dataclass
class FunctionComplexity:
    """Complexity metrics for a single function."""
    filepath: str
    function_name: str
    line_number: int
    cyclomatic_complexity: int
    complexity_level: ComplexityLevel
    cognitive_complexity: int = 0
    lines_of_code: int = 0
    parameters: int = 0
    nested_depth: int = 0


@dataclass
class BigOEstimate:
    """Big O complexity estimate for a function."""
    filepath: str
    function_name: str
    line_number: int
    estimated_complexity: str  # O(1), O(n), O(n^2), etc.
    reasoning: str
    nested_loops: int = 0
    recursive: bool = False


@dataclass
class HeavyImport:
    """A heavy/bloated import detected."""
    filepath: str
    line_number: int
    import_name: str
    reason: str


@dataclass
class PerformanceReport:
    """Complete performance analysis report."""
    complex_functions: List[FunctionComplexity] = field(default_factory=list)
    big_o_estimates: List[BigOEstimate] = field(default_factory=list)
    heavy_imports: List[HeavyImport] = field(default_factory=list)
    average_complexity: float = 0.0
    total_functions_analyzed: int = 0
    high_complexity_count: int = 0
    maintainability_index: float = 100.0
    performance_score: float = 0.0  # 0-100


class PerformanceScanner:
    """
    🚀 VELOCITY & PHYSICS SCANNER

    Analyzes code performance characteristics:
    - Cyclomatic Complexity (via Radon)
    - Big O Estimation (via AST analysis)
    - Heavy/bloated imports detection
    - Nested loop detection
    """

    # Known heavy imports
    HEAVY_IMPORTS = {
        'pandas': 'Heavy data library - consider lazy loading',
        'numpy': 'Large numerical library',
        'tensorflow': 'Very heavy ML framework',
        'torch': 'Heavy ML framework',
        'pytorch': 'Heavy ML framework',
        'sklearn': 'Large ML library',
        'scipy': 'Large scientific library',
        'matplotlib': 'Heavy plotting library',
        'plotly': 'Heavy plotting library',
        'opencv': 'Heavy image processing library',
        'cv2': 'Heavy image processing library',
        'PIL': 'Image processing library',
        'requests': 'Consider httpx for async support',
        'boto3': 'AWS SDK - ensure lazy initialization',
        'django': 'Full framework import detected',
        'sqlalchemy': 'Full ORM import',
    }

    # Complexity thresholds
    HIGH_COMPLEXITY_THRESHOLD = 10
    VERY_HIGH_COMPLEXITY_THRESHOLD = 20

    CODE_EXTENSIONS = {'.py'}  # Focus on Python for deep analysis

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def scan(self) -> PerformanceReport:
        """Execute the full performance scan."""
        report = PerformanceReport()

        # Run Radon for complexity analysis
        self._run_radon_complexity(report)

        # Run custom Big O analysis
        self._analyze_big_o(report)

        # Detect heavy imports
        self._detect_heavy_imports(report)

        # Calculate overall metrics
        self._calculate_metrics(report)

        return report

    def _run_radon_complexity(self, report: PerformanceReport):
        """Run Radon cyclomatic complexity analysis."""
        try:
            result = subprocess.run(
                ['radon', 'cc', str(self.repo_path), '-j', '-a'],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.stdout:
                radon_output = json.loads(result.stdout)

                for filepath, functions in radon_output.items():
                    if filepath == 'average':
                        continue

                    if not isinstance(functions, list):
                        continue

                    relative_path = filepath
                    try:
                        relative_path = str(Path(filepath).relative_to(self.repo_path))
                    except ValueError:
                        pass

                    for func in functions:
                        if not isinstance(func, dict):
                            continue

                        cc = func.get('complexity', 0)
                        report.total_functions_analyzed += 1

                        # Classify complexity
                        if cc <= 5:
                            level = ComplexityLevel.SIMPLE
                        elif cc <= 10:
                            level = ComplexityLevel.LOW
                        elif cc <= 20:
                            level = ComplexityLevel.MODERATE
                        elif cc <= 30:
                            level = ComplexityLevel.HIGH
                        elif cc <= 40:
                            level = ComplexityLevel.VERY_HIGH
                        else:
                            level = ComplexityLevel.UNMAINTAINABLE

                        complexity = FunctionComplexity(
                            filepath=relative_path,
                            function_name=func.get('name', 'unknown'),
                            line_number=func.get('lineno', 0),
                            cyclomatic_complexity=cc,
                            complexity_level=level,
                            lines_of_code=func.get('endline', 0) - func.get('lineno', 0)
                        )

                        if cc >= self.HIGH_COMPLEXITY_THRESHOLD:
                            report.complex_functions.append(complexity)
                            report.high_complexity_count += 1

        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            # Radon not available, fall back to AST analysis
            self._analyze_complexity_ast(report)

    def _analyze_complexity_ast(self, report: PerformanceReport):
        """Fallback AST-based complexity analysis."""
        for filepath in self.repo_path.rglob('*.py'):
            path_str = str(filepath)
            if any(skip in path_str for skip in ['.git', 'node_modules', '__pycache__', 'venv', '.venv']):
                continue

            try:
                content = filepath.read_text(encoding='utf-8', errors='ignore')
                tree = ast.parse(content)
                relative_path = str(filepath.relative_to(self.repo_path))

                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        cc = self._calculate_cyclomatic_complexity(node)
                        report.total_functions_analyzed += 1

                        if cc <= 5:
                            level = ComplexityLevel.SIMPLE
                        elif cc <= 10:
                            level = ComplexityLevel.LOW
                        elif cc <= 20:
                            level = ComplexityLevel.MODERATE
                        elif cc <= 30:
                            level = ComplexityLevel.HIGH
                        elif cc <= 40:
                            level = ComplexityLevel.VERY_HIGH
                        else:
                            level = ComplexityLevel.UNMAINTAINABLE

                        if cc >= self.HIGH_COMPLEXITY_THRESHOLD:
                            complexity = FunctionComplexity(
                                filepath=relative_path,
                                function_name=node.name,
                                line_number=node.lineno,
                                cyclomatic_complexity=cc,
                                complexity_level=level,
                                parameters=len(node.args.args)
                            )
                            report.complex_functions.append(complexity)
                            report.high_complexity_count += 1

            except (SyntaxError, Exception):
                pass

    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity for an AST node."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            # Decision points
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.With, ast.AsyncWith):
                complexity += 1
            elif isinstance(child, ast.Assert):
                complexity += 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.IfExp):
                complexity += 1

        return complexity

    def _analyze_big_o(self, report: PerformanceReport):
        """Analyze Big O complexity via AST."""
        for filepath in self.repo_path.rglob('*.py'):
            path_str = str(filepath)
            if any(skip in path_str for skip in ['.git', 'node_modules', '__pycache__', 'venv', '.venv']):
                continue

            try:
                content = filepath.read_text(encoding='utf-8', errors='ignore')
                tree = ast.parse(content)
                relative_path = str(filepath.relative_to(self.repo_path))

                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        estimate = self._estimate_big_o(node, relative_path)
                        if estimate and estimate.estimated_complexity not in ['O(1)', 'O(log n)']:
                            report.big_o_estimates.append(estimate)

            except (SyntaxError, Exception):
                pass

    def _estimate_big_o(self, func_node: ast.AST, filepath: str) -> Optional[BigOEstimate]:
        """Estimate Big O complexity for a function."""
        loop_depth = 0
        max_depth = 0
        nested_loops = 0
        is_recursive = False

        func_name = getattr(func_node, 'name', 'unknown')

        def analyze_node(node: ast.AST, current_depth: int):
            nonlocal max_depth, nested_loops, is_recursive

            for child in ast.iter_child_nodes(node):
                child_depth = current_depth

                # Check for loops
                if isinstance(child, (ast.For, ast.While, ast.AsyncFor)):
                    child_depth = current_depth + 1
                    if current_depth > 0:
                        nested_loops += 1
                    max_depth = max(max_depth, child_depth)

                # Check for recursion
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name) and child.func.id == func_name:
                        is_recursive = True

                analyze_node(child, child_depth)

        analyze_node(func_node, 0)

        # Estimate complexity
        if is_recursive:
            complexity = "O(2^n) or O(n!)"
            reasoning = "Recursive function detected - complexity depends on base case"
        elif max_depth == 0:
            complexity = "O(1)"
            reasoning = "No loops detected - constant time"
        elif max_depth == 1:
            complexity = "O(n)"
            reasoning = "Single loop iteration"
        elif max_depth == 2:
            complexity = "O(n^2)"
            reasoning = f"Nested loops detected (depth: {max_depth})"
        elif max_depth == 3:
            complexity = "O(n^3)"
            reasoning = f"Triple nested loops (depth: {max_depth})"
        else:
            complexity = f"O(n^{max_depth})"
            reasoning = f"Deep nesting detected (depth: {max_depth})"

        return BigOEstimate(
            filepath=filepath,
            function_name=func_name,
            line_number=getattr(func_node, 'lineno', 0),
            estimated_complexity=complexity,
            reasoning=reasoning,
            nested_loops=nested_loops,
            recursive=is_recursive
        )

    def _detect_heavy_imports(self, report: PerformanceReport):
        """Detect heavy/bloated imports."""
        for filepath in self.repo_path.rglob('*.py'):
            path_str = str(filepath)
            if any(skip in path_str for skip in ['.git', 'node_modules', '__pycache__', 'venv', '.venv']):
                continue

            try:
                content = filepath.read_text(encoding='utf-8', errors='ignore')
                tree = ast.parse(content)
                relative_path = str(filepath.relative_to(self.repo_path))

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            module_name = alias.name.split('.')[0]
                            if module_name in self.HEAVY_IMPORTS:
                                report.heavy_imports.append(HeavyImport(
                                    filepath=relative_path,
                                    line_number=node.lineno,
                                    import_name=alias.name,
                                    reason=self.HEAVY_IMPORTS[module_name]
                                ))

                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            module_name = node.module.split('.')[0]
                            if module_name in self.HEAVY_IMPORTS:
                                report.heavy_imports.append(HeavyImport(
                                    filepath=relative_path,
                                    line_number=node.lineno,
                                    import_name=node.module,
                                    reason=self.HEAVY_IMPORTS[module_name]
                                ))

            except (SyntaxError, Exception):
                pass

    def _calculate_metrics(self, report: PerformanceReport):
        """Calculate overall performance metrics."""
        if report.total_functions_analyzed > 0:
            # Average complexity from complex functions
            total_cc = sum(f.cyclomatic_complexity for f in report.complex_functions)
            all_cc = total_cc + (report.total_functions_analyzed - len(report.complex_functions)) * 3  # Assume avg 3 for simple
            report.average_complexity = all_cc / report.total_functions_analyzed

            # Maintainability Index (simplified)
            # MI = 171 - 5.2 * ln(avg_volume) - 0.23 * avg_cc - 16.2 * ln(avg_loc)
            # Simplified: higher complexity = lower maintainability
            report.maintainability_index = max(0, 100 - (report.average_complexity * 3) - (report.high_complexity_count * 2))

        # Performance score
        # Based on: complexity issues, Big O concerns, heavy imports
        issues = 0
        issues += len([f for f in report.complex_functions if f.cyclomatic_complexity > 20]) * 3
        issues += len([b for b in report.big_o_estimates if 'n^' in b.estimated_complexity]) * 2
        issues += len(report.heavy_imports) * 0.5

        report.performance_score = max(0, 100 - issues * 2)


def format_performance_report(report: PerformanceReport) -> str:
    """Format the performance report for display."""
    lines = [
        "🚀 PERFORMANCE ANALYSIS (VELOCITY & PHYSICS)",
        "=" * 50,
        f"Functions Analyzed: {report.total_functions_analyzed}",
        f"Average Complexity: {report.average_complexity:.1f}",
        f"Maintainability Index: {report.maintainability_index:.1f}/100",
        f"PERFORMANCE SCORE: {report.performance_score:.1f}/100",
        "",
    ]

    # High complexity functions
    if report.complex_functions:
        lines.append(f"🔥 HIGH COMPLEXITY FUNCTIONS ({len(report.complex_functions)}):")
        for func in sorted(report.complex_functions, key=lambda x: x.cyclomatic_complexity, reverse=True)[:15]:
            emoji = "🔴" if func.cyclomatic_complexity > 20 else "🟠" if func.cyclomatic_complexity > 10 else "🟡"
            lines.append(f"  {emoji} {func.function_name}() - CC: {func.cyclomatic_complexity} [{func.complexity_level.value}]")
            lines.append(f"      {func.filepath}:{func.line_number}")

    # Big O estimates
    problematic_bigo = [b for b in report.big_o_estimates if 'n^' in b.estimated_complexity or b.recursive]
    if problematic_bigo:
        lines.append(f"\n⏱️ POTENTIAL BOTTLENECKS ({len(problematic_bigo)}):")
        for estimate in problematic_bigo[:15]:
            emoji = "🔴" if 'n^3' in estimate.estimated_complexity or estimate.recursive else "🟠"
            lines.append(f"  {emoji} {estimate.function_name}() - {estimate.estimated_complexity}")
            lines.append(f"      {estimate.filepath}:{estimate.line_number}")
            lines.append(f"      Reason: {estimate.reasoning}")

    # Heavy imports
    if report.heavy_imports:
        lines.append(f"\n📦 HEAVY IMPORTS ({len(report.heavy_imports)}):")
        for imp in report.heavy_imports[:15]:
            lines.append(f"  ⚠️ {imp.import_name}")
            lines.append(f"      {imp.filepath}:{imp.line_number}")
            lines.append(f"      {imp.reason}")

    return "\n".join(lines)
