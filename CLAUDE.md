# CLAUDE.md - Project Context for Claude Code

## Project Overview

**NOVA v3.1** is a forensic code auditor CLI tool powered by **AETHERBOT** (codename: AETHERLINK). It performs brutal 12-dimensional scans of GitHub repositories to expose code rot, security vulnerabilities, performance issues, and developer desperation markers.

## Architecture

```
nova/
├── __init__.py              # Package init, exports AETHERBOT components
├── cli.py                   # Typer CLI entry point
├── aetherbot/               # AETHERBOT - Intelligent Agentic Core
│   ├── __init__.py          # Exports AetherMemory, AetherBrain, SmartRalphCritic
│   ├── memory.py            # Deep memory with Qdrant vector storage
│   ├── brain.py             # Agentic decision-making engine
│   └── ralph.py             # Smart validation critic
├── agents/                  # LangGraph pipeline
│   ├── state.py             # NovaState TypedDict definitions
│   └── graph.py             # Ralph Loop: Scanner → Analyst → Ralph → Report
├── scanners/                # Protocol scanners (Python-based, no LLM)
│   ├── code_rot.py          # Protocol A: File staleness, churn analysis
│   ├── coder_guilt.py       # Protocol B: TODO/FIXME/HACK, god classes
│   ├── security.py          # Protocol C: Secret leaks, SQL injection
│   └── performance.py       # Protocol D: Cyclomatic complexity, Big O
└── utils/
    ├── display.py           # Rich console output, banners
    └── vector_store.py      # Qdrant integration for semantic search
```

## Key Concepts

### The Ralph Loop
The core quality gate system that validates analysis:
1. **Scanner Agent** - Runs Python forensic tools, collects raw data
2. **Analyst Agent** - Uses Claude to interpret data into structured analysis
3. **Smart Ralph (Critic)** - Validates quality, loops back on FAIL
4. **Report Generator** - Creates NOVA_FORENSIC.md output

### AETHERBOT Components

**AetherMemory** (`nova/aetherbot/memory.py`)
- Memory types: `SHORT_TERM`, `LONG_TERM`, `EPISODIC`, `SEMANTIC`, `WORKING`
- Uses Qdrant for vector similarity search
- `remember()`, `recall()`, `forget()`, `consolidate()` methods
- Stores analysis records in episodic memory

**AetherBrain** (`nova/aetherbot/brain.py`)
- Analyzes repo characteristics to determine scan strategy
- Strategies: `tiny`, `small`, `medium`, `large`, `massive`
- Coordinates agents, evaluates quality, decides on iteration
- Reflects on analyses to improve future scans

**SmartRalphCritic** (`nova/aetherbot/ralph.py`)
- Adaptive quality thresholds based on repo size
- Validation checks: completeness, depth, actionability, consistency
- Returns `ValidationReport` with criticisms and recommendations
- Learns from feedback to adjust thresholds

## Commands

```bash
# Quick scan (Python only, no LLM)
nova scan /path/to/repo --quick

# Full analysis (with Claude LLM)
nova scan /path/to/repo

# Specific protocols
nova scan /path/to/repo --protocols security,guilt

# Docker
docker-compose run nova scan /repo --quick
```

## Environment Variables

```
ANTHROPIC_API_KEY=sk-ant-...     # Required for full analysis
QDRANT_HOST=localhost            # Vector DB host (optional)
QDRANT_PORT=6333                 # Vector DB port (optional)
PYTHONUTF8=1                     # Required on Windows for emoji output
```

## Report Structure

Reports follow a fixed structure:
1. **The Graveyard** - Code rot, abandoned files, chaos zones
2. **The Confessional** - Coder guilt, desperation markers, god classes
3. **The Fortress** - Security vulnerabilities, secret leaks
4. **The Engine** - Performance bottlenecks, complexity issues
5. **Transmutation** - Refactor steps + "Sacred Yes" (positive potential)

## Development Notes

### Adding a New Scanner
1. Create `nova/scanners/new_scanner.py`
2. Implement `scan()` method returning a dataclass report
3. Add to `scanner_agent()` in `nova/agents/graph.py`
4. Update analyst prompt to include new protocol

### Modifying Ralph Validation
- Edit `SmartRalphCritic` in `nova/aetherbot/ralph.py`
- Validation rules in `VALIDATION_RULES` dict
- Add new `_check_*` methods for new validation types

### Memory Persistence
- Memory stored in `~/.aetherbot/memory/memory_state.pkl`
- Only `LONG_TERM`, `EPISODIC`, `SEMANTIC` persist across sessions
- Call `memory.consolidate()` to promote important short-term memories

## Tech Stack

- **Python 3.11+**
- **Typer** - CLI framework
- **Rich** - Terminal formatting
- **LangGraph** - Agent orchestration
- **LangChain + Anthropic** - LLM integration
- **Qdrant** - Vector database (optional)
- **GitPython** - Repository analysis
- **Radon** - Cyclomatic complexity

## Common Issues

1. **Windows emoji error**: Set `PYTHONUTF8=1` before running
2. **Long paths on Windows**: Run `git config --global core.longpaths true`
3. **Missing LangGraph**: `pip install langgraph langchain langchain-anthropic`
4. **No API key**: Export `ANTHROPIC_API_KEY` or add to `.env`

## File Patterns

- Scanners analyze: `.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, `.c`, `.cpp`, `.rb`, `.php`
- Ignored: `node_modules/`, `venv/`, `.git/`, `__pycache__/`, `dist/`, `build/`
- Config files: `pyproject.toml`, `requirements.txt`, `.env.example`

## Testing

```bash
# Run on a local repo
python -m nova.cli scan . --quick

# Run on cloned repo
git clone https://github.com/example/repo /tmp/repo
python -m nova.cli scan /tmp/repo
```

## Repository

- GitHub: https://github.com/Maca2024/NOVA-GIT-SCANNER_22
- License: MIT
- Version: 3.1.0 (AETHERLINK)
