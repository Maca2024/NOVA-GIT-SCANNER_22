"""
🎭 SMART RALPH - The Intelligent Critic
========================================
Enhanced Ralph Loop with agentic decision-making and deep memory.

Ralph is the quality gatekeeper who:
- Validates analysis completeness
- Ensures insights are actionable
- Loops back when quality is insufficient
- Learns from past validations
- Adapts thresholds based on context
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from .memory import AetherMemory, MemoryType
from .brain import AetherBrain, AgentRole, DecisionType


class ValidationResult(Enum):
    """Result of Ralph's validation."""
    PASS = "pass"           # Quality meets threshold
    SOFT_FAIL = "soft_fail" # Minor issues, can continue with warnings
    HARD_FAIL = "hard_fail" # Must iterate/re-scan
    CRITICAL = "critical"   # Analysis fundamentally broken


class CriticismType(Enum):
    """Types of criticism Ralph can provide."""
    COMPLETENESS = "completeness"    # Missing data/coverage
    DEPTH = "depth"                  # Insufficient detail
    ACCURACY = "accuracy"            # Potential errors
    ACTIONABILITY = "actionability"  # Missing recommendations
    CONSISTENCY = "consistency"      # Conflicting information
    RELEVANCE = "relevance"         # Off-topic findings


@dataclass
class Criticism:
    """A single criticism from Ralph."""
    criticism_type: CriticismType
    severity: str  # info, warning, error, critical
    message: str
    affected_area: str
    suggestion: Optional[str] = None
    auto_fixable: bool = False


@dataclass
class ValidationReport:
    """Complete validation report from Ralph."""
    result: ValidationResult
    score: float  # 0-1
    criticisms: List[Criticism]
    timestamp: str
    iteration: int
    recommendations: List[str]
    pass_reasons: List[str]
    fail_reasons: List[str]


