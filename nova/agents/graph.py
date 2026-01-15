"""
🔄 THE RALPH LOOP - LangGraph Implementation
The gatekeeper that ensures quality analysis.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, List, Literal
from dataclasses import asdict

from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from .state import NovaState, ScanResults, AnalysisReport, SeverityLevel
from ..scanners import CodeRotScanner, CoderGuiltScanner, SecurityScanner, PerformanceScanner


# ============================================================================
# SCANNER AGENT NODE
# ============================================================================

def scanner_agent(state: NovaState) -> NovaState:
    """
    🔬 SCANNER AGENT
    Runs all Python forensic tools and collects raw data.
    """
    repo_path = state["repo_path"]
    repo_name = state.get("repo_name", os.path.basename(repo_path))

    scan_results = {
        "repo_name": repo_name,
        "repo_path": repo_path,
        "scan_timestamp": datetime.now().isoformat(),
        "code_rot": {},
        "coder_guilt": {},
        "security": {},
        "performance": {},
        "errors": []
    }

    # Protocol A: Code Rot
    try:
        rot_scanner = CodeRotScanner(repo_path)
        rot_report = rot_scanner.scan()
        scan_results["code_rot"] = {
            "abandoned_files": [
                {"path": f.filepath, "days_stale": f.days_stale, "imported_by": f.imported_by}
                for f in rot_report.abandoned_files[:20]
            ],
            "chaotic_files": [
                {"path": f.filepath, "monthly_churn": f.monthly_churn, "authors": f.authors}
                for f in rot_report.chaotic_files[:20]
            ],
            "silent_dependencies": rot_report.silent_dependencies[:10],
            "rot_score": rot_report.rot_score,
            "total_files": rot_report.total_files_analyzed,
            "average_staleness": rot_report.average_staleness_days
        }
    except Exception as e:
        scan_results["errors"].append(f"Code Rot Scanner: {str(e)}")

    # Protocol B: Coder Guilt
    try:
        guilt_scanner = CoderGuiltScanner(repo_path)
        guilt_report = guilt_scanner.scan()
        scan_results["coder_guilt"] = {
            "total_markers": guilt_report.total_markers,
            "markers_by_type": guilt_report.markers_by_type,
            "guilt_index": guilt_report.guilt_index,
            "god_classes": [
                {"path": gc.filepath, "lines": gc.line_count}
                for gc in guilt_report.god_classes[:10]
            ],
            "hotspots": [
                {"path": hs.filepath, "density": hs.guilt_density}
                for hs in guilt_report.desperation_hotspots[:10]
            ],
            "worst_offenders": [
                {
                    "path": m.filepath,
                    "line": m.line_number,
                    "type": m.marker_type,
                    "content": m.content[:100],
                    "severity": m.severity
                }
                for m in guilt_report.worst_offenders[:20]
            ],
            "total_lines": guilt_report.total_lines_analyzed
        }
    except Exception as e:
        scan_results["errors"].append(f"Coder Guilt Scanner: {str(e)}")

    # Protocol C: Security
    try:
        security_scanner = SecurityScanner(repo_path)
        security_report = security_scanner.scan()
        scan_results["security"] = {
            "vulnerability_score": security_report.vulnerability_score,
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
                {
                    "path": v.filepath,
                    "line": v.line_number,
                    "description": v.description
                }
                for v in security_report.sql_injections[:10]
            ],
            "unprotected_endpoints": [
                {
                    "path": e.filepath,
                    "line": e.line_number,
                    "endpoint": e.endpoint,
                    "method": e.method
                }
                for e in security_report.unprotected_endpoints[:15]
            ],
            "total_scanned": security_report.total_files_scanned
        }
    except Exception as e:
        scan_results["errors"].append(f"Security Scanner: {str(e)}")

    # Protocol D: Performance
    try:
        perf_scanner = PerformanceScanner(repo_path)
        perf_report = perf_scanner.scan()
        scan_results["performance"] = {
            "performance_score": perf_report.performance_score,
            "maintainability_index": perf_report.maintainability_index,
            "average_complexity": perf_report.average_complexity,
            "complex_functions": [
                {
                    "path": f.filepath,
                    "name": f.function_name,
                    "line": f.line_number,
                    "complexity": f.cyclomatic_complexity,
                    "level": f.complexity_level.value
                }
                for f in perf_report.complex_functions[:15]
            ],
            "big_o_concerns": [
                {
                    "path": b.filepath,
                    "name": b.function_name,
                    "line": b.line_number,
                    "complexity": b.estimated_complexity,
                    "reasoning": b.reasoning
                }
                for b in perf_report.big_o_estimates[:15]
            ],
            "heavy_imports": [
                {
                    "path": i.filepath,
                    "import": i.import_name,
                    "reason": i.reason
                }
                for i in perf_report.heavy_imports[:15]
            ],
            "total_functions": perf_report.total_functions_analyzed
        }
    except Exception as e:
        scan_results["errors"].append(f"Performance Scanner: {str(e)}")

    return {
        **state,
        "phase": "analyzing",
        "scan_results": scan_results
    }


# ============================================================================
# ANALYST AGENT NODE
# ============================================================================

def get_analyst_prompt(scan_results: Dict[str, Any], critique_feedback: Optional[str] = None) -> str:
    """Generate the analyst prompt with scan data."""

    base_prompt = f"""You are NOVA, the Forensic Code Auditor. You are a mirror that reveals ugly truths.

