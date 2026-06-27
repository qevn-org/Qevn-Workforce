# LangGraph Agent Orchestrator Service

## Running locally

```bash
pip install -r requirements.txt
pip install -e ../../packages/shared
pip install -e ../../packages/tools
uvicorn src.server:app --host 0.0.0.0 --port 8001
```
