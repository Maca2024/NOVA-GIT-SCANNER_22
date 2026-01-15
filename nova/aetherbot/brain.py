"""
🧠 AETHERBOT BRAIN - Agentic Decision Engine
=============================================
The intelligent decision-making core that orchestrates autonomous actions.

The brain provides:
- Strategic planning for code analysis
- Dynamic agent coordination
- Context-aware decision making
- Learning from past analyses
- Self-improvement through reflection
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from .memory import AetherMemory, MemoryType, AnalysisRecord


class DecisionType(Enum):
    """Types of decisions the brain can make."""
    SCAN_STRATEGY = "scan_strategy"
    DEPTH_ADJUSTMENT = "depth_adjustment"
    PROTOCOL_SELECTION = "protocol_selection"
    QUALITY_THRESHOLD = "quality_threshold"
    REPORT_STYLE = "report_style"
    ITERATION_CONTROL = "iteration_control"


class AgentRole(Enum):
    """Roles in the AETHERBOT agent system."""
    SCANNER = "scanner"          # Data collection
    ANALYST = "analyst"          # Pattern analysis
    CRITIC = "critic"            # Quality validation
    REPORTER = "reporter"        # Report generation
    STRATEGIST = "strategist"    # Planning & coordination


@dataclass
class Decision:
    """A decision made by the AETHERBOT brain."""
    decision_type: DecisionType
    choice: str
    reasoning: str
    confidence: float  # 0-1
    timestamp: str
    context: Dict[str, Any] = field(default_factory=dict)
    outcome: Optional[str] = None


@dataclass
class AgentState:
    """State of an agent in the system."""
    role: AgentRole
    status: str  # idle, working, blocked, completed
    current_task: Optional[str] = None
    progress: float = 0.0  # 0-1
    errors: List[str] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)


class AetherBrain:
    """
    🧠 THE AETHERBOT BRAIN

    The intelligent core that:
    - Makes strategic decisions about analysis approach
    - Coordinates multiple agents working in parallel
    - Learns from past analyses to improve future scans
    - Adapts behavior based on repository characteristics
    - Self-reflects and optimizes strategies
    """

    # Strategy templates for different repo sizes
    REPO_STRATEGIES = {
        "tiny": {           # < 100 files
            "scan_depth": "full",
            "parallel_agents": 1,
            "sampling": False,
            "protocols": ["code_rot", "coder_guilt", "security", "performance"]
        },
        "small": {          # 100-1000 files
            "scan_depth": "full",
            "parallel_agents": 2,
            "sampling": False,
            "protocols": ["code_rot", "coder_guilt", "security", "performance"]
        },
        "medium": {         # 1000-10000 files
            "scan_depth": "smart",
            "parallel_agents": 4,
            "sampling": True,
            "sample_rate": 0.3,
            "protocols": ["code_rot", "coder_guilt", "security", "performance"]
        },
        "large": {          # 10000-100000 files
            "scan_depth": "targeted",
            "parallel_agents": 4,
            "sampling": True,
            "sample_rate": 0.1,
            "focus_dirs": ["src", "lib", "app", "core"],
            "protocols": ["security", "coder_guilt", "performance"]
        },
        "massive": {        # > 100000 files
            "scan_depth": "surgical",
            "parallel_agents": 4,
            "sampling": True,
            "sample_rate": 0.05,
            "focus_dirs": ["src", "lib", "app", "core", "packages"],
            "protocols": ["security", "coder_guilt"]
        }
    }

    # Quality thresholds based on severity
    QUALITY_THRESHOLDS = {
        "critical": 0.95,    # Near-perfect analysis required
        "high": 0.85,        # High quality
        "medium": 0.70,      # Acceptable quality
        "low": 0.50          # Basic analysis
    }

    def __init__(self, memory: Optional[AetherMemory] = None):
        """
        Initialize the AETHERBOT brain.

        Args:
            memory: AetherMemory instance (creates new if not provided)
        """
        self.memory = memory or AetherMemory()
        self.decisions: List[Decision] = []
        self.agents: Dict[AgentRole, AgentState] = {
            role: AgentState(role=role, status="idle")
            for role in AgentRole
        }
        self.current_strategy: Optional[Dict] = None
        self.learning_rate = 0.1  # How much to adjust based on feedback

    # =========================================================================
    # STRATEGIC PLANNING
    # =========================================================================

    def analyze_repository(self, repo_path: Path) -> Dict[str, Any]:
        """
        Analyze repository characteristics to inform strategy.

        Args:
            repo_path: Path to the repository

        Returns:
            Repository analysis results
        """
        analysis = {
            "path": str(repo_path),
            "timestamp": datetime.now().isoformat(),
            "characteristics": {}
        }

        try:
            # Count files
            all_files = list(repo_path.rglob("*"))
            code_files = [f for f in all_files if f.is_file() and f.suffix in
                         [".py", ".js", ".ts", ".java", ".go", ".rs", ".c", ".cpp",
                          ".h", ".rb", ".php", ".cs", ".swift", ".kt"]]

            analysis["characteristics"]["total_files"] = len(all_files)
            analysis["characteristics"]["code_files"] = len(code_files)

            # Determine size category
            file_count = len(code_files)
            if file_count < 100:
                analysis["characteristics"]["size_category"] = "tiny"
            elif file_count < 1000:
                analysis["characteristics"]["size_category"] = "small"
            elif file_count < 10000:
                analysis["characteristics"]["size_category"] = "medium"
            elif file_count < 100000:
                analysis["characteristics"]["size_category"] = "large"
            else:
                analysis["characteristics"]["size_category"] = "massive"

            # Detect primary language
            language_counts = {}
            for f in code_files:
                ext = f.suffix.lower()
                language_counts[ext] = language_counts.get(ext, 0) + 1

            if language_counts:
                primary_ext = max(language_counts, key=language_counts.get)
                analysis["characteristics"]["primary_language"] = self._ext_to_language(primary_ext)
                analysis["characteristics"]["language_distribution"] = language_counts

            # Check for common patterns
            analysis["characteristics"]["has_tests"] = any(
                "test" in str(f).lower() for f in code_files
            )
            analysis["characteristics"]["has_ci"] = (
                (repo_path / ".github" / "workflows").exists() or
                (repo_path / ".gitlab-ci.yml").exists() or
                (repo_path / "Jenkinsfile").exists()
            )
            analysis["characteristics"]["is_monorepo"] = (
                (repo_path / "packages").exists() or
                (repo_path / "apps").exists() or
                len(list(repo_path.glob("*/package.json"))) > 3
            )

        except Exception as e:
            analysis["error"] = str(e)

        # Store analysis in memory
        self.memory.remember(
            content=json.dumps(analysis),
            memory_type=MemoryType.SHORT_TERM,
            metadata={"type": "repo_analysis", "path": str(repo_path)},
            importance=0.6
        )

        return analysis

    def _ext_to_language(self, ext: str) -> str:
        """Convert file extension to language name."""
        mapping = {
            ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
            ".java": "Java", ".go": "Go", ".rs": "Rust",
            ".c": "C", ".cpp": "C++", ".h": "C/C++ Header",
            ".rb": "Ruby", ".php": "PHP", ".cs": "C#",
            ".swift": "Swift", ".kt": "Kotlin"
        }
        return mapping.get(ext, "Unknown")

    def determine_strategy(self, repo_analysis: Dict) -> Dict[str, Any]:
        """
        Determine the optimal scanning strategy based on repo analysis.

        Args:
            repo_analysis: Results from analyze_repository()

        Returns:
            Scanning strategy configuration
        """
        characteristics = repo_analysis.get("characteristics", {})
        size_category = characteristics.get("size_category", "medium")

        # Start with base strategy for repo size
        strategy = self.REPO_STRATEGIES[size_category].copy()

        # Adjust based on past experience
        similar_analyses = self.memory.get_similar_analyses(
            repo_name=Path(repo_analysis.get("path", "")).name
        )

        if similar_analyses:
            # Learn from past analyses
            avg_entropy = sum(a.entropy_score for a in similar_analyses) / len(similar_analyses)
            if avg_entropy > 70:
                # High entropy repos need deeper analysis
                strategy["scan_depth"] = "thorough"
                if "sample_rate" in strategy:
                    strategy["sample_rate"] = min(strategy["sample_rate"] * 1.5, 1.0)

        # Adjust for monorepos
        if characteristics.get("is_monorepo"):
            strategy["focus_dirs"] = strategy.get("focus_dirs", []) + ["packages", "apps"]
            strategy["parallel_agents"] = min(strategy.get("parallel_agents", 2) + 2, 8)

        # Record decision
        decision = Decision(
            decision_type=DecisionType.SCAN_STRATEGY,
            choice=size_category,
            reasoning=f"Repository has {characteristics.get('code_files', 0)} code files, "
                     f"categorized as {size_category}",
            confidence=0.8,
            timestamp=datetime.now().isoformat(),
            context={"repo_analysis": repo_analysis}
        )
        self.decisions.append(decision)

        self.current_strategy = strategy
        return strategy

    # =========================================================================
    # AGENT COORDINATION
    # =========================================================================

    def assign_agent(self, role: AgentRole, task: str) -> bool:
        """
        Assign a task to an agent.

        Args:
            role: The agent role to assign
            task: Description of the task

        Returns:
            Success status
        """
        agent = self.agents[role]
        if agent.status == "working":
            return False

        agent.status = "working"
        agent.current_task = task
        agent.progress = 0.0
        agent.errors = []
        agent.results = {}

        return True

    def update_agent_progress(self, role: AgentRole, progress: float,
                             results: Optional[Dict] = None,
                             error: Optional[str] = None):
        """Update agent progress and status."""
        agent = self.agents[role]
        agent.progress = min(progress, 1.0)

        if results:
            agent.results.update(results)
        if error:
            agent.errors.append(error)

        if progress >= 1.0:
            agent.status = "completed"
        elif error and len(agent.errors) >= 3:
            agent.status = "blocked"

    def complete_agent(self, role: AgentRole, results: Dict) -> None:
        """Mark an agent as completed with results."""
        agent = self.agents[role]
        agent.status = "completed"
        agent.progress = 1.0
        agent.results = results

    def reset_agent(self, role: AgentRole) -> None:
        """Reset an agent to idle state."""
        agent = self.agents[role]
        agent.status = "idle"
        agent.current_task = None
        agent.progress = 0.0
        agent.errors = []
        agent.results = {}

    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        return {
            role.value: {
                "status": agent.status,
                "task": agent.current_task,
                "progress": agent.progress,
                "errors": len(agent.errors),
                "has_results": bool(agent.results)
            }
            for role, agent in self.agents.items()
        }

    # =========================================================================
    # QUALITY & THRESHOLD DECISIONS
    # =========================================================================

    def evaluate_quality(self, results: Dict[str, Any]) -> Tuple[float, str]:
        """
        Evaluate the quality of analysis results.

        Args:
            results: Analysis results to evaluate

        Returns:
            (quality_score, quality_assessment)
        """
        score = 0.0
        factors = []

        # Check completeness
        expected_fields = ["code_rot", "coder_guilt", "security", "performance"]
        present_fields = sum(1 for f in expected_fields if f in results)
        completeness = present_fields / len(expected_fields)
        score += completeness * 0.3
        factors.append(f"Completeness: {completeness:.0%}")

        # Check data depth
        total_findings = 0
        for field in expected_fields:
            if field in results:
                field_data = results[field]
                if isinstance(field_data, dict):
                    total_findings += len(field_data.get("findings", []))
                    total_findings += len(field_data.get("issues", []))

        depth_score = min(total_findings / 20, 1.0)  # 20 findings = max score
        score += depth_score * 0.3
        factors.append(f"Depth: {total_findings} findings")

        # Check consistency
        consistency = 0.8  # Base consistency
        if results.get("errors"):
            consistency -= len(results["errors"]) * 0.1
        score += max(consistency, 0) * 0.2
        factors.append(f"Consistency: {consistency:.0%}")

        # Check actionability
        actionable_items = 0
        for field in expected_fields:
            if field in results:
                field_data = results[field]
                if isinstance(field_data, dict):
                    actionable_items += len(field_data.get("recommendations", []))

        actionability = min(actionable_items / 10, 1.0)
        score += actionability * 0.2
        factors.append(f"Actionability: {actionable_items} recommendations")

        # Generate assessment
        if score >= 0.9:
            assessment = "EXCELLENT - Comprehensive analysis with actionable insights"
        elif score >= 0.7:
            assessment = "GOOD - Solid analysis, some areas could be deeper"
        elif score >= 0.5:
            assessment = "ACCEPTABLE - Basic analysis complete, gaps in coverage"
        else:
            assessment = "INSUFFICIENT - Analysis incomplete, needs re-scan"

        # Record decision
        decision = Decision(
            decision_type=DecisionType.QUALITY_THRESHOLD,
            choice=assessment.split(" - ")[0],
            reasoning="; ".join(factors),
            confidence=score,
            timestamp=datetime.now().isoformat(),
            context={"score": score, "factors": factors}
        )
        self.decisions.append(decision)

        return score, assessment

    def should_iterate(self, quality_score: float, iteration: int,
                      max_iterations: int = 3) -> Tuple[bool, str]:
        """
        Decide whether to iterate (loop back) for more analysis.

        Args:
            quality_score: Current quality score
            iteration: Current iteration number
            max_iterations: Maximum allowed iterations

        Returns:
            (should_iterate, reason)
        """
        # Check iteration limit
        if iteration >= max_iterations:
            return False, f"Maximum iterations ({max_iterations}) reached"

        # Determine threshold based on iteration
        # Be more lenient in later iterations
        threshold = 0.7 - (iteration * 0.1)  # 0.7 -> 0.6 -> 0.5

        if quality_score >= threshold:
            return False, f"Quality score {quality_score:.2f} meets threshold {threshold:.2f}"

        # Calculate improvement potential
        improvement_potential = threshold - quality_score
        if improvement_potential < 0.1:
            return False, f"Marginal improvement potential ({improvement_potential:.2f})"

        # Record decision
        decision = Decision(
            decision_type=DecisionType.ITERATION_CONTROL,
            choice="ITERATE" if quality_score < threshold else "COMPLETE",
            reasoning=f"Score {quality_score:.2f} vs threshold {threshold:.2f}",
            confidence=abs(quality_score - threshold),
            timestamp=datetime.now().isoformat(),
            context={"iteration": iteration, "threshold": threshold}
        )
        self.decisions.append(decision)

        return True, f"Quality {quality_score:.2f} below threshold {threshold:.2f}"

    # =========================================================================
    # LEARNING & REFLECTION
    # =========================================================================

    def reflect_on_analysis(self, analysis_record: AnalysisRecord,
                           feedback: Optional[str] = None) -> Dict[str, Any]:
        """
        Reflect on a completed analysis and learn from it.

        Args:
            analysis_record: The completed analysis record
            feedback: Optional user feedback

        Returns:
            Reflection insights
        """
        insights = {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis_record.repo_name,
            "learnings": []
        }

        # Analyze what worked
        if analysis_record.entropy_score > 70:
            insights["learnings"].append({
                "type": "high_entropy_repo",
                "lesson": "High entropy suggests complex codebase needing deeper analysis"
            })

        # Check if any protocol found nothing
        if analysis_record.security_score == 100:
            insights["learnings"].append({
                "type": "clean_security",
                "lesson": "Repo has good security practices - study patterns for future reference"
            })

        # Learn from recommendations that worked
        if analysis_record.recommendations:
            for rec in analysis_record.recommendations[:3]:
                self.memory.learn_pattern(
                    pattern=rec,
                    examples=[analysis_record.repo_name],
                    category="recommendations"
                )

        # Store reflection
        self.memory.remember(
            content=json.dumps(insights),
            memory_type=MemoryType.LONG_TERM,
            metadata={"type": "reflection", "repo": analysis_record.repo_name},
            importance=0.7
        )

        # Record the analysis in episodic memory
        self.memory.record_analysis(analysis_record)

        return insights

    def get_past_insights(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Get relevant insights from past analyses.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of relevant insights
        """
        memories = self.memory.recall(
            query=query,
            memory_type=MemoryType.LONG_TERM,
            limit=limit
        )

        insights = []
        for memory in memories:
            try:
                data = json.loads(memory.content)
                if data.get("type") == "reflection":
                    insights.append(data)
            except Exception:
                pass

        return insights

    # =========================================================================
    # DECISION HISTORY
    # =========================================================================

    def get_decision_history(self,
                            decision_type: Optional[DecisionType] = None,
                            limit: int = 10) -> List[Decision]:
        """Get history of decisions made by the brain."""
        decisions = self.decisions
        if decision_type:
            decisions = [d for d in decisions if d.decision_type == decision_type]
        return decisions[-limit:]

    def export_decisions(self) -> str:
        """Export all decisions as JSON."""
        return json.dumps([
            {
                "type": d.decision_type.value,
                "choice": d.choice,
                "reasoning": d.reasoning,
                "confidence": d.confidence,
                "timestamp": d.timestamp,
                "outcome": d.outcome
            }
            for d in self.decisions
        ], indent=2)

    def get_stats(self) -> Dict[str, Any]:
        """Get brain statistics."""
        return {
            "total_decisions": len(self.decisions),
            "decisions_by_type": {
                dt.value: sum(1 for d in self.decisions if d.decision_type == dt)
                for dt in DecisionType
            },
            "average_confidence": (
                sum(d.confidence for d in self.decisions) / len(self.decisions)
                if self.decisions else 0
            ),
            "memory_stats": self.memory.get_memory_stats(),
            "agent_status": self.get_agent_status()
        }
