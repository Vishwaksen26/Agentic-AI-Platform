# AgentForge AI – Enterprise Agentic AI Platform

<div align="center">
  <img src="https://img.shields.io/badge/AgentForge-AI%20Platform-6366f1?style=for-the-badge&logo=robot" alt="AgentForge AI" />
  <img src="https://img.shields.io/badge/React-18-61dafb?style=for-the-badge&logo=react" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/LangGraph-Latest-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ed?style=for-the-badge&logo=docker" />
</div>

---

## 🚀 Overview

AgentForge AI is a production-grade enterprise agentic AI platform that allows you to visually create, configure, orchestrate, execute, monitor, and reuse AI agents for complex business workflows.

**Demo Use Case: B2B Customer Discovery & Prospect Intelligence**

The platform runs 16 specialized AI agents in an intelligently orchestrated pipeline to discover, validate, enrich, and rank B2B prospects — with full human-in-the-loop review.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🧠 **Planner Agent** | Dynamic AI planning — reads memory, selects agents, builds execution graph |
| 🎯 **16 Specialized Agents** | Search, Validation, ICP Matching, Enrichment, Contacts, Recommendations + more |
| 🔀 **Drag & Drop Builder** | Visual React Flow workflow builder — connect agents like Lego blocks |
| 🔄 **Real-time Streaming** | WebSocket-based live agent execution with progress, tokens, reasoning |
| 🧩 **Shared Memory** | Redis + ChromaDB + PostgreSQL shared context between all agents |
| 👤 **Human-in-the-Loop** | Approval workflow — review, edit, reject AI recommendations before action |
| 📊 **Analytics Dashboard** | Token usage, success rates, agent efficiency, historical trends |
| 🎬 **One-Click Demo** | Full 20-second B2B discovery workflow with realistic animated data |
| ⌨️ **Command Palette** | Ctrl+K for instant navigation, workflow creation, and search |
| 📄 **Report Generation** | PDF, CSV, Markdown reports with shareable links |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                      │
│  Dashboard │ Workflow Builder │ Analytics │ Approvals     │
│  React Flow │ Framer Motion │ Zustand │ React Query       │
└─────────────────────┬───────────────────────────────────┘
                       │ REST API + WebSocket
┌─────────────────────▼───────────────────────────────────┐
│                   Backend (FastAPI)                       │
│                                                           │
│   ┌─────────────┐    ┌──────────────────────────────┐   │
│   │   Planner   │    │      Agent Registry (16)     │   │
│   │   Agent     │───▶│  Search │ ICP │ Enrichment   │   │
│   │  (LangGraph)│    │  Contacts │ Recommendations  │   │
│   └─────────────┘    └──────────────────────────────┘   │
│          │                         │                      │
│   ┌──────▼─────────────────────────▼──────────────┐     │
│   │              Shared Memory Layer                │     │
│   │  Redis (cache) │ ChromaDB (vectors) │ Postgres  │     │
│   └────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
```

---

## 🤖 The 16 AI Agents

| Agent | Category | Role |
|---|---|---|
| **Planner Agent** | Orchestration | Reads memory, selects agents, builds execution plan |
| **Search Agent** | Discovery | Finds companies matching ICP criteria |
| **Company Validation Agent** | Validation | Validates data quality, filters closed/fake companies |
| **ICP Matching Agent** | Analysis | Scores companies against Ideal Customer Profile |
| **Market Intelligence Agent** | Intelligence | Scans news, growth signals, market position |
| **Company Enrichment Agent** | Enrichment | Funding, tech stack, investors, team size |
| **Decision Maker Finder** | Contacts | Identifies C-suite/VP contacts |
| **LinkedIn Agent** | Contacts | LinkedIn profile enrichment |
| **Email Enrichment Agent** | Contacts | Email discovery and verification |
| **Phone Enrichment Agent** | Contacts | Phone number lookup |
| **Summary Agent** | Synthesis | Generates executive company summaries |
| **Recommendation Agent** | Synthesis | Prioritized action recommendations |
| **Human Approval Agent** | Governance | Pauses for human review |
| **Report Generator Agent** | Output | Builds PDF/Markdown/CSV reports |
| **Memory Agent** | Memory | Reads/writes shared memory context |
| **Analytics Agent** | Analytics | Records execution metrics |

---

## 🚀 Quick Start (Demo Mode — No API Keys Needed)

### Option 1: One Command

```bash
# Clone and run (uses SQLite, no external services needed)
git clone <repo>
cd agentforge