class SmartRalphCritic:
    """
    🎭 SMART RALPH - THE INTELLIGENT CRITIC

    An enhanced quality validation system that:
    - Uses deep memory to learn validation patterns
    - Adapts thresholds based on repo characteristics
    - Provides actionable criticism, not just pass/fail
    - Suggests specific improvements when iterating
    - Tracks validation history for continuous improvement
    """

    # Base validation rules
    VALIDATION_RULES = {
        "min_findings": 3,              # Minimum findings for validity
        "min_recommendations": 2,        # Minimum actionable recommendations
        "max_empty_protocols": 1,        # Maximum protocols with no data
        "min_code_coverage": 0.1,        # Minimum code files analyzed
        "max_error_rate": 0.3,          # Maximum acceptable error rate
    }

    # Severity weights for scoring
    SEVERITY_WEIGHTS = {
        "critical": 0.4,
        "error": 0.25,
        "warning": 0.15,
        "info": 0.05
    }

    def __init__(self, brain: Optional[AetherBrain] = None):
        """
        Initialize Smart Ralph.

        Args:
            brain: AetherBrain instance (creates new if not provided)
        """
        self.brain = brain or AetherBrain()
        self.memory = self.brain.memory
        self.validation_history: List[ValidationReport] = []
        self.current_iteration = 0
        self.max_iterations = 3
        self.adaptive_threshold = 0.7  # Base threshold

    # =========================================================================
    # CORE VALIDATION
    # =========================================================================

    def validate(self, results: Dict[str, Any],
                repo_info: Optional[Dict] = None) -> ValidationReport:
        """
        Validate analysis results.

        Args:
            results: The analysis results to validate
            repo_info: Optional repository information

        Returns:
            ValidationReport with detailed feedback
        """
        self.current_iteration += 1
        criticisms = []
        pass_reasons = []
        fail_reasons = []

        # Run all validation checks
        criticisms.extend(self._check_completeness(results))
        criticisms.extend(self._check_depth(results))
        criticisms.extend(self._check_actionability(results))
        criticisms.extend(self._check_consistency(results))

        # Adapt threshold based on context
        threshold = self._calculate_adaptive_threshold(repo_info)

        # Calculate score
        score = self._calculate_score(results, criticisms)

        # Determine result
        critical_count = sum(1 for c in criticisms if c.severity == "critical")
        error_count = sum(1 for c in criticisms if c.severity == "error")

        if critical_count > 0:
            result = ValidationResult.CRITICAL
            fail_reasons.append(f"{critical_count} critical issues found")
        elif score < threshold * 0.5:
            result = ValidationResult.HARD_FAIL
            fail_reasons.append(f"Score {score:.2f} far below threshold {threshold:.2f}")
        elif score < threshold:
            result = ValidationResult.SOFT_FAIL
            fail_reasons.append(f"Score {score:.2f} below threshold {threshold:.2f}")
        else:
            result = ValidationResult.PASS
            pass_reasons.append(f"Score {score:.2f} meets threshold {threshold:.2f}")

        # Add pass reasons
        if not criticisms:
            pass_reasons.append("No criticisms - analysis is comprehensive")
        if score > 0.8:
            pass_reasons.append("High quality analysis with good coverage")
        if error_count == 0:
            pass_reasons.append("No significant errors detected")

        # Generate recommendations
        recommendations = self._generate_recommendations(criticisms, results)

        # Create report
        report = ValidationReport(
            result=result,
            score=score,
            criticisms=criticisms,
            timestamp=datetime.now().isoformat(),
            iteration=self.current_iteration,
            recommendations=recommendations,
            pass_reasons=pass_reasons,
            fail_reasons=fail_reasons
        )

        # Store in history
        self.validation_history.append(report)

        # Remember this validation
        self._remember_validation(report, results)

        return report

    def _check_completeness(self, results: Dict) -> List[Criticism]:
        """Check if all required data is present."""
        criticisms = []
        expected_protocols = ["code_rot", "coder_guilt", "security", "performance"]

        empty_protocols = []
        for protocol in expected_protocols:
            if protocol not in results or not results[protocol]:
                empty_protocols.append(protocol)
                criticisms.append(Criticism(
                    criticism_type=CriticismType.COMPLETENESS,
                    severity="warning" if len(empty_protocols) <= 1 else "error",
                    message=f"Protocol '{protocol}' returned no data",
                    affected_area=protocol,
                    suggestion=f"Re-run {protocol} scanner with expanded scope",
                    auto_fixable=True
                ))

        if len(empty_protocols) > self.VALIDATION_RULES["max_empty_protocols"]:
            criticisms.append(Criticism(
                criticism_type=CriticismType.COMPLETENESS,
                severity="critical",
                message=f"{len(empty_protocols)} protocols returned no data",
                affected_area="overall",
                suggestion="Analysis is incomplete - verify repository access and scanner configuration"
            ))

        return criticisms

    def _check_depth(self, results: Dict) -> List[Criticism]:
        """Check if analysis has sufficient depth."""
        criticisms = []

        # Count total findings
        total_findings = 0
        for protocol, data in results.items():
            if isinstance(data, dict):
                total_findings += len(data.get("findings", []))
                total_findings += len(data.get("issues", []))
                total_findings += len(data.get("vulnerabilities", []))

        if total_findings < self.VALIDATION_RULES["min_findings"]:
            criticisms.append(Criticism(
                criticism_type=CriticismType.DEPTH,
                severity="warning" if total_findings > 0 else "error",
                message=f"Only {total_findings} findings (minimum: {self.VALIDATION_RULES['min_findings']})",
                affected_area="overall",
                suggestion="Expand analysis scope or lower detection thresholds"
            ))

        # Check per-protocol depth
        for protocol, data in results.items():
            if isinstance(data, dict):
                protocol_findings = (
                    len(data.get("findings", [])) +
                    len(data.get("issues", [])) +
                    len(data.get("vulnerabilities", []))
                )
                if protocol_findings == 0 and protocol not in ["errors"]:
                    continue  # Already handled in completeness
                elif protocol_findings == 1:
                    criticisms.append(Criticism(
                        criticism_type=CriticismType.DEPTH,
                        severity="info",
                        message=f"Protocol '{protocol}' has minimal findings",
                        affected_area=protocol,
                        suggestion=f"Consider deeper scan for {protocol}"
                    ))

        return criticisms

    def _check_actionability(self, results: Dict) -> List[Criticism]:
        """Check if results provide actionable insights."""
        criticisms = []

        # Count recommendations
        total_recommendations = 0
        for protocol, data in results.items():
            if isinstance(data, dict):
                total_recommendations += len(data.get("recommendations", []))

        if total_recommendations < self.VALIDATION_RULES["min_recommendations"]:
            criticisms.append(Criticism(
                criticism_type=CriticismType.ACTIONABILITY,
                severity="warning",
                message=f"Only {total_recommendations} recommendations provided",
                affected_area="recommendations",
                suggestion="Generate specific, actionable recommendations for each finding"
            ))

        # Check for vague recommendations
        all_recs = []
        for protocol, data in results.items():
            if isinstance(data, dict):
                all_recs.extend(data.get("recommendations", []))

        vague_keywords = ["maybe", "might", "consider", "possibly", "perhaps"]
        vague_count = sum(1 for rec in all_recs
                        if any(kw in rec.lower() for kw in vague_keywords))

        if vague_count > len(all_recs) * 0.5 and all_recs:
            criticisms.append(Criticism(
                criticism_type=CriticismType.ACTIONABILITY,
                severity="info",
                message=f"{vague_count} recommendations are vague/uncertain",
                affected_area="recommendations",
                suggestion="Make recommendations more specific and definitive"
            ))

        return criticisms

    def _check_consistency(self, results: Dict) -> List[Criticism]:
        """Check for internal consistency."""
        criticisms = []

        # Check for conflicting severity assessments
        severities = []
        for protocol, data in results.items():
            if isinstance(data, dict):
                if "severity" in data:
                    severities.append((protocol, data["severity"]))

        if severities:
            unique_severities = set(s[1] for s in severities)
            if len(unique_severities) > 2:
                # Check for extreme mismatches
                severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
                severity_values = [severity_order.get(s[1].lower(), 0) for s in severities]
                if max(severity_values) - min(severity_values) >= 3:
                    criticisms.append(Criticism(
                        criticism_type=CriticismType.CONSISTENCY,
                        severity="info",
                        message="Large variance in severity assessments across protocols",
                        affected_area="severity",
                        suggestion="Review and reconcile severity assessments"
                    ))

        return criticisms

    # =========================================================================
    # SCORING & THRESHOLDS
    # =========================================================================

    def _calculate_score(self, results: Dict, criticisms: List[Criticism]) -> float:
        """Calculate overall quality score."""
        score = 1.0

        # Deduct for criticisms based on severity
        for criticism in criticisms:
            weight = self.SEVERITY_WEIGHTS.get(criticism.severity, 0.1)
            score -= weight

        # Ensure non-negative
        score = max(0, score)

        # Boost for good characteristics
        total_findings = sum(
            len(results.get(p, {}).get("findings", [])) +
            len(results.get(p, {}).get("issues", []))
            for p in results if isinstance(results.get(p), dict)
        )

        if total_findings >= 10:
            score = min(score + 0.1, 1.0)
        if total_findings >= 20:
            score = min(score + 0.1, 1.0)

        return round(score, 3)

    def _calculate_adaptive_threshold(self, repo_info: Optional[Dict]) -> float:
        """Calculate adaptive threshold based on context."""
        threshold = self.adaptive_threshold

        if repo_info:
            # Lower threshold for massive repos (harder to analyze completely)
            size_category = repo_info.get("characteristics", {}).get("size_category", "")
            if size_category == "massive":
                threshold -= 0.15
            elif size_category == "large":
                threshold -= 0.1

            # Higher threshold for repos with CI (expect better quality)
            if repo_info.get("characteristics", {}).get("has_ci"):
                threshold += 0.05

        # Adjust based on iteration (be more lenient later)
        if self.current_iteration > 1:
            threshold -= 0.05 * (self.current_iteration - 1)

        # Learn from past validations
        if self.validation_history:
            avg_score = sum(v.score for v in self.validation_history) / len(self.validation_history)
            # If we're consistently failing, slightly lower threshold
            pass_rate = sum(1 for v in self.validation_history
                          if v.result in [ValidationResult.PASS, ValidationResult.SOFT_FAIL]) / len(self.validation_history)
            if pass_rate < 0.3:
                threshold -= 0.05

        return max(0.4, min(0.9, threshold))

    # =========================================================================
    # RECOMMENDATIONS & GUIDANCE
    # =========================================================================

    def _generate_recommendations(self, criticisms: List[Criticism],
                                  results: Dict) -> List[str]:
        """Generate actionable recommendations based on criticisms."""
        recommendations = []

        # Group criticisms by type
        by_type = {}
        for criticism in criticisms:
            ct = criticism.criticism_type
            if ct not in by_type:
                by_type[ct] = []
            by_type[ct].append(criticism)

        # Generate recommendations per type
        if CriticismType.COMPLETENESS in by_type:
            missing = [c.affected_area for c in by_type[CriticismType.COMPLETENESS]
                      if c.affected_area != "overall"]
            if missing:
                recommendations.append(f"Re-run scanners for: {', '.join(missing)}")

        if CriticismType.DEPTH in by_type:
            recommendations.append("Expand analysis scope with lower detection thresholds")
            recommendations.append("Include more file patterns in scan configuration")

        if CriticismType.ACTIONABILITY in by_type:
            recommendations.append("Enhance report with specific fix recommendations")
            recommendations.append("Include code examples for each issue")

        if CriticismType.CONSISTENCY in by_type:
            recommendations.append("Review severity assessments for consistency")

        # Add suggestions from criticisms
        for criticism in criticisms:
            if criticism.suggestion and criticism.suggestion not in recommendations:
                recommendations.append(criticism.suggestion)

        return recommendations[:10]  # Limit to top 10

    def get_iteration_guidance(self, report: ValidationReport) -> Dict[str, Any]:
        """
        Get specific guidance for the next iteration.

        Args:
            report: The validation report from current iteration

        Returns:
            Guidance for improvement
        """
        guidance = {
            "should_iterate": report.result in [ValidationResult.HARD_FAIL, ValidationResult.CRITICAL],
            "iteration": self.current_iteration,
            "max_iterations": self.max_iterations,
            "can_iterate": self.current_iteration < self.max_iterations,
            "focus_areas": [],
            "skip_areas": [],
            "adjustments": {}
        }

        if not guidance["should_iterate"]:
            return guidance

        # Identify focus areas
        for criticism in report.criticisms:
            if criticism.severity in ["critical", "error"]:
                if criticism.affected_area not in guidance["focus_areas"]:
                    guidance["focus_areas"].append(criticism.affected_area)

        # Suggest threshold adjustments
        if report.score < 0.5:
            guidance["adjustments"]["lower_detection_threshold"] = True
            guidance["adjustments"]["expand_file_patterns"] = True

        # Check what protocols succeeded
        completed_protocols = []
        for criticism in report.criticisms:
            if criticism.criticism_type == CriticismType.COMPLETENESS:
                continue
            if criticism.affected_area not in completed_protocols:
                completed_protocols.append(criticism.affected_area)

        guidance["skip_areas"] = completed_protocols

        return guidance

    # =========================================================================
    # MEMORY & LEARNING
    # =========================================================================

    def _remember_validation(self, report: ValidationReport, results: Dict):
        """Store validation in memory for learning."""
        memory_content = {
            "result": report.result.value,
            "score": report.score,
            "criticism_count": len(report.criticisms),
            "criticism_types": [c.criticism_type.value for c in report.criticisms],
            "iteration": report.iteration,
            "timestamp": report.timestamp
        }

        self.memory.remember(
            content=json.dumps(memory_content),
            memory_type=MemoryType.EPISODIC,
            metadata={"type": "validation", "result": report.result.value},
            importance=0.6 if report.result == ValidationResult.PASS else 0.4
        )

    def learn_from_feedback(self, validation_id: int, feedback: str,
                           was_correct: bool):
        """
        Learn from user feedback on validation.

        Args:
            validation_id: Index of validation in history
            feedback: User's feedback
            was_correct: Whether Ralph's assessment was correct
        """
        if validation_id >= len(self.validation_history):
            return

        report = self.validation_history[validation_id]

        # Adjust adaptive threshold based on feedback
        if was_correct:
            # Reinforce current behavior
            pass
        else:
            # Adjust threshold
            if report.result == ValidationResult.PASS:
                # We passed something we shouldn't have - raise threshold
                self.adaptive_threshold = min(0.9, self.adaptive_threshold + 0.05)
            else:
                # We failed something we shouldn't have - lower threshold
                self.adaptive_threshold = max(0.4, self.adaptive_threshold - 0.05)

        # Store feedback in memory
        self.memory.remember(
            content=json.dumps({
                "feedback": feedback,
                "was_correct": was_correct,
                "original_result": report.result.value,
                "original_score": report.score
            }),
            memory_type=MemoryType.LONG_TERM,
            metadata={"type": "validation_feedback"},
            importance=0.8
        )

    # =========================================================================
    # RALPH LOOP CONTROL
    # =========================================================================

    def should_continue(self, report: ValidationReport) -> Tuple[bool, str]:
        """
        Decide whether to continue iterating.

        Args:
            report: Current validation report

        Returns:
            (should_continue, reason)
        """
        # Check if passed
        if report.result == ValidationResult.PASS:
            return False, "PASS - Analysis meets quality threshold"

        # Check if soft fail (continue with warnings)
        if report.result == ValidationResult.SOFT_FAIL:
            return False, "SOFT_PASS - Analysis acceptable with noted issues"

        # Check iteration limit
        if self.current_iteration >= self.max_iterations:
            return False, f"MAX_ITERATIONS - Reached limit of {self.max_iterations}"

        # Check if improvement is possible
        if report.result == ValidationResult.CRITICAL:
            # Check if any criticisms are auto-fixable
            fixable = sum(1 for c in report.criticisms if c.auto_fixable)
            if fixable == 0:
                return False, "CRITICAL - Fundamental issues cannot be auto-fixed"

        return True, "ITERATE - Quality below threshold, attempting improvement"

    def reset(self):
        """Reset Ralph for a new analysis session."""
        self.current_iteration = 0
        self.validation_history = []

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of Ralph's validation session."""
        return {
            "total_iterations": self.current_iteration,
            "max_iterations": self.max_iterations,
            "validations": len(self.validation_history),
            "pass_count": sum(1 for v in self.validation_history
                            if v.result == ValidationResult.PASS),
            "fail_count": sum(1 for v in self.validation_history
                            if v.result in [ValidationResult.HARD_FAIL, ValidationResult.CRITICAL]),
            "average_score": (
                sum(v.score for v in self.validation_history) / len(self.validation_history)
                if self.validation_history else 0
            ),
            "adaptive_threshold": self.adaptive_threshold,
            "all_criticisms": [
                {
                    "type": c.criticism_type.value,
                    "severity": c.severity,
                    "message": c.message
                }
                for v in self.validation_history
                for c in v.criticisms
            ]
        }
