# AgentForge AI – Enterprise Agentic AI Platform

<div align="center">
  <img src="https://img.shields.io/badge/AgentForge-Enterprise%20AI%20Platform-6366f1?style=for-the-badge&logo=robot" alt="AgentForge AI" />
  <img src="https://img.shields.io/badge/React-19-61dafb?style=for-the-badge&logo=react" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript" />
  <img src="https://img.shields.io/badge/PostgreSQL-Ready-336791?style=for-the-badge&logo=postgresql" />
</div>

---

## 🚀 Overview

**AgentForge AI** is a production-grade enterprise platform for building, orchestrating, and managing AI agents at scale. Deploy intelligent agent networks to handle complex, multi-step business processes with full observability, human-in-the-loop controls, and real-time monitoring.

### Core Capabilities

- **Visual Workflow Builder**: Drag-and-drop interface to design agent orchestration flows
- **16 Specialized Agents**: Pre-built agents for discovery, validation, enrichment, and recommendations  
- **Real-time Streaming**: WebSocket-powered live execution tracking with token metrics
- **Production Security**: JWT authentication, role-based access control, audit logging
- **Enterprise UI**: Industry-standard design patterns with dark theme and accessibility
- **Scalable Backend**: FastAPI with async/await, connection pooling, and distributed execution
- **Multi-tenancy Ready**: Workspace isolation, team collaboration, audit trails

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

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ and **npm** 9+
- **Python** 3.11+
- **PostgreSQL** 14+ (optional, uses SQLite for demo)
- **Docker** & **Docker Compose** (optional, for containerized deployment)

### Option 1: Quick Start (Demo Mode)

No external services needed. Perfect for trying out AgentForge:

```bash
# Clone the repository
git clone https://github.com/yourusername/agentforge.git
cd agentforge

# Setup Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Setup frontend
cd frontend
npm install
cd ..

# Run startup script
chmod +x start-dev.sh
./start-dev.sh

# Access the application
# Frontend: http://localhost:5173
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Terminal 3 - (Optional) Redis:**
```bash
redis-server
```

### Option 3: Docker Compose (Production-like)

```bash
docker-compose up --build

# Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 🔐 Authentication Setup

AgentForge includes JWT-based authentication. To set up authentication:

1. **Create a `.env` file** in the project root:

```env
# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database (defaults to SQLite)
DATABASE_URL=sqlite+aiosqlite:///./agentforge.db
# Or for PostgreSQL:
# DATABASE_URL=postgresql+asyncpg://user:password@localhost/agentforge_db

# API Configuration
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000

# Demo Mode
DEMO_MODE=true
```

2. **Register a new user** via `POST /api/v1/auth/register`
3. **Login** via `POST /api/v1/auth/login`
4. **Use returned JWT** token in `Authorization: Bearer <token>` header for all API calls

---

## 🎬 Running the Demo

1. Start both frontend and backend (see Getting Started above)
2. Open http://localhost:5173 in your browser
3. Click **"Login"** (use demo credentials if available)
4. Navigate to **"Workflows"** or **"Dashboard"**
5. Click **"Launch Demo Workflow"**
6. Watch agents execute in real-time with live progress updates
7. Approve recommendations in the approval panel
8. View detailed analytics and reports

---

## 🗄️ Database Setup

### Development (SQLite)

SQLite works out of the box - no setup needed:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Production (PostgreSQL)

For production deployments, use PostgreSQL:

```bash
# Install PostgreSQL
# macOS: brew install postgresql
# Ubuntu: sudo apt install postgresql postgresql-contrib
# Windows: Download from https://www.postgresql.org/download/windows/

# Create database
createdb agentforge_db

# Update .env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/agentforge_db

# Run migrations (when available)
alembic upgrade head

# Start backend
uvicorn backend.main:app --port 8000
```

---

## 📦 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down
```

### Cloud Deployment (AWS Example)

```bash
# Build Docker image
docker build -t agentforge-backend ./backend
docker build -t agentforge-frontend ./frontend

# Push to ECR / Docker Hub
docker tag agentforge-backend:latest your-registry/agentforge-backend:latest
docker push your-registry/agentforge-backend:latest

# Deploy to ECS / EKS with orchestration tool
```

### Environment Variables for Production

```env
# Security - CHANGE THESE IN PRODUCTION
SECRET_KEY=generate-a-secure-random-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=postgresql+asyncpg://user:password@prod-db.aws.com/agentforge

# Cache
REDIS_URL=redis://redis-server:6379

# API
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
DEMO_MODE=false

# LLM (Optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...

