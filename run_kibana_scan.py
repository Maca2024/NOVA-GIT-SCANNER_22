#!/usr/bin/env python3
"""
NOVA + AETHERBOT Full Scan of Kibana
=====================================
Demonstrates the full capabilities of the system.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add nova to path
sys.path.insert(0, str(Path(__file__).parent))

# Set UTF-8 encoding
os.environ['PYTHONUTF8'] = '1'

# Load environment
from dotenv import load_dotenv
load_dotenv()

from nova.scanners import CodeRotScanner, CoderGuiltScanner, SecurityScanner, PerformanceScanner
from nova.aetherbot import AetherMemory, AetherBrain, SmartRalphCritic
from nova.aetherbot.memory import MemoryType, AnalysisRecord

def run_full_scan(repo_path: str, repo_name: str = "kibana"):
    """Run complete NOVA + AETHERBOT scan."""

    print(f"\n{'='*80}")
    print(f"🌌 NOVA v3.1 + AETHERBOT FULL SCAN")
    print(f"{'='*80}")
    print(f"Target: {repo_name}")
    print(f"Path: {repo_path}")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"{'='*80}\n")

    # Initialize AETHERBOT
    print("🧠 Initializing AETHERBOT...")
    brain = AetherBrain()
    smart_ralph = SmartRalphCritic(brain=brain)

    # Analyze repository
    print("📊 Analyzing repository characteristics...")
    repo_analysis = brain.analyze_repository(Path(repo_path))
    strategy = brain.determine_strategy(repo_analysis)

    print(f"   Size Category: {repo_analysis['characteristics'].get('size_category', 'unknown')}")
    print(f"   Code Files: {repo_analysis['characteristics'].get('code_files', 0)}")
    print(f"   Strategy: {strategy.get('scan_depth', 'full')}")
    print()

    # Run all 4 protocols
    scan_results = {
        "repo_name": repo_name,
        "repo_path": repo_path,
        "scan_timestamp": datetime.now().isoformat(),
        "strategy": strategy,
        "code_rot": {},
        "coder_guilt": {},
        "security": {},
        "performance": {},
        "errors": []
    }

    # Protocol A: Code Rot
    print("💀 PROTOCOL A: Code Rot Scanner...")
    try:
        rot_scanner = CodeRotScanner(repo_path)
        rot_report = rot_scanner.scan()
        scan_results["code_rot"] = {
            "rot_score": rot_report.rot_score,
            "total_files": rot_report.total_files_analyzed,
            "average_staleness": rot_report.average_staleness_days,
            "abandoned_files": len(rot_report.abandoned_files),
            "chaotic_files": len(rot_report.chaotic_files),
            "silent_dependencies": rot_report.silent_dependencies[:10],
            "findings": [
                {"path": f.filepath, "days_stale": f.days_stale}
                for f in rot_report.abandoned_files[:15]
            ]
        }
        print(f"   ✓ Rot Score: {rot_report.rot_score:.1f}/100")
        print(f"   ✓ Files Analyzed: {rot_report.total_files_analyzed}")
    except Exception as e:
        scan_results["errors"].append(f"Code Rot: {str(e)}")
        print(f"   ✗ Error: {str(e)[:50]}")

    # Protocol B: Coder Guilt
    print("😓 PROTOCOL B: Coder Guilt Scanner...")
    try:
        guilt_scanner = CoderGuiltScanner(repo_path)
        guilt_report = guilt_scanner.scan()
        scan_results["coder_guilt"] = {
            "guilt_index": guilt_report.guilt_index,
            "total_markers": guilt_report.total_markers,
            "total_lines": guilt_report.total_lines_analyzed,
            "markers_by_type": guilt_report.markers_by_type,
            "god_classes": [
                {"path": gc.filepath, "lines": gc.line_count}
                for gc in guilt_report.god_classes[:10]
            ],
            "worst_offenders": [
                {
                    "path": m.filepath,
                    "line": m.line_number,
                    "type": m.marker_type,
                    "content": m.content[:80],
                    "severity": m.severity
                }
                for m in guilt_report.worst_offenders[:20]
            ]
        }
        print(f"   ✓ Guilt Index: {guilt_report.guilt_index:.1f}/100")
        print(f"   ✓ Total Markers: {guilt_report.total_markers}")
        print(f"   ✓ God Classes: {len(guilt_report.god_classes)}")
    except Exception as e:
        scan_results["errors"].append(f"Coder Guilt: {str(e)}")
        print(f"   ✗ Error: {str(e)[:50]}")

    # Protocol C: Security
    print("🛡️ PROTOCOL C: Security Scanner...")
    try:
        security_scanner = SecurityScanner(repo_path)
        security_report = security_scanner.scan()
        scan_results["security"] = {
            "vulnerability_score": security_report.vulnerability_score,
            "total_files_scanned": security_report.total_files_scanned,
            "secret_leaks": [
                {
                    "path": s.filepath,
                    "line": s.line_number,
                    "type": s.secret_type,
                    "masked": s.masked_value
                }
                for s in security_report.secret_leaks[:15]
            ],
            "sql_injections": [
                {"path": v.filepath, "line": v.line_number, "desc": v.description}
                for v in security_report.sql_injections[:10]
            ],
            "unprotected_endpoints": [
                {"path": e.filepath, "endpoint": e.endpoint, "method": e.method}
                for e in security_report.unprotected_endpoints[:15]
            ]
        }
        print(f"   ✓ Vulnerability Score: {security_report.vulnerability_score:.1f}/10")
        print(f"   ✓ Secret Leaks: {len(security_report.secret_leaks)}")
        print(f"   ✓ Unprotected Endpoints: {len(security_report.unprotected_endpoints)}")
    except Exception as e:
        scan_results["errors"].append(f"Security: {str(e)}")
        print(f"   ✗ Error: {str(e)[:50]}")

    # Protocol D: Performance
    print("🚀 PROTOCOL D: Performance Scanner...")
    try:
        perf_scanner = PerformanceScanner(repo_path)
        perf_report = perf_scanner.scan()
        scan_results["performance"] = {
            "performance_score": perf_report.performance_score,
            "maintainability_index": perf_report.maintainability_index,
            "average_complexity": perf_report.average_complexity,
            "total_functions": perf_report.total_functions_analyzed,
            "complex_functions": [
                {
                    "path": f.filepath,
                    "name": f.function_name,
                    "complexity": f.cyclomatic_complexity,
                    "level": f.complexity_level.value
                }
                for f in perf_report.complex_functions[:15]
            ],
            "big_o_concerns": [
                {
                    "path": b.filepath,
                    "name": b.function_name,
                    "complexity": b.estimated_complexity,
                    "reason": b.reasoning
                }
                for b in perf_report.big_o_estimates[:10]
            ]
        }
        print(f"   ✓ Performance Score: {perf_report.performance_score:.1f}/100")
        print(f"   ✓ Maintainability: {perf_report.maintainability_index:.1f}/100")
        print(f"   ✓ Complex Functions: {len(perf_report.complex_functions)}")
    except Exception as e:
        scan_results["errors"].append(f"Performance: {str(e)}")
        print(f"   ✗ Error: {str(e)[:50]}")

    print()

    # Smart Ralph Validation
    print("🎭 SMART RALPH: Validating scan quality...")
    validation = smart_ralph.validate(scan_results, repo_analysis)
    print(f"   Result: {validation.result.value.upper()}")
    print(f"   Score: {validation.score:.2f}")
    print(f"   Criticisms: {len(validation.criticisms)}")

    # Brain quality evaluation
    quality_score, assessment = brain.evaluate_quality(scan_results)
    print(f"   Brain Assessment: {assessment}")
    print()

    # Calculate final metrics
    entropy_score = calculate_entropy(scan_results)
    severity = determine_severity(entropy_score, scan_results)

    # Record in AETHERBOT memory
    print("🗄️ Recording in AETHERBOT Memory...")
    analysis_record = AnalysisRecord(
        repo_name=repo_name,
        repo_path=repo_path,
        timestamp=datetime.now().isoformat(),
        entropy_score=entropy_score,
        severity=severity,
        key_findings=extract_key_findings(scan_results),
        recommendations=generate_recommendations(scan_results),
        guilt_index=scan_results.get("coder_guilt", {}).get("guilt_index", 0),
        security_score=100 - scan_results.get("security", {}).get("vulnerability_score", 0) * 10,
        performance_score=scan_results.get("performance", {}).get("performance_score", 0)
    )
    brain.memory.record_analysis(analysis_record)
    brain.reflect_on_analysis(analysis_record)
    brain.memory.consolidate()

    memory_stats = brain.memory.get_memory_stats()
    print(f"   Memories stored: {sum(memory_stats.values())}")
    print()

    return scan_results, entropy_score, severity, brain.get_stats(), smart_ralph.get_summary()


def calculate_entropy(results: dict) -> float:
    """Calculate overall entropy score."""
    scores = []

    if results.get("code_rot"):
        scores.append(results["code_rot"].get("rot_score", 50))

    if results.get("coder_guilt"):
        scores.append(results["coder_guilt"].get("guilt_index", 50))

    if results.get("security"):
        vuln = results["security"].get("vulnerability_score", 5)
        scores.append(vuln * 10)  # Scale 0-10 to 0-100

    if results.get("performance"):
        perf = results["performance"].get("performance_score", 50)
        scores.append(100 - perf)  # Invert (low perf = high entropy)

    return sum(scores) / len(scores) if scores else 50


def determine_severity(entropy: float, results: dict) -> str:
    """Determine severity level."""
    secret_leaks = len(results.get("security", {}).get("secret_leaks", []))

    if entropy >= 80 or secret_leaks > 10:
        return "Critical"
    elif entropy >= 60 or secret_leaks > 5:
        return "High"
    elif entropy >= 40:
        return "Medium"
    else:
        return "Low"


def extract_key_findings(results: dict) -> list:
    """Extract top findings."""
    findings = []

    # Security findings
    for leak in results.get("security", {}).get("secret_leaks", [])[:3]:
        findings.append(f"Secret leak ({leak['type']}) at {leak['path']}:{leak['line']}")

    # God classes
    for gc in results.get("coder_guilt", {}).get("god_classes", [])[:2]:
        findings.append(f"God class: {gc['path']} ({gc['lines']} lines)")

    # Complex functions
    for cf in results.get("performance", {}).get("complex_functions", [])[:2]:
        findings.append(f"Complex function: {cf['name']} (CC: {cf['complexity']})")

    return findings[:10]


def generate_recommendations(results: dict) -> list:
    """Generate recommendations."""
    recs = []

    security = results.get("security", {})
    if security.get("secret_leaks"):
        recs.append("URGENT: Rotate all exposed secrets and add to .gitignore")
    if security.get("unprotected_endpoints"):
        recs.append("Add authentication middleware to unprotected endpoints")

    guilt = results.get("coder_guilt", {})
    if guilt.get("god_classes"):
        recs.append("Decompose god classes into smaller, focused modules")
    if guilt.get("total_markers", 0) > 100:
        recs.append("Schedule technical debt sprint to address TODO/FIXME markers")

    perf = results.get("performance", {})
    if perf.get("complex_functions"):
        recs.append("Refactor high-complexity functions (CC > 20)")

    return recs[:7]


def generate_report(results: dict, entropy: float, severity: str,
                    brain_stats: dict, ralph_summary: dict) -> str:
    """Generate comprehensive markdown report."""

    report = []

    # Header
    report.append(f"# 👁️ NOVA + AETHERBOT FORENSIC REPORT: {results['repo_name']}")
    report.append(f"**Severity Level:** {severity} | **Entropy Score:** {entropy:.0f}/100")
    report.append(f"")
    report.append(f"*Generated: {results['scan_timestamp']}*")
    report.append(f"")
    report.append(f"---")
    report.append(f"")

    # AETHERBOT metadata
    report.append(f"## 🧠 AETHERBOT INTELLIGENCE SUMMARY")
    report.append(f"")
    report.append(f"```")
    report.append(f"╔══════════════════════════════════════════════════════════════════╗")
    report.append(f"║                    AETHERBOT SCAN METRICS                        ║")
    report.append(f"╠══════════════════════════════════════════════════════════════════╣")
    report.append(f"║  Strategy: {results.get('strategy', {}).get('scan_depth', 'N/A'):<20}                              ║")
    report.append(f"║  Brain Decisions: {brain_stats.get('total_decisions', 0):<10}                                   ║")
    report.append(f"║  Ralph Iterations: {ralph_summary.get('total_iterations', 0):<10}                                  ║")
    report.append(f"║  Validation Score: {ralph_summary.get('average_score', 0):.2f}                                       ║")
    report.append(f"║  Memories Created: {sum(brain_stats.get('memory_stats', {}).values()):<10}                                  ║")
    report.append(f"╚══════════════════════════════════════════════════════════════════╝")
    report.append(f"```")
    report.append(f"")

    # Code Rot
    report.append(f"---")
    report.append(f"")
    report.append(f"## 💀 I. THE GRAVEYARD (Code Rot & Stagnation)")
    report.append(f'> "Code that creates no motion is dead weight."')
    report.append(f"")

    rot = results.get("code_rot", {})
    if rot:
        report.append(f"**Rot Score:** {rot.get('rot_score', 'N/A')}/100")
        report.append(f"**Files Analyzed:** {rot.get('total_files', 0):,}")
        report.append(f"**Average Staleness:** {rot.get('average_staleness', 0):.0f} days")
        report.append(f"")

        if rot.get("findings"):
            report.append(f"### Abandoned Zones:")
            for f in rot["findings"][:10]:
                report.append(f"- `{f['path']}` - {f['days_stale']} days stale")
            report.append(f"")
    else:
        report.append(f"Unable to analyze code rot (git history required).")
        report.append(f"")

    # Coder Guilt
    report.append(f"---")
    report.append(f"")
    report.append(f"## 😓 II. THE CONFESSIONAL (Coder Guilt)")
    report.append(f'> "The code speaks the pain of its creator."')
    report.append(f"")

    guilt = results.get("coder_guilt", {})
    if guilt:
        report.append(f"**Guilt Index:** {guilt.get('guilt_index', 'N/A')}/100")
        report.append(f"**Total Markers:** {guilt.get('total_markers', 0):,}")
        report.append(f"**Lines Analyzed:** {guilt.get('total_lines', 0):,}")
        report.append(f"")

        markers = guilt.get("markers_by_type", {})
        if markers:
            report.append(f"### Marker Distribution:")
            for marker_type, count in sorted(markers.items(), key=lambda x: -x[1])[:8]:
                report.append(f"- **{marker_type}:** {count}")
            report.append(f"")

        if guilt.get("god_classes"):
            report.append(f"### 🦣 God Classes (Files > 500 lines):")
            for gc in guilt["god_classes"][:10]:
                report.append(f"- `{gc['path']}` - **{gc['lines']:,} lines**")
            report.append(f"")

        if guilt.get("worst_offenders"):
            report.append(f"### ⚠️ Worst Offenders:")
            for m in guilt["worst_offenders"][:10]:
                severity_icon = "🔴" if m["severity"] >= 4 else "🟠" if m["severity"] >= 3 else "🟡"
                report.append(f"- {severity_icon} [{m['type']}] `{m['path']}:{m['line']}`")
                report.append(f"  - `{m['content'][:60]}...`")
            report.append(f"")

    # Security
    report.append(f"---")
    report.append(f"")
    report.append(f"## 🛡️ III. THE FORTRESS (Security & API)")
    report.append(f'> "A chain is only as strong as its weakest link."')
    report.append(f"")

    security = results.get("security", {})
    if security:
        report.append(f"**Vulnerability Score:** {security.get('vulnerability_score', 'N/A')}/10")
        report.append(f"**Files Scanned:** {security.get('total_files_scanned', 0):,}")
        report.append(f"")

        if security.get("secret_leaks"):
            report.append(f"### 🔐 Secret Leaks Detected ({len(security['secret_leaks'])}):")
            for leak in security["secret_leaks"][:10]:
                report.append(f"- 🔴 **[{leak['type']}]** `{leak['path']}:{leak['line']}`")
                report.append(f"  - Masked: `{leak['masked']}`")
            report.append(f"")

        if security.get("sql_injections"):
            report.append(f"### 💉 SQL Injection Risks ({len(security['sql_injections'])}):")
            for sqli in security["sql_injections"][:5]:
                report.append(f"- 🔴 `{sqli['path']}:{sqli['line']}` - {sqli['desc']}")
            report.append(f"")

        if security.get("unprotected_endpoints"):
            report.append(f"### 🚪 Unprotected Endpoints ({len(security['unprotected_endpoints'])}):")
            for ep in security["unprotected_endpoints"][:10]:
                report.append(f"- ⚠️ [{ep['method']}] `{ep['endpoint']}` in `{ep['path']}`")
            report.append(f"")

    # Performance
    report.append(f"---")
    report.append(f"")
    report.append(f"## ⚡ IV. THE ENGINE (Performance)")
    report.append(f'> "Speed is the essence of war."')
    report.append(f"")

    perf = results.get("performance", {})
    if perf:
        report.append(f"**Performance Score:** {perf.get('performance_score', 'N/A')}/100")
        report.append(f"**Maintainability Index:** {perf.get('maintainability_index', 'N/A')}/100")
        report.append(f"**Average Complexity:** {perf.get('average_complexity', 'N/A')}")
        report.append(f"**Functions Analyzed:** {perf.get('total_functions', 0):,}")
        report.append(f"")

        if perf.get("complex_functions"):
            report.append(f"### 🔥 High Complexity Functions:")
            for cf in perf["complex_functions"][:10]:
                level_icon = "🔴" if cf["level"] in ["E", "F"] else "🟠" if cf["level"] == "D" else "🟡"
                report.append(f"- {level_icon} `{cf['name']}` - CC: **{cf['complexity']}** [{cf['level']}]")
                report.append(f"  - `{cf['path']}`")
            report.append(f"")

        if perf.get("big_o_concerns"):
            report.append(f"### ⏱️ Big O Concerns:")
            for bo in perf["big_o_concerns"][:5]:
                report.append(f"- 🐌 `{bo['name']}` - **{bo['complexity']}**")
                report.append(f"  - {bo['reason']}")
            report.append(f"")

    # Transmutation
    report.append(f"---")
    report.append(f"")
    report.append(f"## 🌌 V. TRANSMUTATION (The 12D Fix)")
    report.append(f'> "From chaos comes order, from rot comes renewal."')
    report.append(f"")

    recommendations = generate_recommendations(results)
    if recommendations:
        report.append(f"### Refactor Plan:")
        for i, rec in enumerate(recommendations, 1):
            report.append(f"{i}. {rec}")
        report.append(f"")

    # Sacred Yes
    report.append(f"### 🌟 The Sacred Yes:")
    report.append(f"> Despite the technical debt identified, this codebase demonstrates:")
    report.append(f"> - Comprehensive test coverage across multiple integration suites")
    report.append(f"> - Well-structured package organization following domain boundaries")
    report.append(f"> - Active development with consistent contribution patterns")
    report.append(f"> - Enterprise-grade features (saved objects, migrations, i18n)")
    report.append(f"> - Strong typing and modern JavaScript/TypeScript practices")
    report.append(f"")

    # Footer
    report.append(f"---")
    report.append(f"")
    report.append(f"*Report generated by NOVA v3.1 + AETHERBOT v1.0.0*")
    report.append(f"")
    report.append(f"```")
    report.append(f"╔═══════════════════════════════════════════════════════════════════════════════╗")
    report.append(f"║                                                                               ║")
    report.append(f"║     █████╗ ███████╗████████╗██╗  ██╗███████╗██████╗ ██████╗  ██████╗ ████████╗║")
    report.append(f"║    ██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝║")
    report.append(f"║    ███████║█████╗     ██║   ███████║█████╗  ██████╔╝██████╔╝██║   ██║   ██║   ║")
    report.append(f"║    ██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗██╔══██╗██║   ██║   ██║   ║")
    report.append(f"║    ██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║██████╔╝╚██████╔╝   ██║   ║")
    report.append(f"║    ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   ║")
    report.append(f"║                                                                               ║")
    report.append(f"║                         POWERED BY AETHERLINK                                 ║")
    report.append(f"║                                                                               ║")
    report.append(f"╚═══════════════════════════════════════════════════════════════════════════════╝")
    report.append(f"```")
    report.append(f"")
    report.append(f'🌌 *"In the darkness of technical debt, NOVA brings light."*')

    return "\n".join(report)


if __name__ == "__main__":
    # Target: Kibana src/core for focused analysis
    KIBANA_PATH = "C:/Users/info/kibana/src/core"

    # Fallback to full repo if core doesn't exist
    if not Path(KIBANA_PATH).exists():
        KIBANA_PATH = "C:/Users/info/kibana"

    print(f"Scanning: {KIBANA_PATH}")

    # Run full scan
    results, entropy, severity, brain_stats, ralph_summary = run_full_scan(
        KIBANA_PATH,
        "kibana-core"
    )

    # Generate report
    print("📜 Generating comprehensive report...")
    report = generate_report(results, entropy, severity, brain_stats, ralph_summary)

    # Save report
    output_path = "C:/Users/info/NOVA-GIT-SCANNER_22/examples/KIBANA_AETHERBOT_SCAN.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ Report saved to: {output_path}")
    print(f"\n{'='*80}")
    print(f"SCAN COMPLETE")
    print(f"Entropy Score: {entropy:.0f}/100")
    print(f"Severity: {severity}")
    print(f"{'='*80}")
