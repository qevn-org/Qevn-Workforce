# QEVN Workforce Platform

QEVN Workforce is an enterprise-grade AI Workforce Platform where organizations hire configurable AI Employees to handle business workflows.

## Directory Structure

```
qevn-workforce/
├── apps/
│   ├── web/                    # Next.js Dashboard App
│   ├── gateway/                # FastAPI Gateway Service
│   └── orchestrator/           # LangGraph Orchestrator & LangServe API
├── packages/
│   ├── shared/                 # Shared schemas, db client, models
│   └── tools/                  # Abstract Tool Registry
├── deploy/
│   ├── db/                     # DB Initializations
│   ├── docker/                 # Local docker-compose environment
│   └── k8s/                    # Production Kubernetes manifests
└── .github/
    └── workflows/              # CI/CD workflows
```

## Setup & Running locally

For complete setup instructions, see the database initialization script in `deploy/db/init.sql` and the local docker environment instructions in `deploy/docker/docker-compose.yml`.
