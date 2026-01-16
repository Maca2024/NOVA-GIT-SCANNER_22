# CLAUDE.md - Intelligent Context for Claude Code

## IMMEDIATE START GUIDE

When this repository is opened, follow these steps:

### Step 1: Understand What NOVA Is
NOVA v3.1 is a **forensic code auditor** powered by **AETHERBOT**. It scans Git repositories and generates detailed reports about code health, security, performance, and technical debt.

### Step 2: Know the Core Components
```
NOVA = 4 Scanners + LangGraph Pipeline + AETHERBOT Intelligence

├── SCANNERS (Python-based, no LLM needed)
│   ├── code_rot.py      → Analyzes file staleness & churn
│   ├── coder_guilt.py   → Finds TODO/FIXME/HACK markers
│   ├── security.py      → Detects secrets & vulnerabilities
│   └── performance.py   → Measures complexity & Big O
│
├── LANGGRAPH PIPELINE (Requires ANTHROPIC_API_KEY)
│   └── graph.py         → Scanner → Analyst → Ralph → Report
│
└── AETHERBOT (Intelligent Core)
    ├── memory.py        → Persistent vector memory
    ├── brain.py         → Strategic decision engine
    └── ralph.py         → Smart validation critic
```

### Step 3: Common Tasks & How To Do Them

---

## TASK: RUN A SCAN

**Quick Scan (No API Key):**
```bash
cd C:\Users\info\NOVA-GIT-SCANNER_22
set PYTHONUTF8=1
python -m nova.cli scan <TARGET_REPO_PATH> --quick
```

**Full Analysis (Requires API Key):**
```bash
cd C:\Users\info\NOVA-GIT-SCANNER_22
set PYTHONUTF8=1
set ANTHROPIC_API_KEY=<key>
python -m nova.cli scan <TARGET_REPO_PATH>
```

---

## TASK: MODIFY A SCANNER

1. **Location:** `nova/scanners/<protocol>.py`
2. **Structure:** Each scanner has:
   - `__init__(self, repo_path)` - Initialize with repo path
   - `scan()` - Main method, returns a dataclass report
   - Detection patterns as class constants
3. **To add a new detection pattern:**
   - Add regex/pattern to the patterns dict
   - Update the `scan()` method to use it
   - Add to the report dataclass if needed

**Example - Add new guilt marker:**
```python
# In nova/scanners/coder_guilt.py
GUILT_PATTERNS = {
    ...
    "NEW_MARKER": (r"your_regex_here", severity_level),
}
```

---

## TASK: MODIFY THE RALPH LOOP

1. **Location:** `nova/agents/graph.py`
2. **Key Functions:**
   - `scanner_agent()` - Runs all 4 protocols
   - `analyst_agent()` - Claude interprets data
   - `ralph_critic()` - Validates quality (uses SmartRalph)
   - `report_generator()` - Creates markdown output

**To change validation rules:**
Edit `nova/aetherbot/ralph.py`:
```python
VALIDATION_RULES = {
    "min_findings": 3,        # Minimum total findings
    "min_recommendations": 2,  # Minimum recommendations
    "max_empty_protocols": 1,  # Max protocols with no data
}
```

---

## TASK: MODIFY AETHERBOT

### Memory System (`nova/aetherbot/memory.py`)
- **Add memory type:** Add to `MemoryType` enum
- **Change persistence:** Edit `_save_persistent_memory()`
- **Modify vector search:** Edit `_generate_embedding()`

### Brain (`nova/aetherbot/brain.py`)
- **Change strategies:** Edit `REPO_STRATEGIES` dict
- **Add decision type:** Add to `DecisionType` enum
- **Modify quality eval:** Edit `evaluate_quality()`

### Smart Ralph (`nova/aetherbot/ralph.py`)
- **Add validation check:** Create new `_check_*` method
- **Change thresholds:** Edit `VALIDATION_RULES`
- **Modify scoring:** Edit `_calculate_score()`

---

## TASK: ADD A NEW PROTOCOL

1. Create `nova/scanners/new_protocol.py`:
```python
from dataclasses import dataclass
from typing import List
from pathlib import Path

@dataclass
class NewProtocolReport:
    findings: List[dict]
    score: float

class NewProtocolScanner:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def scan(self) -> NewProtocolReport:
        # Your scanning logic here
        return NewProtocolReport(findings=[], score=0.0)
```

2. Add to `nova/scanners/__init__.py`:
```python
from .new_protocol import NewProtocolScanner, NewProtocolReport
```

3. Add to `scanner_agent()` in `nova/agents/graph.py`

4. Update analyst prompt in `get_analyst_prompt()`

---

## TASK: DEBUG AN ISSUE

**Common Issues:**

| Error | Solution |
|-------|----------|
| `UnicodeEncodeError` | Set `PYTHONUTF8=1` before running |
| `No module 'langgraph'` | `pip install langgraph langchain langchain-anthropic` |
| `ANTHROPIC_API_KEY not set` | Export the key or add to `.env` |
| `Filename too long` (git) | `git config --global core.longpaths true` |
| `No git repository` | Code rot scanner needs git history |

