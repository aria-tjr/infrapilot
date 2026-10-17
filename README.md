# InfraPilot — Enterprise Infrastructure Monitoring & Management

> 🚀 A production-ready infrastructure monitoring and management system with REST API, agent-based metrics collection, alerting, and Docker deployment.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://github.com/aria-tjr/infrapilot/actions/workflows/ci.yml/badge.svg)](https://github.com/aria-tjr/infrapilot/actions)

---

## ✨ Features

| Category | Capabilities |
|----------|-------------|
| **📊 System Monitoring** | CPU, RAM, disk, network I/O, process monitoring via lightweight agent |
| **🔔 Alerting** | Configurable thresholds and alert history (Telegram/email notification settings exist in config, sending is **planned**) |
| **👥 User Management** | Role-based access (admin, viewer, operator), JWT authentication |
| **💻 REST API** | FastAPI with auto-generated OpenAPI docs, pagination, filtering |
| **🐳 Docker Ready** | Docker Compose for server + agent deployment |
| **🧪 Testing** | Agent unit tests (pytest) and lint/import checks in GitHub Actions |
| **📈 Dashboard** | Web-based monitoring dashboard with real-time updates |

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Agent 1    │────▶│              │     │   Web UI     │
│ (systemd)   │     │  FastAPI     │◀────│  (Browser)   │
├─────────────┤     │  Server      │     └──────────────┘
│  Agent 2    │────▶│  + SQLite    │
│ (Docker)    │     │              │     ┌──────────────┐
├─────────────┤     │              │────▶│  Telegram    │
│  Agent N    │────▶│              │     │  Alerts      │
└─────────────┘     └──────────────┘     └──────────────┘
```

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional)

### 1. Clone & Install

```bash
git clone https://github.com/aria-tjr/infrapilot.git
cd infrapilot
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the Server

```bash
# With Docker (recommended) — requires SECRET_KEY in .env
docker compose up -d

# Or manually (set SECRET_KEY in .env first — it is required)
cp .env.example .env
uvicorn server.main:app --reload --port 8000
```

### 3. Run an Agent

```bash
python agent/collector.py --server http://localhost:8000 --interval 30
```

### 4. Open Dashboard

```
http://localhost:8000/docs        # API docs (Swagger)
http://localhost:8000/dashboard    # Web UI
```

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Get JWT token |
| POST | `/api/auth/setup` | Create the first admin user |
| GET | `/api/systems` | List monitored systems |
| GET | `/api/systems/{id}/metrics` | Get system metrics |
| POST | `/api/metrics/ingest` | Submit metrics (agent) |
| GET | `/api/alerts` | List alerts |
| POST | `/api/alerts/{id}/acknowledge` | Acknowledge an alert |
| GET | `/api/dashboard/summary` | Dashboard summary |
| POST | `/api/alerts/config` | Configure alert rules |
| GET | `/api/users` | Manage users (admin) |

## Configuration

All settings via `.env` file:

```env
# Server
SECRET_KEY=            # required, min 32 chars, no default
DATABASE_URL=sqlite:///./infrapilot.db

# Alert thresholds
ALERT_CPU_THRESHOLD=80
ALERT_MEMORY_THRESHOLD=85
ALERT_DISK_THRESHOLD=90
# Notification settings (planned — not sent yet)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Agent
AGENT_NAME=production-server-1
COLLECT_INTERVAL=30
```

## Deployment

```bash
docker compose up -d   # server + agent (SQLite volume)
```

A production compose override and a systemd unit for the agent are **planned**.

## Project Structure

```
infrapilot/
├── agent/              # Lightweight monitoring agent
│   └── collector.py    # Metrics collector (psutil) + HTTP sender
├── server/             # Central FastAPI server
│   ├── main.py         # App entry point
│   ├── models.py       # SQLAlchemy models
│   ├── auth.py         # JWT authentication
│   ├── database.py     # DB connection (SQLite by default)
│   ├── config.py       # Settings (env / .env)
│   └── routers/        # API endpoints
├── dashboard/          # Web UI
├── tests/              # Agent tests
└── docker-compose.yml  # Container orchestration
```

## Why InfraPilot

✅ **Secure defaults** — JWT auth, role-based access, required SECRET_KEY  
✅ **Production monitoring** — Real metrics, not simulations  
✅ **Documented** — auto-generated OpenAPI docs  
✅ **CI** — lint, tests and import checks on every push

## License

MIT — see [LICENSE](LICENSE).

---

*Built with Python, FastAPI, and ❤️ for enterprise IT operations.*