# Monitoring
LOG_LEVEL=INFO
SENTRY_DSN=https://...  # Error tracking
```

---

## 🔧 Configuration Reference

| Variable | Type | Default | Description |
|---|---|---|---|
| `APP_NAME` | string | AgentForge AI | Application name |
| `APP_VERSION` | string | 1.0.0 | App version |
| `DEBUG` | boolean | true | Debug mode |
| `DEMO_MODE` | boolean | true | Use simulated agents |
| `SECRET_KEY` | string | (required) | JWT signing key |
| `DATABASE_URL` | string | sqlite:///./agentforge.db | Database connection |
| `REDIS_URL` | string | optional | Redis cache URL |
| `CORS_ORIGINS` | list | [...] | Allowed CORS origins |
| `OPENAI_API_KEY` | string | optional | OpenAI API key |
| `ANTHROPIC_API_KEY` | string | optional | Anthropic API key |

---

## 📁 Project Structure

```
agentforge/
├── frontend/                    # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/              # Enterprise UI components
│   │   │   ├── enterprise/      # Business components
│   │   │   ├── layout/          # Layout components
│   │   │   └── forms/           # Form components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── types/               # TypeScript types
│   │   ├── utils/               # Utility functions
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                     # FastAPI + Python
│   ├── main.py                  # FastAPI application
│   ├── auth/                    # Authentication & security
│   ├── middleware/              # Request/response middleware
│   ├── exceptions/              # Custom exceptions
│   ├── schemas/                 # Pydantic models
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── workflows.py
│   │       ├── agents.py
│   │       ├── approvals.py
│   │       └── ...
│   ├── agents/                  # AI agent implementations
│   ├── database/                # SQLAlchemy models
│   ├── core/                    # Config, constants
│   └── requirements.txt
│
├── docker-compose.yml           # Multi-container setup
├── Dockerfile                   # Backend container
├── frontend/Dockerfile          # Frontend container
├── .env.example
└── README.md
```

---

## 🎨 Design System & UI Components

The frontend includes a comprehensive enterprise design system:

### Core Components
- **Button** - Multiple variants and sizes
- **Card** - Flexible card layouts
- **Input/TextArea/Select** - Form controls  
- **Badge** - Status indicators
- **Dialog** - Modal dialogs
- **Alert** - Alert messages
- **Progress** - Progress bars
- **LoadingSpinner** - Loading indicator

### Enterprise Components
- **DataTable** - Advanced data table
- **StatCard** - Statistics display
- **StatusIndicator** - Status badges
- **Timeline** - Event timeline

### Layout Components
- **Layout** - Main layout wrapper
- **Sidebar** - Navigation sidebar
- **Breadcrumb** - Navigation breadcrumb

See `frontend/src/components/ui/` for all component examples.

---

## 🔌 API Reference

Interactive API documentation available at: **`http://localhost:8000/docs`**

### Authentication Endpoints

```bash
# Register
POST /api/v1/auth/register
Body: { email, password, name }

# Login
POST /api/v1/auth/login
Body: { email, password }

# Get current user
GET /api/v1/auth/me
Headers: Authorization: Bearer <token>

# Refresh token
POST /api/v1/auth/refresh
Body: { refresh_token }

# Logout
POST /api/v1/auth/logout
Headers: Authorization: Bearer <token>
```

### Workflow Endpoints

```bash
# List workflows
GET /api/v1/workflows?page=1&limit=10

# Get workflow
GET /api/v1/workflows/{id}

# Create workflow
POST /api/v1/workflows
Body: { name, description, nodes, edges }

# Update workflow
PUT /api/v1/workflows/{id}
Body: { name, description, status }

# Delete workflow
DELETE /api/v1/workflows/{id}
```

### Approvals Endpoints

```bash
# List approvals
GET /api/v1/approvals

# Get approval
GET /api/v1/approvals/{id}

# Approve
POST /api/v1/approvals/{id}/approve
Body: { comment }

# Reject
POST /api/v1/approvals/{id}/reject
Body: { comment }
```

### Analytics Endpoints

```bash
# Get analytics summary
GET /api/v1/analytics/summary

# Get metrics
GET /api/v1/analytics/metrics?page=1&limit=10
```

### WebSocket

```bash
# Connect to workflow execution stream
WS /ws/{run_id}
```

---
- `WebSocket /ws/{run_id}` — Real-time execution stream
- `GET /api/v1/approvals` — Pending human approvals
- `POST /api/v1/approvals/{id}/decision` — Submit approval decision

---

## 💻 Development Guide

### Frontend Development

The frontend uses React 19 with TypeScript, Vite for bundling, and Tailwind CSS for styling.

**Available Scripts:**
```bash
npm run dev       # Start development server
npm run build     # Build for production
npm run lint      # Run linter
npm run preview   # Preview production build
```

