"""
🌌 NOVA State Definitions
The shared state that flows through the Ralph Loop.
"""

from typing import Dict, List, Optional, Any, TypedDict
from dataclasses import dataclass, field
from enum import Enum


class AnalysisPhase(Enum):
    """Current phase in the Ralph Loop."""
    SCANNING = "scanning"
    ANALYZING = "analyzing"
    CRITIQUING = "critiquing"
    GENERATING = "generating"
    COMPLETE = "complete"
    FAILED = "failed"


class SeverityLevel(Enum):
    """Overall severity level of findings."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class ScanResults:
    """Raw results from all scanner protocols."""
    # Protocol A: Code Rot
    code_rot_data: Dict[str, Any] = field(default_factory=dict)

    # Protocol B: Coder Guilt
    coder_guilt_data: Dict[str, Any] = field(default_factory=dict)

    # Protocol C: Security
    security_data: Dict[str, Any] = field(default_factory=dict)

    # Protocol D: Performance
    performance_data: Dict[str, Any] = field(default_factory=dict)

    # Metadata
    repo_name: str = ""
    repo_path: str = ""
    scan_timestamp: str = ""
    total_files: int = 0
    total_lines: int = 0


@dataclass
class CritiqueResult:
    """Result of Ralph's critique."""
    passed: bool = False
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    iteration: int = 0
    max_iterations: int = 3


@dataclass
class AnalysisReport:
    """The interpreted analysis from the Analyst Agent."""

    # Summary metrics
    severity_level: SeverityLevel = SeverityLevel.LOW
    entropy_score: float = 0.0  # 0-100

    # Section I: The Graveyard (Code Rot)
    graveyard_summary: str = ""
    abandoned_files: List[Dict[str, Any]] = field(default_factory=list)
    chaotic_files: List[Dict[str, Any]] = field(default_factory=list)
    rot_verdict: str = ""

    # Section II: The Confessional (Coder Guilt)
    confessional_summary: str = ""
    desperation_count: int = 0
    god_classes: List[Dict[str, Any]] = field(default_factory=list)
    guilt_verdict: str = ""

    # Section III: The Fortress (Security)
    fortress_summary: str = ""
    open_wounds: List[Dict[str, Any]] = field(default_factory=list)
    dependency_risks: List[str] = field(default_factory=list)
    security_verdict: str = ""

    # Section IV: The Engine (Performance)
    engine_summary: str = ""
    bottlenecks: List[Dict[str, Any]] = field(default_factory=list)
    bloat_warnings: List[str] = field(default_factory=list)
    performance_verdict: str = ""

    # Section V: Transmutation (12D Fix)
    refactor_plan: List[str] = field(default_factory=list)
    sacred_yes: str = ""  # The positive potential


class NovaState(TypedDict):
    """
    The shared state that flows through the Nova LangGraph.
    This is the single source of truth for the entire analysis pipeline.
    """
    # Input
    repo_path: str
    repo_name: str

    # Phase tracking
    phase: str  # AnalysisPhase value
    error: Optional[str]

    # Raw scan results (from Scanner Agent)
    scan_results: Optional[Dict[str, Any]]

    # Analysis report (from Analyst Agent)
    analysis_report: Optional[Dict[str, Any]]

    # Critique tracking (from Ralph Node)
    critique: Optional[Dict[str, Any]]
    critique_iteration: int

    # Final output
    final_report_markdown: Optional[str]

    # Vector context (from Qdrant)
    vector_context: Optional[List[Dict[str, Any]]]

    # Messages for LLM interaction
    messages: List[Dict[str, str]]
