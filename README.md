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
| **🔔 Alerting** | Configurable thresholds, Telegram/email notifications, alert history |
| **👥 User Management** | Role-based access (admin, viewer, operator), JWT authentication |
| **💻 REST API** | FastAPI with auto-generated OpenAPI docs, pagination, filtering |
| **🐳 Docker Ready** | Docker Compose for server + agent deployment |
| **🧪 Testing** | Comprehensive test suite (pytest), CI/CD via GitHub Actions |
| **📈 Dashboard** | Web-based monitoring dashboard with real-time updates |

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Agent 1    │────▶│              │     │   Web UI     │
│ (systemd)   │     │  FastAPI     │◀────│  (Browser)   │
├─────────────┤     │  Server      │     └──────────────┘
│  Agent 2    │────▶│  + Postgres  │
│ (Docker)    │     │  + Redis     │     ┌──────────────┐
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
# With Docker (recommended)
docker compose up -d

# Or manually
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
| GET | `/api/systems` | List monitored systems |
| GET | `/api/systems/{id}/metrics` | Get system metrics |
| POST | `/api/metrics/ingest` | Submit metrics (agent) |
| GET | `/api/alerts` | List alerts |
| POST | `/api/alerts/config` | Configure alert rules |
| GET | `/api/users` | Manage users (admin) |

## Configuration

All settings via `.env` file:

```env
# Server
SECRET_KEY=change-me-in-production
DATABASE_URL=sqlite:///./infrapilot.db
# or: DATABASE_URL=postgresql://user:pass@db:5432/infrapilot

# Alerts
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
SMTP_SERVER=
SMTP_USER=

# Agent
AGENT_NAME=production-server-1
COLLECT_INTERVAL=30
```

## Deployment

```bash
# Production with Docker
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# With systemd
sudo cp scripts/infrapilot-agent.service /etc/systemd/system/
sudo systemctl enable infrapilot-agent
sudo systemctl start infrapilot-agent
```

## Project Structure

```
infrapilot/
├── agent/              # Lightweight monitoring agent
│   ├── collector.py    # System metrics collector (psutil)
│   ├── config.py       # Agent configuration
│   └── sender.py       # HTTP metrics sender
├── server/             # Central FastAPI server
│   ├── main.py         # App entry point
│   ├── models.py       # SQLAlchemy models
│   ├── auth.py         # JWT authentication
│   ├── database.py     # DB connection
│   └── routers/        # API endpoints
├── dashboard/          # Web UI
├── scripts/            # Deployment scripts
├── tests/              # Test suite
└── docker-compose.yml  # Container orchestration
```

## Why InfraPilot

✅ **Enterprise-ready** — JWT auth, role-based access, structured logging  
✅ **Production monitoring** — Real metrics, not simulations  
✅ **Extensible** — Plugin architecture for custom collectors  
✅ **Well-documented** — OpenAPI, README, architecture docs  
✅ **Tested** — Comprehensive test suite with CI/CD

## License

MIT © Aria Tajeri

---

*Built with Python, FastAPI, and ❤️ for enterprise IT operations.*