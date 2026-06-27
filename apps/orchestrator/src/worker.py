import asyncio
import logging
from arq import cron
from apps.orchestrator.src.graphs.supervisor import orchestrator_graph
from packages.shared.src.db.client import REDIS_URL

logger = logging.getLogger("ArqWorker")

async def run_orchestration_job(ctx, payload: dict) -> dict:
    """
    Background job execution node for AI employee planning loops.
    """
    logger.info(f"Worker dequeued job for task {payload.get('task_id')}")
    
    initial_state = {
        "organization_id": payload.get("organization_id"),
        "employee_id": payload.get("employee_id"),
        "conversation_id": payload.get("conversation_id"),
        "original_goal": payload.get("goal"),
        "current_plan": [],
        "completed_steps": [],
        "messages": [{"role": "user", "content": payload.get("goal")}],
        "next_node": "planner",
        "context_data": payload.get("context_data", {}),
        "approval_required": False,
        "approval_payload": None,
        "human_response": None,
        "loop_count": 0,
        "max_loops": 15,
        "cost_budget": 5.0,
        "accumulated_cost": 0.0
    }
    
    # Execute graph asynchronously
    result = await orchestrator_graph.ainvoke(initial_state)
    logger.info(f"Worker job complete for task {payload.get('task_id')}. Awaiting approval: {result.get('approval_required')}")
    return result

class WorkerSettings:
    """
    ARQ settings class defining Redis connection and registered task handlers.
    """
    redis_settings = REDIS_URL
    functions = [run_orchestration_job]
    
    async def on_startup(ctx):
        logger.info("ARQ AI Orchestrator Worker started successfully.")
        
    async def on_shutdown(ctx):
        logger.info("ARQ AI Orchestrator Worker shutting down.")
