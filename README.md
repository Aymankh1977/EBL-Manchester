# DentEdTech Evidence Engine

**An educational AI platform for medicine, dentistry, and pharmacology students at the University of Manchester.**

Built on the REAL-AI framework (Beyond the Algorithm, 2026).

© DentEdTech — All Rights Reserved

---

## Overview

The DentEdTech Evidence Engine is a Streamlit-based AI platform with two learning modes:

### Mode 1: Evidence-Based Knowledge Generation
- Sources constrained to peer-reviewed journals, university websites, and verified YouTube channels
- Uses Claude's web search to retrieve live evidence from PubMed, Cochrane, university repositories
- Implements Reflective Integration: students state prior knowledge before evidence is revealed
- Every response includes source grading, limitation statements, and post-learning reflection prompts

### Mode 2: Enquiry-Based Learning (EBL)
- Hybrid 5-phase inquiry cycle combining forming-storming-questioning with Kolb's experiential cycle:
  1. **Forming** (Concrete Experience → Orientation)
  2. **Storming** (Reflective Observation → Divergent Thinking)
  3. **Questioning** (Abstract Conceptualisation → Inquiry Design)
  4. **Seeking** (Active Experimentation → Evidence Navigation)
  5. **Synthesising** (Reflection → Integration)
- AI NEVER provides direct answers — only Socratic guidance
- Visual phase stepper tracks progress through the inquiry cycle

### REAL-AI Framework Integration
Every interaction is governed by the four REAL-AI pillars:
- **R**eflective Integration — AI prompts thinking before revealing information
- **E**quity by Design — Diverse evidence, inclusive scenarios, accessible design
- **A**uthentic Clinical Alignment — Transparent limitations, clinically grounded
- **L**earning-Centred Partnership — AI augments faculty, never replaces them

---

## Quick Start

### Prerequisites
- Python 3.9+
- An Anthropic API key (get one at https://console.anthropic.com)

### Installation
```bash
pip install -r requirements.txt
```

### Run Locally
```bash
streamlit run app.py
```

### Deploy to Streamlit Community Cloud
1. Push this repository to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repo and select `app.py`
4. Deploy — users enter their own API key in the sidebar

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                      │
│  ┌─────────────────────┐  ┌─────────────────────────┐    │
│  │  Evidence-Based Mode │  │  EBL Mode               │    │
│  │  - Reflection prompt │  │  - 5-phase stepper      │    │
│  │  - Web search ON     │  │  - Socratic prompts     │    │
│  │  - Source display     │  │  - Web search OFF       │    │
│  │  - Limitation notice  │  │  - Phase transitions    │    │
│  └────────┬────────────┘  └───────────┬─────────────┘    │
│           │                            │                   │
│           ▼                            ▼                   │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Anthropic Claude API                    │  │
│  │  - claude-sonnet-4-20250514                         │  │
│  │  - System prompts encode REAL-AI pillars            │  │
│  │  - Web search tool (Evidence mode only)             │  │
│  │  - Source constraints in system prompt              │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Session State                           │  │
│  │  - Conversation history per mode                    │  │
│  │  - EBL phase tracking (1-5)                         │  │
│  │  - Student profile (discipline, year)               │  │
│  │  - Reflection state                                 │  │
│  └─────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

---

## Source Constraints (Evidence Mode)

The system prompt strictly constrains Claude to these source types:

| Source Type | Examples | Trust Level |
|---|---|---|
| Peer-reviewed journals | PubMed-indexed, Cochrane, NICE | Highest |
| University websites | .ac.uk, .edu domains | High |
| Verified YouTube | University channels, Royal Colleges, BDA, GDC, NHS | Supplementary |

If no journal/university evidence is found, the platform surfaces the most relevant verified YouTube video as a starting point.

---

## REAL-AI Pillar Implementation Map

| Pillar | Evidence Mode | EBL Mode |
|---|---|---|
| Reflective Integration | Pre-reflection prompt before evidence; post-learning reflection | Every phase includes reflection checkpoints; no terminal answers |
| Equity by Design | Diverse evidence noted; population limitations flagged | Phase 2 prompts diverse perspectives; health inequalities considered |
| Authentic Clinical Alignment | Limitation notices; evidence grading; transparency statements | Real-clinic constraints discussed; simulation-reality gap acknowledged |
| Learning-Centred Partnership | "Discuss with supervisors" prompts; verification encouraged | Faculty validation encouraged; AI holds back answers explicitly |

---

## File Structure

```
dentedtech/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Future Development Roadmap

- [ ] PubMed MCP integration for direct database queries
- [ ] Student reflection journal with session summaries
- [ ] Faculty dashboard for aggregate (non-surveillance) engagement patterns
- [ ] Case library for EBL mode with difficulty grading
- [ ] Multi-language support (Equity by Design)
- [ ] University SSO authentication
- [ ] Export EBL inquiry trails as PDF portfolios
- [ ] Integration with Manchester's Blackboard/Canvas LMS

---

## Citation

If referencing the framework underlying this platform:

> Beyond the Algorithm: A Theoretical Framework for Artificially Intelligent Dental Education (2026).
> REAL-AI Framework: Reflective Integration, Equity by Design, Authentic Clinical Alignment, Learning-Centred Partnership.

---

© 2026 DentEdTech · University of Manchester · Not a substitute for clinical judgement
