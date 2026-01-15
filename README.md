<div align="center">

# 🌌 NOVA v3.1

## THE FORENSIC CODE AUDITOR

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker Ready](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-powered-purple.svg)](https://github.com/langchain-ai/langgraph)
[![Claude AI](https://img.shields.io/badge/Claude-AI%20Powered-orange.svg)](https://anthropic.com)

---

**NOVA is not just a scanner—she is a mirror.**
**She reveals the ugly truth to facilitate transmutation.**

---

```
    ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗     ██╗   ██╗██████╗    ██╗
    ████╗  ██║██╔═══██╗██║   ██║██╔══██╗    ██║   ██║╚════██╗  ███║
    ██╔██╗ ██║██║   ██║██║   ██║███████║    ██║   ██║ █████╔╝  ╚██║
    ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║    ╚██╗ ██╔╝ ╚═══██╗   ██║
    ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║     ╚████╔╝ ██████╔╝██╗██║
    ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝      ╚═══╝  ╚═════╝ ╚═╝╚═╝
                    THE FORENSIC CODE AUDITOR
```

*"In the darkness of technical debt, NOVA brings light."*

</div>

---

## 📋 TABLE OF CONTENTS

- [Overview](#-overview)
- [Key Features](#-key-features)
- [The 4 Forensic Protocols](#-the-4-forensic-protocols)
- [The Ralph Loop](#-the-ralph-loop-quality-gate)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [CLI Reference](#-cli-reference)
- [Docker Usage](#-docker-usage)
- [Output Reports](#-output-reports)
- [Architecture](#-architecture)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 OVERVIEW

**NOVA** (Neural Observation & Vulnerability Analyzer) is a **brutal, 12-dimensional forensic scanner** for Git repositories. Built with Python 3.11, powered by LangGraph and Claude AI, NOVA performs deep analysis across multiple dimensions to reveal the hidden truth about any codebase.

### What Makes NOVA Different?

| Traditional Scanners | NOVA v3.1 |
|---------------------|-----------|
| Surface-level metrics | Deep forensic analysis |
| Generic reports | Personality-driven insights |
| Single dimension | 12-dimensional analysis |
| No quality gate | Ralph Loop validation |
| Basic output | McKinsey-style dossiers |

### Mission Statement

> *NOVA exists to reveal what developers hide—even from themselves. The technical debt, the desperate hacks, the security sins, and the performance crimes. Only through brutal honesty can transmutation occur.*

---

## 🎯 KEY FEATURES

### Core Capabilities

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           NOVA CAPABILITIES                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🔬 FORENSIC SCANNING                                                       │
│     ├── Git history analysis (staleness, churn, abandonment)               │
│     ├── Technical debt marker detection (TODO, FIXME, HACK)                │
│     ├── Security vulnerability scanning (secrets, SQL injection)           │
│     └── Performance bottleneck identification (complexity, Big O)          │
│                                                                             │
│  🤖 AI-POWERED ANALYSIS                                                     │
│     ├── Claude AI interpretation of raw metrics                            │
│     ├── Contextual recommendations                                         │
│     ├── Natural language verdicts                                          │
│     └── Transmutation (refactoring) plans                                  │
│                                                                             │
│  🎭 QUALITY ASSURANCE                                                       │
│     ├── Ralph Loop validation                                              │
│     ├── Citation verification                                              │
│     ├── Hallucination prevention                                           │
│     └── Iterative refinement                                               │
│                                                                             │
│  📊 EXECUTIVE REPORTING                                                     │
│     ├── Technical forensic reports                                         │
│     ├── McKinsey-style executive dossiers                                  │
│     ├── Risk assessment matrices                                           │
│     └── Financial impact analysis                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **CLI Framework** | Typer + Rich | Beautiful terminal interface |
| **AI Orchestration** | LangGraph | State machine & agent loops |
| **LLM Provider** | Claude (Anthropic) | Intelligent analysis |
| **Vector Storage** | Qdrant | Semantic code search |
| **Git Analysis** | GitPython | Repository forensics |
| **Code Metrics** | Radon | Cyclomatic complexity |
| **Security Scan** | Bandit + Custom | Vulnerability detection |
| **Containerization** | Docker | Portable deployment |

---

## 🔬 THE 4 FORENSIC PROTOCOLS

NOVA analyzes repositories through four specialized protocols, each targeting a different dimension of code health.

### 💀 PROTOCOL A: CODE ROT DETECTOR
*The Time Dimension*

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  💀 PROTOCOL A: CODE ROT                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  METRICS ANALYZED:                                                          │
│  ─────────────────                                                          │
│  • Staleness Factor    Files untouched > 1 year                            │
│  • Churn Rate          Files edited > 50 times/month                       │
│  • Silent Dependencies Stale files imported by active code                 │
│  • Abandonment Zones   Dead code still in production                       │
│                                                                             │
│  DETECTION METHOD:                                                          │
│  ─────────────────                                                          │
│  Git history iteration → Commit timestamp analysis → Import graph          │
│                                                                             │
│  OUTPUT:                                                                    │
│  ───────                                                                    │
│  • Rot Score (0-100)                                                        │
│  • Abandoned file list with days stale                                     │
│  • Chaotic file list with churn metrics                                    │
│  • Silent dependency warnings                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Example Output:**
```
💀 CODE ROT ANALYSIS
==================================================
Total Files Analyzed: 2,840
Average Staleness: 127 days
ROT SCORE: 34.2/100

🪦 ABANDONED FILES (>1 year untouched):
  - src/legacy/old_handler.py (423 days stale)
  - lib/deprecated/utils.js (512 days stale)

🌀 CHAOTIC FILES (High Churn):
  - src/core/main.py (67 commits/month)
  - api/endpoints.ts (54 commits/month)
```

---

### 😓 PROTOCOL B: CODER GUILT SCANNER
*The Emotional Dimension*

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  😓 PROTOCOL B: CODER GUILT                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  MARKER CATEGORIES:                                                         │
│  ──────────────────                                                         │
│                                                                             │
│  SEVERITY 5 - DESPERATION                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ "god help" | "please work" | "no idea why" | "wtf" | "pray"        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  SEVERITY 4 - DANGER ZONES                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ "do not touch" | "here be dragons" | "will break" | "fragile"      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  SEVERITY 3 - TECHNICAL DEBT                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ "HACK" | "workaround" | "temporary fix" | "band-aid" | "kludge"    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  SEVERITY 2 - KNOWN ISSUES                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ "FIXME" | "BUG" | "BROKEN" | "needs fix"                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  SEVERITY 1 - PLANNED WORK                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ "TODO" | "XXX" | "REVIEW" | "OPTIMIZE" | "REFACTOR"                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ADDITIONAL DETECTION:                                                      │
│  ─────────────────────                                                      │
│  • God Classes (files > 500 lines)                                         │
│  • Guilt Density (markers per 100 LOC)                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Example Output:**
```
😓 CODER GUILT ANALYSIS
==================================================
Total Lines Analyzed: 327,642
Total Guilt Markers: 136
GUILT INDEX: 100.0/100

📊 MARKERS BY TYPE:
  - TODO: 97
  - FIXME: 19
  - HACK: 17
  - DANGER: 3

🦣 GOD CLASSES (5 detected):
  - model.test.ts: 3,521 lines
  - fixtures.ts: 3,363 lines

⚠️ WORST OFFENDERS:
  🔴 [DESPERATION] timelion_function.js:23
      "// WTF is this? How could you not have a fn?"
```

---

### 🛡️ PROTOCOL C: THE IRON DOME
*Security & API Dimension*

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🛡️ PROTOCOL C: IRON DOME                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SECRET DETECTION PATTERNS:                                                 │
│  ──────────────────────────                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ AWS_ACCESS_KEY      │ AKIA[0-9A-Z]{16}                             │   │
│  │ AWS_SECRET_KEY      │ [A-Za-z0-9/+=]{40}                           │   │
│  │ OPENAI_API_KEY      │ sk-[A-Za-z0-9]{48}                           │   │
│  │ ANTHROPIC_API_KEY   │ sk-ant-[A-Za-z0-9\-]{93}                     │   │
│  │ STRIPE_LIVE_KEY     │ sk_live_[A-Za-z0-9]{24}                      │   │
│  │ GITHUB_TOKEN        │ ghp_[A-Za-z0-9]{36}                          │   │
│  │ PRIVATE_KEY         │ -----BEGIN.*PRIVATE KEY-----                 │   │
│  │ DATABASE_URL        │ (postgres|mysql|mongodb)://.*:.*@            │   │
│  │ GENERIC_SECRET      │ secret\s*[:=]\s*["'][^"']+["']               │   │
│  │ GENERIC_PASSWORD    │ password\s*[:=]\s*["'][^"']+["']             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  SQL INJECTION DETECTION:                                                   │
│  ─────────────────────────                                                  │
│  • String concatenation in execute()                                       │
│  • F-strings in SQL queries                                                │
│  • Raw query string building                                               │
│                                                                             │
│  ENDPOINT ANALYSIS:                                                         │
│  ──────────────────                                                         │
│  • Missing auth decorators (Flask, Django, FastAPI)                        │
│  • Unprotected routes (Express)                                            │
│  • Public endpoints without rate limiting                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Example Output:**
```
🛡️ SECURITY ANALYSIS (THE IRON DOME)
==================================================
Files Scanned: 2,840
VULNERABILITY SCORE: 10.0/10

🔐 SECRET LEAKS DETECTED (15):
  🔴 [AWS_SECRET_KEY] keystore/create.test.js:12
      Value: IxR0****22UD
  🔴 [STRIPE_LIVE_KEY] payments/config.py:45
      Value: sk_l****_8xK

💉 SQL INJECTION RISKS (2):
  🔴 sample_data/logs/saved_objects.ts:78
      String concatenation in SELECT

🚪 UNPROTECTED ENDPOINTS (590):
  ⚠️ [GET] /api/users
  ⚠️ [POST] /api/data
```

---

### 🚀 PROTOCOL D: VELOCITY & PHYSICS
*Performance Dimension*

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🚀 PROTOCOL D: VELOCITY & PHYSICS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CYCLOMATIC COMPLEXITY SCALE:                                               │
│  ────────────────────────────                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  A (1-5)    │ Simple        │ 🟢 Easily maintainable               │   │
│  │  B (6-10)   │ Low           │ 🟢 Acceptable complexity             │   │
│  │  C (11-20)  │ Moderate      │ 🟡 Consider refactoring              │   │
│  │  D (21-30)  │ High          │ 🟠 Refactoring recommended           │   │
│  │  E (31-40)  │ Very High     │ 🔴 Refactoring required              │   │
│  │  F (41+)    │ Unmaintainable│ 🔴 Critical - split immediately      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  BIG O ESTIMATION:                                                          │
│  ─────────────────                                                          │
│  AST analysis detects:                                                      │
│  • Nested loop depth → O(n²), O(n³), etc.                                  │
│  • Recursive patterns → O(2^n), O(n!)                                      │
│  • Linear iterations → O(n)                                                │
│  • Constant operations → O(1)                                              │
│                                                                             │
│  HEAVY IMPORT DETECTION:                                                    │
│  ────────────────────────                                                   │
│  • pandas, numpy, tensorflow, torch                                        │
│  • Large framework imports in lightweight files                            │
│  • Lazy loading recommendations                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Example Output:**
```
🚀 PERFORMANCE ANALYSIS (VELOCITY & PHYSICS)
==================================================
Functions Analyzed: 1,247
Average Complexity: 4.2
Maintainability Index: 78.5/100
PERFORMANCE SCORE: 82.0/100

🔥 HIGH COMPLEXITY FUNCTIONS (12):
  🔴 process_batch() - CC: 34 [E]
      src/processing/batch.py:145
  🟠 validate_input() - CC: 22 [D]
      src/validation/input.py:89

⏱️ POTENTIAL BOTTLENECKS (8):
  🔴 nested_search() - O(n³)
      src/search/deep.py:234
      Reason: Triple nested loops (depth: 3)

📦 HEAVY IMPORTS (5):
  ⚠️ pandas
      utils/lightweight.py:1
      Heavy data library - consider lazy loading
```

---

## 🔄 THE RALPH LOOP (Quality Gate)

NOVA implements a unique quality assurance mechanism called **The Ralph Loop**—a critic agent that validates analysis quality before report generation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           THE RALPH LOOP                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                    ┌──────────────────┐                                     │
│                    │  SCANNER AGENT   │                                     │
│                    │   (Raw Data)     │                                     │
│                    └────────┬─────────┘                                     │
│                             │                                               │
│                             ▼                                               │
│                    ┌──────────────────┐                                     │
│                    │  ANALYST AGENT   │                                     │
│                    │  (LLM Analysis)  │                                     │
│                    └────────┬─────────┘                                     │
│                             │                                               │
│                             ▼                                               │
│                    ┌──────────────────┐                                     │
│              ┌────▶│   RALPH NODE     │◀────┐                               │
│              │     │   (The Critic)   │     │                               │
│              │     └────────┬─────────┘     │                               │
│              │              │               │                               │
│              │         ┌────┴────┐          │                               │
│              │         │         │          │                               │
│              │       PASS      FAIL         │                               │
│              │         │         │          │                               │
│              │         ▼         └──────────┘                               │
│              │  ┌──────────────────┐     (Max 3 iterations)                 │
│              │  │ REPORT GENERATOR │                                        │
│              │  └──────────────────┘                                        │
│              │              │                                               │
│              │              ▼                                               │
│              │     📜 NOVA_FORENSIC.md                                      │
│              │                                                              │
│              └──────────────────────────────────────────────────────────    │
│                                                                             │
│  RALPH'S VALIDATION CHECKS:                                                 │
│  ──────────────────────────                                                 │
│  ✓ Did the Analyst cite specific file paths?                               │
│  ✓ Is Code Rot backed by actual dates?                                     │
│  ✓ Are Security risks validated against scan data?                         │
│  ✓ Are recommendations actionable and specific?                            │
│  ✓ Is the Sacred Yes genuine and insightful?                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 INSTALLATION

### Prerequisites

- Python 3.10 or higher
- Git
- Docker (optional, for containerized usage)

### Option 1: pip install

```bash
# Clone the repository
git clone https://github.com/Maca2024/NOVA-GIT-SCANNER_22.git
cd NOVA-GIT-SCANNER_22

# Install basic version
pip install -e .

# Install with full LLM support
pip install -e ".[full]"

# Install with development tools
pip install -e ".[dev]"
```

### Option 2: Docker

```bash
# Build the image
docker build -t nova-scanner .

# Run NOVA
docker run -v /path/to/repo:/repo nova-scanner scan /repo
```

### Option 3: Docker Compose

```bash
# Clone and start
git clone https://github.com/Maca2024/NOVA-GIT-SCANNER_22.git
cd NOVA-GIT-SCANNER_22

# Set your target repository
export SCAN_TARGET=/path/to/your/repo
export ANTHROPIC_API_KEY=your_key

# Launch
docker-compose up nova
```

---

## 🚀 QUICK START

### Basic Quick Scan (No API Key Required)

```bash
# Scan current directory
nova scan .

# Scan specific repository
nova scan /path/to/repo

# Scan with custom output
nova scan /path/to/repo --output ./my_report.md
```

### Full LLM-Powered Analysis

```bash
# Set your API key
export ANTHROPIC_API_KEY=your_key

# Run full analysis with Ralph Loop
nova scan /path/to/repo --full
```

### Single Protocol Scan

```bash
# Run only security scan
nova scan /path/to/repo --protocol security

# Run only guilt scan
nova scan /path/to/repo --protocol guilt

# Run only code rot scan
nova scan /path/to/repo --protocol rot

# Run only performance scan
nova scan /path/to/repo --protocol performance
```

---

## 📖 CLI REFERENCE

### Main Commands

| Command | Description |
|---------|-------------|
| `nova scan <path>` | Perform forensic scan |
| `nova version` | Show version information |
| `nova protocols` | List available protocols |

### Scan Options

| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Custom output file path |
| `--full` | `-f` | Enable LLM-powered analysis |
| `--quiet` | `-q` | Minimal output |
| `--protocol` | `-p` | Run specific protocol only |

### Examples

```bash
# Quick scan with minimal output
nova scan /repo -q

# Full analysis with custom output
nova scan /repo --full -o ./reports/analysis.md

# Security-only scan
nova scan /repo -p security

# Performance analysis
nova scan /repo -p performance
```

---

## 🐳 DOCKER USAGE

### Build Image

```bash
docker build -t nova-scanner .
```

### Quick Scan

```bash
docker run -v /path/to/repo:/repo nova-scanner scan /repo
```

### Full Analysis

```bash
docker run \
  -e ANTHROPIC_API_KEY=your_key \
  -v /path/to/repo:/repo \
  -v ./reports:/reports \
  nova-scanner scan /repo --full --output /reports/NOVA_FORENSIC.md
```

### Docker Compose

```yaml
# docker-compose.yml usage
services:
  nova:
    build: .
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ${SCAN_TARGET}:/repo:ro
      - ./reports:/reports
    command: ["scan", "/repo", "--full", "-o", "/reports/report.md"]
```

```bash
# Run with compose
SCAN_TARGET=/your/repo docker-compose up nova
```

---

## 📜 OUTPUT REPORTS

### Quick Scan Report Structure

```markdown
# 👁️ NOVA FORENSIC REPORT: [REPO NAME]
**Severity Level:** [Low/Medium/High/Critical] | **Entropy Score:** [0-100]

## 💀 I. THE GRAVEYARD (Code Rot & Stagnation)
## 😓 II. THE CONFESSIONAL (Coder Guilt)
## 🛡️ III. THE FORTRESS (Security & API)
## ⚡ IV. THE ENGINE (Performance)
## 🌌 V. TRANSMUTATION (The 12D Fix)
```

### Full Analysis Report (LLM-Powered)

Includes everything above plus:
- AI-interpreted summaries
- Contextual verdicts
- Specific file citations with line numbers
- Actionable refactoring plans
- "The Sacred Yes" - hidden potential analysis

### Executive Dossier Format

For enterprise reporting, NOVA can generate McKinsey-style dossiers including:
- Executive Summary
- Technology Stack Analysis
- Risk Assessment Matrix
- Financial Impact Analysis
- 90-Day Remediation Roadmap

See [examples/](./examples/) for sample reports.

---

## 🏗️ ARCHITECTURE

### Project Structure

```
nova/
├── __init__.py              # Package metadata
├── cli.py                   # Typer CLI interface
│
├── scanners/                # The 4 Forensic Protocols
│   ├── __init__.py
│   ├── code_rot.py          # 💀 Protocol A: Time Dimension
│   ├── coder_guilt.py       # 😓 Protocol B: Emotional Dimension
│   ├── security.py          # 🛡️ Protocol C: Security Dimension
│   └── performance.py       # 🚀 Protocol D: Performance Dimension
│
├── agents/                  # LangGraph Implementation
│   ├── __init__.py
│   ├── state.py             # State definitions
│   └── graph.py             # Ralph Loop & agent nodes
│
├── utils/                   # Utilities
│   ├── __init__.py
│   ├── display.py           # Rich console output
│   └── vector_store.py      # Qdrant integration
│
└── templates/               # Report templates
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            NOVA DATA FLOW                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   INPUT                PROCESSING                        OUTPUT             │
│   ─────                ──────────                        ──────             │
│                                                                             │
│   ┌──────────┐        ┌──────────────────────────┐      ┌──────────────┐   │
│   │   Git    │───────▶│     Protocol A           │─────▶│  Rot Score   │   │
│   │  Repo    │        │     (Code Rot)           │      │  + Details   │   │
│   └──────────┘        └──────────────────────────┘      └──────────────┘   │
│        │                                                        │           │
│        │              ┌──────────────────────────┐              │           │
│        ├─────────────▶│     Protocol B           │──────────────┤           │
│        │              │     (Guilt)              │              │           │
│        │              └──────────────────────────┘              │           │
│        │                                                        │           │
│        │              ┌──────────────────────────┐              │           │
│        ├─────────────▶│     Protocol C           │──────────────┤           │
│        │              │     (Security)           │              │           │
│        │              └──────────────────────────┘              │           │
│        │                                                        │           │
│        │              ┌──────────────────────────┐              │           │
│        └─────────────▶│     Protocol D           │──────────────┤           │
│                       │     (Performance)        │              │           │
│                       └──────────────────────────┘              │           │
│                                                                 │           │
│                                                                 ▼           │
│                                                        ┌──────────────┐     │
│                                                        │   Analyst    │     │
│                              ┌─────────────────────────│    Agent     │     │
│                              │                         └──────┬───────┘     │
│                              │                                │             │
│                              ▼                                ▼             │
│                       ┌──────────────┐                ┌──────────────┐      │
│                       │    Ralph     │◀───────────────│   Report     │      │
│                       │   Critic     │                │  Generator   │      │
│                       └──────────────┘                └──────┬───────┘      │
│                                                              │              │
│                                                              ▼              │
│                                                     📜 NOVA_FORENSIC.md     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ CONFIGURATION

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Claude API key for full analysis | For `--full` |
| `QDRANT_HOST` | Qdrant server host | No (default: localhost) |
| `QDRANT_PORT` | Qdrant server port | No (default: 6333) |

### Configuration File

Create a `.env` file in your project root:

```env
# Required for full LLM analysis
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Qdrant configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

### Custom Thresholds

Modify thresholds in scanner modules:

```python
# In nova/scanners/code_rot.py
STALE_THRESHOLD_DAYS = 365  # 1 year
CHURN_THRESHOLD = 50        # commits per month

# In nova/scanners/coder_guilt.py
GOD_CLASS_LINES = 500       # lines threshold

# In nova/scanners/performance.py
HIGH_COMPLEXITY_THRESHOLD = 10
VERY_HIGH_COMPLEXITY_THRESHOLD = 20
```

---

## 📂 EXAMPLES

### Example Reports

The `examples/` directory contains real-world analysis reports:

| File | Description |
|------|-------------|
| `KIBANA_FULL_FORENSIC.md` | Claude-powered analysis of Elastic Kibana |
| `KIBANA_EXECUTIVE_DOSSIER_FULL.md` | McKinsey-style 30-page dossier |

### Scanning Popular Repositories

```bash
# Scan a local clone
git clone https://github.com/elastic/kibana.git --depth 1
nova scan ./kibana --full

# Scan specific subdirectory
nova scan ./kibana/src/core -o kibana_core_report.md
```

---

## 🔌 API REFERENCE

### Python API

```python
from nova.scanners import (
    CodeRotScanner,
    CoderGuiltScanner,
    SecurityScanner,
    PerformanceScanner
)

# Individual scanner usage
rot_scanner = CodeRotScanner("/path/to/repo")
rot_report = rot_scanner.scan()
print(f"Rot Score: {rot_report.rot_score}")

# Full LangGraph pipeline
from nova.agents import run_nova_analysis

result = run_nova_analysis("/path/to/repo", "my-repo")
print(result["final_report_markdown"])
```

### Scanner Classes

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `CodeRotScanner` | Git history analysis | `scan()` → `CodeRotReport` |
| `CoderGuiltScanner` | Debt marker detection | `scan()` → `CoderGuiltReport` |
| `SecurityScanner` | Vulnerability scanning | `scan()` → `SecurityReport` |
| `PerformanceScanner` | Complexity analysis | `scan()` → `PerformanceReport` |

---

## 🤝 CONTRIBUTING

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Maca2024/NOVA-GIT-SCANNER_22.git
cd NOVA-GIT-SCANNER_22

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black nova/
ruff check nova/
```

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution

- [ ] Additional language support (Go, Rust, Java analyzers)
- [ ] New detection patterns for security vulnerabilities
- [ ] Performance optimizations for large repositories
- [ ] Additional report formats (PDF, HTML)
- [ ] Integration with CI/CD platforms

---

## 📄 LICENSE

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 ACKNOWLEDGMENTS

- **Anthropic** - Claude AI powers the intelligent analysis
- **LangChain/LangGraph** - Agent orchestration framework
- **Typer/Rich** - Beautiful CLI interfaces
- **Radon** - Python complexity metrics
- **Bandit** - Python security scanning
- **GitPython** - Git repository analysis

---

## 📞 SUPPORT

- **Issues:** [GitHub Issues](https://github.com/Maca2024/NOVA-GIT-SCANNER_22/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Maca2024/NOVA-GIT-SCANNER_22/discussions)

---

<div align="center">

## 🌌 THE NOVA PHILOSOPHY

*"Code that creates no motion is dead weight."*

*"The code speaks the pain of its creator."*

*"A chain is only as strong as its weakest link."*

*"Speed is the essence of war."*

*"From chaos comes order, from rot comes renewal."*

---

**In the darkness of technical debt, NOVA brings light.**

---

</div>

---

<div align="center">

```
    ___    _____ ______ __  __ ______ ____   ____   ____  ______
   /   |  / ___//_  __// / / // ____// __ \ / __ ) / __ \/_  __/
  / /| |  \__ \  / /  / /_/ // __/  / /_/ // __  |/ / / / / /
 / ___ | ___/ / / /  / __  // /___ / _, _// /_/ // /_/ / / /
/_/  |_|/____/ /_/  /_/ /_//_____//_/ |_|/_____/ \____/ /_/

```

```
    ____   ____  _       __ ______ ____   ______ ____     ____   __  __
   / __ \ / __ \| |     / // ____// __ \ / ____// __ \   / __ ) / / / /
  / /_/ // / / /| | /| / // __/  / /_/ // __/  / / / /  / __  |/ /_/ /
 / ____// /_/ / | |/ |/ // /___ / _, _// /___ / /_/ /  / /_/ // __  /
/_/     \____/  |__/|__//_____//_/ |_|/_____//_____/  /_____//_/ /_/

     ___    ______ ______ __  __ ______ ____   __     ____ _   __ __ __
    /   |  / ____//_  __// / / // ____// __ \ / /    /  _// | / // //_/
   / /| | / __/    / /  / /_/ // __/  / /_/ // /     / / /  |/ // ,<
  / ___ |/ /___   / /  / __  // /___ / _, _// /___ _/ / / /|  // /| |
 /_/  |_/_____/  /_/  /_/ /_//_____//_/ |_|/_____//___//_/ |_//_/ |_|

```

---

**AETHERBOT**
*Powered by AETHERLINK*

---

</div>
