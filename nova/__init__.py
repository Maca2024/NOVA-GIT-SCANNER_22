"""
🌌 NOVA v3.1 CLI: THE FORENSIC CODE AUDITOR
AETHERBOT POWERED BY AETHERLINK

Mission: Brutal 12-Dimensional forensic scan of GitHub repositories
with intelligent memory, agentic decision-making, and adaptive quality gates.

The AETHERBOT provides:
- Deep Memory: Persistent vector storage for long-term context
- Smart Ralph Loop: Critic that validates and iterates until quality is met
- Agentic Decisions: Autonomous problem-solving capabilities
- Learning System: Remembers past analyses for pattern recognition
"""

__version__ = "3.1.0"
__codename__ = "AETHERLINK"

# AETHERBOT Core Components
from .aetherbot import AetherMemory, MemoryType, AetherBrain, SmartRalphCritic

__all__ = [
    "AetherMemory",
    "MemoryType",
    "AetherBrain",
    "SmartRalphCritic",
]