Analyze this repository scan data and create a structured analysis report.

## SCAN DATA:
```json
{json.dumps(scan_results, indent=2, default=str)}
```

{f"## PREVIOUS CRITIQUE FEEDBACK (Address these issues):{chr(10)}{critique_feedback}" if critique_feedback else ""}

## YOUR TASK:
Create a detailed analysis with these EXACT sections. Be specific with file paths and line numbers.

### REQUIRED OUTPUT FORMAT (JSON):
```json
{{
  "severity_level": "Low|Medium|High|Critical",
  "entropy_score": <0-100>,

  "graveyard": {{
    "summary": "<2-3 sentences about code rot findings>",
    "abandoned_files": ["<file:reason>", ...],
    "chaotic_files": ["<file:reason>", ...],
    "verdict": "<actionable advice>"
  }},

  "confessional": {{
    "summary": "<2-3 sentences about coder guilt>",
    "desperation_markers": <count>,
    "god_classes": ["<file:linecount>", ...],
    "verdict": "<actionable advice>"
  }},

  "fortress": {{
    "summary": "<2-3 sentences about security>",
    "open_wounds": ["<vulnerability description with file:line>", ...],
    "dependency_risks": ["<risk description>", ...],
    "verdict": "<actionable advice>"
  }},

  "engine": {{
    "summary": "<2-3 sentences about performance>",
    "bottlenecks": ["<function name in file - O(complexity)>", ...],
    "bloat": ["<heavy import warning>", ...],
    "verdict": "<actionable advice>"
  }},

  "transmutation": {{
    "refactor_steps": ["<specific step 1>", "<specific step 2>", ...],
    "sacred_yes": "<the hidden potential and positive aspects of this codebase>"
  }}
}}
```

CRITICAL REQUIREMENTS:
1. ALWAYS cite specific file paths and line numbers
2. Back up Code Rot claims with dates/days stale
3. Security risks must reference actual scan findings
4. Be brutally honest but constructive
5. The sacred_yes must find genuine potential