**Debug Mode:**
```python
# Add to any scanner for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## PROJECT FILE MAP

```
C:\Users\info\NOVA-GIT-SCANNER_22\
│
├── nova/
│   ├── __init__.py              # Version: 3.1.0, Codename: AETHERLINK
│   ├── cli.py                   # Entry: `python -m nova.cli`
│   │
│   ├── aetherbot/
│   │   ├── __init__.py          # Exports: AetherMemory, AetherBrain, SmartRalphCritic
│   │   ├── memory.py            # Lines: ~530 | Classes: AetherMemory, MemoryEntry
│   │   ├── brain.py             # Lines: ~606 | Classes: AetherBrain, Decision
│   │   └── ralph.py             # Lines: ~606 | Classes: SmartRalphCritic, ValidationReport
│   │
│   ├── scanners/
│   │   ├── __init__.py          # Exports all scanners
│   │   ├── code_rot.py          # Protocol A | Git history analysis
│   │   ├── coder_guilt.py       # Protocol B | Marker detection
│   │   ├── security.py          # Protocol C | Secret/vuln scanning
│   │   └── performance.py       # Protocol D | Complexity analysis
│   │
│   ├── agents/
│   │   ├── state.py             # NovaState TypedDict
│   │   └── graph.py             # LangGraph pipeline + AETHERBOT integration
│   │
│   └── utils/
│       ├── display.py           # Rich console (NovaConsole class)
│       └── vector_store.py      # Qdrant wrapper
│
├── examples/
│   ├── KIBANA_FULL_FORENSIC.md
│   └── KIBANA_EXECUTIVE_DOSSIER_FULL.md
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
└── README.md                    # Full documentation with diagrams
```

---

## EXECUTION FLOW REFERENCE

```
USER RUNS: nova scan /repo

    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. CLI (cli.py)                                                 │
│    • Parse arguments                                            │
│    • Set up Rich console                                        │
│    • Call run_nova_analysis() or quick_scan()                   │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. AETHER BRAIN (brain.py)                                      │
│    • analyze_repository() → detect size category                │
│    • determine_strategy() → choose scan approach                │
│    • Query episodic memory for similar past analyses            │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. SCANNER AGENT (graph.py:scanner_agent)                       │
│    • CodeRotScanner.scan()      → rot_report                    │
│    • CoderGuiltScanner.scan()   → guilt_report                  │
│    • SecurityScanner.scan()     → security_report               │
│    • PerformanceScanner.scan()  → perf_report                   │
│    • Combine into scan_results dict                             │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. ANALYST AGENT (graph.py:analyst_agent)                       │
│    • Build prompt with scan_results                             │
│    • Call Claude API (claude-sonnet-4-20250514)                     │
│    • Parse JSON response into analysis_report                   │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. SMART RALPH (graph.py:ralph_critic → ralph.py)               │
│    • validate() → check completeness, depth, actionability      │
│    • Calculate adaptive threshold based on repo size            │
│    • Return ValidationReport with PASS/FAIL/SOFT_FAIL           │
│                                                                 │
│    IF FAIL AND iteration < 3:                                   │
│        → Return to ANALYST AGENT with guidance                  │
│    ELSE:                                                        │
│        → Continue to REPORT GENERATOR                           │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. REPORT GENERATOR (graph.py:report_generator)                 │
│    • Build markdown sections (Graveyard, Confessional, etc.)    │
│    • Add AETHERBOT metadata                                     │
│    • Record analysis in episodic memory                         │
│    • Consolidate memories (short-term → long-term)              │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. OUTPUT                                                       │
│    • Write NOVA_FORENSIC.md to disk                             │
│    • Display summary in terminal                                │
│    • Store in AETHER MEMORY for future reference                │
└─────────────────────────────────────────────────────────────────┘
```

---

## QUICK REFERENCE COMMANDS

```bash
# Setup
cd C:\Users\info\NOVA-GIT-SCANNER_22
pip install -e ".[full]"
set PYTHONUTF8=1

# Run quick scan
python -m nova.cli scan . --quick

# Run full analysis
set ANTHROPIC_API_KEY=your_key
python -m nova.cli scan /path/to/repo

# Run specific protocol
python -m nova.cli scan /path/to/repo --protocol security

# Docker
docker-compose run nova scan /repo --quick

# Test individual scanner
python -c "from nova.scanners import SecurityScanner; s = SecurityScanner('.'); print(s.scan())"
```

---

## WHEN USER ASKS TO...

| User Request | Action |
|--------------|--------|
| "Scan a repo" | Run `nova scan <path>` with appropriate flags |
| "Add detection for X" | Add pattern to relevant scanner in `nova/scanners/` |
| "Change validation rules" | Edit `VALIDATION_RULES` in `nova/aetherbot/ralph.py` |
| "Make Ralph stricter/looser" | Adjust `adaptive_threshold` in SmartRalphCritic |
| "Add new report section" | Edit `report_generator()` in `nova/agents/graph.py` |
| "Remember past scans" | Already done via AETHER MEMORY episodic storage |
| "Improve performance" | Adjust `REPO_STRATEGIES` in `nova/aetherbot/brain.py` |
| "Debug scan issue" | Check common issues table, add logging |
| "Push to GitHub" | `git add . && git commit -m "msg" && git push` |

---

## IMPORTANT NOTES

1. **Always set `PYTHONUTF8=1`** on Windows before running
2. **API key required** for full analysis (not for `--quick`)
3. **Memory persists** at `~/.aetherbot/memory/memory_state.pkl`
4. **Max 3 Ralph iterations** before forcing report generation
5. **Ignored directories:** `node_modules/`, `venv/`, `.git/`, `__pycache__/`

---

## REPOSITORY INFO

- **GitHub:** https://github.com/Maca2024/NOVA-GIT-SCANNER_22
- **Version:** 3.1.0 (AETHERLINK)
- **AETHERBOT Version:** 1.0.0
- **Python:** 3.11+
- **Main Entry:** `python -m nova.cli`