# Install frontend deps
cd frontend && npm install && cd ..

# Install backend deps
cd backend && pip install -r requirements.txt && cd ..

# Run everything
./start-dev.sh  # or see manual steps below
```

### Option 2: Manual

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# → Opens at http://localhost:5173
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
# → API at http://localhost:8000
# → Docs at http://localhost:8000/docs
```

Demo mode now auto-completes the human approval step so the workflow finishes without manual intervention when you launch the demo.

### Option 3: Docker

```bash
docker-compose up --build
# → Frontend: http://localhost:3000
# → Backend: http://localhost:8000
# → API Docs: http://localhost:8000/docs
```

---

## 🎬 Running the Demo

1. Open `http://localhost:5173`
2. On the Dashboard, click **"Launch Demo Workflow"**
3. Watch the planner read memory, select agents, and stream execution in real time
4. See the human approval step appear and auto-complete in demo mode
5. Review 5 enriched company cards with recommendations
6. Open the generated report and planner activity feed

---

## 🔧 Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000/api/v1` |
| `VITE_WS_URL` | WebSocket URL | `ws://localhost:8000` |
| `OPENAI_API_KEY` | OpenAI key (optional) | None (demo mode) |
| `ANTHROPIC_API_KEY` | Anthropic key (optional) | None (demo mode) |
| `DATABASE_URL` | PostgreSQL URL | SQLite (auto) |
| `REDIS_URL` | Redis URL (optional) | In-memory |
| `DEMO_MODE` | Use simulated agents | `true` |

---

## 📁 Project Structure

```
agentforge/
├── frontend/                    # React + Vite + TypeScript
│   ├── src/
│   │   ├── pages/               # 12 application pages
│   │   ├── components/          # Reusable UI components
│   │   │   ├── layout/          # AppShell, Sidebar, TopBar
│   │   │   ├── execution/       # PlannerConsole, AgentCard, Timeline
│   │   │   ├── company/         # CompanyCard, CompanyGrid
│   │   │   ├── workflow/        # React Flow builder + nodes
│   │   │   ├── approvals/       # Human approval UI
│   │   │   └── ui/              # Design system components
│   │   ├── store/               # Zustand state stores
│   │   ├── hooks/               # Custom React hooks
│   │   ├── api/                 # Axios client + React Query hooks
│   │   └── types/               # TypeScript interfaces
│   └── package.json
│
├── backend/                     # FastAPI + Python
│   ├── main.py                  # FastAPI application
│   ├── agents/                  # 16 AI agents
│   ├── api/routes/              # REST API endpoints
│   ├── planner/                 # LangGraph orchestration
│   ├── memory/                  # Memory layer (Redis/ChromaDB/Postgres)
│   ├── database/                # SQLAlchemy models + schemas
│   ├── workflows/               # Workflow execution engine
│   ├── core/                    # Config, security, WebSocket
│   └── requirements.txt
│
├── docker-compose.yml
├── README.md
└── .env.example
```

---

## 🎨 Design System

- **Dark theme** throughout — #0a0a0f background
- **Glassmorphism** cards with backdrop-filter blur
- **Inter font** from Google Fonts
- **Indigo/Violet/Cyan** color palette
- **Framer Motion** animations on all interactions
- **React Flow** drag-and-drop workflow canvas

---

## 🔌 API Documentation

When backend is running: `http://localhost:8000/docs`

Key endpoints:
- `POST /api/v1/demo/start` — Start demo workflow
- `GET /api/v1/agents` — List all 16 agents
- `GET /api/v1/analytics/summary` — Platform analytics
- `WebSocket /ws/{run_id}` — Real-time execution stream
- `GET /api/v1/approvals` — Pending human approvals
- `POST /api/v1/approvals/{id}/decision` — Submit approval decision

---

## 🏢 Extending for Other Use Cases

AgentForge is designed to support any workflow:

| Use Case | Agents to Add |
|---|---|
| **Recruiting** | JobParser, CandidateScorer, InterviewScheduler |
| **Real Estate** | PropertyValuation, MarketComps, BuyerMatch |
| **Healthcare** | TriageAgent, InsuranceVerifier, AppointmentScheduler |
| **Finance** | RiskAssessor, ComplianceChecker, PortfolioAnalyzer |

Simply extend `BaseAgent` and register in `AGENT_REGISTRY`.

---

## 📄 License

MIT License — Build commercial products freely.

---

<div align="center">
  Built with React, FastAPI, LangGraph, and 16 AI Agents
</div>
