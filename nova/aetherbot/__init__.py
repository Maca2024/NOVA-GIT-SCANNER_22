"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ███████╗████████╗██╗  ██╗███████╗██████╗ ██████╗  ██████╗ ████████╗║
║    ██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝║
║    ███████║█████╗     ██║   ███████║█████╗  ██████╔╝██████╔╝██║   ██║   ██║   ║
║    ██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗██╔══██╗██║   ██║   ██║   ║
║    ██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║██████╔╝╚██████╔╝   ██║   ║
║    ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   ║
║                                                                               ║
║                         POWERED BY AETHERLINK                                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

AETHERBOT - The Intelligent Agentic Core
=========================================

AETHERBOT is the smart, agentic brain behind NOVA v3.1. It provides:
- Deep Memory: Persistent vector storage for long-term context
- Smart Ralph Loop: Critic that validates and iterates until quality is met
- Agentic Decisions: Autonomous problem-solving capabilities
- Learning System: Remembers past analyses for pattern recognition
"""

__version__ = "1.0.0"
__codename__ = "AETHERLINK"

from .memory import AetherMemory, MemoryType
from .brain import AetherBrain
from .ralph import SmartRalphCritic

__all__ = [
    "AetherMemory",
    "MemoryType",
    "AetherBrain",
    "SmartRalphCritic"
]