Output ONLY the JSON, no additional text."""

    return base_prompt


def analyst_agent(state: NovaState) -> NovaState:
    """
    🧠 ANALYST AGENT
    Uses LLM (Claude) to interpret scan data into structured analysis.
    """
    scan_results = state.get("scan_results", {})
    critique = state.get("critique")

    critique_feedback = None
    if critique and not critique.get("passed", False):
        critique_feedback = "\n".join(critique.get("issues", []))

    # Get API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            **state,
            "phase": "failed",
            "error": "ANTHROPIC_API_KEY not set"
        }

    try:
        llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            api_key=api_key,
            max_tokens=4096
        )

        prompt = get_analyst_prompt(scan_results, critique_feedback)

        response = llm.invoke([
            SystemMessage(content="You are NOVA, a forensic code auditor. Output only valid JSON."),
            HumanMessage(content=prompt)
        ])

        # Parse the response
        response_text = response.content
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        analysis_report = json.loads(response_text.strip())

        return {
            **state,
            "phase": "critiquing",
            "analysis_report": analysis_report
        }

    except json.JSONDecodeError as e:
        return {
            **state,
            "phase": "failed",
            "error": f"Failed to parse analyst response: {str(e)}"
        }
    except Exception as e:
        return {
            **state,
            "phase": "failed",
            "error": f"Analyst agent error: {str(e)}"
        }


# ============================================================================
# RALPH NODE (THE CRITIC)
# ============================================================================

def ralph_critic(state: NovaState) -> NovaState:
    """
    🎭 RALPH - THE CRITIC
    Validates the analysis report for quality and specificity.
    """
    analysis = state.get("analysis_report", {})
    scan_results = state.get("scan_results", {})
    iteration = state.get("critique_iteration", 0)
    max_iterations = 3

    issues = []
    suggestions = []

    # Check 1: Did the Analyst cite specific file paths?
    def has_file_paths(section: Dict) -> bool:
        section_str = json.dumps(section)
        # Look for common file path patterns
        return any(ext in section_str for ext in ['.py', '.js', '.ts', '.java', '.go', '/', '\\'])

    if "graveyard" in analysis:
        if not analysis["graveyard"].get("abandoned_files") and scan_results.get("code_rot", {}).get("abandoned_files"):
            issues.append("Graveyard section missing abandoned file citations despite scan data showing them")

    if "confessional" in analysis:
        if not analysis["confessional"].get("god_classes") and scan_results.get("coder_guilt", {}).get("god_classes"):
            issues.append("Confessional section missing god class citations")

    # Check 2: Is Code Rot backed by dates?
    if "graveyard" in analysis:
        graveyard_str = json.dumps(analysis["graveyard"])
        if scan_results.get("code_rot", {}).get("abandoned_files"):
            if not any(word in graveyard_str.lower() for word in ["day", "month", "year", "stale", "ago"]):
                issues.append("Code Rot findings should mention staleness duration (days/months)")

    # Check 3: Is Security validated against scan data?
    if "fortress" in analysis:
        fortress = analysis["fortress"]
        scan_security = scan_results.get("security", {})

        # If scan found secrets but report doesn't mention them
        if scan_security.get("secret_leaks") and not fortress.get("open_wounds"):
            issues.append("Security section should address the detected secret leaks")

        # If scan found SQL injection but report doesn't mention
        if scan_security.get("sql_injections") and "sql" not in json.dumps(fortress).lower():
            issues.append("Security section should address SQL injection findings")

    # Check 4: Ensure transmutation section is actionable
    if "transmutation" in analysis:
        trans = analysis["transmutation"]
        if not trans.get("refactor_steps") or len(trans.get("refactor_steps", [])) < 3:
            suggestions.append("Transmutation section should have at least 3 specific refactor steps")

        if not trans.get("sacred_yes") or len(trans.get("sacred_yes", "")) < 50:
            suggestions.append("Sacred Yes should be more detailed about the codebase's potential")

    # Check 5: Severity and entropy must be present
    if "severity_level" not in analysis:
        issues.append("Missing severity_level classification")
    if "entropy_score" not in analysis:
        issues.append("Missing entropy_score")

    # Determine pass/fail
    passed = len(issues) == 0 or iteration >= max_iterations - 1

    critique = {
        "passed": passed,
        "issues": issues,
        "suggestions": suggestions,
        "iteration": iteration + 1,
        "max_iterations": max_iterations
    }

    next_phase = "generating" if passed else "analyzing"

    return {
        **state,
        "phase": next_phase,
        "critique": critique,
        "critique_iteration": iteration + 1
    }


# ============================================================================
# REPORT GENERATOR NODE
# ============================================================================

def report_generator(state: NovaState) -> NovaState:
    """
    📜 REPORT GENERATOR
    Generates the final NOVA_FORENSIC.md report.
    """
    analysis = state.get("analysis_report", {})
    scan_results = state.get("scan_results", {})
    repo_name = state.get("repo_name", "Unknown Repository")

    severity = analysis.get("severity_level", "Medium")
    entropy = analysis.get("entropy_score", 50)

    # Build the markdown report
    report_lines = [
        f"# 👁️ NOVA FORENSIC REPORT: {repo_name}",
        f"**Severity Level:** {severity} | **Entropy Score:** {entropy}/100",
        f"",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        f"",
        "---",
        "",
    ]

    # Section I: The Graveyard
    graveyard = analysis.get("graveyard", {})
    report_lines.extend([
        "## 💀 I. THE GRAVEYARD (Code Rot & Stagnation)",
        "> \"Code that creates no motion is dead weight.\"",
        "",
        graveyard.get("summary", "No code rot analysis available."),
        "",
    ])

    if graveyard.get("abandoned_files"):
        report_lines.append("### Abandoned Zones:")
        for f in graveyard["abandoned_files"][:10]:
            report_lines.append(f"- {f}")
        report_lines.append("")

    if graveyard.get("chaotic_files"):
        report_lines.append("### High Churn (Chaos Zones):")
        for f in graveyard["chaotic_files"][:10]:
            report_lines.append(f"- {f}")
        report_lines.append("")

    if graveyard.get("verdict"):
        report_lines.extend([
            "### The Verdict:",
            graveyard["verdict"],
            "",
        ])

    # Section II: The Confessional
    confessional = analysis.get("confessional", {})
    report_lines.extend([
        "---",
        "",
        "## 😓 II. THE CONFESSIONAL (Coder Guilt)",
        "> \"The code speaks the pain of its creator.\"",
        "",
        confessional.get("summary", "No guilt analysis available."),
        "",
    ])

    markers = confessional.get("desperation_markers", 0)
    if markers:
        report_lines.append(f"**Desperation Detected:** Found {markers} markers of developer desperation.")
        report_lines.append("")

    if confessional.get("god_classes"):
        report_lines.append("### The God Classes:")
        for gc in confessional["god_classes"][:10]:
            report_lines.append(f"- {gc}")
        report_lines.append("")

    if confessional.get("verdict"):
        report_lines.extend([
            "### The Verdict:",
            confessional["verdict"],
            "",
        ])

    # Section III: The Fortress
    fortress = analysis.get("fortress", {})
    report_lines.extend([
        "---",
        "",
        "## 🛡️ III. THE FORTRESS (Security & API)",
        "> \"A chain is only as strong as its weakest link.\"",
        "",
        fortress.get("summary", "No security analysis available."),
        "",
    ])

    if fortress.get("open_wounds"):
        report_lines.append("### Open Wounds:")
        for wound in fortress["open_wounds"][:10]:
            report_lines.append(f"- 🔴 {wound}")
        report_lines.append("")

    if fortress.get("dependency_risks"):
        report_lines.append("### Dependency Risks:")
        for risk in fortress["dependency_risks"][:10]:
            report_lines.append(f"- ⚠️ {risk}")
        report_lines.append("")

    if fortress.get("verdict"):
        report_lines.extend([
            "### The Verdict:",
            fortress["verdict"],
            "",
        ])

    # Section IV: The Engine
    engine = analysis.get("engine", {})
    report_lines.extend([
        "---",
        "",
        "## ⚡ IV. THE ENGINE (Performance)",
        "> \"Speed is the essence of war.\"",
        "",
        engine.get("summary", "No performance analysis available."),
        "",
    ])

    if engine.get("bottlenecks"):
        report_lines.append("### Bottlenecks:")
        for bn in engine["bottlenecks"][:10]:
            report_lines.append(f"- 🐌 {bn}")
        report_lines.append("")

    if engine.get("bloat"):
        report_lines.append("### Bloat Warnings:")
        for bloat in engine["bloat"][:10]:
            report_lines.append(f"- 📦 {bloat}")
        report_lines.append("")

    if engine.get("verdict"):
        report_lines.extend([
            "### The Verdict:",
            engine["verdict"],
            "",
        ])

    # Section V: Transmutation
    transmutation = analysis.get("transmutation", {})
    report_lines.extend([
        "---",
        "",
        "## 🌌 V. TRANSMUTATION (The 12D Fix)",
        "> \"From chaos comes order, from rot comes renewal.\"",
        "",
    ])

    if transmutation.get("refactor_steps"):
        report_lines.append("### Refactor Plan:")
        for i, step in enumerate(transmutation["refactor_steps"], 1):
            report_lines.append(f"{i}. {step}")
        report_lines.append("")

    if transmutation.get("sacred_yes"):
        report_lines.extend([
            "### 🌟 The Sacred Yes:",
            f"> {transmutation['sacred_yes']}",
            "",
        ])

    # Footer
    report_lines.extend([
        "---",
        "",
        "*Report generated by NOVA v3.1 - The Forensic Code Auditor*",
        "",
        "```",
        "🌌 \"In the darkness of technical debt, NOVA brings light.\"",
        "```",
    ])

    final_report = "\n".join(report_lines)

    return {
        **state,
        "phase": "complete",
        "final_report_markdown": final_report
    }


# ============================================================================
# ROUTING LOGIC
# ============================================================================

def should_continue(state: NovaState) -> Literal["analyst", "generator", "end"]:
    """Determine the next node based on critique results."""
    phase = state.get("phase", "")

    if phase == "analyzing":
        return "analyst"
    elif phase == "generating":
        return "generator"
    elif phase == "complete" or phase == "failed":
        return "end"

    return "end"


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def create_nova_graph() -> StateGraph:
    """
    🔄 Create the NOVA LangGraph with Ralph Loop.

    Flow:
    1. Scanner Agent -> Collects Raw Data
    2. Analyst Agent -> Interprets with LLM
    3. Ralph Critic -> Validates Quality
       - FAIL: Back to Analyst
       - PASS: To Report Generator
    4. Report Generator -> Final Output
    """

    # Create the graph
    workflow = StateGraph(NovaState)

    # Add nodes
    workflow.add_node("scanner", scanner_agent)
    workflow.add_node("analyst", analyst_agent)
    workflow.add_node("ralph", ralph_critic)
    workflow.add_node("generator", report_generator)

    # Set entry point
    workflow.set_entry_point("scanner")

    # Add edges
    workflow.add_edge("scanner", "analyst")
    workflow.add_edge("analyst", "ralph")

    # Conditional edge from Ralph
    workflow.add_conditional_edges(
        "ralph",
        should_continue,
        {
            "analyst": "analyst",
            "generator": "generator",
            "end": END
        }
    )

    workflow.add_edge("generator", END)

    return workflow.compile()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_nova_analysis(repo_path: str, repo_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Execute the full NOVA analysis pipeline.

    Args:
        repo_path: Path to the repository to analyze
        repo_name: Optional name for the repository

    Returns:
        Final state including the forensic report
    """
    if repo_name is None:
        repo_name = os.path.basename(repo_path)

    initial_state: NovaState = {
        "repo_path": repo_path,
        "repo_name": repo_name,
        "phase": "scanning",
        "error": None,
        "scan_results": None,
        "analysis_report": None,
        "critique": None,
        "critique_iteration": 0,
        "final_report_markdown": None,
        "vector_context": None,
        "messages": []
    }

    graph = create_nova_graph()
    result = graph.invoke(initial_state)

    return result
