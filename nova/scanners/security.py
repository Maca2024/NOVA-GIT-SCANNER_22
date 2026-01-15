"""
🛡️ PROTOCOL C: THE IRON DOME (Security & API Scanner)
Detects hardcoded secrets, unprotected endpoints, and security vulnerabilities.
"""

import re
import ast
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum


class VulnerabilitySeverity(Enum):
    """Vulnerability severity levels."""
    CRITICAL = 10
    HIGH = 8
    MEDIUM = 5
    LOW = 3
    INFO = 1


@dataclass
class SecurityVulnerability:
    """A single security vulnerability."""
    filepath: str
    line_number: int
    vulnerability_type: str
    description: str
    severity: VulnerabilitySeverity
    code_snippet: str = ""
    recommendation: str = ""


@dataclass
class SecretLeak:
    """A detected secret or credential leak."""
    filepath: str
    line_number: int
    secret_type: str
    masked_value: str
    severity: VulnerabilitySeverity = VulnerabilitySeverity.CRITICAL


@dataclass
class UnprotectedEndpoint:
    """An API endpoint without authentication."""
    filepath: str
    line_number: int
    endpoint: str
    method: str
    framework: str


@dataclass
class SecurityReport:
    """Complete security analysis report."""
    vulnerabilities: List[SecurityVulnerability] = field(default_factory=list)
    secret_leaks: List[SecretLeak] = field(default_factory=list)
    unprotected_endpoints: List[UnprotectedEndpoint] = field(default_factory=list)
    sql_injections: List[SecurityVulnerability] = field(default_factory=list)
    bandit_findings: List[Dict] = field(default_factory=list)
    vulnerability_score: float = 0.0  # 0-10
    total_files_scanned: int = 0


