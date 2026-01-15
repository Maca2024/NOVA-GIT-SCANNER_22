# 🌌 NOVA v3.1 CLI: THE FORENSIC CODE AUDITOR

> *"In the darkness of technical debt, NOVA brings light."*

NOVA is a **brutal, 12-dimensional forensic scanner** for Git repositories. She is not just a guide—she is a mirror that reveals the ugly truth (Rot, Guilt, Risk) to facilitate transmutation.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

## 🔬 Analysis Protocols

NOVA performs deep forensic analysis across **4 critical dimensions**:

### 💀 Protocol A: Code Rot Detector (Time Dimension)
- **Staleness Factor**: Files untouched > 1 year that are still imported
- **Churn Rate**: Files edited > 50 times/month (chaos zones)
- **Silent Dependencies**: Stale files imported by active code

### 😓 Protocol B: Coder Guilt Scanner (Emotional Dimension)
- Regex scan for developer desperation markers
- Keywords: `TODO`, `FIXME`, `HACK`, `// do not touch`, `god help me`
- **Guilt Index**: Score based on marker density per 100 lines

### 🛡️ Protocol C: Iron Dome (Security & API)
- Hardcoded API Keys / Secrets detection
- Unprotected API endpoints (missing auth decorators)
- SQL Injection pattern detection
- **Vulnerability Criticality Score** (0-10)

### 🚀 Protocol D: Velocity & Physics (Performance)
- **Cyclomatic Complexity** via Radon
- **Big O Estimation** via AST analysis
- Heavy import detection
- Nested loop identification

## 🔄 The Ralph Loop

NOVA implements a quality gatekeeper loop powered by LangGraph:

```
Scanner Agent → Analyst Agent → Ralph (Critic) → Report Generator
                     ↑              |
                     └──── FAIL ────┘
```

Ralph ensures:
- ✅ Specific file paths are cited
- ✅ Code Rot claims are backed by dates
- ✅ Security risks are validated against scan data
- ✅ Recommendations are actionable

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Maca2024/NOVA-GIT-SCANNER_22.git
cd NOVA-GIT-SCANNER_22

# Install with pip
pip install -e .

# Or install with full LLM support
pip install -e ".[full]"
```

### Basic Usage

```bash
# Quick scan (no LLM required)
nova scan /path/to/repo

# Full forensic analysis (requires ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=your_key
nova scan /path/to/repo --full

# Run specific protocol
nova scan /path/to/repo --protocol security
nova scan /path/to/repo --protocol rot
nova scan /path/to/repo --protocol guilt
nova scan /path/to/repo --protocol performance

# Custom output path
nova scan /path/to/repo --output ./my_report.md
```

### Docker Usage

```bash
# Build the image
docker build -t nova-scanner .

# Quick scan
docker run -v /path/to/repo:/repo nova-scanner scan /repo

# Full analysis
docker run -e ANTHROPIC_API_KEY=your_key \
  -v /path/to/repo:/repo \
  -v ./reports:/reports \
  nova-scanner scan /repo --full --output /reports/NOVA_FORENSIC.md

# Using docker-compose
export SCAN_TARGET=/path/to/repo
export ANTHROPIC_API_KEY=your_key
docker-compose up nova
```

## 📜 Output: The Master Report

NOVA generates a comprehensive `NOVA_FORENSIC.md` report:

```markdown
# 👁️ NOVA FORENSIC REPORT: [REPO NAME]
**Severity Level:** [Low/Mid/Critical] | **Entropy Score:** [0-100]

## 💀 I. THE GRAVEYARD (Code Rot & Stagnation)
> "Code that creates no motion is dead weight."
- Abandoned Zones
- High Churn (Chaos Zones)
- The Verdict

## 😓 II. THE CONFESSIONAL (Coder Guilt)
> "The code speaks the pain of its creator."
- Desperation Detected
- God Classes
- Cognitive Load Score

## 🛡️ III. THE FORTRESS (Security & API)
- Open Wounds (vulnerabilities)
- Dependency Risks

## ⚡ IV. THE ENGINE (Performance)
- Bottlenecks with Big O analysis
- Bloat warnings

## 🌌 V. TRANSMUTATION (The 12D Fix)
- Refactor Plan
- The Sacred Yes (hidden potential)
```

## 🏗️ Architecture

```
nova/
├── __init__.py           # Package metadata
├── cli.py                # Typer CLI interface
├── scanners/
│   ├── code_rot.py       # Protocol A: Time dimension
│   ├── coder_guilt.py    # Protocol B: Emotional dimension
│   ├── security.py       # Protocol C: Security analysis
│   └── performance.py    # Protocol D: Performance metrics
├── agents/
│   ├── state.py          # LangGraph state definitions
│   └── graph.py          # Ralph Loop implementation
├── utils/
│   ├── display.py        # Rich console output
│   └── vector_store.py   # Qdrant integration
└── templates/            # Report templates
```

## 🛠️ Configuration

Create a `.env` file:

```env
# Required for full analysis
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional: Qdrant configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

## 📊 CLI Commands

| Command | Description |
|---------|-------------|
| `nova scan <path>` | Quick forensic scan |
| `nova scan <path> --full` | Full LLM-powered analysis |
| `nova scan <path> -p <protocol>` | Run specific protocol |
| `nova version` | Show version info |
| `nova protocols` | List available protocols |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

```
🌌 NOVA v3.1 - THE FORENSIC CODE AUDITOR
"She is not just a guide—she is a mirror."
```