**Creating New Components:**
1. Create component in `src/components/[category]/`
2. Export from component index
3. Use in pages and other components
4. Type with TypeScript interfaces

**Styling:**
- Tailwind CSS for utilities
- CSS modules for component-specific styles
- Dark theme by default (#0a0a0f background)
- Indigo/Violet color palette

### Backend Development

The backend uses FastAPI with async/await for high performance.

**Development Workflow:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Creating New Endpoints:**
1. Create route file in `api/routes/`
2. Define request/response schemas in `schemas/`
3. Implement route handlers with proper error handling
4. Include auth dependencies if needed
5. Register router in `main.py`

**Code Style:**
- Follow PEP 8
- Use type hints on all functions
- Include docstrings on public methods
- Handle errors gracefully with custom exceptions

### Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests (when configured)
cd frontend
npm test
```

---

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find and kill process
# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Database Connection Issues**
```bash
# Check database
psql agentforge_db

# Reset SQLite database
rm backend/agentforge.db
```

**Frontend Build Issues**
```bash
# Clear cache and reinstall
rm -rf frontend/node_modules package-lock.json
cd frontend && npm install
```

**Authentication Token Expired**
- Refresh token automatically when expired
- Clear browser storage: `localStorage.removeItem('auth_token')`
- Login again

### Logs & Debugging

**Backend logs:**
```bash
# Tail logs
tail -f logs/backend.log

# Set log level
LOG_LEVEL=DEBUG uvicorn main:app --reload
```

**Frontend debugging:**
- Use React DevTools browser extension
- Open Chrome DevTools → Sources tab
- Check Application tab for LocalStorage

---

## 🔒 Security Best Practices

1. **Secrets Management**
   - Never commit `.env` to git
   - Use `AGENTFORGE_SECRETS_BACKEND` environment variable
   - Rotate `SECRET_KEY` regularly

2. **Database Security**
   - Use strong PostgreSQL passwords
   - Enable SSL connections in production
   - Run regular backups

3. **API Security**
   - All endpoints require authentication (except `/health`)
   - Rate limiting enabled on sensitive endpoints
   - CORS configured for trusted origins only
   - Security headers added automatically

4. **Frontend Security**
   - JWT tokens stored in memory (not localStorage)
   - CSRF protection enabled
   - Content Security Policy enforced

---

## 📊 Performance Optimization

### Backend
- Connection pooling for database
- Redis caching for frequently accessed data
- Async/await for non-blocking I/O
- Response compression

### Frontend
- Code splitting with React Router
- Lazy loading of heavy components
- React Query for efficient data fetching
- Image optimization

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes with tests
4. **Commit**: `git commit -m 'Add amazing feature'`
5. **Push**: `git push origin feature/amazing-feature`
6. **Open** a Pull Request

**Code Style:**
- Python: PEP 8 via `black`
- TypeScript: ESLint + Prettier
- Commit messages: Conventional Commits

---

## 📈 Roadmap

- [ ] Multi-tenancy support
- [ ] Advanced analytics dashboard
- [ ] Workflow versioning & rollback
- [ ] Agent marketplace
- [ ] Custom agent templates
- [ ] Mobile app
- [ ] Extended API coverage

---

## 🆘 Support & Community

- **Documentation**: [Full docs](https://docs.agentforge.ai)
- **Issues**: [GitHub Issues](https://github.com/agentforge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/agentforge/discussions)
- **Email**: support@agentforge.ai

---

## 🏢 Use Cases

AgentForge is designed to support any workflow:

| Use Case | Agents to Add |
|---|---|
| **Recruiting** | JobParser, CandidateScorer, InterviewScheduler |
| **Real Estate** | PropertyValuation, MarketComps, BuyerMatch |
| **Healthcare** | TriageAgent, InsuranceVerifier, AppointmentScheduler |
| **Finance** | RiskAssessor, ComplianceChecker, PortfolioAnalyzer |
| **Sales** | LeadScorer, CompetitorAnalyzer, DealTracker |
| **Legal** | ContractAnalyzer, ComplianceChecker, DocumentReview |

Simply extend `BaseAgent` and register in `AGENT_REGISTRY`.

---

## 📄 License

MIT License — Build commercial products freely.

See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [React](https://react.dev) and [Tailwind CSS](https://tailwindcss.com/)
- Real-time streaming with [WebSockets](https://websockets.readthedocs.io/)
- Workflow orchestration inspired by [LangGraph](https://langchain-ai.github.io/langgraph/)

---

<div align="center">
  <strong>Made with ❤️ for the AI community</strong>
  
  [Star us on GitHub](https://github.com/agentforge) • [Follow on Twitter](https://twitter.com/agentforge) • [Join Discord](https://discord.gg/agentforge)
</div>