class SecurityScanner:
    """
    🛡️ THE IRON DOME

    Comprehensive security scanner that detects:
    - Hardcoded API Keys / Secrets
    - Unprotected API endpoints
    - SQL Injection patterns
    - Other OWASP Top 10 vulnerabilities
    """

    # Secret patterns with descriptions
    SECRET_PATTERNS = {
        'AWS_ACCESS_KEY': (r'AKIA[0-9A-Z]{16}', VulnerabilitySeverity.CRITICAL),
        'AWS_SECRET_KEY': (r'[A-Za-z0-9/+=]{40}', VulnerabilitySeverity.CRITICAL),
        'OPENAI_API_KEY': (r'sk-[A-Za-z0-9]{48}', VulnerabilitySeverity.CRITICAL),
        'ANTHROPIC_API_KEY': (r'sk-ant-[A-Za-z0-9\-]{93}', VulnerabilitySeverity.CRITICAL),
        'STRIPE_API_KEY': (r'sk_live_[A-Za-z0-9]{24}', VulnerabilitySeverity.CRITICAL),
        'STRIPE_TEST_KEY': (r'sk_test_[A-Za-z0-9]{24}', VulnerabilitySeverity.MEDIUM),
        'GITHUB_TOKEN': (r'ghp_[A-Za-z0-9]{36}', VulnerabilitySeverity.CRITICAL),
        'GITHUB_OAUTH': (r'gho_[A-Za-z0-9]{36}', VulnerabilitySeverity.CRITICAL),
        'SLACK_TOKEN': (r'xox[baprs]-[A-Za-z0-9\-]{10,}', VulnerabilitySeverity.HIGH),
        'PRIVATE_KEY': (r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', VulnerabilitySeverity.CRITICAL),
        'GOOGLE_API_KEY': (r'AIza[0-9A-Za-z\-_]{35}', VulnerabilitySeverity.HIGH),
        'HEROKU_API_KEY': (r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', VulnerabilitySeverity.MEDIUM),
        'GENERIC_API_KEY': (r'["\']?api[_-]?key["\']?\s*[:=]\s*["\'][A-Za-z0-9]{16,}["\']', VulnerabilitySeverity.HIGH),
        'GENERIC_SECRET': (r'["\']?secret["\']?\s*[:=]\s*["\'][A-Za-z0-9]{8,}["\']', VulnerabilitySeverity.HIGH),
        'GENERIC_PASSWORD': (r'["\']?password["\']?\s*[:=]\s*["\'][^"\']{4,}["\']', VulnerabilitySeverity.HIGH),
        'DATABASE_URL': (r'(postgres|mysql|mongodb)://[^:]+:[^@]+@', VulnerabilitySeverity.CRITICAL),
        'JWT_SECRET': (r'jwt[_-]?secret\s*[:=]\s*["\'][^"\']+["\']', VulnerabilitySeverity.CRITICAL),
    }

    # SQL Injection patterns
    SQL_INJECTION_PATTERNS = [
        (r'execute\s*\(\s*["\'].*%s.*["\']', "String formatting in SQL execute"),
        (r'execute\s*\(\s*f["\']', "F-string in SQL execute"),
        (r'cursor\.execute\s*\([^,)]+\+', "String concatenation in cursor.execute"),
        (r'\.query\s*\([^,)]+\+', "String concatenation in .query()"),
        (r'SELECT.*FROM.*WHERE.*\+\s*\w+', "String concatenation in SELECT"),
        (r'INSERT\s+INTO.*\+\s*\w+', "String concatenation in INSERT"),
        (r'UPDATE.*SET.*\+\s*\w+', "String concatenation in UPDATE"),
        (r'DELETE\s+FROM.*\+\s*\w+', "String concatenation in DELETE"),
        (r'\.raw\s*\([^)]*\+', "String concatenation in .raw() query"),
    ]

    # Framework-specific auth decorators
    AUTH_DECORATORS = {
        'flask': ['@login_required', '@auth_required', '@jwt_required', '@token_required'],
        'django': ['@login_required', '@permission_required', '@user_passes_test'],
        'fastapi': ['Depends(', 'Security(', 'HTTPBearer', 'OAuth2'],
        'express': ['authenticate', 'isAuthenticated', 'passport.authenticate'],
    }

    # Route decorators
    ROUTE_PATTERNS = {
        'flask': r'@\w+\.route\s*\(["\']([^"\']+)["\'].*?\)',
        'django': r'path\s*\(["\']([^"\']+)["\']',
        'fastapi': r'@\w+\.(get|post|put|delete|patch)\s*\(["\']([^"\']+)["\']',
        'express': r'\.(get|post|put|delete|patch)\s*\(["\']([^"\']+)["\']',
    }

    CODE_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rb', '.php'}

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self._compiled_secret_patterns: Dict[str, Tuple[re.Pattern, VulnerabilitySeverity]] = {}
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns."""
        for name, (pattern, severity) in self.SECRET_PATTERNS.items():
            self._compiled_secret_patterns[name] = (re.compile(pattern), severity)

    def scan(self) -> SecurityReport:
        """Execute the full security scan."""
        report = SecurityReport()

        for filepath in self.repo_path.rglob('*'):
            if not filepath.is_file():
                continue

            if filepath.suffix not in self.CODE_EXTENSIONS:
                continue

            # Skip vendor/test directories
            path_str = str(filepath)
            if any(skip in path_str for skip in ['.git', 'node_modules', 'vendor', '__pycache__', 'venv', '.venv', 'test_', '_test.', 'spec.']):
                continue

            report.total_files_scanned += 1
            relative_path = str(filepath.relative_to(self.repo_path))

            try:
                content = filepath.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')

                # Scan for secrets
                self._scan_secrets(relative_path, lines, report)

                # Scan for SQL injection
                self._scan_sql_injection(relative_path, lines, report)

                # Scan for unprotected endpoints (Python files)
                if filepath.suffix == '.py':
                    self._scan_unprotected_endpoints_python(relative_path, content, lines, report)

                # Scan for unprotected endpoints (JS/TS files)
                if filepath.suffix in {'.js', '.ts'}:
                    self._scan_unprotected_endpoints_js(relative_path, content, lines, report)

            except Exception:
                pass

        # Run Bandit if available (Python security)
        self._run_bandit(report)

        # Calculate vulnerability score
        report.vulnerability_score = self._calculate_score(report)

        return report

    def _scan_secrets(self, filepath: str, lines: List[str], report: SecurityReport):
        """Scan for hardcoded secrets."""
        for line_num, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('*'):
                continue

            for secret_type, (pattern, severity) in self._compiled_secret_patterns.items():
                match = pattern.search(line)
                if match:
                    # Mask the secret value
                    secret_value = match.group(0)
                    masked = secret_value[:4] + '*' * (len(secret_value) - 8) + secret_value[-4:] if len(secret_value) > 8 else '****'

                    leak = SecretLeak(
                        filepath=filepath,
                        line_number=line_num,
                        secret_type=secret_type,
                        masked_value=masked,
                        severity=severity
                    )
                    report.secret_leaks.append(leak)

    def _scan_sql_injection(self, filepath: str, lines: List[str], report: SecurityReport):
        """Scan for SQL injection vulnerabilities."""
        full_content = '\n'.join(lines)

        for pattern, description in self.SQL_INJECTION_PATTERNS:
            for match in re.finditer(pattern, full_content, re.IGNORECASE | re.MULTILINE):
                # Find line number
                line_start = full_content[:match.start()].count('\n') + 1

                vuln = SecurityVulnerability(
                    filepath=filepath,
                    line_number=line_start,
                    vulnerability_type="SQL_INJECTION",
                    description=description,
                    severity=VulnerabilitySeverity.CRITICAL,
                    code_snippet=match.group(0)[:100],
                    recommendation="Use parameterized queries or ORM methods instead of string concatenation"
                )
                report.sql_injections.append(vuln)
                report.vulnerabilities.append(vuln)

    def _scan_unprotected_endpoints_python(self, filepath: str, content: str, lines: List[str], report: SecurityReport):
        """Scan Python files for unprotected API endpoints."""
        # Detect framework
        framework = None
        if 'flask' in content.lower() or 'Flask' in content:
            framework = 'flask'
        elif 'fastapi' in content.lower() or 'FastAPI' in content:
            framework = 'fastapi'
        elif 'django' in content.lower():
            framework = 'django'

        if not framework:
            return

        # Find route definitions
        route_pattern = self.ROUTE_PATTERNS.get(framework)
        if not route_pattern:
            return

        auth_decorators = self.AUTH_DECORATORS.get(framework, [])

        for i, line in enumerate(lines):
            # Check for route decorator
            route_match = re.search(route_pattern, line)
            if route_match:
                endpoint = route_match.group(1) if route_match.lastindex else route_match.group(0)

                # Look for auth decorator in surrounding lines (5 lines before)
                context_start = max(0, i - 5)
                context = '\n'.join(lines[context_start:i + 1])

                has_auth = any(auth in context for auth in auth_decorators)

                if not has_auth:
                    # Determine method
                    method = 'GET'
                    if 'post' in line.lower():
                        method = 'POST'
                    elif 'put' in line.lower():
                        method = 'PUT'
                    elif 'delete' in line.lower():
                        method = 'DELETE'

                    endpoint_vuln = UnprotectedEndpoint(
                        filepath=filepath,
                        line_number=i + 1,
                        endpoint=endpoint,
                        method=method,
                        framework=framework
                    )
                    report.unprotected_endpoints.append(endpoint_vuln)

    def _scan_unprotected_endpoints_js(self, filepath: str, content: str, lines: List[str], report: SecurityReport):
        """Scan JavaScript/TypeScript files for unprotected endpoints."""
        # Check if it's an Express-like file
        if 'express' not in content.lower() and 'router' not in content.lower():
            return

        route_pattern = self.ROUTE_PATTERNS.get('express')
        auth_decorators = self.AUTH_DECORATORS.get('express', [])

        for i, line in enumerate(lines):
            route_match = re.search(route_pattern, line)
            if route_match:
                method = route_match.group(1).upper()
                endpoint = route_match.group(2)

                # Check for auth middleware in the same line or nearby
                context_start = max(0, i - 2)
                context = '\n'.join(lines[context_start:i + 3])

                has_auth = any(auth in context for auth in auth_decorators)

                if not has_auth:
                    endpoint_vuln = UnprotectedEndpoint(
                        filepath=filepath,
                        line_number=i + 1,
                        endpoint=endpoint,
                        method=method,
                        framework='express'
                    )
                    report.unprotected_endpoints.append(endpoint_vuln)

    def _run_bandit(self, report: SecurityReport):
        """Run Bandit security scanner on Python files."""
        try:
            result = subprocess.run(
                ['bandit', '-r', str(self.repo_path), '-f', 'json', '-q'],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.stdout:
                bandit_output = json.loads(result.stdout)
                report.bandit_findings = bandit_output.get('results', [])

                # Convert Bandit findings to vulnerabilities
                for finding in report.bandit_findings:
                    severity_map = {
                        'HIGH': VulnerabilitySeverity.HIGH,
                        'MEDIUM': VulnerabilitySeverity.MEDIUM,
                        'LOW': VulnerabilitySeverity.LOW,
                    }

                    vuln = SecurityVulnerability(
                        filepath=finding.get('filename', ''),
                        line_number=finding.get('line_number', 0),
                        vulnerability_type=f"BANDIT_{finding.get('test_id', 'UNKNOWN')}",
                        description=finding.get('issue_text', ''),
                        severity=severity_map.get(finding.get('issue_severity', 'LOW'), VulnerabilitySeverity.LOW),
                        code_snippet=finding.get('code', ''),
                        recommendation=finding.get('issue_cwe', {}).get('link', '')
                    )
                    report.vulnerabilities.append(vuln)

        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass  # Bandit not available or failed

    def _calculate_score(self, report: SecurityReport) -> float:
        """Calculate overall vulnerability score (0-10)."""
        score = 0.0

        # Secret leaks are most critical
        for leak in report.secret_leaks:
            score += leak.severity.value * 0.5

        # SQL injections
        score += len(report.sql_injections) * 2

        # Unprotected endpoints
        score += len(report.unprotected_endpoints) * 0.5

        # Other vulnerabilities
        for vuln in report.vulnerabilities:
            if vuln.vulnerability_type.startswith('BANDIT'):
                score += vuln.severity.value * 0.2

        return min(10.0, score)


def format_security_report(report: SecurityReport) -> str:
    """Format the security report for display."""
    lines = [
        "🛡️ SECURITY ANALYSIS (THE IRON DOME)",
        "=" * 50,
        f"Files Scanned: {report.total_files_scanned}",
        f"VULNERABILITY SCORE: {report.vulnerability_score:.1f}/10",
        "",
    ]

    # Critical: Secret Leaks
    if report.secret_leaks:
        lines.append(f"🔐 SECRET LEAKS DETECTED ({len(report.secret_leaks)}):")
        for leak in sorted(report.secret_leaks, key=lambda x: x.severity.value, reverse=True)[:15]:
            emoji = "🔴" if leak.severity == VulnerabilitySeverity.CRITICAL else "🟠"
            lines.append(f"  {emoji} [{leak.secret_type}] {leak.filepath}:{leak.line_number}")
            lines.append(f"      Value: {leak.masked_value}")

    # SQL Injections
    if report.sql_injections:
        lines.append(f"\n💉 SQL INJECTION RISKS ({len(report.sql_injections)}):")
        for sqli in report.sql_injections[:10]:
            lines.append(f"  🔴 {sqli.filepath}:{sqli.line_number}")
            lines.append(f"      {sqli.description}")

    # Unprotected Endpoints
    if report.unprotected_endpoints:
        lines.append(f"\n🚪 UNPROTECTED ENDPOINTS ({len(report.unprotected_endpoints)}):")
        for endpoint in report.unprotected_endpoints[:15]:
            lines.append(f"  ⚠️ [{endpoint.method}] {endpoint.endpoint}")
            lines.append(f"      {endpoint.filepath}:{endpoint.line_number} ({endpoint.framework})")

    # Bandit Findings Summary
    if report.bandit_findings:
        lines.append(f"\n🔍 BANDIT FINDINGS ({len(report.bandit_findings)}):")
        severity_counts = {}
        for finding in report.bandit_findings:
            sev = finding.get('issue_severity', 'UNKNOWN')
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        for sev, count in sorted(severity_counts.items()):
            lines.append(f"  - {sev}: {count}")

    return "\n".join(lines)
